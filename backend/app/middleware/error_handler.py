"""Global exception handler middleware.

Catches all unhandled exceptions and returns a consistent JSON error
response. Stack traces are included in development but stripped in
production to avoid information leakage.
"""

import traceback

import structlog
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import get_settings

logger = structlog.get_logger(__name__)


def configure_error_handlers(app: FastAPI) -> None:
    """Register global exception handlers on the FastAPI app.

    Args:
        app: The FastAPI application instance.
    """
    settings = get_settings()

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        """Handle expected HTTP exceptions with a standard envelope."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.status_code,
                    "message": exc.detail,
                    "request_id": getattr(request.state, "request_id", None),
                }
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle Pydantic validation errors with detailed field info."""
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": 422,
                    "message": "Validation error",
                    "details": exc.errors(),
                    "request_id": getattr(request.state, "request_id", None),
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Catch-all for unexpected exceptions."""
        request_id = getattr(request.state, "request_id", None)
        await logger.aerror(
            "unhandled_exception",
            request_id=request_id,
            error=str(exc),
            traceback=traceback.format_exc(),
        )

        detail: str | dict[str, str] = "Internal server error"
        if not settings.is_production:
            detail = {"message": str(exc), "traceback": traceback.format_exc()}

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": 500,
                    "message": detail,
                    "request_id": request_id,
                }
            },
        )
