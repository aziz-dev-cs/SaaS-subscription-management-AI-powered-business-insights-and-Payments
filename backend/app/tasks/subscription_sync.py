import logging

logger = logging.getLogger(__name__)

# Simulated subscriptions that need syncing
_subscriptions = [
    {"id": "sub_101", "tenant": "tenant_a", "status": "active", "provider_status": "active"},
    {"id": "sub_102", "tenant": "tenant_b", "status": "active", "provider_status": "canceled"},
    {"id": "sub_103", "tenant": "tenant_c", "status": "past_due", "provider_status": "active"},
]


def sync_subscriptions() -> int:
    logger.info("Starting subscription sync, %d subscription(s) to check", len(_subscriptions))
    updated = 0

    for sub in _subscriptions:
        if sub["status"] != sub["provider_status"]:
            logger.info(
                "Subscription %s drift detected: local=%s provider=%s → updating",
                sub["id"], sub["status"], sub["provider_status"],
            )
            sub["status"] = sub["provider_status"]
            updated += 1
        else:
            logger.debug("Subscription %s in sync", sub["id"])

    logger.info("Subscription sync complete: %d updated", updated)
    return updated
