import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.subscriptions.models import Subscription


class SubscriptionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_subscription(self, subscription_id: uuid.UUID) -> Subscription | None:
        stmt = select(Subscription).where(Subscription.id == subscription_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_subscription(self, subscription: Subscription) -> Subscription:
        self._session.add(subscription)
        await self._session.flush()
        return subscription

    async def update_subscription(self, subscription: Subscription) -> Subscription:
        await self._session.merge(subscription)
        await self._session.flush()
        return subscription
