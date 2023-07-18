"""CORS middleware configuration.

Reads allowed origins from application settings. In production,
wildcard origins are explicitly rejected.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings


def configure_cors(app: FastAPI) -> None:
    """Attach CORS middleware to the FastAPI application.

    Args:
        app: The FastAPI application instance.
    """
    settings = get_settings()

    if settings.is_production and "*" in settings.cors_origins:
        raise ValueError("Wildcard CORS origin is not allowed in production")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-RateLimit-Limit", "X-RateLimit-Remaining"],
    )
