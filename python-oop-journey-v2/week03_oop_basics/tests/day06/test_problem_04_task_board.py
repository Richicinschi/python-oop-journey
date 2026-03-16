"""Tests for Problem 04: Task Board (Kanban)."""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from week03_oop_basics.solutions.day06.problem_04_task_board import (
    Board,
    Column,
    Priority,
    Task,
    TaskManager,
    TaskStatus,
    User,
)


class TestUser:
    """Tests for User class."""
    
    def test_user_creation(self) -> None:
        """Test user initialization."""
        user = User("USER001", "Alice", "alice@example.com", "developer")
        assert user.user_id == "USER001"
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.role == "developer"
    
    def test_user_default_role(self) -> None:
        """Test user default role."""
        user = User("USER001", "Alice", "alice@example.com")
        assert user.role == "member"


class TestTask:
    """Tests for Task class."""
    
    def test_task_creation(self) -> None:
        """Test task initialization."""
        task = Task("TASK001", "Fix bug", "Fix login bug", Priority.HIGH)
        assert task.task_id == "TASK001"
        assert task.title == "Fix bug"
        assert task.description == "Fix login bug"
        assert task.priority == Priority.HIGH
        assert task.status == TaskStatus.TODO
        assert task.assignee is None
    
    def test_task_assign_to(self) -> None:
        """Test task assignment."""
        task = Task("TASK001", "Fix bug", "Fix login bug")
        user = User("USER001", "Alice", "alice@example.com")
        
        task.assign_to(user)
        assert task.assignee == user
        
        task.assign_to(None)
        assert task.assignee is None
    
    def test_task_update_priority(self) -> None:
        """Test priority update."""
        task = Task("TASK001", "Fix bug", "Fix login bug", Priority.LOW)
        task.update_priority(Priority.CRITICAL)
        assert task.priority == Priority.CRITICAL
    
    def test_task_update_status(self) -> None:
        """Test status update."""
        task = Task("TASK001", "Fix bug")
        task.update_status(TaskStatus.IN_PROGRESS)
        assert task.status == TaskStatus.IN_PROGRESS
    
    def test_task_is_overdue(self) -> None:
        """Test overdue detection."""
        yesterday = datetime.now() - timedelta(days=1)
        task = Task("TASK001", "Fix bug", due_date=yesterday)
        assert task.is_overdue() is True
    
    def test_task_not_overdue(self) -> None:
        """Test non-overdue task."""
        tomorrow = datetime.now() + timedelta(days=1)
        task = Task("TASK001", "Fix bug", due_date=tomorrow)
        assert task.is_overdue() is False
    
    def test_task_no_due_date(self) -> None:
        """Test task without due date."""
        task = Task("TASK001", "Fix bug")
        assert task.is_overdue() is False


