"""Authentication service."""

import hashlib
import logging
import secrets
from datetime import datetime, timedelta
from uuid import uuid4

from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import get_settings
from api.models.auth_token import AuthToken
from api.models.user import User
from api.services.email import get_email_service

logger = logging.getLogger(__name__)
settings = get_settings()


class AuthService:
    """Service for authentication operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.email_service = get_email_service()

    async def get_or_create_user(self, email: str) -> User:
        """Get existing user or create new one."""
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            user.last_seen = datetime.utcnow()
            await self.session.commit()
            return user

        # Create new user
        user = User(email=email)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"Created new user: {email}")
        return user

    async def get_user_by_id(self, user_id: str) -> User | None:
        """Get user by ID."""
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email."""
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    def _hash_token(self, token: str) -> str:
        """Hash a token for secure storage."""
        return hashlib.sha256(token.encode()).hexdigest()

    def _generate_secure_token(self) -> str:
        """Generate a cryptographically secure random token."""
        return secrets.token_urlsafe(32)

    async def create_magic_link(self, email: str) -> str:
        """Create a magic link for the user.
        
        Args:
            email: User's email address
            
        Returns:
            Full magic link URL
        """
        # Get or create user
        user = await self.get_or_create_user(email)
        
        # Generate secure token
        token = self._generate_secure_token()
        token_hash = self._hash_token(token)
        
        # Calculate expiration
        expires_at = datetime.utcnow() + timedelta(
            minutes=settings.magic_link_expire_minutes
        )
        
        # Store token hash in database
        auth_token = AuthToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.session.add(auth_token)
        await self.session.commit()
        
        # Construct full magic link URL
        base_url = settings.magic_link_base_url or settings.allowed_origins[0]
        magic_link = f"{base_url}/auth/callback?token={token}"
        
        logger.info(f"Created magic link for user: {email}")
        return magic_link

    async def verify_magic_link(self, token: str) -> User | None:
        """Verify a magic link token and return the user.
        
        Args:
            token: The magic link token from URL
            
        Returns:
            User if token is valid, None otherwise
        """
        token_hash = self._hash_token(token)
        
        # Find token in database
        stmt = (
            select(AuthToken)
            .where(AuthToken.token_hash == token_hash)
            .where(AuthToken.used_at.is_(None))
            .where(AuthToken.expires_at > datetime.utcnow())
        )
        result = await self.session.execute(stmt)
        auth_token = result.scalar_one_or_none()
        
        if not auth_token:
            logger.warning("Invalid, expired, or already used magic token")
            return None
        
        # Mark token as used
        auth_token.used_at = datetime.utcnow()
        
        # Update user's last login
        user = await self.get_user_by_id(auth_token.user_id)
        if user:
            user.last_login_at = datetime.utcnow()
            await self.session.commit()
            logger.info(f"Magic link verified for user: {user.email}")
        
        return user

    def generate_jwt(self, user: User) -> str:
        """Generate JWT access token for user.
        
        Args:
            user: The authenticated user
            
        Returns:
            JWT access token string
        """
        expires = datetime.utcnow() + timedelta(
            days=settings.jwt_access_token_expire_days
        )
        payload = {
            "sub": user.id,
            "email": user.email,
            "type": "access",
            "exp": expires,
            "iat": datetime.utcnow(),
            "jti": str(uuid4()),
        }
        return jwt.encode(
            payload, settings.secret_key, algorithm=settings.jwt_algorithm
        )

    def verify_jwt(self, token: str) -> dict | None:
        """Verify and decode a JWT access token.
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.jwt_algorithm]
            )
            if payload.get("type") != "access":
                return None
            return payload
        except JWTError as e:
            logger.debug(f"JWT verification failed: {e}")
            return None

    def verify_token(self, token: str, token_type: str = "access") -> dict | None:
        """Verify and decode a JWT token with specific type.
        
        Args:
            token: JWT token string
            token_type: Expected token type ("access" or "refresh")
            
        Returns:
            Decoded payload if valid and type matches, None otherwise
        """
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.jwt_algorithm]
            )
            if payload.get("type") != token_type:
                logger.debug(f"Token type mismatch: expected {token_type}, got {payload.get('type')}")
                return None
            return payload
        except JWTError as e:
            logger.debug(f"Token verification failed: {e}")
            return None

    async def revoke_all_user_tokens(self, user_id: str) -> int:
        """Revoke all active magic link tokens for a user.
        
        Args:
            user_id: The user's ID
            
        Returns:
            Number of tokens revoked
        """
        stmt = (
            select(AuthToken)
            .where(AuthToken.user_id == user_id)
            .where(AuthToken.used_at.is_(None))
            .where(AuthToken.expires_at > datetime.utcnow())
        )
        result = await self.session.execute(stmt)
        tokens = result.scalars().all()
        
        count = 0
        for token in tokens:
            token.used_at = datetime.utcnow()
            count += 1
        
        await self.session.commit()
        logger.info(f"Revoked {count} tokens for user {user_id}")
        return count

    # Legacy methods for backward compatibility
    def create_access_token(self, user_id: str) -> tuple[str, datetime]:
        """Create JWT access token."""
        expires = datetime.utcnow() + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )
        payload = {
            "sub": user_id,
            "type": "access",
            "exp": expires,
            "iat": datetime.utcnow(),
            "jti": str(uuid4()),
        }
        token = jwt.encode(
            payload, settings.secret_key, algorithm=settings.jwt_algorithm
        )
        return token, expires

    def create_refresh_token(self, user_id: str) -> tuple[str, datetime]:
        """Create JWT refresh token."""
        expires = datetime.utcnow() + timedelta(
            days=settings.jwt_refresh_token_expire_days
        )
        payload = {
            "sub": user_id,
            "type": "refresh",
            "exp": expires,
            "iat": datetime.utcnow(),
            "jti": str(uuid4()),
        }
        token = jwt.encode(
            payload, settings.secret_key, algorithm=settings.jwt_algorithm
        )
        return token, expires


# Dependency injection function
async def get_auth_service(session: AsyncSession) -> AuthService:
    """Get AuthService instance with session."""
    return AuthService(session)
