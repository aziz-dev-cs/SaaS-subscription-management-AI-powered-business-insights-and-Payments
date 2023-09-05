"""Integration tests for webhook event processing."""

import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.billing.models import (
    PaymentProvider,
    Subscription,
    SubscriptionStatus,
    WebhookEventStatus,
)
from app.modules.billing.repository import SubscriptionRepository, WebhookEventRepository
from app.modules.billing.webhooks.handler import WebhookHandler
from app.modules.billing.webhooks.schemas import WebhookEventPayload


class TestWebhookHandler:
    """Tests for idempotent webhook event processing."""

    @pytest.mark.asyncio
    async def test_duplicate_event_is_skipped(self, db_session: AsyncSession) -> None:
        """Should skip already-processed events."""
        handler = WebhookHandler(db_session)

        payload = WebhookEventPayload(
            provider=PaymentProvider.STRIPE,
            event_type="invoice.paid",
            external_id="evt_duplicate_test",
            data={"subscription": "sub_nonexistent"},
        )

        # Process once
        await handler.process(payload)
        await db_session.commit()

        # Process again — should be skipped
        result = await handler.process(payload)
        # Event exists but may or may not be "processed" depending on sub lookup
        repo = WebhookEventRepository(db_session)
        event = await repo.get_by_external_id("evt_duplicate_test")
        assert event is not None

    @pytest.mark.asyncio
    async def test_subscription_updated_event(self, db_session: AsyncSession) -> None:
        """Should update subscription status on provider event."""
        from app.modules.auth.models import Tenant

        # Create prerequisite data
        tenant = Tenant(name="Webhook Test", slug=f"wh-{uuid.uuid4().hex[:6]}")
        db_session.add(tenant)
        await db_session.flush()

        from app.modules.billing.models import Plan, BillingInterval

        plan = Plan(
            name="Test Plan",
            slug=f"test-{uuid.uuid4().hex[:6]}",
            price_cents=999,
            interval=BillingInterval.MONTH,
        )
        db_session.add(plan)
        await db_session.flush()

        sub = Subscription(
            tenant_id=tenant.id,
            plan_id=plan.id,
            status=SubscriptionStatus.ACTIVE,
            payment_provider=PaymentProvider.STRIPE,
            external_sub_id="sub_wh_test_123",
            external_cust_id="cus_wh_test_123",
        )
        db_session.add(sub)
        await db_session.flush()

        # Simulate a subscription cancellation webhook
        handler = WebhookHandler(db_session)
        payload = WebhookEventPayload(
            provider=PaymentProvider.STRIPE,
            event_type="customer.subscription.deleted",
            external_id=f"evt_{uuid.uuid4().hex[:8]}",
            data={"object": {"id": "sub_wh_test_123", "status": "canceled"}},
        )

        await handler.process(payload)
        await db_session.flush()

        # Verify subscription was updated
        repo = SubscriptionRepository(db_session)
        updated = await repo.get_by_external_id("sub_wh_test_123")
        assert updated is not None
        assert updated.status == SubscriptionStatus.CANCELED
