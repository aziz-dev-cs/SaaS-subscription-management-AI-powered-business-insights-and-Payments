"""Token-bucket rate limiter backed by Redis.

Applies per-IP rate limiting with configurable limits. Auth endpoints
receive a stricter limit to prevent brute-force attacks.
"""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config import get_settings

settings = get_settings()

AUTH_PATHS = {"/api/v1/auth/login", "/api/v1/auth/register"}
AUTH_RATE_LIMIT = 10  # stricter limit for auth endpoints


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """Redis-backed token-bucket rate limiter."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Check rate limits before forwarding the request.

        Args:
            request: The incoming HTTP request.
            call_next: The next middleware or route handler.

        Returns:
            The response, or a 429 if the rate limit is exceeded.
        """
        if not hasattr(request.app.state, "redis"):
            return await call_next(request)

        redis = request.app.state.redis
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path

        # Determine the appropriate limit
        if path in AUTH_PATHS:
            limit = AUTH_RATE_LIMIT
            key = f"rate_limit:auth:{client_ip}"
        else:
            limit = settings.rate_limit_per_minute
            key = f"rate_limit:global:{client_ip}"

        current = await redis.get(key)

        if current is not None and int(current) >= limit:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded. Please try again later.",
                    "retry_after_seconds": 60,
                },
                headers={"Retry-After": "60"},
            )

        pipe = redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, 60)
        await pipe.execute()

        response = await call_next(request)
        remaining = max(0, limit - (int(current or 0) + 1))
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response
