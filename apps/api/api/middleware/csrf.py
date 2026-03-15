"""CSRF protection middleware and utilities.

This module provides CSRF protection using the double-submit cookie pattern.
CSRF tokens are generated per-session and validated on state-changing requests.

Security features:
- Cryptographically secure random token generation
- Token expiration (24 hours by default)
- Origin/Referer header validation as additional protection
- Configurable exempt paths for public endpoints
"""

import logging
import secrets
from datetime import datetime, timedelta
from typing import Optional, Set

from fastapi import HTTPException, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from api.config import get_settings

logger = logging.getLogger(__name__)

# CSRF cookie and header names
CSRF_COOKIE_NAME = "csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"
CSRF_TOKEN_EXPIRY_HOURS = 24

# HTTP methods that require CSRF protection
STATE_CHANGING_METHODS = {"POST", "PUT", "DELETE", "PATCH"}

# Public paths exempt from CSRF validation (must be lowercase for comparison)
EXEMPT_PATHS: Set[str] = {
    "/api/v1/auth/magic-link",
    "/api/v1/auth/verify",
    "/api/v1/auth/refresh",
    "/api/v1/csrf-token",  # The token endpoint itself is exempt
    "/api/v1/execute",  # Legacy code execution endpoint
    "/api/v1/execute/run",  # Code execution endpoint
    "/api/v1/execute/syntax-check",  # Syntax check endpoint
    "/api/v1/execute/analyze",  # Code analysis endpoint
    "/api/v1/execute/health",  # Execution health check
    "/api/v1/verify",  # Solution verification endpoint
    "/health",
    "/ready",
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
}


class CSRFTokenStore:
    """In-memory CSRF token store with expiration.
    
    In production, consider using Redis or database storage for:
    - Horizontal scaling support
    - Persistence across server restarts
    - Better memory management
    """
    
    def __init__(self):
        self._tokens: dict[str, tuple[str, datetime]] = {}
    
    def generate_token(self, session_id: str) -> str:
        """Generate a new CSRF token for a session.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            The generated CSRF token
        """
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=CSRF_TOKEN_EXPIRY_HOURS)
        self._tokens[session_id] = (token, expires_at)
        return token
    
    def validate_token(self, session_id: str, token: str) -> bool:
        """Validate a CSRF token for a session.
        
        Args:
            session_id: Unique session identifier
            token: CSRF token to validate
            
        Returns:
            True if token is valid and not expired
        """
        if session_id not in self._tokens:
            return False
        
        stored_token, expires_at = self._tokens[session_id]
        
        # Check expiration
        if datetime.utcnow() > expires_at:
            # Clean up expired token
            del self._tokens[session_id]
            return False
        
        # Use constant-time comparison to prevent timing attacks
        return secrets.compare_digest(stored_token, token)
    
    def revoke_token(self, session_id: str) -> None:
        """Revoke a CSRF token for a session.
        
        Args:
            session_id: Unique session identifier
        """
        self._tokens.pop(session_id, None)
    
    def cleanup_expired(self) -> int:
        """Clean up expired tokens.
        
        Returns:
            Number of tokens cleaned up
        """
        now = datetime.utcnow()
        expired = [
            sid for sid, (_, exp) in self._tokens.items()
            if now > exp
        ]
        for sid in expired:
            del self._tokens[sid]
        return len(expired)


# Global token store instance
# In production with multiple workers, use Redis or database
csrf_store = CSRFTokenStore()


def get_session_id(request: Request) -> str:
    """Get or create a session ID for CSRF protection.
    
    Uses a combination of:
    - User ID if authenticated (from JWT token)
    - Session cookie or IP + User-Agent fingerprint
    
    Args:
        request: FastAPI request object
        
    Returns:
        Session identifier string
    """
    # Try to get user ID from JWT token first (most reliable)
    # This requires the auth middleware to have run first
    if hasattr(request.state, "user") and request.state.user:
        return f"user:{request.state.user.id}"
    
    # Fall back to session-based identifier
    # Use existing session cookie or create fingerprint
    session_cookie = request.cookies.get("session_id")
    if session_cookie:
        return f"session:{session_cookie}"
    
    # Create fingerprint from IP and User-Agent
    # Note: This is less reliable but better than nothing
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")
    fingerprint = f"{client_ip}:{hash(user_agent) % 1000000}"
    return f"fp:{fingerprint}"


def is_exempt_path(path: str) -> bool:
    """Check if a path is exempt from CSRF validation.
    
    Args:
        path: Request path
        
    Returns:
        True if path is exempt
    """
    path_lower = path.lower()
    
    # Exact match
    if path_lower in EXEMPT_PATHS:
        return True
    
    # Prefix match for auth paths, execute paths, verify paths, and health checks
    exempt_prefixes = [
        "/api/v1/auth/",
        "/api/v1/execute/",  # All execute endpoints (run, syntax-check, analyze, health)
        "/api/v1/verify/",   # Dynamic verify paths like /verify/{problem_slug}
        "/health",
        "/ready",
        "/docs",
        "/redoc",
        "/openapi.json",
    ]
    for prefix in exempt_prefixes:
        if path_lower.startswith(prefix):
            return True
    
    return False


