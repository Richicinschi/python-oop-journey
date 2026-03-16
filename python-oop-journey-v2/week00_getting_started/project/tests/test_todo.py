"""Tests for the Todo List CLI Application.

This module contains comprehensive tests for all components of the
todo list application including Task, TaskManager, storage, and CLI.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import uuid
from datetime import datetime
from unittest.mock import patch

import pytest

# Import from reference solution
from week00_getting_started.project.reference_solution.task import Task
from week00_getting_started.project.reference_solution.manager import TaskManager
from week00_getting_started.project.reference_solution import storage
from week00_getting_started.project.reference_solution import cli


def get_test_filepath() -> str:
    """Generate a unique test file path."""
    return f"test_tasks_{uuid.uuid4().hex}.json"


def cleanup_file(filepath: str) -> None:
    """Remove test file if it exists."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except (OSError, PermissionError):
        pass


@pytest.fixture
def temp_tasks_file():
    """Create a temporary tasks file path and clean up after test."""
    filepath = get_test_filepath()
    yield filepath
    cleanup_file(filepath)


@pytest.fixture
def isolated_manager():
    """Create a TaskManager with a unique temporary file."""
    filepath = get_test_filepath()
    manager = TaskManager(filepath)
    yield manager
    cleanup_file(filepath)


# =============================================================================
# Task Model Tests (10 tests)
# =============================================================================


def test_task_creation_basic() -> None:
    """Test basic task creation."""
    task = Task(1, "Test task")
    assert task.id == 1
    assert task.description == "Test task"
    assert task.priority == "medium"
    assert task.completed is False


def test_task_creation_with_all_fields() -> None:
    """Test task creation with all fields specified."""
    task = Task(
        task_id=2,
        description="High priority task",
        priority="high",
        due_date="2026-12-31",
        completed=True,
    )
    assert task.id == 2
    assert task.priority == "high"
    assert task.due_date == "2026-12-31"
    assert task.completed is True


def test_task_empty_description_raises() -> None:
    """Test that empty description raises ValueError."""
    with pytest.raises(ValueError, match="description"):
        Task(1, "")


def test_task_whitespace_description_raises() -> None:
    """Test that whitespace-only description raises ValueError."""
    with pytest.raises(ValueError, match="description"):
        Task(1, "   ")


def test_task_invalid_priority_raises() -> None:
    """Test that invalid priority raises ValueError."""
    with pytest.raises(ValueError, match="priority"):
        Task(1, "Test", priority="invalid")


def test_task_priority_case_insensitive() -> None:
    """Test that priority is stored in lowercase."""
    task = Task(1, "Test", priority="HIGH")
    assert task.priority == "high"


def test_task_mark_completed() -> None:
    """Test marking a task as completed."""
    task = Task(1, "Test")
    assert task.completed is False
    assert task.completed_at is None

    task.mark_completed()
    assert task.completed is True
    assert task.completed_at is not None


def test_task_to_dict() -> None:
    """Test converting task to dictionary."""
    task = Task(1, "Test task", priority="high", due_date="2026-01-01")
    data = task.to_dict()

    assert data["id"] == 1
    assert data["description"] == "Test task"
    assert data["priority"] == "high"
    assert data["due_date"] == "2026-01-01"
    assert data["completed"] is False
    assert "created_at" in data


def test_task_from_dict() -> None:
    """Test creating task from dictionary."""
    data = {
        "id": 5,
        "description": "From dict",
        "priority": "low",
        "due_date": None,
        "completed": True,
        "created_at": "2026-01-01T00:00:00",
        "completed_at": "2026-01-02T00:00:00",
    }
    task = Task.from_dict(data)

    assert task.id == 5
    assert task.description == "From dict"
    assert task.priority == "low"
    assert task.completed is True


def test_task_str_representation() -> None:
    """Test string representation of task."""
    task = Task(1, "Test task")
    assert "1" in str(task)
    assert "Test task" in str(task)


def test_task_description_stripped() -> None:
    """Test that description is stripped of leading/trailing whitespace."""
    task = Task(1, "  Test task  ")
    assert task.description == "Test task"


# =============================================================================
# Storage Tests (5 tests)
# =============================================================================


def test_load_tasks_nonexistent_file(temp_tasks_file) -> None:
    """Test loading from non-existent file returns empty list."""
    cleanup_file(temp_tasks_file)
    tasks = storage.load_tasks(temp_tasks_file)
    assert tasks == []


def test_save_and_load_tasks(temp_tasks_file) -> None:
    """Test saving and loading tasks preserves data."""
    tasks = [Task(1, "Task 1"), Task(2, "Task 2", priority="high")]

    assert storage.save_tasks(tasks, temp_tasks_file) is True
    loaded = storage.load_tasks(temp_tasks_file)

    assert len(loaded) == 2
    assert loaded[0].description == "Task 1"
    assert loaded[1].priority == "high"


