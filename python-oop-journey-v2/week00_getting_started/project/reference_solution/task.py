"""Task data model for the Todo List application.

This module defines the Task class used throughout the application.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional


class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier for the task
        description: Task description text
        priority: Task priority ("high", "medium", or "low")
        due_date: Optional due date in ISO format (YYYY-MM-DD)
        completed: Whether the task is completed
        created_at: ISO timestamp when task was created
        completed_at: ISO timestamp when task was completed, or None
    """

    VALID_PRIORITIES = {"high", "medium", "low"}

    def __init__(
        self,
        task_id: int,
        description: str,
        priority: str = "medium",
        due_date: Optional[str] = None,
        completed: bool = False,
        created_at: Optional[str] = None,
        completed_at: Optional[str] = None,
    ) -> None:
        """Initialize a Task.

        Args:
            task_id: Unique identifier
            description: Task description
            priority: Priority level ("high", "medium", "low")
            due_date: Optional due date in ISO format
            completed: Initial completion status
            created_at: Creation timestamp (auto-generated if None)
            completed_at: Completion timestamp

        Raises:
            ValueError: If priority is invalid or description is empty
        """
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")

        priority_lower = priority.lower()
        if priority_lower not in self.VALID_PRIORITIES:
            raise ValueError(
                f"Invalid priority: {priority}. "
                f"Must be one of: {', '.join(self.VALID_PRIORITIES)}"
            )

        self.id = task_id
        self.description = description.strip()
        self.priority = priority_lower
        self.due_date = due_date
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at

    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the task
        """
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        """Create a Task from a dictionary.

        Args:
            data: Dictionary containing task data

        Returns:
            New Task instance
        """
        return cls(
            task_id=data["id"],
            description=data["description"],
            priority=data.get("priority", "medium"),
            due_date=data.get("due_date"),
            completed=data.get("completed", False),
            created_at=data.get("created_at"),
            completed_at=data.get("completed_at"),
        )

    def mark_completed(self) -> None:
        """Mark the task as completed and set completion timestamp."""
        self.completed = True
        self.completed_at = datetime.now().isoformat()

    def __str__(self) -> str:
        """Return string representation of the task."""
        status = "✓" if self.completed else " "
        priority_indicator = {"high": "!!!", "medium": "!", "low": ""}.get(
            self.priority, ""
        )
        due = f" (Due: {self.due_date})" if self.due_date else ""
        return f"[{status}] {self.id}: {self.description}{priority_indicator}{due}"

    def __repr__(self) -> str:
        """Return detailed representation of the task."""
        return (
            f"Task(id={self.id}, description='{self.description}', "
            f"priority='{self.priority}', completed={self.completed})"
        )
