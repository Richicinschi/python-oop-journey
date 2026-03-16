"""Task manager module.

Provides high-level operations for managing tasks.
"""

from __future__ import annotations

from typing import List, Optional

from .storage import load_tasks, save_tasks
from .task import Task


class TaskManager:
    """Manages a collection of tasks.

    Provides methods for adding, retrieving, updating, and deleting tasks.
    Automatically persists changes to a file.

    Attributes:
        tasks: List of Task objects
        filepath: Path to the storage file
        next_id: Next available task ID
    """

    def __init__(self, filepath: str = "tasks.json") -> None:
        """Initialize the TaskManager.

        Args:
            filepath: Path to the tasks JSON file
        """
        # TODO: Initialize and load existing tasks
        raise NotImplementedError("Implement TaskManager.__init__")

    def add_task(
        self,
        description: str,
        priority: str = "medium",
        due_date: Optional[str] = None,
    ) -> Task:
        """Add a new task.

        Args:
            description: Task description
            priority: Task priority ("high", "medium", "low")
            due_date: Optional due date in ISO format

        Returns:
            The newly created Task

        Raises:
            ValueError: If description is empty or priority is invalid
        """
        raise NotImplementedError("Implement add_task")

    def get_tasks(
        self,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        sort_by: str = "id",
    ) -> List[Task]:
        """Get tasks with optional filtering and sorting.

        Args:
            completed: Filter by completion status (None = all)
            priority: Filter by priority (None = all)
            sort_by: Sort field ("id", "priority", "due_date", "created_at")

        Returns:
            List of matching tasks
        """
        raise NotImplementedError("Implement get_tasks")

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID.

        Args:
            task_id: The task ID to look up

        Returns:
            The Task if found, None otherwise
        """
        raise NotImplementedError("Implement get_task_by_id")

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed.

        Args:
            task_id: ID of the task to complete

        Returns:
            True if task was found and marked complete, False otherwise
        """
        raise NotImplementedError("Implement complete_task")

    def delete_task(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was found and deleted, False otherwise
        """
        raise NotImplementedError("Implement delete_task")

    def clear_completed(self) -> int:
        """Remove all completed tasks.

        Returns:
            Number of tasks removed
        """
        raise NotImplementedError("Implement clear_completed")

    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by description.

        Args:
            query: Search string (case-insensitive)

        Returns:
            List of matching tasks
        """
        raise NotImplementedError("Implement search_tasks")

    def save(self) -> bool:
        """Save tasks to file.

        Returns:
            True if successful, False otherwise
        """
        raise NotImplementedError("Implement save")

    def get_stats(self) -> dict:
        """Get task statistics.

        Returns:
            Dictionary with task statistics
        """
        raise NotImplementedError("Implement get_stats")
