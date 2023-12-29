"""Retry-capable background task runner.

Provides an exponential-backoff retry mechanism used by webhook processors
and other async jobs that need resilient execution.
"""

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_MAX_RETRIES = 5
BACKOFF_MULTIPLIER = 2
INITIAL_DELAY_SECONDS = 30


async def run_with_retry(
    task: Callable[..., Awaitable[Any]],
    *args: Any,
    max_retries: int = DEFAULT_MAX_RETRIES,
    initial_delay: float = INITIAL_DELAY_SECONDS,
    **kwargs: Any,
) -> Any:
    """Execute an async callable with exponential-backoff retries.

    Retries on any exception up to ``max_retries`` times. The delay between
    retries doubles each attempt: 30s → 60s → 120s → 240s → 480s by default.

    Args:
        task: The async function to execute.
        *args: Positional arguments forwarded to the task.
        max_retries: Maximum number of retry attempts.
        initial_delay: Seconds to wait before the first retry.
        **kwargs: Keyword arguments forwarded to the task.

    Returns:
        The result of the task if it eventually succeeds.

    Raises:
        Exception: The last exception if all retries are exhausted.
    """
    delay = initial_delay
    last_exception: Exception | None = None

    for attempt in range(max_retries + 1):
        try:
            return await task(*args, **kwargs)
        except Exception as exc:
            last_exception = exc
            if attempt < max_retries:
                logger.warning(
                    "Task %s failed (attempt %d/%d), retrying in %.0fs: %s",
                    task.__name__,
                    attempt + 1,
                    max_retries + 1,
                    delay,
                    str(exc),
                )
                await asyncio.sleep(delay)
                delay *= BACKOFF_MULTIPLIER
            else:
                logger.error(
                    "Task %s exhausted all %d retries: %s",
                    task.__name__,
                    max_retries + 1,
                    str(exc),
                )

    raise last_exception  # type: ignore[misc]
