"""Authentication dependencies for FastAPI endpoints.

This module provides dependencies for extracting and validating the current
user from JWT tokens or session cookies.

TODO: Implement actual JWT validation when auth system is ready.
For now, this returns a mock user ID for development purposes.
"""

import os
from fastapi import Header, HTTPException, status
from typing import Optional


# Mock user ID for development - should be replaced with actual auth
MOCK_USER_ID = os.getenv("MOCK_USER_ID", "user-dev-001")


async def get_current_user_id(
    authorization: Optional[str] = Header(None),
) -> str:
    """Get the current user ID from the authorization header.
    
    TODO: Implement actual JWT token validation:
    1. Extract token from Authorization header (Bearer token)
    2. Validate token signature
    3. Check token expiration
    4. Extract user_id from token claims
    5. Verify user exists in database
    
    Args:
        authorization: The Authorization header value (Bearer token)
        
    Returns:
        str: The current user's ID
        
    Raises:
        HTTPException: 401 if authentication is required but missing/invalid
    """
    # TODO: Replace with actual JWT validation
    # For development, return mock user ID
    # In production, this should validate the JWT and extract the real user ID
    
    if authorization:
        # If authorization header is provided, we could validate it here
        # For now, just log that we received it
        # Token format: "Bearer <token>"
        pass
    
    # Return mock user ID for development
    # This allows the API to work without a full auth system
    return MOCK_USER_ID


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
    # TODO: Implement actual optional auth check
    return MOCK_USER_ID if authorization else None


async def require_auth(
    authorization: Optional[str] = Header(None),
) -> str:
    """Require authentication - raises 401 if not provided.
    
    TODO: Implement actual JWT validation
    
    Args:
        authorization: The Authorization header value
        
    Returns:
        str: The validated user ID
        
    Raises:
        HTTPException: 401 if authentication is missing or invalid
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # TODO: Validate the JWT token here
    # For now, return mock user ID
    return MOCK_USER_ID