def test_load_tasks_invalid_json(temp_tasks_file) -> None:
    """Test loading file with invalid JSON raises error."""
    with open(temp_tasks_file, "w") as f:
        f.write("not valid json")

    with pytest.raises(json.JSONDecodeError):
        storage.load_tasks(temp_tasks_file)


def test_ensure_directory_exists(temp_tasks_file) -> None:
    """Test that directory is created if it doesn't exist."""
    nested_dir = f"test_dir_{uuid.uuid4().hex}"
    filepath = os.path.join(nested_dir, "sub", "tasks.json")

    try:
        storage.ensure_directory_exists(filepath)
        assert os.path.exists(nested_dir)
    finally:
        import shutil
        if os.path.exists(nested_dir):
            shutil.rmtree(nested_dir, ignore_errors=True)


def test_save_tasks_creates_directory(temp_tasks_file) -> None:
    """Test that saving creates parent directories."""
    nested_dir = f"test_nested_{uuid.uuid4().hex}"
    filepath = os.path.join(nested_dir, "tasks.json")
    tasks = [Task(1, "Test")]

    try:
        assert storage.save_tasks(tasks, filepath) is True
        assert os.path.exists(nested_dir)
    finally:
        import shutil
        if os.path.exists(nested_dir):
            shutil.rmtree(nested_dir, ignore_errors=True)


# =============================================================================
# TaskManager Tests (22 tests)
# =============================================================================


def test_manager_init_creates_empty(temp_tasks_file) -> None:
    """Test manager initializes with empty tasks if no file exists."""
    manager = TaskManager(temp_tasks_file)
    assert manager.tasks == []
    assert manager.next_id == 1


def test_manager_add_task(isolated_manager) -> None:
    """Test adding a task assigns correct ID."""
    task = isolated_manager.add_task("Test task")

    assert task.id == 1
    assert task.description == "Test task"
    assert isolated_manager.next_id == 2


def test_manager_add_multiple_tasks(isolated_manager) -> None:
    """Test adding multiple tasks increments IDs."""
    task1 = isolated_manager.add_task("Task 1")
    task2 = isolated_manager.add_task("Task 2")
    task3 = isolated_manager.add_task("Task 3")

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3


def test_manager_add_task_invalid_description(isolated_manager) -> None:
    """Test adding task with invalid description raises error."""
    with pytest.raises(ValueError):
        isolated_manager.add_task("")


def test_manager_get_task_by_id(isolated_manager) -> None:
    """Test retrieving task by ID."""
    task = isolated_manager.add_task("Find me")

    found = isolated_manager.get_task_by_id(task.id)
    assert found is not None
    assert found.description == "Find me"


def test_manager_get_task_by_id_not_found(isolated_manager) -> None:
    """Test retrieving non-existent task returns None."""
    assert isolated_manager.get_task_by_id(999) is None


def test_manager_complete_task(isolated_manager) -> None:
    """Test completing a task."""
    task = isolated_manager.add_task("Complete me")

    assert isolated_manager.complete_task(task.id) is True
    assert task.completed is True


def test_manager_complete_task_not_found(isolated_manager) -> None:
    """Test completing non-existent task returns False."""
    assert isolated_manager.complete_task(999) is False


def test_manager_delete_task(isolated_manager) -> None:
    """Test deleting a task."""
    task = isolated_manager.add_task("Delete me")
    task_id = task.id

    assert isolated_manager.delete_task(task_id) is True
    assert isolated_manager.get_task_by_id(task_id) is None


def test_manager_delete_task_not_found(isolated_manager) -> None:
    """Test deleting non-existent task returns False."""
    assert isolated_manager.delete_task(999) is False


def test_manager_clear_completed(isolated_manager) -> None:
    """Test clearing completed tasks."""
    task1 = isolated_manager.add_task("Pending")
    task2 = isolated_manager.add_task("Completed")
    isolated_manager.complete_task(task2.id)

    count = isolated_manager.clear_completed()
    assert count == 1
    assert len(isolated_manager.tasks) == 1
    assert isolated_manager.tasks[0].id == task1.id


def test_manager_get_tasks_filter_completed(isolated_manager) -> None:
    """Test filtering tasks by completion status."""
    task1 = isolated_manager.add_task("Pending")
    task2 = isolated_manager.add_task("Completed")
    isolated_manager.complete_task(task2.id)

    pending = isolated_manager.get_tasks(completed=False)
    completed = isolated_manager.get_tasks(completed=True)

    assert len(pending) == 1
    assert len(completed) == 1
    assert pending[0].id == task1.id
    assert completed[0].id == task2.id


def test_manager_get_tasks_filter_priority(isolated_manager) -> None:
    """Test filtering tasks by priority."""
    isolated_manager.add_task("High task", priority="high")
    isolated_manager.add_task("Low task", priority="low")

    high_tasks = isolated_manager.get_tasks(priority="high")
    assert len(high_tasks) == 1
    assert high_tasks[0].priority == "high"


