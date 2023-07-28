from unittest.mock import AsyncMock, MagicMock

import pytest

from app.modules.auth.schemas import UserCreate, UserLogin
from app.modules.auth.service import AuthService


@pytest.fixture
def auth_service():
    repo = AsyncMock()
    repo.create_user.return_value = MagicMock(id="fake-uuid", email="test@example.com")
    repo.get_user_by_email.return_value = MagicMock(id="fake-uuid", email="test@example.com")
    return AuthService(repo=repo)


@pytest.mark.asyncio
async def test_register_user(auth_service):
    payload = UserCreate(email="new@example.com", password="Pass1234", full_name="New User", tenant_name="Acme")
    user = await auth_service.register_user(payload)
    assert user is not None
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_login_user(auth_service):
    payload = UserLogin(email="test@example.com", password="Pass1234")
    user = await auth_service.login_user(payload)
    assert user is not None
