import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from utils.json_logger import logger


class RequestIDMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        response = await call_next(request)

        logger.info(f"RequestID: {request_id} Path: {request.url.path}")

        response.headers["X-Request-ID"] = request_id
        return response
