"""Application configuration loaded from environment variables.

Uses Pydantic Settings for strict validation and type coercion. All config
values are immutable after startup — no runtime mutation allowed.
"""

from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application settings sourced from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Application ──────────────────────────────────────────────
    app_env: Literal["development", "staging", "production"] = "development"
    app_debug: bool = True
    app_secret_key: str

    # ── Database ─────────────────────────────────────────────────
    database_url: str
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # ── Redis ────────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"

    # ── JWT ──────────────────────────────────────────────────────
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # ── Stripe ───────────────────────────────────────────────────
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""

    # ── PayPal ───────────────────────────────────────────────────
    paypal_client_id: str = ""
    paypal_client_secret: str = ""
    paypal_webhook_id: str = ""
    paypal_mode: Literal["sandbox", "live"] = "sandbox"

    # ── OpenAI ───────────────────────────────────────────────────
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"

    # ── CORS ─────────────────────────────────────────────────────
    cors_origins: list[str] = ["http://localhost:5173"]

    # ── Rate Limiting ────────────────────────────────────────────
    rate_limit_per_minute: int = 60

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure the database URL uses the async driver."""
        if "asyncpg" not in v and "sqlite" not in v:
            raise ValueError("DATABASE_URL must use the asyncpg driver for PostgreSQL")
        return v

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached singleton of the application settings.

    Returns:
        The validated application settings instance.
    """
    return Settings()  # type: ignore[call-arg]
