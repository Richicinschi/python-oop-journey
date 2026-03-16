"""Task model with descriptor-based validation.

Reference implementation using descriptors for validated attributes.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum, auto
from typing import TYPE_CHECKING, Any
import uuid

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
    """Descriptor for validated string attributes."""
    
    def __init__(
        self,
        min_length: int = 0,
        max_length: int = 1000,
        required: bool = True,
    ) -> None:
        self.min_length = min_length
        self.max_length = max_length
        self.required = required
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.private_name = f"_{name}"
    
    def __get__(self, instance: Any, owner: type) -> str:
        if instance is None:
            return ""
        return getattr(instance, self.private_name, "")
    
    def __set__(self, instance: Any, value: str) -> None:
        if value is None:
            value = ""
        
        if not isinstance(value, str):
            raise ValueError(f"{self.name} must be a string")
        
        if self.required and not value.strip():
            raise ValueError(f"{self.name} is required")
        
        if len(value) < self.min_length:
            raise ValueError(f"{self.name} must be at least {self.min_length} characters")
        
        if len(value) > self.max_length:
            raise ValueError(f"{self.name} must be at most {self.max_length} characters")
        
        setattr(instance, self.private_name, value)


class ValidatedChoice:
    """Descriptor for enum/choice attributes."""
    
    def __init__(self, choices: type[Enum], default: Enum | None = None) -> None:
        self.choices = choices
        self.default = default
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.private_name = f"_{name}"
    
    def __get__(self, instance: Any, owner: type) -> Enum:
        if instance is None:
            return self.default if self.default else list(self.choices)[0]
        return getattr(instance, self.private_name, self.default)
    
    def __set__(self, instance: Any, value: Enum) -> None:
        if isinstance(value, str):
            try:
                value = self.choices[value]
            except KeyError:
                raise ValueError(f"Invalid {self.name}: {value}")
        
        if not isinstance(value, self.choices):
            raise ValueError(f"{self.name} must be a {self.choices.__name__}")
        
        setattr(instance, self.private_name, value)


class ValidatedDatetime:
    """Descriptor for optional datetime attributes."""
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.private_name = f"_{name}"
    
    def __get__(self, instance: Any, owner: type) -> datetime | None:
        if instance is None:
            return None
        return getattr(instance, self.private_name, None)
    
    def __set__(self, instance: Any, value: datetime | str | None) -> None:
        if value is None:
            setattr(instance, self.private_name, None)
            return
        
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError(f"Invalid datetime format: {value}")
        
        if not isinstance(value, datetime):
            raise ValueError(f"{self.name} must be a datetime or ISO string")
        
        setattr(instance, self.private_name, value)


class Task:
    """Task model with descriptor-based validation."""
    
    title = ValidatedString(min_length=3, max_length=100, required=True)
    description = ValidatedString(min_length=0, max_length=1000, required=False)
    priority = ValidatedChoice(Priority, Priority.MEDIUM)
    status = ValidatedChoice(Status, Status.BACKLOG)
    deadline = ValidatedDatetime()
    
    def __init__(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        deadline: datetime | str | None = None,
    ) -> None:
        self._task_id = str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.priority = priority
        self.status = Status.BACKLOG
        self.deadline = deadline
        self._assignee: User | None = None
        self._tags: set[str] = set()
        self.created_at = datetime.now()
        self.modified_at = self.created_at
    
    @property
    def task_id(self) -> str:
        return self._task_id
    
    @property
    def assignee(self) -> User | None:
        return self._assignee
    
    @property
    def tags(self) -> set[str]:
        return self._tags.copy()
    
    def assign_to(self, user: User | None) -> None:
        """Assign task to a user."""
        self._assignee = user
        self._touch()
    
    def unassign(self) -> None:
        """Remove task assignment."""
        self._assignee = None
        self._touch()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the task."""
        if not isinstance(tag, str) or not tag.strip():
            raise ValueError("Tag must be a non-empty string")
        if len(tag) > 50:
            raise ValueError("Tag must be at most 50 characters")
        self._tags.add(tag.strip().lower())
        self._touch()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the task."""
        self._tags.discard(tag.strip().lower())
        self._touch()
    
    def _touch(self) -> None:
        """Update modified timestamp."""
        self.modified_at = datetime.now()
    
    def can_transition_to(self, new_status: Status) -> bool:
        """Check if status transition is valid."""
        return new_status in VALID_TRANSITIONS.get(self.status, set())
    
    def transition_to(self, new_status: Status) -> None:
        """Attempt to transition to new status."""
        if not self.can_transition_to(new_status):
            raise ValueError(
                f"Cannot transition from {self.status.name} to {new_status.name}"
            )
        self.status = new_status
        self._touch()
    
    def start_progress(self) -> None:
        """Shortcut: Move from TODO/BACKLOG to IN_PROGRESS."""
        if self.status == Status.BACKLOG:
            self.transition_to(Status.TODO)
        if self.status == Status.TODO:
            self.transition_to(Status.IN_PROGRESS)
    
    def complete(self) -> None:
        """Shortcut: Move to DONE (via REVIEW if CRITICAL)."""
        if self.priority == Priority.CRITICAL and self.status != Status.REVIEW:
            # Critical tasks must go through review
            if self.status == Status.IN_PROGRESS:
                self.transition_to(Status.REVIEW)
            elif self.status == Status.BACKLOG:
                self.transition_to(Status.TODO)
                self.transition_to(Status.IN_PROGRESS)
                self.transition_to(Status.REVIEW)
            elif self.status == Status.TODO:
                self.transition_to(Status.IN_PROGRESS)
                self.transition_to(Status.REVIEW)
        else:
            # Non-critical can go directly
            if self.status == Status.BACKLOG:
                self.transition_to(Status.TODO)
            if self.status == Status.TODO:
                self.transition_to(Status.IN_PROGRESS)
            if self.status == Status.IN_PROGRESS:
                self.transition_to(Status.DONE)
            elif self.status == Status.REVIEW:
                self.transition_to(Status.DONE)
            elif self.status == Status.BACKLOG:
                # Handle case where we just transitioned to TODO above
                self.transition_to(Status.IN_PROGRESS)
                self.transition_to(Status.DONE)
    
    def cancel(self) -> None:
        """Cancel the task if not terminal."""
        if self.status == Status.DONE:
            raise ValueError("Cannot cancel a terminal task")
        if self.status == Status.CANCELLED:
            return  # Already cancelled
        self.transition_to(Status.CANCELLED)
    
    def is_overdue(self) -> bool:
        """Check if task is past deadline."""
        if self.deadline is None:
            return False
        if self.status in (Status.DONE, Status.CANCELLED):
            return False
        return datetime.now() > self.deadline
    
    def to_dict(self) -> dict[str, Any]:
        """Serialize task to dictionary."""
        return {
            "task_id": self._task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.name,
            "status": self.status.name,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "assignee": self._assignee.username if self._assignee else None,
            "tags": list(self._tags),
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any], users: dict[str, User] | None = None) -> Task:
        """Create Task from dictionary."""
        task = cls.__new__(cls)
        task._task_id = data["task_id"]
        task._title = data["title"]
        task._description = data.get("description", "")
        task._priority = Priority[data["priority"]]
        task._status = Status[data["status"]]
        
        deadline = data.get("deadline")
        task._deadline = datetime.fromisoformat(deadline) if deadline else None
        
        # Resolve assignee
        assignee_username = data.get("assignee")
        if assignee_username and users:
            task._assignee = users.get(assignee_username)
        else:
            task._assignee = None
        
        task._tags = set(data.get("tags", []))
        task.created_at = datetime.fromisoformat(data["created_at"])
        task.modified_at = datetime.fromisoformat(data["modified_at"])
        
        return task
    
    def __repr__(self) -> str:
        return (
            f"Task({self._task_id!r}, title={self.title!r}, "
            f"status={self.status.name}, priority={self.priority.name})"
        )
