"""Google OAuth authentication router."""

import os
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse, JSONResponse
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.models.user import User
from api.services.auth import generate_jwt

router = APIRouter(prefix="/api/v1/auth/google", tags=["auth"])

logger = logging.getLogger(__name__)

# Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


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
    Handle Google OAuth callback, create/find user, and issue JWT.
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
        
        # Find or create user
        user = await User.find_by_email(db, email)
        
        if user:
            # Update last login
            await user.update_last_login(db)
            logger.info(f"Existing user logged in: {email}")
        else:
            # Create new user
            user = await User.create(
                db,
                email=email,
                display_name=name,
                avatar_url=picture,
                auth_provider="google"
            )
            logger.info(f"New user created: {email}")
        
        # Generate JWT
        jwt_token = generate_jwt(user.id)
        
        # Redirect to frontend with token
        return RedirectResponse(
            f"{FRONTEND_URL}/auth/callback?token={jwt_token}"
        )
        
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
