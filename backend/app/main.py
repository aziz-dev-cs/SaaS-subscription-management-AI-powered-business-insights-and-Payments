"""FastAPI application factory.

Assembles the application by registering middleware, routers, and
startup/shutdown lifecycle hooks. This is the single entrypoint
for the ASGI server.
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

import structlog
from fastapi import FastAPI
from redis.asyncio import from_url as redis_from_url

from app.config import get_settings
from app.middleware.cors import configure_cors
from app.middleware.error_handler import configure_error_handlers
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware
from app.shared.idempotency import IdempotencyStore

settings = get_settings()
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager — handles startup and shutdown.

    Initializes Redis connection pool and idempotency store on startup.
    Gracefully closes connections on shutdown.

    Args:
        app: The FastAPI application instance.

    Yields:
        Control back to the framework between startup and shutdown.
    """
    # ── Startup ──────────────────────────────────────────────────
    await logger.ainfo("Starting SaaS Dashboard API", env=settings.app_env)

    app.state.redis = redis_from_url(settings.redis_url, decode_responses=True)
    app.state.idempotency_store = IdempotencyStore(app.state.redis)

    yield

    # ── Shutdown ─────────────────────────────────────────────────
    await logger.ainfo("Shutting down SaaS Dashboard API")
    await app.state.redis.close()


def create_app() -> FastAPI:
    """Build and configure the FastAPI application.

    Returns:
        The fully configured FastAPI application instance.
    """
    app = FastAPI(
        title="SaaS Subscription Dashboard",
        description="Modular monolith API for subscription management with Stripe/PayPal integration",
        version="1.0.0",
        docs_url="/api/docs" if not settings.is_production else None,
        redoc_url="/api/redoc" if not settings.is_production else None,
        openapi_url="/api/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # ── Middleware (applied in reverse order) ────────────────────
    app.add_middleware(RateLimiterMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    configure_cors(app)
    configure_error_handlers(app)

    # ── Routers ──────────────────────────────────────────────────
    from app.modules.auth.router import router as auth_router
    from app.modules.billing.router import router as billing_router
    from app.modules.billing.webhooks.router import router as webhooks_router
    from app.modules.subscriptions.router import router as subscriptions_router
    from app.modules.analytics.router import router as analytics_router
    from app.modules.ai_insights.router import router as insights_router

    api_prefix = "/api/v1"
    app.include_router(auth_router, prefix=api_prefix)
    app.include_router(billing_router, prefix=api_prefix)
    app.include_router(subscriptions_router, prefix=api_prefix)
    app.include_router(analytics_router, prefix=api_prefix)
    app.include_router(insights_router, prefix=api_prefix)

    # Webhooks are mounted at root level (no auth, no API prefix)
    app.include_router(webhooks_router)

    @app.get("/health", tags=["System"])
    async def health_check() -> dict[str, str]:
        """Liveness probe for container orchestration."""
        return {"status": "healthy", "version": "1.0.0"}

    return app


app = create_app()
