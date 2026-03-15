"""Security headers middleware for FastAPI.

This module provides security headers to protect against common web vulnerabilities
including XSS, clickjacking, MIME sniffing, and other client-side attacks.
"""

import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# Security header values
CONTENT_SECURITY_POLICY = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "  # Needed for Monaco editor
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data: https:; "
    "font-src 'self'; "
    "connect-src 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self';"
)

PERMISSIONS_POLICY = (
    "accelerometer=(), "
    "camera=(), "
    "geolocation=(), "
    "gyroscope=(), "
    "magnetometer=(), "
    "microphone=(), "
    "payment=(), "
    "usb=()"
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses.
    
    Headers added:
    - X-Content-Type-Options: Prevents MIME type sniffing
    - X-Frame-Options: Prevents clickjacking
    - X-XSS-Protection: Legacy XSS filter (for older browsers)
    - Strict-Transport-Security: Enforces HTTPS
    - Content-Security-Policy: Restricts resource loading
    - Referrer-Policy: Controls referrer information
    - Permissions-Policy: Restricts browser features
    """
    
    async def dispatch(self, request: Request, call_next):
        """Add security headers to response."""
        response = await call_next(request)
        
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        
        # Legacy XSS protection (for older browsers)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Content Security Policy
        response.headers["Content-Security-Policy"] = CONTENT_SECURITY_POLICY
        
        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Permissions Policy
        response.headers["Permissions-Policy"] = PERMISSIONS_POLICY
        
        return response


class HSTSHeaderMiddleware(BaseHTTPMiddleware):
    """HSTS (HTTP Strict Transport Security) middleware.
    
    Only active in production to enforce HTTPS connections.
    Should be placed after HTTPS termination (e.g., by load balancer/reverse proxy).
    """
    
    def __init__(self, app, max_age: int = 31536000, include_subdomains: bool = True, preload: bool = True):
        super().__init__(app)
        self.max_age = max_age
        self.include_subdomains = include_subdomains
        self.preload = preload
    
    async def dispatch(self, request: Request, call_next):
        """Add HSTS header to response."""
        response = await call_next(request)
        
        # Build HSTS value
        hsts_value = f"max-age={self.max_age}"
        if self.include_subdomains:
            hsts_value += "; includeSubDomains"
        if self.preload:
            hsts_value += "; preload"
        
        response.headers["Strict-Transport-Security"] = hsts_value
        
        return response
