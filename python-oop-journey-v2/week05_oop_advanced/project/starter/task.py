"""Task model with descriptor-based validation.

Implement Task class using descriptors for validated attributes.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum, auto
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .user import User


class Priority(Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Status(Enum):
    """Task status workflow states."""
    BACKLOG = auto()
    TODO = auto()
    IN_PROGRESS = auto()
    REVIEW = auto()
    DONE = auto()
    CANCELLED = auto()


# Valid status transitions: current -> {allowed next states}
VALID_TRANSITIONS: dict[Status, set[Status]] = {
    Status.BACKLOG: {Status.TODO, Status.CANCELLED},
    Status.TODO: {Status.IN_PROGRESS, Status.CANCELLED},
    Status.IN_PROGRESS: {Status.REVIEW, Status.TODO, Status.CANCELLED},
    Status.REVIEW: {Status.DONE, Status.IN_PROGRESS, Status.CANCELLED},
    Status.DONE: set(),  # Terminal state
    Status.CANCELLED: set(),  # Terminal state
}


class ValidatedString:
    """Descriptor for validated string attributes.
    
    TODO: Implement string descriptor that:
    1. Takes min_length, max_length, required in __init__
    2. Validates on __set__
    3. Raises ValueError for invalid values
    4. Stores in private attribute
    """
    raise NotImplementedError("Implement ValidatedString descriptor")


class ValidatedChoice:
    """Descriptor for enum/choice attributes.
    
    TODO: Implement choice descriptor that:
    1. Takes valid choices (Enum class or list) in __init__
    2. Validates value is in choices on __set__
    3. Raises ValueError for invalid choices
    4. Stores in private attribute
    """
    raise NotImplementedError("Implement ValidatedChoice descriptor")


class ValidatedDatetime:
    """Descriptor for optional datetime attributes.
    
    TODO: Implement datetime descriptor that:
    1. Accepts datetime objects or ISO format strings
    2. Validates format if string provided
    3. Stores as datetime object or None
    4. Returns datetime or None on get
    """
    raise NotImplementedError("Implement ValidatedDatetime descriptor")


class Task:
    """Task model with descriptor-based validation.
    
    Uses descriptors for type-safe, validated attributes.
    
    TODO: Implement Task class with:
    1. ValidatedString for title and description
    2. ValidatedChoice for priority and status
    3. ValidatedDatetime for deadline
    4. Status workflow enforcement
    5. Assignment and tagging functionality
    """
    
    # TODO: Define descriptors as class attributes
    # title = ValidatedString(...)
    # description = ValidatedString(...)
    # priority = ValidatedChoice(...)
    # status = ValidatedChoice(...)
    # deadline = ValidatedDatetime(...)
    
    def __init__(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        deadline: datetime | str | None = None,
    ) -> None:
        raise NotImplementedError("Implement Task.__init__")
    
    def assign_to(self, user: User | None) -> None:
        """Assign task to a user.
        
        TODO: Set assignee attribute.
        """
        raise NotImplementedError("Implement assign_to")
    
    def unassign(self) -> None:
        """Remove task assignment.
        
        TODO: Clear assignee.
        """
        raise NotImplementedError("Implement unassign")
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the task.
        
        TODO: Validate tag is valid string, add to tags set/list.
        """
        raise NotImplementedError("Implement add_tag")
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the task.
        
        TODO: Remove tag if present.
        """
        raise NotImplementedError("Implement remove_tag")
    
    def can_transition_to(self, new_status: Status) -> bool:
        """Check if status transition is valid.
        
        TODO: Check VALID_TRANSITIONS matrix.
        """
        raise NotImplementedError("Implement can_transition_to")
    
    def transition_to(self, new_status: Status) -> None:
        """Attempt to transition to new status.
        
        TODO: Validate transition, raise ValueError if invalid,
        otherwise update status and modified_at.
        """
        raise NotImplementedError("Implement transition_to")
    
    def start_progress(self) -> None:
        """Shortcut: Move from TODO/BACKLOG to IN_PROGRESS.
        
        TODO: Implement status transition shortcut.
        """
        raise NotImplementedError("Implement start_progress")
    
    def complete(self) -> None:
        """Shortcut: Move to DONE (via REVIEW if CRITICAL).
        
        TODO: CRITICAL tasks must go through REVIEW first.
        """
        raise NotImplementedError("Implement complete")
    
    def cancel(self) -> None:
        """Cancel the task if not terminal.
        
        TODO: Transition to CANCELLED if valid.
        """
        raise NotImplementedError("Implement cancel")
    
    def is_overdue(self) -> bool:
        """Check if task is past deadline.
        
        TODO: Compare deadline to current time.
        """
        raise NotImplementedError("Implement is_overdue")
    
    def to_dict(self) -> dict[str, Any]:
        """Serialize task to dictionary.
        
        TODO: Return dict with all task fields.
        """
        raise NotImplementedError("Implement to_dict")
    
    @classmethod
    def from_dict(cls, data: dict[str, Any], users: dict[str, User] | None = None) -> Task:
        """Create Task from dictionary.
        
        TODO: Deserialize from dict, resolving assignee from users dict.
        """
        raise NotImplementedError("Implement from_dict")
    
    def __repr__(self) -> str:
        raise NotImplementedError("Implement __repr__")
