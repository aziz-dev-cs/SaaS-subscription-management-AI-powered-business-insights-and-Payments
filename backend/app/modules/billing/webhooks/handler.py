import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.billing.webhooks.schemas import WebhookEventSchema

logger = logging.getLogger(__name__)

# Simple in-memory set to track processed events (placeholder for DB lookup)
_processed_events: set[str] = set()


async def process_webhook_event(db: AsyncSession, event: WebhookEventSchema) -> bool:
    # Duplicate check
    if event.external_id in _processed_events:
        logger.info("Event %s already processed, skipping", event.external_id)
        return False

    # Mark as processed
    _processed_events.add(event.external_id)

    # TODO: persist event to webhook_events table via db
    logger.info("Processed %s event: %s", event.provider, event.event_type)
    return True
