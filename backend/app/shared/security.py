"""JWT token management and password hashing utilities.

Centralizes all authentication primitives so that no module directly
interacts with cryptographic libraries.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password using bcrypt.

    Args:
        plain_password: The user-supplied plaintext password.

    Returns:
        The bcrypt-hashed password string.
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its bcrypt hash.

    Args:
        plain_password: The user-supplied plaintext password.
        hashed_password: The stored bcrypt hash.

    Returns:
        True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, extra_claims: dict[str, Any] | None = None) -> str:
    """Create a short-lived JWT access token.

    Args:
        subject: The token subject (typically user ID).
        extra_claims: Optional additional claims to embed.

    Returns:
        The encoded JWT string.
    """
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    payload: dict[str, Any] = {"sub": subject, "exp": expires, "type": "access"}
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str) -> str:
    """Create a long-lived JWT refresh token.

    Args:
        subject: The token subject (typically user ID).

    Returns:
        The encoded JWT string.
    """
    expires = datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_token_expire_days)
    payload: dict[str, Any] = {"sub": subject, "exp": expires, "type": "refresh"}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token.

    Args:
        token: The raw JWT string.

    Returns:
        The decoded payload dictionary.

    Raises:
        JWTError: If the token is invalid or expired.
    """
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


__all__ = [
    "JWTError",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "hash_password",
    "verify_password",
]
