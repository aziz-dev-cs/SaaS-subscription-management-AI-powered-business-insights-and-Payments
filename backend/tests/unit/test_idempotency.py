"""Unit tests for the idempotency store."""

import json
from unittest.mock import AsyncMock

import pytest

from app.shared.idempotency import IdempotencyStore


@pytest.fixture
def mock_redis() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def store(mock_redis: AsyncMock) -> IdempotencyStore:
    return IdempotencyStore(mock_redis)


class TestIdempotencyStore:
    """Tests for IdempotencyStore operations."""

    async def test_get_returns_none_for_missing_key(
        self, store: IdempotencyStore, mock_redis: AsyncMock
    ) -> None:
        """Should return None when the key doesn't exist."""
        mock_redis.get.return_value = None
        result = await store.get("nonexistent-key")
        assert result is None

    async def test_get_returns_cached_response(
        self, store: IdempotencyStore, mock_redis: AsyncMock
    ) -> None:
        """Should return the cached response dict."""
        cached = {"status_code": 201, "body": {"id": "123"}}
        mock_redis.get.return_value = json.dumps(cached)

        result = await store.get("my-key")
        assert result is not None
        assert result["status_code"] == 201
        assert result["body"]["id"] == "123"

    async def test_set_stores_with_ttl(
        self, store: IdempotencyStore, mock_redis: AsyncMock
    ) -> None:
        """Should store the response with a 24-hour TTL."""
        await store.set("my-key", 201, {"id": "123"})

        mock_redis.setex.assert_called_once()
        args = mock_redis.setex.call_args
        assert args[0][0] == "idempotency:my-key"
        assert args[0][1] == 86400  # 24 hours in seconds

    async def test_exists_returns_true_for_existing_key(
        self, store: IdempotencyStore, mock_redis: AsyncMock
    ) -> None:
        """Should return True when the key exists."""
        mock_redis.exists.return_value = 1
        assert await store.exists("my-key") is True

    async def test_exists_returns_false_for_missing_key(
        self, store: IdempotencyStore, mock_redis: AsyncMock
    ) -> None:
        """Should return False when the key doesn't exist."""
        mock_redis.exists.return_value = 0
        assert await store.exists("missing-key") is False
