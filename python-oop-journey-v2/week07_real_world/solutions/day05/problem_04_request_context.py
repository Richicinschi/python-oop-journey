"""Reference solution for Problem 04: Request Context."""

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
    """Immutable request-scoped context."""
    
    request_id: str
    correlation_id: str | None
    user_info: UserInfo
    started_at: datetime
    status: RequestStatus
    metadata: dict[str, Any] = field(default_factory=dict)
    
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
        """Factory method to create a new request context."""
        # Default to anonymous user if not provided
        if user_info is None:
            user_info = UserInfo(user_id=0, username="anonymous")
        
        return cls(
            request_id=str(uuid.uuid4()),
            correlation_id=correlation_id,
            user_info=user_info,
            started_at=datetime.now(),
            status=RequestStatus.PENDING,
            metadata=dict(metadata) if metadata else {},
        )
    
    @property
    def is_authenticated(self) -> bool:
        """Check if request has authenticated user."""
        return self.user_info.is_authenticated
    
    @property
    def duration_ms(self) -> int:
        """Calculate request duration in milliseconds."""
        elapsed = datetime.now() - self.started_at
        return int(elapsed.total_seconds() * 1000)
    
    @property
    def is_complete(self) -> bool:
        """Check if request processing is finished."""
        return self.status in (RequestStatus.COMPLETED, RequestStatus.FAILED)
    
    def with_status(self, status: RequestStatus) -> RequestContext:
        """Create new context with updated status."""
        return RequestContext(
            request_id=self.request_id,
            correlation_id=self.correlation_id,
            user_info=self.user_info,
            started_at=self.started_at,
            status=status,
            metadata=dict(self.metadata),
        )
    
    def with_metadata(self, key: str, value: Any) -> RequestContext:
        """Create new context with additional metadata."""
        new_metadata = dict(self.metadata)
        new_metadata[key] = value
        
        return RequestContext(
            request_id=self.request_id,
            correlation_id=self.correlation_id,
            user_info=self.user_info,
            started_at=self.started_at,
            status=self.status,
            metadata=new_metadata,
        )
    
    @classmethod
    def get_current(cls) -> RequestContext | None:
        """Get the current request context from context variable."""
        return cls._current.get()
    
    @classmethod
    def set_current(cls, context: RequestContext | None) -> contextvars.Token:
        """Set the current request context."""
        return cls._current.set(context)


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
    """Service for managing request contexts."""
    
    def __init__(self, logger: Logger) -> None:
        """Initialize with logger."""
        self._logger = logger
    
    def start_request(
        self,
        user_info: UserInfo | None = None,
        correlation_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> RequestContext:
        """Start a new request context."""
        context = RequestContext.create(
            user_info=user_info,
            correlation_id=correlation_id,
            metadata=metadata,
        )
        
        # Set status to PROCESSING
        context = context.with_status(RequestStatus.PROCESSING)
        
        # Set as current context
        RequestContext.set_current(context)
        
        # Log start
        self._logger.info(
            "Request started",
            request_id=context.request_id,
            user_id=context.user_info.user_id,
            username=context.user_info.username,
        )
        
        return context
    
    def complete_request(self, context: RequestContext) -> RequestContext:
        """Mark request as completed."""
        completed_context = context.with_status(RequestStatus.COMPLETED)
        RequestContext.set_current(completed_context)
        
        self._logger.info(
            "Request completed",
            request_id=completed_context.request_id,
            duration_ms=completed_context.duration_ms,
        )
        
        return completed_context
    
    def fail_request(
        self,
        context: RequestContext,
        error: Exception | str,
    ) -> RequestContext:
        """Mark request as failed."""
        failed_context = context.with_status(RequestStatus.FAILED)
        RequestContext.set_current(failed_context)
        
        error_message = str(error)
        
        self._logger.error(
            "Request failed",
            request_id=failed_context.request_id,
            error=error_message,
            duration_ms=failed_context.duration_ms,
        )
        
        return failed_context
    
    def log_info(self, message: str, **kwargs: Any) -> None:
        """Log info message with current request context."""
        context = RequestContext.get_current()
        
        log_data = dict(kwargs)
        if context:
            log_data["request_id"] = context.request_id
            log_data["user_id"] = context.user_info.user_id
        
        self._logger.info(message, **log_data)
    
    def log_error(self, message: str, **kwargs: Any) -> None:
        """Log error message with current request context."""
        context = RequestContext.get_current()
        
        log_data = dict(kwargs)
        if context:
            log_data["request_id"] = context.request_id
            log_data["user_id"] = context.user_info.user_id
        
        self._logger.error(message, **log_data)
    
    def get_current_context(self) -> RequestContext | None:
        """Get the current request context."""
        return RequestContext.get_current()
