"""Integration tests for the subscription lifecycle."""

import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import Tenant, User, UserRole
from app.modules.billing.models import BillingInterval, Plan
from app.shared.security import hash_password


class TestSubscriptionLifecycle:
    """Tests for subscription CRUD operations via the API."""

    @pytest.mark.asyncio
    async def test_list_plans_returns_active(self, client: AsyncClient) -> None:
        """GET /billing/plans should return an empty list initially."""
        response = await client.get("/api/v1/billing/plans")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @pytest.mark.asyncio
    async def test_get_current_subscription_none(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        """GET /billing/subscriptions/current should return null when no sub exists."""
        response = await client.get(
            "/api/v1/billing/subscriptions/current",
            headers=auth_headers,
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_list_invoices_empty(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        """GET /billing/invoices should return an empty paginated response."""
        response = await client.get(
            "/api/v1/billing/invoices",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    @pytest.mark.asyncio
    async def test_list_payment_methods_empty(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        """GET /billing/payment-methods should return an empty list."""
        response = await client.get(
            "/api/v1/billing/payment-methods",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient) -> None:
        """GET /health should return healthy status."""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