class TestColumn:
    """Tests for Column class."""
    
    def test_column_creation(self) -> None:
        """Test column initialization."""
        col = Column("COL001", "To Do", TaskStatus.TODO, 5)
        assert col.column_id == "COL001"
        assert col.name == "To Do"
        assert col.status == TaskStatus.TODO
        assert col.wip_limit == 5
        assert col.task_count == 0
    
    def test_add_task_success(self) -> None:
        """Test adding task to column."""
        col = Column("COL001", "To Do", TaskStatus.TODO, 5)
        task = Task("TASK001", "Fix bug")
        
        assert col.add_task(task) is True
        assert col.task_count == 1
        assert task.status == TaskStatus.TODO
    
    def test_add_task_wip_limit(self) -> None:
        """Test WIP limit enforcement."""
        col = Column("COL001", "To Do", TaskStatus.TODO, 2)
        
        col.add_task(Task("TASK001", "Fix bug"))
        col.add_task(Task("TASK002", "Add feature"))
        
        # Third task should fail
        result = col.add_task(Task("TASK003", "Refactor"))
        assert result is False
        assert col.task_count == 2
    
    def test_add_duplicate_task(self) -> None:
        """Test adding same task twice fails."""
        col = Column("COL001", "To Do", TaskStatus.TODO, 5)
        task = Task("TASK001", "Fix bug")
        
        col.add_task(task)
        assert col.add_task(task) is False
    
    def test_remove_task(self) -> None:
        """Test removing task from column."""
        col = Column("COL001", "To Do", TaskStatus.TODO, 5)
        task = Task("TASK001", "Fix bug")
        
        col.add_task(task)
        assert col.remove_task(task) is True
        assert col.task_count == 0
    
    def test_remove_nonexistent_task(self) -> None:
        """Test removing task not in column."""
        col = Column("COL001", "To Do", TaskStatus.TODO, 5)
        task = Task("TASK001", "Fix bug")
        
        assert col.remove_task(task) is False
    
    def test_has_capacity(self) -> None:
        """Test capacity check."""
        col = Column("COL001", "To Do", TaskStatus.TODO, 2)
        assert col.has_capacity() is True
        
        col.add_task(Task("TASK001", "Fix bug"))
        assert col.has_capacity() is True
        
        col.add_task(Task("TASK002", "Add feature"))
        assert col.has_capacity() is False
    
    def test_tasks_sorted_by_priority(self) -> None:
        """Test tasks are sorted by priority."""
        col = Column("COL001", "To Do", TaskStatus.TODO, 5)
        
        task_low = Task("TASK001", "Low", priority=Priority.LOW)
        task_critical = Task("TASK002", "Critical", priority=Priority.CRITICAL)
        task_high = Task("TASK003", "High", priority=Priority.HIGH)
        
        col.add_task(task_low)
        col.add_task(task_critical)
        col.add_task(task_high)
        
        tasks = col.tasks
        assert tasks[0].priority == Priority.CRITICAL
        assert tasks[1].priority == Priority.HIGH
        assert tasks[2].priority == Priority.LOW
    
    def test_get_tasks_by_priority(self) -> None:
        """Test filtering tasks by priority."""
        col = Column("COL001", "To Do", TaskStatus.TODO, 5)
        
        col.add_task(Task("TASK001", "Low", priority=Priority.LOW))
        col.add_task(Task("TASK002", "High", priority=Priority.HIGH))
        col.add_task(Task("TASK003", "Low", priority=Priority.LOW))
        
        low_tasks = col.get_tasks_by_priority(Priority.LOW)
        assert len(low_tasks) == 2


class TestBoard:
    """Tests for Board class."""
    
    def test_board_creation(self) -> None:
        """Test board initialization."""
        board = Board("BOARD001", "Dev Board")
        assert board.board_id == "BOARD001"
        assert board.name == "Dev Board"
        assert board.columns == []
    
    def test_add_column(self) -> None:
        """Test adding column to board."""
        board = Board("BOARD001", "Dev Board")
        col = Column("COL001", "To Do", TaskStatus.TODO)
        
        board.add_column(col)
        assert len(board.columns) == 1
    
    def test_add_column_at_position(self) -> None:
        """Test adding column at specific position."""
        board = Board("BOARD001", "Dev Board")
        
        col1 = Column("COL001", "To Do", TaskStatus.TODO)
        col2 = Column("COL002", "Done", TaskStatus.DONE)
        col3 = Column("COL003", "In Progress", TaskStatus.IN_PROGRESS)
        
        board.add_column(col1)
        board.add_column(col2)
        board.add_column(col3, position=1)
        
        assert board.columns[0].name == "To Do"
        assert board.columns[1].name == "In Progress"
        assert board.columns[2].name == "Done"
    
    def test_get_column_by_status(self) -> None:
        """Test finding column by status."""
        board = Board("BOARD001", "Dev Board")
        col = Column("COL001", "To Do", TaskStatus.TODO)
        
        board.add_column(col)
        found = board.get_column(TaskStatus.TODO)
        assert found == col
    
    def test_get_column_not_found(self) -> None:
        """Test finding non-existent column."""
        board = Board("BOARD001", "Dev Board")
        assert board.get_column(TaskStatus.TODO) is None
    
    def test_get_task_location(self) -> None:
        """Test finding which column contains a task."""
        board = Board("BOARD001", "Dev Board")
        col = Column("COL001", "To Do", TaskStatus.TODO)
        task = Task("TASK001", "Fix bug")
        
        board.add_column(col)
        col.add_task(task)
        
        assert board.get_task_location(task) == col
    
    def test_get_task_location_not_found(self) -> None:
        """Test finding task not on board."""
        board = Board("BOARD001", "Dev Board")
        col = Column("COL001", "To Do", TaskStatus.TODO)
        task = Task("TASK001", "Fix bug")
        
        board.add_column(col)
        assert board.get_task_location(task) is None
    
    def test_can_move_with_capacity(self) -> None:
        """Test can move when destination has capacity."""
        board = Board("BOARD001", "Dev Board")
        todo = Column("COL001", "To Do", TaskStatus.TODO)
        in_progress = Column("COL002", "In Progress", TaskStatus.IN_PROGRESS)
        
        board.add_column(todo)
        board.add_column(in_progress)
        
        task = Task("TASK001", "Fix bug")
        todo.add_task(task)
        
        assert board.can_move(task, in_progress) is True
    
    def test_can_move_without_capacity(self) -> None:
        """Test cannot move when destination full."""
        board = Board("BOARD001", "Dev Board")
        todo = Column("COL001", "To Do", TaskStatus.TODO, 5)
        in_progress = Column("COL002", "In Progress", TaskStatus.IN_PROGRESS, 1)
        
        board.add_column(todo)
        board.add_column(in_progress)
        
        in_progress.add_task(Task("TASK002", "Other task"))
        
        task = Task("TASK001", "Fix bug")
        todo.add_task(task)
        
        assert board.can_move(task, in_progress) is False


