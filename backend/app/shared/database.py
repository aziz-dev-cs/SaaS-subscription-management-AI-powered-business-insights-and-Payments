"""Async SQLAlchemy engine and session factory.

Provides a single engine instance and a session-local factory that is injected
into request handlers via FastAPI's dependency system.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    echo=settings.app_debug,
    future=True,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""

    pass


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a transactional database session.

    The session is automatically committed on success and rolled back on
    unhandled exceptions. Always closed after the request completes.

    Yields:
        An async SQLAlchemy session bound to the current request.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
