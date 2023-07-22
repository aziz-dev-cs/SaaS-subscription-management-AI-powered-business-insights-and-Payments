import uuid

from app.modules.auth.models import User
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import UserCreate, UserLogin


class AuthService:
    def __init__(self, repo: AuthRepository) -> None:
        self._repo = repo

    async def register_user(self, payload: UserCreate) -> User:
        # TODO: hash password, create user via repo
        user = User(
            email=payload.email,
            hashed_password=payload.password,  # placeholder — hash in real impl
            full_name=payload.full_name,
        )
        return await self._repo.create_user(user)

    async def login_user(self, payload: UserLogin) -> User | None:
        # TODO: verify password, return user or None
        user = await self._repo.get_user_by_email(payload.email)
        return user

    async def get_current_user(self, user_id: str) -> User | None:
        # TODO: fetch authenticated user by id
        return await self._repo.get_user_by_id(uuid.UUID(user_id))
