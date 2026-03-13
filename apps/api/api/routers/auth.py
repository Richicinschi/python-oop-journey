"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import get_settings
from api.database import get_db
from api.middleware.auth import get_current_user, get_optional_user
from api.models.user import User
from api.schemas.user import (
    MagicLinkRequest,
    MagicLinkVerify,
    TokenResponse,
    User as UserSchema,
    UserUpdate,
)
from api.services.auth import AuthService

router = APIRouter()
security = HTTPBearer(auto_error=False)
settings = get_settings()


@router.post(
    "/magic-link",
    summary="Request magic link",
    description="Send a magic login link to the user's email.",
    status_code=status.HTTP_202_ACCEPTED,
)
async def send_magic_link(
    request: Request,
    body: MagicLinkRequest,
    db: AsyncSession = Depends(get_db),
):
    """Request a magic link for passwordless login.
    
    Always returns success to prevent email enumeration attacks.
    Rate limited to 5 requests per 15 minutes per IP.
    """
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
        response["debug"] = {
            "magic_link": magic_link,
            "email_sent": email_sent,
        }
    
    return response


@router.get(
    "/verify",
    response_model=TokenResponse,
    summary="Verify magic token",
    description="Verify magic link token and return JWT access token.",
    responses={
        401: {"description": "Invalid or expired token"},
    },
)
async def verify_magic_link_get(
    token: str,
    db: AsyncSession = Depends(get_db),
):
    """Verify magic link token from URL query parameter.
    
    This endpoint is called when the user clicks the magic link.
    Returns JWT in JSON body (not redirect).
    """
    auth_service = AuthService(db)
    
    # Verify token
    user = await auth_service.verify_magic_link(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired magic link",
        )
    
    # Generate JWT
    access_token = auth_service.generate_jwt(user)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.jwt_access_token_expire_days * 24 * 60 * 60,
    )


@router.post(
    "/verify",
    response_model=TokenResponse,
    summary="Verify magic token (POST)",
    description="Verify magic link token via POST request.",
)
async def verify_magic_link_post(
    body: MagicLinkVerify,
    db: AsyncSession = Depends(get_db),
):
    """Verify magic link token via POST request."""
    auth_service = AuthService(db)
    
    # Verify token
    user = await auth_service.verify_magic_link(body.token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired magic link",
        )
    
    # Generate JWT
    access_token = auth_service.generate_jwt(user)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.jwt_access_token_expire_days * 24 * 60 * 60,
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Get a new access token using current valid token.",
)
async def refresh_token(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Refresh access token before expiry.
    
    Requires a valid JWT in the Authorization header.
    Returns a new JWT with fresh expiration.
    """
    auth_service = AuthService(db)
    
    # Generate new JWT
    access_token = auth_service.generate_jwt(current_user)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.jwt_access_token_expire_days * 24 * 60 * 60,
    )


@router.post(
    "/logout",
    summary="Logout user",
    description="Invalidate current JWT and logout user.",
)
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Logout user and invalidate JWT.
    
    In a full implementation, this would add the JWT to a Redis denylist.
    For now, we revoke all magic tokens for the user.
    """
    auth_service = AuthService(db)
    
    # Revoke all magic tokens for this user
    await auth_service.revoke_all_user_tokens(current_user.id)
    
    # Clear auth cookie if used
    response.delete_cookie("access_token")
    
    return {"success": True, "message": "Logged out successfully"}


@router.get(
    "/me",
    response_model=UserSchema,
    summary="Get current user",
    description="Get the currently authenticated user's profile.",
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """Get current authenticated user's profile."""
    return current_user


@router.patch(
    "/me",
    response_model=UserSchema,
    summary="Update current user",
    description="Update the current user's profile.",
)
async def update_me(
    update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update current user's profile."""
    # Update allowed fields
    if update.display_name is not None:
        current_user.display_name = update.display_name
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user


# Legacy endpoints for backward compatibility

@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token (legacy)",
    description="Get a new access token using a refresh token.",
    include_in_schema=False,
)
async def refresh_token_legacy(
    request: MagicLinkVerify,  # Reuse schema as it just needs a token
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token using refresh token."""
    auth_service = AuthService(db)

    # Verify refresh token
    payload = auth_service.verify_token(request.token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user_id = payload.get("sub")
    user = await auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Create new tokens
    access_token, _ = auth_service.create_access_token(user.id)
    refresh_token, _ = auth_service.create_refresh_token(user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=auth_service.get_settings().jwt_access_token_expire_minutes * 60,
    )
