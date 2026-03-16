"""Problem 09: Attribute History

Topic: Tracks all value changes
Difficulty: Medium

Create a descriptor that tracks the complete history of value changes.
"""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class HistoryEntry:
    """A single entry in the attribute history.
    
    Attributes:
        value: The value at this point in time
        timestamp: When the value was set
        previous_value: The value before this change
    """
    value: Any
    timestamp: datetime
    previous_value: Any = None


class History:
    """A descriptor that tracks all value changes.
    
    The descriptor should:
    - Store a complete history of all values set
    - Include timestamps for each change
    - Support accessing current, previous, and all historical values
    - Allow clearing history (keeping current value)
    
    Attributes:
        default: Optional default value
        max_history: Maximum number of entries to keep (0 = unlimited)
    """
    
    def __init__(self, default: Any = None, max_history: int = 0) -> None:
        """Initialize with optional default and history limit.
        
        Args:
            default: Default value
            max_history: Maximum history entries (0 = unlimited)
        """
        raise NotImplementedError("Implement History.__init__")
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Called when descriptor is assigned to class.
        
        Args:
            owner: The class
            name: The attribute name
        """
        raise NotImplementedError("Implement History.__set_name__")
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        """Get the current value.
        
        Args:
            instance: The instance, or None for class access
            owner: The owner class
            
        Returns:
            Current value, or self if class access
        """
        raise NotImplementedError("Implement History.__get__")
    
    def __set__(self, instance: object, value: Any) -> None:
        """Set value and record in history.
        
        Args:
            instance: The instance
            value: The new value
        """
        raise NotImplementedError("Implement History.__set__")
    
    def get_history(self, instance: object) -> list[HistoryEntry]:
        """Get complete history for an instance.
        
        Args:
            instance: The instance
            
        Returns:
            List of history entries (oldest first)
        """
        raise NotImplementedError("Implement History.get_history")
    
    def get_previous(self, instance: object) -> Any:
        """Get the previous value.
        
        Args:
            instance: The instance
            
        Returns:
            Previous value, or None if no history
        """
        raise NotImplementedError("Implement History.get_previous")
    
    def clear_history(self, instance: object) -> None:
        """Clear history, keeping only current value.
        
        Args:
            instance: The instance
        """
        raise NotImplementedError("Implement History.clear_history")
    
    def rollback(self, instance: object, steps: int = 1) -> bool:
        """Rollback to a previous value.
        
        Args:
            instance: The instance
            steps: Number of steps to rollback
            
        Returns:
            True if rollback was successful
        """
        raise NotImplementedError("Implement History.rollback")


class Document:
    """A document with versioned content.
    
    Attributes:
        title: Document title
        
    History-tracked Attributes:
        content: Document content with full history
    """
    
    title: str = ""
    content = History()
    
    def __init__(self, title: str, content: str = "") -> None:
        """Initialize document.
        
        Args:
            title: Document title
            content: Initial content
        """
        raise NotImplementedError("Implement Document.__init__")
    
    def edit(self, new_content: str) -> None:
        """Edit the document content.
        
        Args:
            new_content: New content
        """
        raise NotImplementedError("Implement Document.edit")
    
    def get_versions(self) -> list[HistoryEntry]:
        """Get all versions of the document.
        
        Returns:
            List of history entries
        """
        raise NotImplementedError("Implement Document.get_versions")
    
    def undo(self) -> bool:
        """Undo the last edit.
        
        Returns:
            True if undo was successful
        """
        raise NotImplementedError("Implement Document.undo")


class Setting:
    """A user setting with change history.
    
    Attributes:
        name: Setting name
        description: Setting description
        
    History-tracked Attributes:
        value: The setting value with history
    """
    
    name: str = ""
    description: str = ""
    value = History()
    
    def __init__(self, name: str, description: str, default_value: Any = None) -> None:
        """Initialize setting.
        
        Args:
            name: Setting name
            description: Setting description
            default_value: Default value
        """
        raise NotImplementedError("Implement Setting.__init__")
    
    def update(self, new_value: Any) -> None:
        """Update the setting value.
        
        Args:
            new_value: New value
        """
        raise NotImplementedError("Implement Setting.update")
    
    def get_changes(self) -> list[HistoryEntry]:
        """Get all changes to this setting.
        
        Returns:
            List of history entries
        """
        raise NotImplementedError("Implement Setting.get_changes")
    
    def has_changed(self) -> bool:
        """Check if value has ever been changed.
        
        Returns:
            True if there's more than one history entry
        """
        raise NotImplementedError("Implement Setting.has_changed")


# Hints for Attribute History (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to track the complete history of changes, not just the current value.
# Think about storing a list of (timestamp, old_value, new_value) tuples.
#
# Hint 2 - Structural plan:
# - Store history as a list of change records per instance
# - In __set__, append a record with current time, old value, and new value
# - In __delete__, record the deletion event
# - Provide methods to get_history(), get_value_at_time(), and get_current_value()
# - rollback() should restore the value from the last record and remove it
#
# Hint 3 - Edge-case warning:
# What if rollback() is called with no history? What if get_value_at_time() is called
# with a time before any changes? Also, be careful with the first set - there's no
# "old value" yet, so handle that case.
