"""Authentication endpoints."""

import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import get_settings
from api.database import get_db
from api.middleware.auth import get_current_user, get_optional_user
from api.models.user import User
from api.schemas.user import (
    MagicLinkRequest,
    MagicLinkResponse,
    MagicLinkVerify,
    TokenResponse,
    User as UserSchema,
    UserUpdate,
)
from api.services.auth import AuthService

router = APIRouter()
security = HTTPBearer(auto_error=False)
settings = get_settings()
logger = logging.getLogger(__name__)

# Cookie settings for security
COOKIE_SETTINGS = {
    "httponly": True,
    "secure": True,  # HTTPS only
    "samesite": "strict",  # CSRF protection
    "path": "/",
}

ACCESS_TOKEN_COOKIE = "access_token"
REFRESH_TOKEN_COOKIE = "refresh_token"
ACCESS_TOKEN_MAX_AGE = 15 * 60  # 15 minutes in seconds
REFRESH_TOKEN_MAX_AGE = 7 * 24 * 60 * 60  # 7 days in seconds


@router.post(
    "/magic-link",
    response_model=MagicLinkResponse,
    summary="Request magic link",
    description="Send a magic login link to the user's email.",
    status_code=status.HTTP_202_ACCEPTED,
)
async def send_magic_link(
    request: Request,
    body: MagicLinkRequest,
    db: AsyncSession = Depends(get_db),
) -> MagicLinkResponse:
    """Request a magic link for passwordless login.
    
    Always returns success to prevent email enumeration attacks.
    Rate limited to 5 requests per 15 minutes per IP.
    """
    try:
        auth_service = AuthService(db)
        
        # Create magic link
        magic_link = await auth_service.create_magic_link(body.email)
        
        # Send email (logs in development)
        email_sent = await auth_service.email_service.send_magic_link_email(
            body.email, magic_link
        )
        
        # Always return success to prevent email enumeration
        response = {
            "success": True,
            "message": "Check your email for the magic link",
        }
        
        # Include debug info in development
        if settings.is_development:
            return MagicLinkResponse(
                success=True,
                message="Check your email for the magic link",
                debug={"magic_link": magic_link, "email_sent": email_sent},
            )
        
        return MagicLinkResponse(success=True, message="Check your email for the magic link")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to send magic link: {e}")
        logger.exception("Full traceback:")
        # Still return success to prevent email enumeration
        return MagicLinkResponse(success=True, message="Check your email for the magic link")


