"""Integration tests for the auth flow (register → login → me)."""

import pytest
from httpx import AsyncClient


class TestAuthFlow:
    """End-to-end auth flow tests against the live API."""

    @pytest.mark.asyncio
    async def test_register_returns_tokens(self, client: AsyncClient) -> None:
        """POST /auth/register should return a token pair."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "StrongPass1",
                "full_name": "New User",
                "tenant_name": "Test Corp",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_with_valid_credentials(self, client: AsyncClient) -> None:
        """POST /auth/login should return tokens for valid credentials."""
        # Register first
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "logintest@example.com",
                "password": "StrongPass1",
                "full_name": "Login User",
                "tenant_name": "Login Corp",
            },
        )

        # Login
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "logintest@example.com",
                "password": "StrongPass1",
            },
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

    @pytest.mark.asyncio
    async def test_login_with_wrong_password(self, client: AsyncClient) -> None:
        """POST /auth/login should return 401 for wrong password."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "nobody@example.com",
                "password": "WrongPass1",
            },
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_me_requires_auth(self, client: AsyncClient) -> None:
        """GET /auth/me should return 401 without a token."""
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_me_returns_user(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        """GET /auth/me should return the authenticated user's profile."""
        response = await client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "full_name" in data
        assert "tenant_id" in data
