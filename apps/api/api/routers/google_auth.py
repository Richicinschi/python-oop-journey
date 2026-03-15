"""Google OAuth authentication router."""

import os
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Query, Response
from fastapi.responses import RedirectResponse, JSONResponse
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.services.auth import AuthService

router = APIRouter(prefix="/api/v1/auth/google", tags=["auth"])

logger = logging.getLogger(__name__)

# Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Cookie settings for security (must match auth.py)
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


@router.get("/login")
async def google_login():
    """
    Redirect user to Google OAuth consent screen.
    """
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth not configured. Set GOOGLE_CLIENT_ID environment variable."
        )
    
    # Build Google OAuth URL manually
    redirect_uri = f"{FRONTEND_URL}/auth/callback/google"
    scope = "openid email profile"
    
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        "&response_type=code"
        f"&scope={scope}"
        "&access_type=offline"
        "&prompt=consent"
    )
    
    logger.info(f"Redirecting to Google OAuth: {auth_url[:100]}...")
    return RedirectResponse(auth_url)


@router.get("/callback")
async def google_callback(
    code: str = Query(...),
    error: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Handle Google OAuth callback, create/find user, and set secure cookies.
    """
    if error:
        logger.error(f"Google OAuth error: {error}")
        return RedirectResponse(f"{FRONTEND_URL}/auth/login?error={error}")
    
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth not fully configured"
        )
    
    try:
        # Exchange code for tokens
        import httpx
        
        token_url = "https://oauth2.googleapis.com/token"
        redirect_uri = f"{FRONTEND_URL}/auth/callback/google"
        
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                token_url,
                data={
                    "code": code,
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
        
        if token_response.status_code != 200:
            logger.error(f"Token exchange failed: {token_response.text}")
            return RedirectResponse(
                f"{FRONTEND_URL}/auth/login?error=token_exchange_failed"
            )
        
        tokens = token_response.json()
        id_token_str = tokens.get("id_token")
        
        if not id_token_str:
            return RedirectResponse(
                f"{FRONTEND_URL}/auth/login?error=no_id_token"
            )
        
        # Verify ID token
        idinfo = id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10
        )
        
        # Extract user info
        email = idinfo.get("email")
        name = idinfo.get("name", email.split("@")[0] if email else "User")
        picture = idinfo.get("picture")
        
        if not email:
            return RedirectResponse(
                f"{FRONTEND_URL}/auth/login?error=no_email"
            )
        
        logger.info(f"Google auth successful for: {email}")
        
        # Find or create user using AuthService
        auth_service = AuthService(db)
        user = await auth_service.get_user_by_email(email)
        
        if user:
            # Update last login
            user.last_seen = datetime.utcnow()
            user.last_login_at = datetime.utcnow()
            await db.commit()
            logger.info(f"Existing user logged in: {email}")
        else:
            # Create new user
            user = await auth_service.get_or_create_user(
                email=email,
                display_name=name,
                avatar_url=picture,
                auth_provider="google",
                auth_provider_id=idinfo.get("sub")
            )
            logger.info(f"New user created: {email}")
        
        # Generate tokens
        access_token = auth_service.generate_jwt(user)
        refresh_token, _ = auth_service.create_refresh_token(user.id)
        
        # Create response with redirect
        response = RedirectResponse(f"{FRONTEND_URL}/auth/callback?success=true")
        
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
        
        return response
        
    except Exception as e:
        logger.exception("Google OAuth callback error")
        return RedirectResponse(
            f"{FRONTEND_URL}/auth/login?error=auth_failed"
        )


@router.get("/config")
async def google_config():
    """
    Return Google OAuth configuration for frontend.
    """
    return JSONResponse({
        "client_id": GOOGLE_CLIENT_ID,
        "enabled": bool(GOOGLE_CLIENT_ID),
    })
