"""Problem 04: Request Context

Topic: Request-scoped context, context propagation, metadata handling
Difficulty: Medium

Implement a RequestContext class and RequestContextManager service for
tracking request-scoped information like user, timestamps, and request metadata.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, ClassVar
import contextvars
import uuid


class RequestStatus(Enum):
    """Request processing status."""
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass(frozen=True)
class UserInfo:
    """Lightweight user information for request context."""
    user_id: int
    username: str
    roles: tuple[str, ...] = field(default_factory=tuple)
    
    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated (has valid ID)."""
        return self.user_id > 0
    
    def has_role(self, role: str) -> bool:
        """Check if user has specific role."""
        return role in self.roles


@dataclass
class RequestContext:
    """Immutable request-scoped context.
    
    Contains all information relevant to a single request:
    - Request identification and tracking
    - User information (if authenticated)
    - Timing information
    - Custom metadata
    
    Attributes:
        request_id: Unique identifier for the request
        correlation_id: ID linking related requests (optional)
        user_info: Information about the requesting user
        started_at: When request processing began
        status: Current processing status
        metadata: Custom key-value data for the request
    
    Example:
        >>> user = UserInfo(user_id=123, username="alice", roles=("admin",))
        >>> ctx = RequestContext.create(user_info=user)
        >>> print(ctx.request_id)  # UUID
        >>> print(ctx.is_authenticated)  # True
    """
    
    request_id: str
    correlation_id: str | None
    user_info: UserInfo
    started_at: datetime
    status: RequestStatus
    metadata: dict[str, Any] = field(default_factory=dict)
    
    # Class-level context variable for current request
    _current: ClassVar[contextvars.ContextVar[RequestContext | None]] = (
        contextvars.ContextVar("request_context", default=None)
    )
    
    @classmethod
    def create(
        cls,
        user_info: UserInfo | None = None,
        correlation_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> RequestContext:
        """Factory method to create a new request context.
        
        Generates a UUID for request_id using uuid.uuid4().
        Sets started_at to datetime.now().
        Status starts as PENDING.
        
        Args:
            user_info: User information (defaults to anonymous)
            correlation_id: Optional correlation ID for tracing
            metadata: Optional initial metadata
            
        Returns:
            New RequestContext instance
        """
        raise NotImplementedError("Implement create")
    
    @property
    def is_authenticated(self) -> bool:
        """Check if request has authenticated user."""
        raise NotImplementedError("Implement is_authenticated")
    
    @property
    def duration_ms(self) -> int:
        """Calculate request duration in milliseconds.
        
        Returns:
            Milliseconds since request started
        """
        raise NotImplementedError("Implement duration_ms")
    
    @property
    def is_complete(self) -> bool:
        """Check if request processing is finished."""
        raise NotImplementedError("Implement is_complete")
    
    def with_status(self, status: RequestStatus) -> RequestContext:
        """Create new context with updated status.
        
        Returns a new context since contexts are immutable.
        
        Args:
            status: New status value
            
        Returns:
            New RequestContext with updated status
        """
        raise NotImplementedError("Implement with_status")
    
    def with_metadata(self, key: str, value: Any) -> RequestContext:
        """Create new context with additional metadata.
        
        Args:
            key: Metadata key
            value: Metadata value
            
        Returns:
            New RequestContext with added metadata
        """
        raise NotImplementedError("Implement with_metadata")
    
    @classmethod
    def get_current(cls) -> RequestContext | None:
        """Get the current request context from context variable.
        
        Returns:
            Current RequestContext or None if not set
        """
        raise NotImplementedError("Implement get_current")
    
    @classmethod
    def set_current(cls, context: RequestContext | None) -> contextvars.Token:
        """Set the current request context.
        
        Args:
            context: Context to set as current
            
        Returns:
            Token for resetting context
        """
        raise NotImplementedError("Implement set_current")


class Logger(ABC):
    """Abstract logger for request tracking."""
    
    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message with context."""
        raise NotImplementedError("Implement info")
    
    @abstractmethod
    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message with context."""
        raise NotImplementedError("Implement error")


class RequestContextManager:
    """Service for managing request contexts.
    
    Provides a high-level API for:
    - Creating and entering request contexts
    - Tracking request lifecycle
    - Logging with request context
    - Managing context scope
    
    This service wraps the lower-level RequestContext operations
    and integrates with logging.
    
    Example:
        >>> manager = RequestContextManager(logger)
        >>> with manager.start_request(user_info=user) as ctx:
        ...     # Do work with ctx available
        ...     manager.log_info("Processing item")
        ...     # Context automatically tracked
    """
    
    def __init__(self, logger: Logger) -> None:
        """Initialize with logger.
        
        Args:
            logger: Logger for request tracking
        """
        raise NotImplementedError("Implement __init__")
    
    def start_request(
        self,
        user_info: UserInfo | None = None,
        correlation_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> RequestContext:
        """Start a new request context.
        
        Creates a new RequestContext, sets it as current,
        logs the request start, and returns it.
        
        Args:
            user_info: User information (defaults to anonymous)
            correlation_id: Optional correlation ID
            metadata: Optional initial metadata
            
        Returns:
            New RequestContext with status PROCESSING
        """
        raise NotImplementedError("Implement start_request")
    
    def complete_request(self, context: RequestContext) -> RequestContext:
        """Mark request as completed.
        
        Updates status to COMPLETED and logs completion.
        
        Args:
            context: Context to complete
            
        Returns:
            Updated context
        """
        raise NotImplementedError("Implement complete_request")
    
    def fail_request(
        self,
        context: RequestContext,
        error: Exception | str,
    ) -> RequestContext:
        """Mark request as failed.
        
        Updates status to FAILED and logs error.
        
        Args:
            context: Context to mark failed
            error: Exception or error message
            
        Returns:
            Updated context
        """
        raise NotImplementedError("Implement fail_request")
    
    def log_info(self, message: str, **kwargs: Any) -> None:
        """Log info message with current request context.
        
        Automatically includes request_id and user_id if available.
        
        Args:
            message: Log message
            **kwargs: Additional log fields
        """
        raise NotImplementedError("Implement log_info")
    
    def log_error(self, message: str, **kwargs: Any) -> None:
        """Log error message with current request context.
        
        Automatically includes request_id and user_id if available.
        
        Args:
            message: Error message
            **kwargs: Additional log fields
        """
        raise NotImplementedError("Implement log_error")
    
    def get_current_context(self) -> RequestContext | None:
        """Get the current request context.
        
        Returns:
            Current RequestContext or None
        """
        raise NotImplementedError("Implement get_current_context")