def test_manager_get_tasks_sort_by_priority(isolated_manager) -> None:
    """Test sorting tasks by priority."""
    isolated_manager.add_task("Low", priority="low")
    isolated_manager.add_task("High", priority="high")
    isolated_manager.add_task("Medium", priority="medium")

    sorted_tasks = isolated_manager.get_tasks(sort_by="priority")
    assert sorted_tasks[0].priority == "high"
    assert sorted_tasks[1].priority == "medium"
    assert sorted_tasks[2].priority == "low"


def test_manager_search_tasks(isolated_manager) -> None:
    """Test searching tasks by description."""
    isolated_manager.add_task("Buy groceries")
    isolated_manager.add_task("Call mom")
    isolated_manager.add_task("Buy milk")

    results = isolated_manager.search_tasks("buy")
    assert len(results) == 2


def test_manager_search_case_insensitive(isolated_manager) -> None:
    """Test that search is case-insensitive."""
    isolated_manager.add_task("Buy GROCERIES")

    results = isolated_manager.search_tasks("buy")
    assert len(results) == 1


def test_manager_get_stats(isolated_manager) -> None:
    """Test getting task statistics."""
    isolated_manager.add_task("Task 1", priority="high")
    isolated_manager.add_task("Task 2", priority="medium")
    task3 = isolated_manager.add_task("Task 3", priority="low")
    isolated_manager.complete_task(task3.id)

    stats = isolated_manager.get_stats()
    assert stats["total"] == 3
    assert stats["completed"] == 1
    assert stats["pending"] == 2
    assert stats["by_priority"]["high"] == 1
    assert stats["by_priority"]["medium"] == 1
    assert stats["by_priority"]["low"] == 1


def test_manager_next_id_after_load(temp_tasks_file) -> None:
    """Test that next_id is calculated correctly after loading."""
    manager1 = TaskManager(temp_tasks_file)
    manager1.add_task("Task 1")
    manager1.add_task("Task 2")

    manager2 = TaskManager(temp_tasks_file)
    task3 = manager2.add_task("Task 3")

    assert task3.id == 3


# =============================================================================
# CLI Tests (8 tests)
# =============================================================================


def test_cli_format_task() -> None:
    """Test task formatting for display."""
    task = Task(1, "Test task", priority="high")
    formatted = cli.format_task(task)
    assert "1" in formatted
    assert "Test task" in formatted


def test_cli_parser_add_command() -> None:
    """Test parser recognizes add command."""
    parser = cli.create_parser()
    args = parser.parse_args(["add", "Test task"])
    assert args.command == "add"
    assert args.description == "Test task"


def test_cli_parser_add_with_options() -> None:
    """Test parser handles add command options."""
    parser = cli.create_parser()
    args = parser.parse_args(["add", "Test", "--priority", "high", "--due-date", "2026-01-01"])
    assert args.priority == "high"
    assert args.due_date == "2026-01-01"


def test_cli_parser_list_command() -> None:
    """Test parser recognizes list command."""
    parser = cli.create_parser()
    args = parser.parse_args(["list"])
    assert args.command == "list"


def test_cli_parser_list_filters() -> None:
    """Test parser handles list filters."""
    parser = cli.create_parser()
    args = parser.parse_args(["list", "--completed", "--priority", "high"])
    assert args.completed is True
    assert args.priority == "high"


def test_cli_parser_complete_command() -> None:
    """Test parser recognizes complete command."""
    parser = cli.create_parser()
    args = parser.parse_args(["complete", "5"])
    assert args.command == "complete"
    assert args.task_id == 5


def test_cli_parser_delete_command() -> None:
    """Test parser recognizes delete command."""
    parser = cli.create_parser()
    args = parser.parse_args(["delete", "3"])
    assert args.command == "delete"
    assert args.task_id == 3


def test_cli_parser_search_command() -> None:
    """Test parser recognizes search command."""
    parser = cli.create_parser()
    args = parser.parse_args(["search", "query"])
    assert args.command == "search"
    assert args.query == "query"


# =============================================================================
# Integration Tests (2 tests)
# =============================================================================


def test_full_workflow(temp_tasks_file) -> None:
    """Test complete workflow: add, complete, delete tasks."""
    manager = TaskManager(temp_tasks_file)

    task1 = manager.add_task("Task 1", priority="high")
    task2 = manager.add_task("Task 2")

    manager.complete_task(task1.id)
    manager.delete_task(task2.id)

    assert len(manager.tasks) == 1
    assert manager.tasks[0].completed is True

    manager2 = TaskManager(temp_tasks_file)
    assert len(manager2.tasks) == 1


def test_persistence_across_sessions(temp_tasks_file) -> None:
    """Test that data persists across manager instances."""
    manager1 = TaskManager(temp_tasks_file)
    manager1.add_task("Persistent task")

    manager2 = TaskManager(temp_tasks_file)
    assert len(manager2.tasks) == 1
    assert manager2.tasks[0].description == "Persistent task"


# Total: 47 tests
