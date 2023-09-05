import logging
import random

logger = logging.getLogger(__name__)

MAX_RETRIES = 3

# Simulated list of failed webhook events
_failed_events = [
    {"id": "evt_001", "provider": "stripe", "type": "invoice.paid", "attempts": 0},
    {"id": "evt_002", "provider": "paypal", "type": "PAYMENT.SALE.COMPLETED", "attempts": 2},
    {"id": "evt_003", "provider": "stripe", "type": "customer.subscription.deleted", "attempts": 1},
]


def retry_failed_webhooks() -> None:
    logger.info("Starting webhook retry, %d event(s) queued", len(_failed_events))
    for event in _failed_events:
        retry_failed_webhook(event)


def retry_failed_webhook(event: dict) -> bool:
    event_id = event["id"]

    if event["attempts"] >= MAX_RETRIES:
        logger.warning("Event %s exceeded max retries, skipping", event_id)
        return False

    event["attempts"] += 1
    success = random.random() > 0.3  # ~70% chance of success

    if success:
        logger.info("Event %s retried successfully (attempt %d)", event_id, event["attempts"])
    else:
        logger.info("Event %s retry failed (attempt %d/%d)", event_id, event["attempts"], MAX_RETRIES)

    return success
