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
        # TODO: Implement validation and initialization
        raise NotImplementedError("Implement Task.__init__")

    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the task
        """
        raise NotImplementedError("Implement Task.to_dict")

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        """Create a Task from a dictionary.

        Args:
            data: Dictionary containing task data

        Returns:
            New Task instance
        """
        raise NotImplementedError("Implement Task.from_dict")

    def mark_completed(self) -> None:
        """Mark the task as completed and set completion timestamp."""
        raise NotImplementedError("Implement Task.mark_completed")

    def __str__(self) -> str:
        """Return string representation of the task."""
        raise NotImplementedError("Implement Task.__str__")

    def __repr__(self) -> str:
        """Return detailed representation of the task."""
        raise NotImplementedError("Implement Task.__repr__")
