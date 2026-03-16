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
        """Initialize the logger mixin."""
        super().__init__(*args, **kwargs)
        self._logs: list[dict[str, Any]] = []
    
    def log(self, message: str, level: str = "INFO") -> None:
        """Add a log entry.
        
        Args:
            message: The log message.
            level: The log level (default: INFO).
        """
        self._logs.append({
            "timestamp": datetime.now(),
            "level": level,
            "message": message
        })
    
    def get_logs(self) -> list[dict[str, Any]]:
        """Return a copy of all logs.
        
        Returns:
            List of log entry dictionaries.
        """
        return self._logs.copy()


class TimestampMixin:
    """Mixin that adds timestamp tracking.
    
    Attributes:
        _created_at: The datetime when the object was created.
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the timestamp mixin."""
        super().__init__(*args, **kwargs)
        self._created_at = datetime.now()
    
    @property
    def created_at(self) -> datetime:
        """Get the creation timestamp.
        
        Returns:
            The datetime when the object was created.
        """
        return self._created_at
    
    def get_age_seconds(self) -> float:
        """Get the age of the object in seconds.
        
        Returns:
            Number of seconds since creation.
        """
        return (datetime.now() - self._created_at).total_seconds()


class Base(LoggerMixin, TimestampMixin):
    """Base class combining LoggerMixin and TimestampMixin.
    
    Attributes:
        _logs: Inherited from LoggerMixin.
        _created_at: Inherited from TimestampMixin.
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the base class."""
        super().__init__(*args, **kwargs)


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
        """Initialize a document.
        
        Args:
            title: The document title.
            content: The document content.
            author: The document author.
        """
        super().__init__()
        self.title = title
        self.content = content
        self.author = author
        self.log(f"Document created by {author}")
    
    def update_content(self, new_content: str, editor: str) -> None:
        """Update the document content and log the change.
        
        Args:
            new_content: The new content.
            editor: Who made the change.
        """
        old_length = len(self.content)
        self.content = new_content
        self.log(f"Content updated by {editor} (length: {old_length} -> {len(new_content)})")
    
    def __str__(self) -> str:
        """Return string representation.
        
        Returns:
            Formatted string with title and author.
        """
        return f"Document('{self.title}' by {self.author})"
