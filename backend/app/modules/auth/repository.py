import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import User


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_by_email(self, email: str) -> User | None:
        # TODO: query user by email
        pass

    async def create_user(self, user: User) -> User:
        # TODO: persist user to database
        self._session.add(user)
        await self._session.flush()
        return user

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        # TODO: query user by primary key
        pass