class TestTaskManager:
    """Tests for TaskManager class."""
    
    def test_create_task(self) -> None:
        """Test task creation."""
        board = Board("BOARD001", "Dev Board")
        board.add_column(Column("COL001", "To Do", TaskStatus.TODO))
        
        manager = TaskManager(board)
        task = manager.create_task("TASK001", "Fix bug")
        
        assert task.task_id == "TASK001"
        assert task.title == "Fix bug"
    
    def test_create_task_with_assignee(self) -> None:
        """Test task creation with assignee."""
        board = Board("BOARD001", "Dev Board")
        board.add_column(Column("COL001", "To Do", TaskStatus.TODO))
        
        manager = TaskManager(board)
        user = User("USER001", "Alice", "alice@example.com")
        task = manager.create_task("TASK001", "Fix bug", assignee=user)
        
        assert task.assignee == user
    
    def test_move_task(self) -> None:
        """Test moving task between columns."""
        board = Board("BOARD001", "Dev Board")
        board.add_column(Column("COL001", "To Do", TaskStatus.TODO))
        board.add_column(Column("COL002", "In Progress", TaskStatus.IN_PROGRESS))
        
        manager = TaskManager(board)
        task = manager.create_task("TASK001", "Fix bug")
        
        assert manager.move_task(task, TaskStatus.IN_PROGRESS) is True
        assert task.status == TaskStatus.IN_PROGRESS
    
    def test_move_task_no_column(self) -> None:
        """Test moving to non-existent column."""
        board = Board("BOARD001", "Dev Board")
        board.add_column(Column("COL001", "To Do", TaskStatus.TODO))
        
        manager = TaskManager(board)
        task = manager.create_task("TASK001", "Fix bug")
        
        assert manager.move_task(task, TaskStatus.REVIEW) is False
    
    def test_get_tasks_for_user(self) -> None:
        """Test getting tasks assigned to user."""
        board = Board("BOARD001", "Dev Board")
        board.add_column(Column("COL001", "To Do", TaskStatus.TODO))
        board.add_column(Column("COL002", "In Progress", TaskStatus.IN_PROGRESS))
        
        manager = TaskManager(board)
        user = User("USER001", "Alice", "alice@example.com")
        
        task1 = manager.create_task("TASK001", "Fix bug", assignee=user)
        task2 = manager.create_task("TASK002", "Add feature", assignee=user)
        manager.create_task("TASK003", "Refactor")  # No assignee
        
        user_tasks = manager.get_tasks_for_user(user)
        assert len(user_tasks) == 2
        assert task1 in user_tasks
        assert task2 in user_tasks
    
    def test_get_overdue_tasks(self) -> None:
        """Test getting overdue tasks."""
        board = Board("BOARD001", "Dev Board")
        board.add_column(Column("COL001", "To Do", TaskStatus.TODO))
        
        manager = TaskManager(board)
        yesterday = datetime.now() - timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=1)
        
        overdue = manager.create_task("TASK001", "Overdue", due_date=yesterday)
        not_overdue = manager.create_task("TASK002", "Not Overdue", due_date=tomorrow)
        
        overdue_tasks = manager.get_overdue_tasks()
        assert len(overdue_tasks) == 1
        assert overdue in overdue_tasks
        assert not_overdue not in overdue_tasks