def validate_origin(request: Request) -> bool:
    """Validate the Origin/Referer header for additional CSRF protection.
    
    This is a defense-in-depth measure in addition to token validation.
    
    Args:
        request: FastAPI request object
        
    Returns:
        True if origin is valid or cannot be determined
    """
    settings = get_settings()
    allowed_origins = settings.allowed_origins
    
    # Skip validation if no allowed origins configured (development)
    if not allowed_origins or "*" in allowed_origins:
        return True
    
    # Check Origin header first
    origin = request.headers.get("origin")
    if origin:
        return origin in allowed_origins
    
    # Fall back to Referer header
    referer = request.headers.get("referer")
    if referer:
        # Extract origin from referer
        try:
            from urllib.parse import urlparse
            parsed = urlparse(referer)
            referer_origin = f"{parsed.scheme}://{parsed.netloc}"
            return referer_origin in allowed_origins
        except Exception:
            pass
    
    # Allow if no origin/referer (some legitimate requests may not have these)
    # This is a trade-off for usability vs security
    return True


class CSRFMiddleware(BaseHTTPMiddleware):
    """CSRF protection middleware.
    
    Validates CSRF tokens on state-changing requests (POST, PUT, DELETE, PATCH).
    Skips validation for:
    - GET, HEAD, OPTIONS, TRACE requests
    - Exempt paths (auth endpoints, health checks)
    - Requests with valid Origin/Referer headers from allowed origins
    
    Usage:
        app.add_middleware(CSRFMiddleware)
    """
    
    async def dispatch(self, request: Request, call_next):
        """Process request and validate CSRF token if required."""
        method = request.method.upper()
        path = request.url.path
        
        # Skip CSRF check for safe methods
        if method not in STATE_CHANGING_METHODS:
            return await call_next(request)
        
        # Skip CSRF check for exempt paths
        if is_exempt_path(path):
            return await call_next(request)
        
        # Additional origin validation (defense in depth)
        if not validate_origin(request):
            logger.warning(f"CSRF: Invalid origin for {method} {path}")
            return Response(
                content='{"error": "Invalid origin"}',
                status_code=status.HTTP_403_FORBIDDEN,
                headers={"Content-Type": "application/json"},
            )
        
        # Get session ID for token validation
        session_id = get_session_id(request)
        
        # Get token from header
        csrf_token = request.headers.get(CSRF_HEADER_NAME)
        
        if not csrf_token:
            logger.warning(f"CSRF: Missing token for {method} {path}")
            return Response(
                content='{"error": "CSRF token missing"}',
                status_code=status.HTTP_403_FORBIDDEN,
                headers={"Content-Type": "application/json"},
            )
        
        # Validate token
        if not csrf_store.validate_token(session_id, csrf_token):
            logger.warning(f"CSRF: Invalid token for {method} {path}")
            return Response(
                content='{"error": "Invalid CSRF token"}',
                status_code=status.HTTP_403_FORBIDDEN,
                headers={"Content-Type": "application/json"},
            )
        
        # Token is valid, proceed with request
        return await call_next(request)


def generate_csrf_token(request: Request, response: Response) -> str:
    """Generate and set a CSRF token for the current session.
    
    Args:
        request: FastAPI request object
        response: FastAPI response object
        
    Returns:
        The generated CSRF token
    """
    session_id = get_session_id(request)
    token = csrf_store.generate_token(session_id)
    
    # Set CSRF token in cookie for JavaScript access
    # This is not HttpOnly so JS can read it
    settings = get_settings()
    response.set_cookie(
        CSRF_COOKIE_NAME,
        token,
        max_age=CSRF_TOKEN_EXPIRY_HOURS * 3600,
        httponly=False,  # JavaScript needs to read this
        secure=not settings.is_development,  # HTTPS only in production
        samesite="strict",
        path="/",
    )
    
    return token


def get_csrf_token(request: Request) -> Optional[str]:
    """Get the current CSRF token for a session if it exists.
    
    Args:
        request: FastAPI request object
        
    Returns:
        The CSRF token if valid, None otherwise
    """
    session_id = get_session_id(request)
    token_cookie = request.cookies.get(CSRF_COOKIE_NAME)
    
    if token_cookie and csrf_store.validate_token(session_id, token_cookie):
        return token_cookie
    
    return None


def revoke_csrf_token(request: Request, response: Response) -> None:
    """Revoke the CSRF token for the current session.
    
    Args:
        request: FastAPI request object
        response: FastAPI response object
    """
    session_id = get_session_id(request)
    csrf_store.revoke_token(session_id)
    response.delete_cookie(CSRF_COOKIE_NAME, path="/")
