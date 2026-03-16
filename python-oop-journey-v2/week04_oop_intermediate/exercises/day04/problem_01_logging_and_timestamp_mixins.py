"""Problem 01: Logging and Timestamp Mixins.

Implement mixins that provide logging and timestamp functionality.

Classes to implement:
- LoggerMixin: Provides logging capability with log() method
- TimestampMixin: Provides created_at timestamp tracking
- Base: Base class that uses both mixins
- Document: A document class inheriting from Base with title and content

Example:
    >>> doc = Document("Test", "Hello World", "alice")
    >>> doc.title
    'Test'
    >>> doc.get_age_seconds() >= 0
    True
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


class LoggerMixin:
    """Mixin that adds logging capability.
    
    Attributes:
        _logs: List of log entries.
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # TODO: Initialize the _logs list and call super().__init__
        raise NotImplementedError("Initialize _logs and call super().__init__")
    
    def log(self, message: str, level: str = "INFO") -> None:
        """Add a log entry.
        
        Args:
            message: The log message.
            level: The log level (default: INFO).
        """
        # TODO: Append a dict with timestamp, level, and message to _logs
        raise NotImplementedError("Append log entry to _logs")
    
    def get_logs(self) -> list[dict[str, Any]]:
        """Return a copy of all logs.
        
        Returns:
            List of log entry dictionaries.
        """
        # TODO: Return a copy of the _logs list
        raise NotImplementedError("Return copy of _logs")


class TimestampMixin:
    """Mixin that adds timestamp tracking.
    
    Attributes:
        _created_at: The datetime when the object was created.
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # TODO: Set _created_at to current datetime and call super().__init__
        raise NotImplementedError("Set _created_at and call super().__init__")
    
    @property
    def created_at(self) -> datetime:
        """Get the creation timestamp.
        
        Returns:
            The datetime when the object was created.
        """
        # TODO: Return _created_at
        raise NotImplementedError("Return _created_at")
    
    def get_age_seconds(self) -> float:
        """Get the age of the object in seconds.
        
        Returns:
            Number of seconds since creation.
        """
        # TODO: Calculate and return seconds since _created_at
        raise NotImplementedError("Calculate age in seconds")


class Base(LoggerMixin, TimestampMixin):
    """Base class combining LoggerMixin and TimestampMixin.
    
    Attributes:
        _logs: Inherited from LoggerMixin.
        _created_at: Inherited from TimestampMixin.
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # TODO: Call super().__init__ to trigger the MRO chain
        raise NotImplementedError("Call super().__init__ to initialize mixins")


class Document(Base):
    """A document with logging and timestamp capabilities.
    
    Attributes:
        title: The document title.
        content: The document content.
        author: The document author.
        _logs: List of logs (from LoggerMixin).
        _created_at: Creation timestamp (from TimestampMixin).
    
    Args:
        title: The document title.
        content: The document content.
        author: The document author.
    """
    
    def __init__(self, title: str, content: str, author: str) -> None:
        # TODO: Call super().__init__ first, then set title, content, author
        # TODO: Log the creation with message "Document created"
        raise NotImplementedError("Initialize document and log creation")
    
    def update_content(self, new_content: str, editor: str) -> None:
        """Update the document content and log the change.
        
        Args:
            new_content: The new content.
            editor: Who made the change.
        """
        # TODO: Update content and log the change with editor info
        raise NotImplementedError("Update content and log change")
    
    def __str__(self) -> str:
        """Return string representation.
        
        Returns:
            Formatted string with title and author.
        """
        # TODO: Return f"Document('{self.title}' by {self.author})"
        raise NotImplementedError("Return string representation")
