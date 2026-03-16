"""Problem 04: Task Board (Kanban).

Topic: Class Design Principles
Difficulty: Medium

Design a task board system with the following classes:
- User: Team member with name and role
- Task: Work item with title, description, priority, and assignee
- Column: Kanban column containing tasks (e.g., To Do, In Progress, Done)
- Board: Collection of columns representing the workflow
- TaskManager: Handles task operations and movement between columns

Requirements:
- Tasks have priority levels (low, medium, high, critical)
- Columns maintain ordered list of tasks
- Tasks can be moved between columns
- Board validates workflow (can enforce column sequence)
- Users can be assigned to tasks
- Tasks can have due dates

Hints:
    - Hint 1: Column stores tasks in a list; Board tracks columns in ordered dict or list
    - Hint 2: TaskManager validates moves by checking column order in the board
    - Hint 3: Assign user to task by storing User object reference in Task._assignee
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum, auto


class Priority(Enum):
    """Task priority levels."""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


class TaskStatus(Enum):
    """Possible task statuses."""
    TODO = auto()
    IN_PROGRESS = auto()
    REVIEW = auto()
    DONE = auto()


class User:
    """Team member who can be assigned tasks.
    
    Attributes:
        user_id: Unique user identifier
        name: User's display name
        email: User's email
        role: User's role in team
    """
    
    def __init__(self, user_id: str, name: str, email: str, role: str = "member") -> None:
        raise NotImplementedError("Implement User.__init__")


class Task:
    """A unit of work on the board.
    
    Attributes:
        task_id: Unique task identifier
        title: Task title
        description: Task description
        priority: Task priority level
        status: Current task status
        assignee: User assigned to task (can be None)
        due_date: Optional due date
        created_at: When task was created
    """
    
    def __init__(
        self,
        task_id: str,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        due_date: datetime | None = None
    ) -> None:
        raise NotImplementedError("Implement Task.__init__")
    
    def assign_to(self, user: User | None) -> None:
        """Assign task to a user (or unassign if None)."""
        raise NotImplementedError("Implement Task.assign_to")
    
    def update_priority(self, priority: Priority) -> None:
        """Update task priority."""
        raise NotImplementedError("Implement Task.update_priority")
    
    def update_status(self, status: TaskStatus) -> None:
        """Update task status."""
        raise NotImplementedError("Implement Task.update_status")
    
    def is_overdue(self) -> bool:
        """Check if task is past due date."""
        raise NotImplementedError("Implement Task.is_overdue")


class Column:
    """A column on the Kanban board.
    
    Attributes:
        column_id: Unique column identifier
        name: Display name (e.g., "To Do", "In Progress")
        status: TaskStatus this column represents
        wip_limit: Work-in-progress limit (max tasks)
    """
    
    def __init__(self, column_id: str, name: str, status: TaskStatus, wip_limit: int = 10) -> None:
        raise NotImplementedError("Implement Column.__init__")
    
    @property
    def tasks(self) -> list[Task]:
        """Get tasks in this column (ordered by priority)."""
        raise NotImplementedError("Implement Column.tasks")
    
    def add_task(self, task: Task) -> bool:
        """Add a task to this column.
        
        Args:
            task: Task to add
            
        Returns:
            True if added (within WIP limit)
        """
        raise NotImplementedError("Implement Column.add_task")
    
    def remove_task(self, task: Task) -> bool:
        """Remove a task from this column.
        
        Args:
            task: Task to remove
            
        Returns:
            True if task was in column and removed
        """
        raise NotImplementedError("Implement Column.remove_task")
    
    def has_capacity(self) -> bool:
        """Check if column has room for more tasks."""
        raise NotImplementedError("Implement Column.has_capacity")
    
    def get_tasks_by_priority(self, priority: Priority) -> list[Task]:
        """Get tasks filtered by priority."""
        raise NotImplementedError("Implement Column.get_tasks_by_priority")


class Board:
    """Kanban board containing columns.
    
    Attributes:
        board_id: Unique board identifier
        name: Board name
        columns: Ordered list of columns representing workflow
    """
    
    def __init__(self, board_id: str, name: str) -> None:
        raise NotImplementedError("Implement Board.__init__")
    
    def add_column(self, column: Column, position: int | None = None) -> None:
        """Add a column to the board.
        
        Args:
            column: Column to add
            position: Optional position (None = append)
        """
        raise NotImplementedError("Implement Board.add_column")
    
    def get_column(self, status: TaskStatus) -> Column | None:
        """Get column by status type."""
        raise NotImplementedError("Implement Board.get_column")
    
    def get_task_location(self, task: Task) -> Column | None:
        """Find which column contains a task."""
        raise NotImplementedError("Implement Board.get_task_location")
    
    def can_move(self, task: Task, to_column: Column) -> bool:
        """Check if task can be moved to column.
        
        Validates workflow sequence and WIP limits.
        """
        raise NotImplementedError("Implement Board.can_move")


class TaskManager:
    """Manages task operations on the board.
    
    Single Responsibility: Task lifecycle and movement operations.
    """
    
    def __init__(self, board: Board) -> None:
        raise NotImplementedError("Implement TaskManager.__init__")
    
    def create_task(
        self,
        task_id: str,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        assignee: User | None = None,
        due_date: datetime | None = None
    ) -> Task:
        """Create a new task and add to To Do column."""
        raise NotImplementedError("Implement TaskManager.create_task")
    
    def move_task(self, task: Task, to_status: TaskStatus) -> bool:
        """Move task to a different column.
        
        Args:
            task: Task to move
            to_status: Target column status
            
        Returns:
            True if moved successfully
        """
        raise NotImplementedError("Implement TaskManager.move_task")
    
    def assign_task(self, task: Task, user: User | None) -> None:
        """Assign or unassign a task."""
        raise NotImplementedError("Implement TaskManager.assign_task")
    
    def get_tasks_for_user(self, user: User) -> list[Task]:
        """Get all tasks assigned to a user across all columns."""
        raise NotImplementedError("Implement TaskManager.get_tasks_for_user")
    
    def get_overdue_tasks(self) -> list[Task]:
        """Get all overdue tasks across all columns."""
        raise NotImplementedError("Implement TaskManager.get_overdue_tasks")
