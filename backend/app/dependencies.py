"""FastAPI dependency injection providers.

Centralizes all injectable dependencies: database sessions, authenticated
user context, and third-party client instances. Every route handler receives
its dependencies through this module — never via global imports.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.shared.database import get_db_session
from app.shared.security import JWTError, decode_token

# ── Type aliases for DI ─────────────────────────────────────────

DBSession = Annotated[AsyncSession, Depends(get_db_session)]
AppSettings = Annotated[Settings, Depends(get_settings)]

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> str:
    """Extract and validate the user ID from the JWT bearer token.

    Args:
        credentials: The HTTP bearer credentials from the Authorization header.

    Returns:
        The user ID (UUID string) embedded in the token subject.

    Raises:
        HTTPException: 401 if the token is missing, invalid, or expired.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_token(credentials.credentials)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


CurrentUserID = Annotated[str, Depends(get_current_user_id)]
