"""Problem 03: Attribute Diff Tool.

Topic: Attribute Tracking, __setattr__, __getattr__
Difficulty: Medium

Implement a tool that tracks and compares object attribute changes over time.

This is useful for:
- Debugging state changes
- Audit logging
- Undo/redo functionality
- Detecting unexpected mutations

Example:
    >>> obj = TrackedObject()
    >>> obj.name = "Alice"
    >>> obj.age = 30
    >>> diff = obj.get_changes()
    >>> diff.added
    {'name': 'Alice', 'age': 30}
    
    >>> obj.age = 31
    >>> diff = obj.get_changes()
    >>> diff.modified
    {'age': (30, 31)}
    
    >>> obj.checkpoint()
    >>> del obj.name
    >>> diff = obj.get_changes()
    >>> diff.removed
    {'name': 'Alice'}
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class DiffResult:
    """Result of comparing two states.
    
    Attributes:
        added: Attributes that exist now but didn't before.
        removed: Attributes that existed before but don't now.
        modified: Attributes with changed values (name -> (old, new)).
        unchanged: Attributes that stayed the same.
    """
    added: dict[str, Any]
    removed: dict[str, Any]
    modified: dict[str, tuple[Any, Any]]
    unchanged: dict[str, Any]
    
    def has_changes(self) -> bool:
        """Check if any changes were detected."""
        raise NotImplementedError("Implement has_changes")


class TrackedObject:
    """An object that tracks attribute changes.
    
    This class intercepts attribute modifications and maintains
    a history of changes for debugging and auditing.
    
    Attributes:
        _checkpoint: Snapshot of attributes at last checkpoint.
        _history: List of all changes made.
    """
    
    def __init__(self) -> None:
        """Initialize the tracked object."""
        raise NotImplementedError("Implement __init__")
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Track attribute assignments.
        
        Args:
            name: The attribute name.
            value: The new value.
        """
        raise NotImplementedError("Implement __setattr__")
    
    def __delattr__(self, name: str) -> None:
        """Track attribute deletions.
        
        Args:
            name: The attribute name.
        
        Raises:
            AttributeError: If the attribute doesn't exist.
        """
        raise NotImplementedError("Implement __delattr__")
    
    def checkpoint(self) -> None:
        """Save the current state as the baseline for future comparisons."""
        raise NotImplementedError("Implement checkpoint")
    
    def get_changes(self) -> DiffResult:
        """Get changes since the last checkpoint.
        
        Returns:
            DiffResult showing added, removed, modified, and unchanged attrs.
        """
        raise NotImplementedError("Implement get_changes")
    
    def get_history(self) -> list[dict[str, Any]]:
        """Get the full change history.
        
        Returns:
            List of change records, each with 'action', 'name', 'old', 'new'.
        """
        raise NotImplementedError("Implement get_history")
    
    def rollback(self) -> None:
        """Revert all changes since the last checkpoint."""
        raise NotImplementedError("Implement rollback")
    
    def clear_history(self) -> None:
        """Clear the change history and reset checkpoint."""
        raise NotImplementedError("Implement clear_history")


class AttributeWatcher:
    """Watch attribute changes on an external object.
    
    Unlike TrackedObject, this wraps an existing object and
    monitors changes without modifying the target class.
    
    Example:
        >>> class Person:
        ...     def __init__(self, name: str) -> None:
        ...         self.name = name
        ...
        >>> person = Person("Alice")
        >>> watcher = AttributeWatcher(person)
        >>> person.name = "Bob"
        >>> changes = watcher.get_changes()
    """
    
    def __init__(self, target: object) -> None:
        """Initialize the watcher for a target object.
        
        Args:
            target: The object to watch.
        """
        raise NotImplementedError("Implement __init__")
    
    def snapshot(self) -> None:
        """Take a snapshot of the current state."""
        raise NotImplementedError("Implement snapshot")
    
    def get_changes(self) -> DiffResult:
        """Compare current state to the last snapshot.
        
        Returns:
            DiffResult showing differences.
        """
        raise NotImplementedError("Implement get_changes")
