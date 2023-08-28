import logging

from app.tasks.webhook_retry import retry_failed_webhooks
from app.tasks.subscription_sync import sync_subscriptions

logger = logging.getLogger(__name__)

TASK_REGISTRY = {
    "retry_webhooks": retry_failed_webhooks,
    "sync_subscriptions": sync_subscriptions,
}


class Worker:
    def __init__(self, tasks: list[str] | None = None) -> None:
        self._tasks = tasks or list(TASK_REGISTRY.keys())

    def run(self) -> None:
        logger.info("Worker started, processing %d task(s)", len(self._tasks))
        for task_name in self._tasks:
            self.process_task(task_name)
        logger.info("Worker finished all tasks")

    def process_task(self, task_name: str) -> None:
        handler = TASK_REGISTRY.get(task_name)
        if handler is None:
            logger.warning("Unknown task: %s", task_name)
            return
        logger.info("Running task: %s", task_name)
        handler()
        logger.info("Completed task: %s", task_name)
