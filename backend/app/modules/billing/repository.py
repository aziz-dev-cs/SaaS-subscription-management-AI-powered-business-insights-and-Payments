"""Data access layer for the billing module.

Pure database queries — no business logic. All queries are tenant-scoped
by default to enforce data isolation.
"""

import uuid
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.billing.models import (
    DailyRevenueSnapshot,
    Invoice,
    PaymentMethod,
    Plan,
    Subscription,
    SubscriptionStatus,
    WebhookEvent,
    WebhookEventStatus,
)


class PlanRepository:
    """Database operations for Plan entities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, plan_id: uuid.UUID) -> Plan | None:
        """Fetch a plan by ID.

        Args:
            plan_id: The plan's UUID.

        Returns:
            The Plan or None.
        """
        return await self._session.get(Plan, plan_id)

    async def get_active_plans(self) -> list[Plan]:
        """Fetch all active plans ordered by sort_order.

        Returns:
            A list of active Plan instances.
        """
        stmt = select(Plan).where(Plan.is_active.is_(True)).order_by(Plan.sort_order)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_slug(self, slug: str) -> Plan | None:
        """Fetch a plan by slug.

        Args:
            slug: The plan's unique slug.

        Returns:
            The Plan or None.
        """
        stmt = select(Plan).where(Plan.slug == slug)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()


class SubscriptionRepository:
    """Database operations for Subscription entities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, sub_id: uuid.UUID) -> Subscription | None:
        """Fetch a subscription by ID.

        Args:
            sub_id: The subscription's UUID.

        Returns:
            The Subscription or None.
        """
        return await self._session.get(Subscription, sub_id)

    async def get_active_by_tenant(self, tenant_id: uuid.UUID) -> Subscription | None:
        """Fetch the active subscription for a tenant.

        Args:
            tenant_id: The tenant's UUID.

        Returns:
            The active Subscription or None.
        """
        stmt = select(Subscription).where(
            Subscription.tenant_id == tenant_id,
            Subscription.status.in_([SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_external_id(self, external_id: str) -> Subscription | None:
        """Fetch a subscription by its external provider ID.

        Args:
            external_id: The provider's subscription ID.

        Returns:
            The Subscription or None.
        """
        stmt = select(Subscription).where(Subscription.external_sub_id == external_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_tenant(self, tenant_id: uuid.UUID) -> list[Subscription]:
        """Fetch all subscriptions for a tenant.

        Args:
            tenant_id: The tenant's UUID.

        Returns:
            A list of Subscription instances.
        """
        stmt = (
            select(Subscription)
            .where(Subscription.tenant_id == tenant_id)
            .order_by(Subscription.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, subscription: Subscription) -> Subscription:
        """Persist a new subscription.

        Args:
            subscription: The Subscription instance.

        Returns:
            The persisted Subscription.
        """
        self._session.add(subscription)
        await self._session.flush()
        return subscription

    async def update(self, subscription: Subscription) -> Subscription:
        """Update an existing subscription.

        Args:
            subscription: The Subscription with updated fields.

        Returns:
            The updated Subscription.
        """
        await self._session.merge(subscription)
        await self._session.flush()
        return subscription


class InvoiceRepository:
    """Database operations for Invoice entities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_tenant(
        self, tenant_id: uuid.UUID, limit: int = 50, offset: int = 0
    ) -> list[Invoice]:
        """Fetch invoices for a tenant with pagination.

        Args:
            tenant_id: The tenant's UUID.
            limit: Max records to return.
            offset: Number of records to skip.

        Returns:
            A list of Invoice instances.
        """
        stmt = (
            select(Invoice)
            .where(Invoice.tenant_id == tenant_id)
            .order_by(Invoice.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def count_by_tenant(self, tenant_id: uuid.UUID) -> int:
        """Count total invoices for a tenant.

        Args:
            tenant_id: The tenant's UUID.

        Returns:
            The total count.
        """
        stmt = select(func.count(Invoice.id)).where(Invoice.tenant_id == tenant_id)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def create(self, invoice: Invoice) -> Invoice:
        """Persist a new invoice.

        Args:
            invoice: The Invoice instance.

        Returns:
            The persisted Invoice.
        """
        self._session.add(invoice)
        await self._session.flush()
        return invoice


class PaymentMethodRepository:
    """Database operations for PaymentMethod entities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_tenant(self, tenant_id: uuid.UUID) -> list[PaymentMethod]:
        """Fetch all payment methods for a tenant.

        Args:
            tenant_id: The tenant's UUID.

        Returns:
            A list of PaymentMethod instances.
        """
        stmt = select(PaymentMethod).where(PaymentMethod.tenant_id == tenant_id)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, pm: PaymentMethod) -> PaymentMethod:
        """Persist a new payment method.

        Args:
            pm: The PaymentMethod instance.

        Returns:
            The persisted PaymentMethod.
        """
        self._session.add(pm)
        await self._session.flush()
        return pm


class WebhookEventRepository:
    """Database operations for WebhookEvent entities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_external_id(self, external_id: str) -> WebhookEvent | None:
        """Check if a webhook event has already been received.

        Args:
            external_id: The provider's event ID.

        Returns:
            The WebhookEvent or None.
        """
        stmt = select(WebhookEvent).where(WebhookEvent.external_id == external_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, event: WebhookEvent) -> WebhookEvent:
        """Persist a new webhook event.

        Args:
            event: The WebhookEvent instance.

        Returns:
            The persisted WebhookEvent.
        """
        self._session.add(event)
        await self._session.flush()
        return event

    async def update(self, event: WebhookEvent) -> WebhookEvent:
        """Update a webhook event (e.g., mark as processed or failed).

        Args:
            event: The WebhookEvent with updated fields.

        Returns:
            The updated WebhookEvent.
        """
        await self._session.merge(event)
        await self._session.flush()
        return event

    async def get_failed_events(self, limit: int = 50) -> list[WebhookEvent]:
        """Fetch failed webhook events eligible for retry.

        Args:
            limit: Max events to return.

        Returns:
            A list of failed WebhookEvent instances.
        """
        stmt = (
            select(WebhookEvent)
            .where(
                WebhookEvent.status == WebhookEventStatus.FAILED,
                WebhookEvent.retry_count < 5,
            )
            .order_by(WebhookEvent.next_retry_at.asc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
