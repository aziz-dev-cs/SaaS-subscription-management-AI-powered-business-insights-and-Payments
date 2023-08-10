"""Business logic for the billing module.

Orchestrates subscription lifecycle operations by coordinating between
the internal repository layer and external payment providers (Stripe/PayPal).
"""

import uuid
from datetime import datetime, timezone

from app.modules.billing.exceptions import (
    ActiveSubscriptionExistsError,
    PlanNotFoundError,
    SubscriptionNotFoundError,
)
from app.modules.billing.models import (
    Invoice,
    InvoiceStatus,
    PaymentMethod,
    PaymentProvider,
    Subscription,
    SubscriptionStatus,
)
from app.modules.billing.providers.base import PaymentProviderBase
from app.modules.billing.providers.paypal import PayPalProvider
from app.modules.billing.providers.stripe import StripeProvider
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
from app.shared.pagination import PaginatedResponse, PaginationParams


class BillingService:
    """Handles subscription creation, cancellation, and invoice queries."""

    def __init__(
        self,
        plan_repo: PlanRepository,
        sub_repo: SubscriptionRepository,
        invoice_repo: InvoiceRepository,
        pm_repo: PaymentMethodRepository,
    ) -> None:
        self._plan_repo = plan_repo
        self._sub_repo = sub_repo
        self._invoice_repo = invoice_repo
        self._pm_repo = pm_repo

    def _get_provider(self, provider: PaymentProvider) -> PaymentProviderBase:
        """Resolve the payment provider implementation.

        Args:
            provider: The payment provider enum value.

        Returns:
            The concrete PaymentProviderBase implementation.
        """
        if provider == PaymentProvider.STRIPE:
            return StripeProvider()
        return PayPalProvider()

    async def list_plans(self) -> list[PlanResponse]:
        """Retrieve all active subscription plans.

        Returns:
            A list of serialized plan responses.
        """
        plans = await self._plan_repo.get_active_plans()
        return [PlanResponse.model_validate(p) for p in plans]

    async def create_subscription(
        self,
        tenant_id: uuid.UUID,
        user_email: str,
        user_name: str,
        payload: CreateSubscriptionRequest,
    ) -> SubscriptionResponse:
        """Create a new subscription for a tenant.

        Validates no active subscription exists, resolves the plan,
        creates the customer and subscription in the external provider,
        then persists the local record.

        Args:
            tenant_id: The tenant creating the subscription.
            user_email: The billing contact email.
            user_name: The billing contact name.
            payload: Validated subscription creation data.

        Returns:
            The created subscription response.

        Raises:
            ActiveSubscriptionExistsError: If the tenant already has one.
            PlanNotFoundError: If the plan doesn't exist.
        """
        existing = await self._sub_repo.get_active_by_tenant(tenant_id)
        if existing is not None:
            raise ActiveSubscriptionExistsError()

        plan = await self._plan_repo.get_by_id(payload.plan_id)
        if plan is None:
            raise PlanNotFoundError(str(payload.plan_id))

        provider = self._get_provider(payload.payment_provider)

        # Create customer in external system
        customer = await provider.create_customer(
            email=user_email,
            name=user_name,
            tenant_id=str(tenant_id),
        )

        # Determine the price ID based on provider
        price_id = (
            plan.stripe_price_id
            if payload.payment_provider == PaymentProvider.STRIPE
            else plan.paypal_plan_id
        )

        # Create subscription in external system
        ext_sub = await provider.create_subscription(
            customer_id=customer.external_id,
            price_id=price_id or "",
            payment_method_token=payload.payment_method_token,
        )

        # Store payment method details
        pm_details = await provider.get_payment_method(payload.payment_method_token)
        await self._pm_repo.create(
            PaymentMethod(
                tenant_id=tenant_id,
                provider=payload.payment_provider,
                external_id=pm_details.external_id,
                last_four=pm_details.last_four,
                brand=pm_details.brand,
                exp_month=pm_details.exp_month,
                exp_year=pm_details.exp_year,
                is_default=True,
            )
        )

        # Persist local subscription record
        subscription = await self._sub_repo.create(
            Subscription(
                tenant_id=tenant_id,
                plan_id=plan.id,
                status=SubscriptionStatus(ext_sub.status),
                payment_provider=payload.payment_provider,
                external_sub_id=ext_sub.external_id,
                external_cust_id=customer.external_id,
                current_period_start=datetime.fromtimestamp(
                    ext_sub.current_period_start, tz=timezone.utc
                )
                if ext_sub.current_period_start
                else None,
                current_period_end=datetime.fromtimestamp(
                    ext_sub.current_period_end, tz=timezone.utc
                )
                if ext_sub.current_period_end
                else None,
            )
        )

        return SubscriptionResponse.model_validate(subscription)

    async def cancel_subscription(
        self,
        tenant_id: uuid.UUID,
        subscription_id: uuid.UUID,
        payload: CancelSubscriptionRequest,
    ) -> SubscriptionResponse:
        """Cancel an existing subscription.

        Args:
            tenant_id: The owning tenant's UUID.
            subscription_id: The subscription to cancel.
            payload: Cancellation options.

        Returns:
            The updated subscription response.

        Raises:
            SubscriptionNotFoundError: If no matching subscription exists.
        """
        subscription = await self._sub_repo.get_by_id(subscription_id)
        if subscription is None or subscription.tenant_id != tenant_id:
            raise SubscriptionNotFoundError(str(subscription_id))

        provider = self._get_provider(subscription.payment_provider)
        ext_sub = await provider.cancel_subscription(
            external_sub_id=subscription.external_sub_id or "",
            cancel_immediately=payload.cancel_immediately,
        )

        if payload.cancel_immediately:
            subscription.status = SubscriptionStatus.CANCELED
            subscription.canceled_at = datetime.now(timezone.utc)
        else:
            subscription.cancel_at_period_end = True

        await self._sub_repo.update(subscription)
        return SubscriptionResponse.model_validate(subscription)

    async def get_subscription(
        self, tenant_id: uuid.UUID
    ) -> SubscriptionResponse | None:
        """Get the current active subscription for a tenant.

        Args:
            tenant_id: The tenant's UUID.

        Returns:
            The subscription response or None.
        """
        sub = await self._sub_repo.get_active_by_tenant(tenant_id)
        if sub is None:
            return None
        return SubscriptionResponse.model_validate(sub)

    async def list_invoices(
        self, tenant_id: uuid.UUID, params: PaginationParams
    ) -> PaginatedResponse[InvoiceResponse]:
        """Retrieve paginated invoices for a tenant.

        Args:
            tenant_id: The tenant's UUID.
            params: Pagination parameters.

        Returns:
            A paginated list of invoice responses.
        """
        invoices = await self._invoice_repo.get_by_tenant(
            tenant_id, limit=params.page_size, offset=params.offset
        )
        total = await self._invoice_repo.count_by_tenant(tenant_id)
        items = [InvoiceResponse.model_validate(inv) for inv in invoices]
        return PaginatedResponse.create(items=items, total=total, params=params)

    async def list_payment_methods(
        self, tenant_id: uuid.UUID
    ) -> list[PaymentMethodResponse]:
        """Retrieve all payment methods for a tenant.

        Args:
            tenant_id: The tenant's UUID.

        Returns:
            A list of payment method responses.
        """
        methods = await self._pm_repo.get_by_tenant(tenant_id)
        return [PaymentMethodResponse.model_validate(m) for m in methods]
