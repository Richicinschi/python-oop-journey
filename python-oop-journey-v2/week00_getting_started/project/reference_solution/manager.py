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
        self.filepath = filepath
        self.tasks: List[Task] = load_tasks(filepath)
        self.next_id = self._calculate_next_id()

    def _calculate_next_id(self) -> int:
        """Calculate the next available task ID.

        Returns:
            Next available ID (1 if no tasks exist)
        """
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

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
        task = Task(
            task_id=self.next_id,
            description=description,
            priority=priority,
            due_date=due_date,
        )
        self.tasks.append(task)
        self.next_id += 1
        self.save()
        return task

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
        result = self.tasks.copy()

        if completed is not None:
            result = [t for t in result if t.completed == completed]

        if priority is not None:
            priority_lower = priority.lower()
            result = [t for t in result if t.priority == priority_lower]

        # Sort by specified field
        if sort_by == "id":
            result.sort(key=lambda t: t.id)
        elif sort_by == "priority":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            result.sort(key=lambda t: priority_order.get(t.priority, 3))
        elif sort_by == "due_date":
            result.sort(key=lambda t: (t.due_date is None, t.due_date or ""))
        elif sort_by == "created_at":
            result.sort(key=lambda t: t.created_at)

        return result

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID.

        Args:
            task_id: The task ID to look up

        Returns:
            The Task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed.

        Args:
            task_id: ID of the task to complete

        Returns:
            True if task was found and marked complete, False otherwise
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        task.mark_completed()
        self.save()
        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was found and deleted, False otherwise
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save()
                return True
        return False

    def clear_completed(self) -> int:
        """Remove all completed tasks.

        Returns:
            Number of tasks removed
        """
        initial_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.completed]
        removed = initial_count - len(self.tasks)
        if removed > 0:
            self.save()
        return removed

    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by description.

        Args:
            query: Search string (case-insensitive)

        Returns:
            List of matching tasks
        """
        query_lower = query.lower()
        return [t for t in self.tasks if query_lower in t.description.lower()]

    def save(self) -> bool:
        """Save tasks to file.

        Returns:
            True if successful, False otherwise
        """
        return save_tasks(self.tasks, self.filepath)

    def get_stats(self) -> dict:
        """Get task statistics.

        Returns:
            Dictionary with task statistics
        """
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed

        by_priority = {"high": 0, "medium": 0, "low": 0}
        for task in self.tasks:
            if task.priority in by_priority:
                by_priority[task.priority] += 1

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "by_priority": by_priority,
        }
