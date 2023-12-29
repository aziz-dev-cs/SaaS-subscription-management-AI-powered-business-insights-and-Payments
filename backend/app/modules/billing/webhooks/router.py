from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database import get_db_session
from app.modules.billing.webhooks.handler import process_webhook_event
from app.modules.billing.webhooks.schemas import WebhookEventSchema

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/stripe")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db_session)):
    body = await request.json()
    event = WebhookEventSchema(
        provider="stripe",
        event_type=body.get("type", ""),
        external_id=body.get("id", ""),
        payload=body,
    )
    processed = await process_webhook_event(db, event)
    return {"status": "processed" if processed else "duplicate"}


@router.post("/paypal")
async def paypal_webhook(request: Request, db: AsyncSession = Depends(get_db_session)):
    body = await request.json()
    event = WebhookEventSchema(
        provider="paypal",
        event_type=body.get("event_type", ""),
        external_id=body.get("id", ""),
        payload=body,
    )
    processed = await process_webhook_event(db, event)
    return {"status": "processed" if processed else "duplicate"}
