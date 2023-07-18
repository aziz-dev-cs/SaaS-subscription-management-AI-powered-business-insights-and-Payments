"""Idempotency key store and decorator for mutation endpoints.

Prevents duplicate side-effects when clients retry requests by caching
the original response keyed by a client-supplied Idempotency-Key header.
Keys expire after 24 hours.
"""

import json
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Any, Callable

from fastapi import Request, Response
from redis.asyncio import Redis

IDEMPOTENCY_TTL = timedelta(hours=24)
HEADER_NAME = "Idempotency-Key"


class IdempotencyStore:
    """Redis-backed store for idempotency keys."""

    def __init__(self, redis: Redis) -> None:  # type: ignore[type-arg]
        self._redis = redis
        self._prefix = "idempotency:"

    async def get(self, key: str) -> dict[str, Any] | None:
        """Retrieve a cached response for the given idempotency key.

        Args:
            key: The client-supplied idempotency key.

        Returns:
            The cached response dict or None if not found.
        """
        raw = await self._redis.get(f"{self._prefix}{key}")
        if raw is None:
            return None
        return json.loads(raw)

    async def set(self, key: str, status_code: int, body: dict[str, Any]) -> None:
        """Cache a response against the given idempotency key.

        Args:
            key: The client-supplied idempotency key.
            status_code: The HTTP status code of the response.
            body: The JSON response body.
        """
        payload = json.dumps({"status_code": status_code, "body": body})
        await self._redis.setex(
            f"{self._prefix}{key}",
            int(IDEMPOTENCY_TTL.total_seconds()),
            payload,
        )

    async def exists(self, key: str) -> bool:
        """Check whether a key already exists in the store.

        Args:
            key: The client-supplied idempotency key.

        Returns:
            True if the key is present, False otherwise.
        """
        return bool(await self._redis.exists(f"{self._prefix}{key}"))


def idempotent(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that enforces idempotency on a route handler.

    The decorated handler must accept ``request: Request`` and have access
    to ``request.app.state.idempotency_store``.

    Args:
        fn: The async route handler to wrap.

    Returns:
        The wrapped handler with idempotency enforcement.
    """

    @wraps(fn)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        request: Request = kwargs.get("request") or args[0]
        idem_key = request.headers.get(HEADER_NAME)

        if not idem_key:
            return await fn(*args, **kwargs)

        store: IdempotencyStore = request.app.state.idempotency_store
        cached = await store.get(idem_key)

        if cached is not None:
            return Response(
                content=json.dumps(cached["body"]),
                status_code=cached["status_code"],
                media_type="application/json",
            )

        result = await fn(*args, **kwargs)
        return result

    return wrapper
