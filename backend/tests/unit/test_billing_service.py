"""Unit tests for the BillingService."""

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.modules.billing.exceptions import (
    ActiveSubscriptionExistsError,
    PlanNotFoundError,
)
from app.modules.billing.models import (
    BillingInterval,
    PaymentProvider,
    Plan,
    SubscriptionStatus,
)
from app.modules.billing.schemas import CreateSubscriptionRequest
from app.modules.billing.service import BillingService


@pytest.fixture
def plan_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def sub_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def invoice_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def pm_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def billing_service(
    plan_repo: AsyncMock,
    sub_repo: AsyncMock,
    invoice_repo: AsyncMock,
    pm_repo: AsyncMock,
) -> BillingService:
    return BillingService(
        plan_repo=plan_repo,
        sub_repo=sub_repo,
        invoice_repo=invoice_repo,
        pm_repo=pm_repo,
    )


class TestListPlans:
    """Tests for BillingService.list_plans."""

    async def test_returns_active_plans(
        self, billing_service: BillingService, plan_repo: AsyncMock
    ) -> None:
        """Should return serialized active plans."""
        mock_plan = MagicMock()
        mock_plan.id = uuid.uuid4()
        mock_plan.name = "Pro"
        mock_plan.slug = "pro"
        mock_plan.description = "Pro plan"
        mock_plan.price_cents = 2999
        mock_plan.currency = "usd"
        mock_plan.interval = BillingInterval.MONTH
        mock_plan.features = {"max_seats": 10}
        mock_plan.is_active = True
        mock_plan.sort_order = 1

        plan_repo.get_active_plans.return_value = [mock_plan]

        plans = await billing_service.list_plans()
        assert len(plans) == 1
        assert plans[0].name == "Pro"
        assert plans[0].price_cents == 2999


class TestCreateSubscription:
    """Tests for BillingService.create_subscription."""

    async def test_fails_if_active_subscription_exists(
        self, billing_service: BillingService, sub_repo: AsyncMock
    ) -> None:
        """Should raise ActiveSubscriptionExistsError."""
        sub_repo.get_active_by_tenant.return_value = MagicMock()

        payload = CreateSubscriptionRequest(
            plan_id=uuid.uuid4(),
            payment_provider=PaymentProvider.STRIPE,
            payment_method_token="pm_test",
        )

        with pytest.raises(ActiveSubscriptionExistsError):
            await billing_service.create_subscription(
                tenant_id=uuid.uuid4(),
                user_email="user@test.com",
                user_name="Test",
                payload=payload,
            )

    async def test_fails_if_plan_not_found(
        self, billing_service: BillingService, sub_repo: AsyncMock, plan_repo: AsyncMock
    ) -> None:
        """Should raise PlanNotFoundError for invalid plan ID."""
        sub_repo.get_active_by_tenant.return_value = None
        plan_repo.get_by_id.return_value = None

        payload = CreateSubscriptionRequest(
            plan_id=uuid.uuid4(),
            payment_provider=PaymentProvider.STRIPE,
            payment_method_token="pm_test",
        )

        with pytest.raises(PlanNotFoundError):
            await billing_service.create_subscription(
                tenant_id=uuid.uuid4(),
                user_email="user@test.com",
                user_name="Test",
                payload=payload,
            )
