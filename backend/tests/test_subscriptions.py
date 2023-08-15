from unittest.mock import AsyncMock, MagicMock

import pytest

from app.modules.subscriptions.schemas import SubscriptionCreate
from app.modules.subscriptions.service import SubscriptionService


@pytest.fixture
def sub_service():
    repo = AsyncMock()
    repo.create.return_value = MagicMock(
        id="sub-uuid",
        tenant_id="tenant_a",
        plan_id="plan_pro",
        status="active",
        cancel_at_period_end=False,
    )
    repo.get_by_id.return_value = MagicMock(
        id="sub-uuid",
        tenant_id="tenant_a",
        plan_id="plan_pro",
        status="active",
        cancel_at_period_end=False,
    )
    return SubscriptionService(repo=repo)


@pytest.mark.asyncio
async def test_subscription_creation(sub_service):
    payload = SubscriptionCreate(tenant_id="tenant_a", plan_id="plan_pro")
    sub = await sub_service.create_subscription(payload)
    assert sub is not None
    assert sub.status == "active"


@pytest.mark.asyncio
async def test_subscription_cancel(sub_service):
    sub = await sub_service.cancel_subscription("sub-uuid")
    assert sub is not None
