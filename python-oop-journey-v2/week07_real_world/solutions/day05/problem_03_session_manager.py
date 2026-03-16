"""Reference solution for Problem 03: Session Manager."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any
import secrets


@dataclass(frozen=True)
class Session:
    """Immutable session object."""
    session_id: str
    user_id: int
    created_at: datetime
    expires_at: datetime
    data: dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_expired(self) -> bool:
        """Check if session has expired."""
        return datetime.now() > self.expires_at
    
    @property
    def ttl_seconds(self) -> int:
        """Calculate remaining time to live in seconds."""
        remaining = (self.expires_at - datetime.now()).total_seconds()
        return max(0, int(remaining))


class SessionStore(ABC):
    """Abstract session storage backend."""
    
    @abstractmethod
    def save(self, session_id: str, session: Session, ttl: int) -> bool:
        """Save session with TTL in seconds."""
        raise NotImplementedError("Implement save")
    
    @abstractmethod
    def get(self, session_id: str) -> Session | None:
        """Retrieve session by ID."""
        raise NotImplementedError("Implement get")
    
    @abstractmethod
    def delete(self, session_id: str) -> bool:
        """Delete session by ID."""
        raise NotImplementedError("Implement delete")
    
    @abstractmethod
    def extend_ttl(self, session_id: str, additional_seconds: int) -> bool:
        """Extend session TTL."""
        raise NotImplementedError("Implement extend_ttl")


@dataclass
class SessionCreationResult:
    """Result of session creation."""
    success: bool
    session: Session | None = None
    error_message: str | None = None


class SessionManager:
    """Service for managing user sessions."""
    
    def __init__(
        self,
        session_store: SessionStore,
        default_ttl: int = 3600,
    ) -> None:
        """Initialize session manager."""
        self._store = session_store
        self._default_ttl = default_ttl
    
    def _generate_session_id(self) -> str:
        """Generate a cryptographically secure session ID."""
        return secrets.token_urlsafe(32)
    
    def create_session(
        self,
        user_id: int,
        data: dict[str, Any] | None = None,
        custom_ttl: int | None = None,
    ) -> SessionCreationResult:
        """Create a new session for a user."""
        ttl = custom_ttl if custom_ttl is not None else self._default_ttl
        
        session_id = self._generate_session_id()
        now = datetime.now()
        expires_at = now + timedelta(seconds=ttl)
        
        session = Session(
            session_id=session_id,
            user_id=user_id,
            created_at=now,
            expires_at=expires_at,
            data=data or {},
        )
        
        success = self._store.save(session_id, session, ttl)
        
        if not success:
            return SessionCreationResult(
                success=False,
                error_message="Failed to save session",
            )
        
        return SessionCreationResult(success=True, session=session)
    
    def validate_session(self, session_id: str) -> Session | None:
        """Validate and retrieve a session."""
        session = self._store.get(session_id)
        
        if session is None:
            return None
        
        if session.is_expired:
            self._store.delete(session_id)
            return None
        
        return session
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate (logout) a session."""
        return self._store.delete(session_id)
    
    def refresh_session(self, session_id: str) -> Session | None:
        """Extend session lifetime."""
        session = self._store.get(session_id)
        
        if session is None:
            return None
        
        if session.is_expired:
            self._store.delete(session_id)
            return None
        
        # Extend TTL
        success = self._store.extend_ttl(session_id, self._default_ttl)
        
        if not success:
            return None
        
        # Return updated session
        return self._store.get(session_id)
    
    def get_session_data(self, session_id: str, key: str) -> Any | None:
        """Get value from session data."""
        session = self._store.get(session_id)
        
        if session is None or session.is_expired:
            return None
        
        return session.data.get(key)
    
    def set_session_data(
        self,
        session_id: str,
        key: str,
        value: Any,
    ) -> bool:
        """Set value in session data."""
        session = self._store.get(session_id)
        
        if session is None or session.is_expired:
            return False
        
        # Create new session with updated data
        new_data = dict(session.data)
        new_data[key] = value
        
        new_session = Session(
            session_id=session.session_id,
            user_id=session.user_id,
            created_at=session.created_at,
            expires_at=session.expires_at,
            data=new_data,
        )
        
        # Calculate remaining TTL
        ttl = session.ttl_seconds
        
        return self._store.save(session_id, new_session, ttl)
