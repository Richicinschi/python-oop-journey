"""Authentication dependencies for FastAPI endpoints.

This module provides dependencies for extracting and validating the current
user from JWT tokens or session cookies.
"""

import logging
from typing import Optional

from fastapi import Header, HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import get_settings
from api.database import get_db
from api.models.user import User
from api.services.auth import AuthService

logger = logging.getLogger(__name__)
settings = get_settings()

# Use HTTPBearer for JWT token extraction
security = HTTPBearer(auto_error=False)


async def get_current_user_id(
    authorization: Optional[str] = Header(None),
) -> str:
    """Get the current user ID from the authorization header.
    
    Validates the JWT token from the Authorization header and extracts
    the user ID from the token claims.
    
    Args:
        authorization: The Authorization header value (Bearer token)
        
    Returns:
        str: The current user's ID
        
    Raises:
        HTTPException: 401 if authentication is required but missing/invalid
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.replace("Bearer ", "")
    
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
        
        # Validate token type
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user_id
        
    except JWTError as e:
        logger.debug(f"JWT validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_id_optional(
    authorization: Optional[str] = Header(None),
) -> Optional[str]:
    """Get the current user ID if available, otherwise return None.
    
    This is useful for endpoints that work with or without authentication.
    
    Args:
        authorization: The Authorization header value
        
    Returns:
        Optional[str]: The user ID if authenticated, None otherwise
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.replace("Bearer ", "")
    
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
        
        # Validate token type
        if payload.get("type") != "access":
            return None
        
        return payload.get("sub")
        
    except JWTError:
        return None


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get current authenticated user from JWT token.
    
    This dependency extracts the JWT from the Authorization header or cookie,
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


async def require_auth(
    authorization: Optional[str] = Header(None),
) -> str:
    """Require authentication - raises 401 if not provided.
    
    Args:
        authorization: The Authorization header value
        
    Returns:
        str: The validated user ID
        
    Raises:
        HTTPException: 401 if authentication is missing or invalid
    """
    return await get_current_user_id(authorization)


def verify_token_for_websocket(token: str) -> Optional[dict]:
    """Verify a JWT token for WebSocket authentication.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
        
        # Validate token type
        if payload.get("type") != "access":
            logger.warning("WebSocket auth failed: invalid token type")
            return None
        
        # Check required fields
        if not payload.get("sub"):
            logger.warning("WebSocket auth failed: missing user ID in token")
            return None
        
        return payload
        
    except JWTError as e:
        logger.debug(f"WebSocket token verification failed: {e}")
        return None
