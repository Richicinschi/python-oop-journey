"""Authentication middleware and dependencies."""

import logging
from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import get_settings
from api.database import get_db
from api.models.user import User
from api.services.auth import AuthService

logger = logging.getLogger(__name__)
settings = get_settings()

# Use HTTPBearer for JWT token extraction
security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get current authenticated user from JWT token.
    
    This dependency extracts the JWT from the Authorization header,
    validates it, and returns the corresponding user.
    
    Args:
        request: FastAPI request object
        credentials: HTTP Bearer credentials
        db: Database session
        
    Returns:
        Authenticated User object
        
    Raises:
        HTTPException: If token is missing, invalid, or user not found
    """
    # Check for token in Authorization header
    token = None
    if credentials:
        token = credentials.credentials
    else:
        # Also check for token in cookie
        token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify JWT
    auth_service = AuthService(db)
    payload = auth_service.verify_jwt(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user ID from token
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Fetch user from database
    user = await auth_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )
    
    return user


async def get_optional_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """Get current user if authenticated, otherwise return None.
    
    This is useful for endpoints that work for both authenticated
    and anonymous users.
    
    Args:
        request: FastAPI request object
        credentials: HTTP Bearer credentials
        db: Database session
        
    Returns:
        User if authenticated, None otherwise
    """
    try:
        return await get_current_user(request, credentials, db)
    except HTTPException:
        return None


class AuthMiddleware:
    """Middleware to handle authentication and add user to request state."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        """Process request and add user to scope."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        # Note: Middleware-level auth is complex with async SQLAlchemy
        # We use dependency injection instead for most cases
        await self.app(scope, receive, send)


def require_auth():
    """Dependency to require authentication.
    
    Usage:
        @router.get("/protected")
        async def protected_route(user: User = Depends(require_auth())):
            return {"message": f"Hello {user.email}"}
    """
    return get_current_user


def optional_auth():
    """Dependency for optional authentication.
    
    Usage:
        @router.get("/maybe-protected")
        async def maybe_protected(user: Optional[User] = Depends(optional_auth())):
            if user:
                return {"message": f"Hello {user.email}"}
            return {"message": "Hello guest"}
    """
    return get_optional_user
