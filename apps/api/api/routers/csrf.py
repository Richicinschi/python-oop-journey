"""CSRF token endpoint.

Provides endpoints for CSRF token generation and management.
"""

import logging

from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

from api.middleware.csrf import (
    CSRF_COOKIE_NAME,
    CSRF_HEADER_NAME,
    generate_csrf_token,
    get_csrf_token,
)

logger = logging.getLogger(__name__)
router = APIRouter()


class CSRFTokenResponse(BaseModel):
    """CSRF token response."""
    csrf_token: str
    token_name: str
    header_name: str
    refreshed: bool


@router.get(
    "/csrf-token",
    response_model=CSRFTokenResponse,
    summary="Get CSRF token",
    description="Generate and return a CSRF token for the current session.",
    response_description="CSRF token for use in state-changing requests",
)
async def get_csrf_token_endpoint(
    request: Request,
    response: Response,
) -> dict:
    """Generate a new CSRF token for the current session.
    
    The token is returned in the response body and also set as a cookie.
    Include the token in the X-CSRF-Token header for all state-changing requests.
    
    Example usage:
        1. Call GET /api/v1/csrf-token to get a token
        2. Store the token value
        3. Include in headers for POST/PUT/DELETE requests:
           X-CSRF-Token: <token_value>
    
    Returns:
        Dictionary containing the CSRF token and metadata
    """
    # Check if there's already a valid token
    existing_token = get_csrf_token(request)
    
    if existing_token:
        # Return existing valid token
        return {
            "csrf_token": existing_token,
            "token_name": CSRF_COOKIE_NAME,
            "header_name": CSRF_HEADER_NAME,
            "refreshed": False,
        }
    
    # Generate new token
    token = generate_csrf_token(request, response)
    
    logger.debug(f"Generated new CSRF token for session")
    
    return {
        "csrf_token": token,
        "token_name": CSRF_COOKIE_NAME,
        "header_name": CSRF_HEADER_NAME,
        "refreshed": True,
    }


@router.post(
    "/csrf-refresh",
    response_model=CSRFTokenResponse,
    summary="Refresh CSRF token",
    description="Force generation of a new CSRF token.",
)
async def refresh_csrf_token(
    request: Request,
    response: Response,
) -> dict:
    """Force generation of a new CSRF token.
    
    Use this when you suspect token compromise or after session changes.
    
    Returns:
        Dictionary containing the new CSRF token
    """
    from api.middleware.csrf import csrf_store
    
    session_id = "user:{}".format(
        getattr(request.state, "user", None) and request.state.user.id
        or request.client.host if request.client else "unknown"
    )
    
    # Revoke old token if exists
    csrf_store.revoke_token(session_id)
    
    # Generate new token
    token = generate_csrf_token(request, response)
    
    logger.info(f"Refreshed CSRF token for session")
    
    return {
        "csrf_token": token,
        "token_name": CSRF_COOKIE_NAME,
        "header_name": CSRF_HEADER_NAME,
        "refreshed": True,
    }
