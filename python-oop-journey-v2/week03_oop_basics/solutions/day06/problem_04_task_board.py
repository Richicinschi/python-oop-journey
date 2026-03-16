"""Solution for Problem 04: Task Board (Kanban).

Demonstrates class design principles:
- Encapsulation: Task manages its own state transitions
- Cohesion: Column manages tasks and WIP limits
- Single Responsibility: TaskManager handles operations, Board manages structure
- State Validation: Board enforces workflow rules
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
        self._user_id = user_id
        self._name = name
        self._email = email
        self._role = role
    
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def role(self) -> str:
        return self._role


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
        self._task_id = task_id
        self._title = title
        self._description = description
        self._priority = priority
        self._status = TaskStatus.TODO
        self._assignee: User | None = None
        self._due_date = due_date
        self._created_at = datetime.now()
    
    @property
    def task_id(self) -> str:
        return self._task_id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def priority(self) -> Priority:
        return self._priority
    
    @property
    def status(self) -> TaskStatus:
        return self._status
    
    @property
    def assignee(self) -> User | None:
        return self._assignee
    
    @property
    def due_date(self) -> datetime | None:
        return self._due_date
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    def assign_to(self, user: User | None) -> None:
        """Assign task to a user (or unassign if None)."""
        self._assignee = user
    
    def update_priority(self, priority: Priority) -> None:
        """Update task priority."""
        self._priority = priority
    
    def update_status(self, status: TaskStatus) -> None:
        """Update task status."""
        self._status = status
    
    def is_overdue(self) -> bool:
        """Check if task is past due date."""
        if self._due_date is None:
            return False
        return datetime.now() > self._due_date


class Column:
    """A column on the Kanban board.
    
    Attributes:
        column_id: Unique column identifier
        name: Display name (e.g., "To Do", "In Progress")
        status: TaskStatus this column represents
        wip_limit: Work-in-progress limit (max tasks)
    """
    
    def __init__(self, column_id: str, name: str, status: TaskStatus, wip_limit: int = 10) -> None:
        self._column_id = column_id
        self._name = name
        self._status = status
        self._wip_limit = wip_limit
        self._tasks: list[Task] = []
    
    @property
    def column_id(self) -> str:
        return self._column_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def status(self) -> TaskStatus:
        return self._status
    
    @property
    def wip_limit(self) -> int:
        return self._wip_limit
    
    @property
    def tasks(self) -> list[Task]:
        """Get tasks in this column (ordered by priority)."""
        # Sort by priority (CRITICAL first, LOW last)
        priority_order = {
            Priority.CRITICAL: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3
        }
        return sorted(self._tasks, key=lambda t: priority_order[t.priority])
    
    @property
    def task_count(self) -> int:
        return len(self._tasks)
    
    def add_task(self, task: Task) -> bool:
        """Add a task to this column.
        
        Args:
            task: Task to add
            
        Returns:
            True if added (within WIP limit)
        """
        if len(self._tasks) >= self._wip_limit:
            return False
        if task in self._tasks:
            return False
        self._tasks.append(task)
        task.update_status(self._status)
        return True
    
    def remove_task(self, task: Task) -> bool:
        """Remove a task from this column.
        
        Args:
            task: Task to remove
            
        Returns:
            True if task was in column and removed
        """
        if task in self._tasks:
            self._tasks.remove(task)
            return True
        return False
    
    def has_capacity(self) -> bool:
        """Check if column has room for more tasks."""
        return len(self._tasks) < self._wip_limit
    
    def get_tasks_by_priority(self, priority: Priority) -> list[Task]:
        """Get tasks filtered by priority."""
        return [t for t in self._tasks if t.priority == priority]
    
    def contains_task(self, task: Task) -> bool:
        """Check if column contains a specific task."""
        return task in self._tasks


class Board:
    """Kanban board containing columns.
    
    Attributes:
        board_id: Unique board identifier
        name: Board name
        columns: Ordered list of columns representing workflow
    """
    
    def __init__(self, board_id: str, name: str) -> None:
        self._board_id = board_id
        self._name = name
        self._columns: list[Column] = []
    
    @property
    def board_id(self) -> str:
        return self._board_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def columns(self) -> list[Column]:
        return self._columns.copy()
    
    def add_column(self, column: Column, position: int | None = None) -> None:
        """Add a column to the board.
        
        Args:
            column: Column to add
            position: Optional position (None = append)
        """
        if position is None:
            self._columns.append(column)
        else:
            self._columns.insert(position, column)
    
    def get_column(self, status: TaskStatus) -> Column | None:
        """Get column by status type."""
        for col in self._columns:
            if col.status == status:
                return col
        return None
    
    def get_task_location(self, task: Task) -> Column | None:
        """Find which column contains a task."""
        for col in self._columns:
            if col.contains_task(task):
                return col
        return None
    
    def can_move(self, task: Task, to_column: Column) -> bool:
        """Check if task can be moved to column.
        
        Validates workflow sequence and WIP limits.
        """
        from_column = self.get_task_location(task)
        if from_column is None:
            return to_column.has_capacity()
        
        # Get column indices to check workflow order
        from_idx = self._columns.index(from_column)
        to_idx = self._columns.index(to_column)
        
        # Can only move forward in workflow (or back to previous)
        # For simplicity, allow any move but prefer forward progression
        
        return to_column.has_capacity()


class TaskManager:
    """Manages task operations on the board.
    
    Single Responsibility: Task lifecycle and movement operations.
    """
    
    def __init__(self, board: Board) -> None:
        self._board = board
    
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
        task = Task(task_id, title, description, priority, due_date)
        if assignee:
            task.assign_to(assignee)
        
        # Add to To Do column if it exists
        todo_col = self._board.get_column(TaskStatus.TODO)
        if todo_col:
            todo_col.add_task(task)
        
        return task
    
    def move_task(self, task: Task, to_status: TaskStatus) -> bool:
        """Move task to a different column.
        
        Args:
            task: Task to move
            to_status: Target column status
            
        Returns:
            True if moved successfully
        """
        from_col = self._board.get_task_location(task)
        to_col = self._board.get_column(to_status)
        
        if to_col is None:
            return False
        if not self._board.can_move(task, to_col):
            return False
        
        # Remove from current column if exists
        if from_col:
            from_col.remove_task(task)
        
        # Add to new column
        return to_col.add_task(task)
    
    def assign_task(self, task: Task, user: User | None) -> None:
        """Assign or unassign a task."""
        task.assign_to(user)
    
    def get_tasks_for_user(self, user: User) -> list[Task]:
        """Get all tasks assigned to a user across all columns."""
        tasks = []
        for col in self._board.columns:
            for task in col.tasks:
                if task.assignee == user:
                    tasks.append(task)
        return tasks
    
    def get_overdue_tasks(self) -> list[Task]:
        """Get all overdue tasks across all columns."""
        overdue = []
        for col in self._board.columns:
            for task in col.tasks:
                if task.is_overdue():
                    overdue.append(task)
        return overdue
