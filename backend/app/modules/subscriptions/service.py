import uuid

from app.modules.subscriptions.models import Subscription
from app.modules.subscriptions.repository import SubscriptionRepository
from app.modules.subscriptions.schemas import SubscriptionCreate


class SubscriptionService:
    def __init__(self, repo: SubscriptionRepository) -> None:
        self._repo = repo

    async def create_subscription(self, payload: SubscriptionCreate) -> Subscription:
        subscription = Subscription(
            tenant_id=payload.tenant_id,
            plan_id=payload.plan_id,
            status="active",
        )
        return await self._repo.create_subscription(subscription)

    async def cancel_subscription(self, subscription_id: uuid.UUID) -> Subscription | None:
        subscription = await self._repo.get_subscription(subscription_id)
        if subscription is None:
            return None
        subscription.cancel_at_period_end = True
        return await self._repo.update_subscription(subscription)