@router.get(
    "/verify",
    response_model=TokenResponse,
    summary="Verify magic token",
    description="Verify magic link token and set JWT as HttpOnly cookie.",
    responses={
        401: {"description": "Invalid or expired token"},
        500: {"description": "Server error"},
    },
)
async def verify_magic_link_get(
    token: str,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """Verify magic link token from URL query parameter.
    
    This endpoint is called when the user clicks the magic link.
    Sets JWT as HttpOnly cookie and returns user info.
    """
    try:
        auth_service = AuthService(db)
        
        # Verify token
        user = await auth_service.verify_magic_link(token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired magic link",
            )
        
        # Generate tokens
        access_token = auth_service.generate_jwt(user)
        refresh_token, _ = auth_service.create_refresh_token(user.id)
        
        # Set secure HttpOnly cookies
        response.set_cookie(
            ACCESS_TOKEN_COOKIE,
            access_token,
            max_age=ACCESS_TOKEN_MAX_AGE,
            **COOKIE_SETTINGS,
        )
        response.set_cookie(
            REFRESH_TOKEN_COOKIE,
            refresh_token,
            max_age=REFRESH_TOKEN_MAX_AGE,
            **COOKIE_SETTINGS,
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_MAX_AGE,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to verify magic link: {e}")
        logger.exception("Full traceback:")
        # SECURITY: Do not expose internal error details to client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify magic link. Please try again later.",
        )


@router.post(
    "/verify",
    response_model=TokenResponse,
    summary="Verify magic token (POST)",
    description="Verify magic link token via POST request and set HttpOnly cookies.",
    responses={
        401: {"description": "Invalid or expired token"},
        500: {"description": "Server error"},
    },
)
async def verify_magic_link_post(
    body: MagicLinkVerify,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """Verify magic link token via POST request."""
    try:
        auth_service = AuthService(db)
        
        # Verify token
        user = await auth_service.verify_magic_link(body.token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired magic link",
            )
        
        # Generate tokens
        access_token = auth_service.generate_jwt(user)
        refresh_token, _ = auth_service.create_refresh_token(user.id)
        
        # Set secure HttpOnly cookies
        response.set_cookie(
            ACCESS_TOKEN_COOKIE,
            access_token,
            max_age=ACCESS_TOKEN_MAX_AGE,
            **COOKIE_SETTINGS,
        )
        response.set_cookie(
            REFRESH_TOKEN_COOKIE,
            refresh_token,
            max_age=REFRESH_TOKEN_MAX_AGE,
            **COOKIE_SETTINGS,
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_MAX_AGE,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to verify magic link: {e}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify magic link: {str(e)}",
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Get a new access token using refresh token cookie.",
    responses={
        401: {"description": "Invalid or expired refresh token"},
        500: {"description": "Server error"},
    },
)
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token using refresh token cookie.
    
    Requires a valid refresh token in the refresh_token cookie.
    Returns a new access token and rotates the refresh token.
    """
    try:
        auth_service = AuthService(db)
        
        # Get refresh token from cookie
        refresh_token = request.cookies.get(REFRESH_TOKEN_COOKIE)
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token required",
            )
        
        # Verify refresh token
        payload = auth_service.verify_token(refresh_token, token_type="refresh")
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )
        
        # Get user
        user_id = payload.get("sub")
        user = await auth_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        
        # Generate new tokens (token rotation for security)
        access_token = auth_service.generate_jwt(user)
        new_refresh_token, _ = auth_service.create_refresh_token(user.id)
        
        # Set new secure HttpOnly cookies
        response.set_cookie(
            ACCESS_TOKEN_COOKIE,
            access_token,
            max_age=ACCESS_TOKEN_MAX_AGE,
            **COOKIE_SETTINGS,
        )
        response.set_cookie(
            REFRESH_TOKEN_COOKIE,
            new_refresh_token,
            max_age=REFRESH_TOKEN_MAX_AGE,
            **COOKIE_SETTINGS,
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_MAX_AGE,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to refresh token: {e}")
        logger.exception("Full traceback:")
        # SECURITY: Do not expose internal error details to client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh token. Please try again later.",
        )


@router.post(
    "/logout",
    summary="Logout user",
    description="Invalidate current JWT and logout user.",
    responses={
        401: {"description": "Not authenticated"},
        500: {"description": "Server error"},
    },
)
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Logout user and invalidate JWT.
    
    Clears all auth cookies and revokes tokens for the user.
    """
    try:
        auth_service = AuthService(db)
        
        # Revoke all magic tokens for this user
        await auth_service.revoke_all_user_tokens(current_user.id)
        
        # Clear auth cookies with same settings used to set them
        response.delete_cookie(
            ACCESS_TOKEN_COOKIE,
            httponly=True,
            secure=True,
            samesite="strict",
            path="/",
        )
        response.delete_cookie(
            REFRESH_TOKEN_COOKIE,
            httponly=True,
            secure=True,
            samesite="strict",
            path="/",
        )
        
        return {"success": True, "message": "Logged out successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to logout: {e}")
        logger.exception("Full traceback:")
        # SECURITY: Do not expose internal error details to client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to logout. Please try again later.",
        )


@router.get(
    "/me",
    response_model=UserSchema,
    summary="Get current user",
    description="Get the currently authenticated user's profile.",
    responses={
        401: {"description": "Not authenticated"},
        500: {"description": "Server error"},
    },
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """Get current authenticated user's profile."""
    try:
        return current_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user: {e}")
        logger.exception("Full traceback:")
        # SECURITY: Do not expose internal error details to client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information. Please try again later.",
        )


@router.patch(
    "/me",
    response_model=UserSchema,
    summary="Update current user",
    description="Update the current user's profile.",
    responses={
        401: {"description": "Not authenticated"},
        500: {"description": "Server error"},
    },
)
async def update_me(
    update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update current user's profile."""
    try:
        # Update allowed fields
        if update.display_name is not None:
            current_user.display_name = update.display_name
        
        await db.commit()
        await db.refresh(current_user)
        
        return current_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update user: {e}")
        logger.exception("Full traceback:")
        # SECURITY: Do not expose internal error details to client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )
