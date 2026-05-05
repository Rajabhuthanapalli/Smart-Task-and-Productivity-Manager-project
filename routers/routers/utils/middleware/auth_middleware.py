from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from utils.auth import verify_token


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # Skip auth for health check
        if request.url.path == "/health":
            return await call_next(request)

        verify_token(request)

        response = await call_next(request)
        return response
