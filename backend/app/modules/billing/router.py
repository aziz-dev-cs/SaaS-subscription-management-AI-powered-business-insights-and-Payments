"""HTTP endpoints for the billing module.

Handles plan listing, subscription management, invoice retrieval,
and payment method queries. All mutations require authentication.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import CurrentUserID, DBSession
from app.modules.auth.repository import UserRepository
from app.modules.billing.exceptions import (
    ActiveSubscriptionExistsError,
    BillingError,
    PlanNotFoundError,
    SubscriptionNotFoundError,
)
from app.modules.billing.repository import (
    InvoiceRepository,
    PaymentMethodRepository,
    PlanRepository,
    SubscriptionRepository,
)
from app.modules.billing.schemas import (
    CancelSubscriptionRequest,
    CreateSubscriptionRequest,
    InvoiceResponse,
    PaymentMethodResponse,
    PlanResponse,
    SubscriptionResponse,
)
from app.modules.billing.service import BillingService
from app.shared.pagination import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/billing", tags=["Billing"])


def _get_billing_service(session: DBSession) -> BillingService:
    """Build a BillingService with repository dependencies.

    Args:
        session: The injected database session.

    Returns:
        A fully-wired BillingService instance.
    """
    return BillingService(
        plan_repo=PlanRepository(session),
        sub_repo=SubscriptionRepository(session),
        invoice_repo=InvoiceRepository(session),
        pm_repo=PaymentMethodRepository(session),
    )


async def _get_tenant_id(user_id: CurrentUserID, session: DBSession) -> uuid.UUID:
    """Resolve the tenant ID from the authenticated user.

    Args:
        user_id: The authenticated user's ID.
        session: The database session.

    Returns:
        The user's tenant UUID.

    Raises:
        HTTPException: 404 if the user is not found.
    """
    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(uuid.UUID(user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.tenant_id


@router.get("/plans", response_model=list[PlanResponse], summary="List available plans")
async def list_plans(service: BillingService = Depends(_get_billing_service)) -> list[PlanResponse]:
    """Retrieve all active subscription plans.

    Args:
        service: Injected billing service.

    Returns:
        A list of active plans.
    """
    return await service.list_plans()


@router.post(
    "/subscriptions",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new subscription",
)
async def create_subscription(
    payload: CreateSubscriptionRequest,
    user_id: CurrentUserID = Depends(),
    session: AsyncSession = Depends(),
    service: BillingService = Depends(_get_billing_service),
) -> SubscriptionResponse:
    """Create a subscription for the authenticated user's tenant.

    Args:
        payload: Subscription creation data.
        user_id: The authenticated user's ID.
        session: The database session.
        service: Injected billing service.

    Returns:
        The created subscription.
    """
    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(uuid.UUID(user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        return await service.create_subscription(
            tenant_id=user.tenant_id,
            user_email=user.email,
            user_name=user.full_name,
            payload=payload,
        )
    except ActiveSubscriptionExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message)
    except PlanNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    except BillingError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get(
    "/subscriptions/current",
    response_model=SubscriptionResponse | None,
    summary="Get current subscription",
)
async def get_current_subscription(
    user_id: CurrentUserID,
    session: DBSession,
    service: BillingService = Depends(_get_billing_service),
) -> SubscriptionResponse | None:
    """Get the current active subscription for the user's tenant.

    Args:
        user_id: The authenticated user's ID.
        session: The database session.
        service: Injected billing service.

    Returns:
        The active subscription or None.
    """
    tenant_id = await _get_tenant_id(user_id, session)
    return await service.get_subscription(tenant_id)


@router.post(
    "/subscriptions/{subscription_id}/cancel",
    response_model=SubscriptionResponse,
    summary="Cancel a subscription",
)
async def cancel_subscription(
    subscription_id: uuid.UUID,
    payload: CancelSubscriptionRequest,
    user_id: CurrentUserID,
    session: DBSession,
    service: BillingService = Depends(_get_billing_service),
) -> SubscriptionResponse:
    """Cancel an existing subscription.

    Args:
        subscription_id: The subscription to cancel.
        payload: Cancellation options.
        user_id: The authenticated user's ID.
        session: The database session.
        service: Injected billing service.

    Returns:
        The updated subscription.
    """
    tenant_id = await _get_tenant_id(user_id, session)
    try:
        return await service.cancel_subscription(tenant_id, subscription_id, payload)
    except SubscriptionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    except BillingError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get(
    "/invoices",
    response_model=PaginatedResponse[InvoiceResponse],
    summary="List invoices",
)
async def list_invoices(
    user_id: CurrentUserID,
    session: DBSession,
    page: int = 1,
    page_size: int = 20,
    service: BillingService = Depends(_get_billing_service),
) -> PaginatedResponse[InvoiceResponse]:
    """Retrieve paginated invoices for the user's tenant.

    Args:
        user_id: The authenticated user's ID.
        session: The database session.
        page: Page number.
        page_size: Items per page.
        service: Injected billing service.

    Returns:
        A paginated list of invoices.
    """
    tenant_id = await _get_tenant_id(user_id, session)
    params = PaginationParams(page=page, page_size=page_size)
    return await service.list_invoices(tenant_id, params)


@router.get(
    "/payment-methods",
    response_model=list[PaymentMethodResponse],
    summary="List payment methods",
)
async def list_payment_methods(
    user_id: CurrentUserID,
    session: DBSession,
    service: BillingService = Depends(_get_billing_service),
) -> list[PaymentMethodResponse]:
    """Retrieve all payment methods for the user's tenant.

    Args:
        user_id: The authenticated user's ID.
        session: The database session.
        service: Injected billing service.

    Returns:
        A list of stored payment methods.
    """
    tenant_id = await _get_tenant_id(user_id, session)
    return await service.list_payment_methods(tenant_id)
