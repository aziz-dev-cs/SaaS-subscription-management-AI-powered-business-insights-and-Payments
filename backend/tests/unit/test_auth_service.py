"""Unit tests for the AuthService."""

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.modules.auth.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UserInactiveError,
)
from app.modules.auth.models import User, UserRole
from app.modules.auth.schemas import RegisterRequest
from app.modules.auth.service import AuthService
from app.shared.security import hash_password


@pytest.fixture
def user_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def tenant_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def auth_service(user_repo: AsyncMock, tenant_repo: AsyncMock) -> AuthService:
    return AuthService(user_repo=user_repo, tenant_repo=tenant_repo)


class TestRegister:
    """Tests for AuthService.register."""

    async def test_register_success(
        self, auth_service: AuthService, user_repo: AsyncMock, tenant_repo: AsyncMock
    ) -> None:
        """Should create a tenant and user, returning tokens."""
        user_repo.email_exists.return_value = False
        tenant_repo.slug_exists.return_value = False

        mock_tenant = MagicMock()
        mock_tenant.id = uuid.uuid4()
        tenant_repo.create.return_value = mock_tenant

        mock_user = MagicMock()
        mock_user.id = uuid.uuid4()
        mock_user.tenant_id = mock_tenant.id
        user_repo.create.return_value = mock_user

        payload = RegisterRequest(
            email="new@example.com",
            password="StrongPass1",
            full_name="New User",
            tenant_name="New Corp",
        )

        user, tenant, tokens = await auth_service.register(payload)

        assert tokens.access_token
        assert tokens.refresh_token
        user_repo.create.assert_called_once()
        tenant_repo.create.assert_called_once()

    async def test_register_duplicate_email(
        self, auth_service: AuthService, user_repo: AsyncMock
    ) -> None:
        """Should raise EmailAlreadyExistsError for duplicate emails."""
        user_repo.email_exists.return_value = True

        payload = RegisterRequest(
            email="taken@example.com",
            password="StrongPass1",
            full_name="User",
            tenant_name="Corp",
        )

        with pytest.raises(EmailAlreadyExistsError):
            await auth_service.register(payload)


class TestLogin:
    """Tests for AuthService.login."""

    async def test_login_success(
        self, auth_service: AuthService, user_repo: AsyncMock
    ) -> None:
        """Should return tokens for valid credentials."""
        mock_user = MagicMock()
        mock_user.id = uuid.uuid4()
        mock_user.tenant_id = uuid.uuid4()
        mock_user.hashed_password = hash_password("CorrectPass1")
        mock_user.is_active = True
        user_repo.get_by_email.return_value = mock_user

        user, tokens = await auth_service.login("user@example.com", "CorrectPass1")

        assert tokens.access_token
        assert tokens.token_type == "bearer"

    async def test_login_wrong_password(
        self, auth_service: AuthService, user_repo: AsyncMock
    ) -> None:
        """Should raise InvalidCredentialsError for wrong password."""
        mock_user = MagicMock()
        mock_user.hashed_password = hash_password("CorrectPass1")
        user_repo.get_by_email.return_value = mock_user

        with pytest.raises(InvalidCredentialsError):
            await auth_service.login("user@example.com", "WrongPass1")

    async def test_login_inactive_user(
        self, auth_service: AuthService, user_repo: AsyncMock
    ) -> None:
        """Should raise UserInactiveError for deactivated accounts."""
        mock_user = MagicMock()
        mock_user.hashed_password = hash_password("CorrectPass1")
        mock_user.is_active = False
        user_repo.get_by_email.return_value = mock_user

        with pytest.raises(UserInactiveError):
            await auth_service.login("user@example.com", "CorrectPass1")

    async def test_login_nonexistent_user(
        self, auth_service: AuthService, user_repo: AsyncMock
    ) -> None:
        """Should raise InvalidCredentialsError for unknown email."""
        user_repo.get_by_email.return_value = None

        with pytest.raises(InvalidCredentialsError):
            await auth_service.login("nobody@example.com", "SomePass1")
