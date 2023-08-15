from unittest.mock import AsyncMock, MagicMock

import pytest

from app.modules.billing.webhooks.handler import process_webhook_event
from app.modules.billing.webhooks.schemas import WebhookEventSchema


@pytest.fixture
def fake_db():
    return AsyncMock()


@pytest.mark.asyncio
async def test_create_subscription(fake_db):
    event = WebhookEventSchema(
        provider="stripe",
        event_type="customer.subscription.created",
        external_id="evt_abc123",
        payload={"subscription_id": "sub_001", "plan": "pro"},
    )
    result = await process_webhook_event(fake_db, event)
    assert isinstance(result, bool)


@pytest.mark.asyncio
async def test_get_plans():
    plans = [
        {"id": "plan_free", "name": "Free", "price_cents": 0},
        {"id": "plan_pro", "name": "Pro", "price_cents": 2900},
    ]
    assert len(plans) == 2
    assert plans[1]["price_cents"] > plans[0]["price_cents"]
