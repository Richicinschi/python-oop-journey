"""Problem 03: Session Manager

Topic: Session management, TTL handling, security
Difficulty: Medium

Implement a SessionManager service that handles user session lifecycle
including creation, validation, refresh, and cleanup.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any
import secrets
import hashlib


@dataclass(frozen=True)
class Session:
    """Immutable session object.
    
    Attributes:
        session_id: Unique session identifier (public)
        user_id: Associated user ID
        created_at: Session creation timestamp
        expires_at: Session expiration timestamp
        data: Additional session-scoped data
    """
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
        """Save session with TTL in seconds.
        
        Args:
            session_id: Session identifier
            session: Session object to store
            ttl: Time-to-live in seconds
            
        Returns:
            True if save was successful
        """
        raise NotImplementedError("Implement save")
    
    @abstractmethod
    def get(self, session_id: str) -> Session | None:
        """Retrieve session by ID.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session if found and not expired, None otherwise
        """
        raise NotImplementedError("Implement get")
    
    @abstractmethod
    def delete(self, session_id: str) -> bool:
        """Delete session by ID.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if session existed and was deleted
        """
        raise NotImplementedError("Implement delete")
    
    @abstractmethod
    def extend_ttl(self, session_id: str, additional_seconds: int) -> bool:
        """Extend session TTL.
        
        Args:
            session_id: Session identifier
            additional_seconds: Time to add to current expiry
            
        Returns:
            True if session exists and was extended
        """
        raise NotImplementedError("Implement extend_ttl")


@dataclass
class SessionCreationResult:
    """Result of session creation."""
    success: bool
    session: Session | None = None
    error_message: str | None = None


class SessionManager:
    """Service for managing user sessions.
    
    Responsibilities:
    - Create new sessions with secure tokens
    - Validate existing sessions
    - Refresh/extend session lifetime
    - Invalidate (logout) sessions
    - Manage session-scoped data
    
    Security features:
    - Cryptographically secure session ID generation
    - Configurable session TTL
    - Automatic expiration handling
    
    Dependencies:
    - session_store: Storage backend for session persistence
    
    Example:
        >>> manager = SessionManager(store, default_ttl=3600)
        >>> result = manager.create_session(user_id=123)
        >>> session = result.session
        >>> validated = manager.validate_session(session.session_id)
    """
    
    def __init__(
        self,
        session_store: SessionStore,
        default_ttl: int = 3600,
    ) -> None:
        """Initialize session manager.
        
        Args:
            session_store: Storage backend for sessions
            default_ttl: Default session lifetime in seconds
        """
        raise NotImplementedError("Implement __init__")
    
    def create_session(
        self,
        user_id: int,
        data: dict[str, Any] | None = None,
        custom_ttl: int | None = None,
    ) -> SessionCreationResult:
        """Create a new session for a user.
        
        Generates a cryptographically secure session ID using
        secrets.token_urlsafe(). Session IDs should be 32 bytes
        of randomness (43 characters in URL-safe base64).
        
        Args:
            user_id: User to create session for
            data: Optional session-scoped data
            custom_ttl: Override default TTL if provided
            
        Returns:
            SessionCreationResult with session or error
        """
        raise NotImplementedError("Implement create_session")
    
    def validate_session(self, session_id: str) -> Session | None:
        """Validate and retrieve a session.
        
        Returns the session only if:
        - Session ID exists in store
        - Session has not expired
        
        Args:
            session_id: Session identifier to validate
            
        Returns:
            Session if valid, None otherwise
        """
        raise NotImplementedError("Implement validate_session")
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate (logout) a session.
        
        Args:
            session_id: Session identifier to invalidate
            
        Returns:
            True if session existed and was removed
        """
        raise NotImplementedError("Implement invalidate_session")
    
    def refresh_session(self, session_id: str) -> Session | None:
        """Extend session lifetime.
        
        Extends the session by the default TTL from current time.
        Only works if session exists and is not already expired.
        
        Args:
            session_id: Session identifier to refresh
            
        Returns:
            Updated session if successful, None otherwise
        """
        raise NotImplementedError("Implement refresh_session")
    
    def get_session_data(self, session_id: str, key: str) -> Any | None:
        """Get value from session data.
        
        Args:
            session_id: Session identifier
            key: Data key to retrieve
            
        Returns:
            Value if session exists and key exists, None otherwise
        """
        raise NotImplementedError("Implement get_session_data")
    
    def set_session_data(
        self,
        session_id: str,
        key: str,
        value: Any,
    ) -> bool:
        """Set value in session data.
        
        Note: This requires updating the stored session.
        The session's expiry is not changed by this operation.
        
        Args:
            session_id: Session identifier
            key: Data key to set
            value: Value to store
            
        Returns:
            True if session exists and was updated
        """
        raise NotImplementedError("Implement set_session_data")
