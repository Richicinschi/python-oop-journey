"""Request ID middleware for tracing requests across the system."""

import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware that assigns a unique ID to each request for tracing.
    
    The request ID is stored in request.state.request_id and returned
    in the X-Request-ID response header for client-side tracking.
    """
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
