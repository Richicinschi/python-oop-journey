"""Comprehensive tests for Task Management System.

Tests cover:
- Decorators (logging, timing, permissions, validation)
- Descriptors (email, username, validated strings, choices, datetime)
- User model and role-based permissions
- Task model with status workflows
- Project model with member and task management
- Storage with transaction support

Total: 70+ tests
"""

from __future__ import annotations

import json
import os
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path

import pytest

# Import from reference solution
from week05_oop_advanced.project.reference_solution.decorators import (
    log_operation,
    timing_decorator,
    require_permission,
    validate_types,
    singleton,
    retry_on_error,
    deprecated,
    count_calls,
)
from week05_oop_advanced.project.reference_solution.user import (
    User,
    Role,
    Permission,
    ROLE_PERMISSIONS,
)
from week05_oop_advanced.project.reference_solution.task import (
    Task,
    Priority,
    Status,
    VALID_TRANSITIONS,
)
from week05_oop_advanced.project.reference_solution.project import (
    Project,
    ProjectStatus,
)
from week05_oop_advanced.project.reference_solution.storage import (
    Storage,
    Transaction,
    StorageError,
)


# =============================================================================
# Decorator Tests
# =============================================================================

class TestLogOperationDecorator:
    """Tests for log_operation decorator."""
    
    def test_logs_function_call(self, capsys):
        """Test that function calls are logged."""
        @log_operation
        def add(a: int, b: int) -> int:
            return a + b
        
        result = add(2, 3)
        captured = capsys.readouterr()
        
        assert result == 5
        assert "[LOG] add(2, 3)" in captured.out
        assert "[LOG] add -> 5" in captured.out
    
    def test_logs_exception(self, capsys):
        """Test that exceptions are logged."""
        @log_operation
        def fail() -> None:
            raise ValueError("oops")
        
        with pytest.raises(ValueError):
            fail()
        
        captured = capsys.readouterr()
        assert "[LOG] fail" in captured.out
        assert "ValueError" in captured.out


class TestTimingDecorator:
    """Tests for timing_decorator."""
    
    def test_measures_execution_time(self, capsys):
        """Test that execution time is measured and printed."""
        @timing_decorator
        def slow_op() -> str:
            time.sleep(0.01)
            return "done"
        
        result = slow_op()
        captured = capsys.readouterr()
        
        assert result == "done"
        assert "[TIMING] slow_op took" in captured.out
        assert "seconds" in captured.out


class TestRequirePermissionDecorator:
    """Tests for require_permission decorator."""
    
    def test_allows_with_permission(self):
        """Test that permitted operations succeed."""
        class Resource:
            def __init__(self) -> None:
                self.user = User("admin", "admin@test.com", Role.ADMIN)
            
            def has_permission(self, perm: Permission) -> bool:
                return self.user.has_permission(perm)
            
            @require_permission("CREATE_TASK")
            def create(self) -> str:
                return "created"
        
        r = Resource()
        assert r.create() == "created"
    
    def test_denies_without_permission(self):
        """Test that unpermitted operations raise PermissionError."""
        class Resource:
            def __init__(self) -> None:
                self.user = User("viewer", "view@test.com", Role.VIEWER)
            
            def has_permission(self, perm: Permission) -> bool:
                return self.user.has_permission(perm)
            
            @require_permission("CREATE_TASK")
            def create(self) -> str:
                return "created"
        
        r = Resource()
        with pytest.raises(PermissionError):
            r.create()


class TestValidateTypesDecorator:
    """Tests for validate_types decorator."""
    
    def test_validates_correct_types(self):
        """Test that correct types pass validation."""
        @validate_types(name=str, age=int)
        def greet(name: str, age: int) -> str:
            return f"Hello {name}, age {age}"
        
        assert greet("Alice", 30) == "Hello Alice, age 30"
    
    def test_rejects_wrong_types(self):
        """Test that wrong types raise TypeError."""
        @validate_types(name=str, age=int)
        def greet(name: str, age: int) -> str:
            return f"Hello {name}, age {age}"
        
        with pytest.raises(TypeError) as exc_info:
            greet("Alice", "thirty")
        assert "age" in str(exc_info.value)
        assert "int" in str(exc_info.value)


class TestSingletonDecorator:
    """Tests for singleton decorator."""
    
    def test_returns_same_instance(self):
        """Test that singleton returns same instance."""
        @singleton
        class Database:
            def __init__(self) -> None:
                self.id = id(self)
        
        db1 = Database()
        db2 = Database()
        
        assert db1 is db2
        assert db1.id == db2.id


class TestRetryOnErrorDecorator:
    """Tests for retry_on_error decorator."""
    
    def test_succeeds_after_retries(self):
        """Test that operation succeeds after retries."""
        call_count = 0
        
        @retry_on_error(max_attempts=3, delay=0.01)
        def flaky() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RuntimeError("fail")
            return "success"
        
        result = flaky()
        assert result == "success"
        assert call_count == 3
    
    def test_raises_after_max_attempts(self):
        """Test that exception is raised after max attempts."""
        @retry_on_error(max_attempts=2, delay=0.01)
        def always_fail() -> None:
            raise RuntimeError("always fails")
        
        with pytest.raises(RuntimeError, match="always fails"):
            always_fail()


class TestDeprecatedDecorator:
    """Tests for deprecated decorator."""
    
    def test_emits_deprecation_warning(self):
        """Test that deprecated function emits warning."""
        @deprecated("Use new_function instead")
        def old_function() -> str:
            return "result"
        
        with pytest.warns(DeprecationWarning, match="old_function is deprecated"):
            result = old_function()
        
        assert result == "result"


class TestCountCallsDecorator:
    """Tests for count_calls decorator."""
    
    def test_counts_calls(self):
        """Test that calls are counted."""
        @count_calls
        def my_func() -> None:
            pass
        
        assert my_func.call_count == 0
        my_func()
        assert my_func.call_count == 1
        my_func()
        my_func()
        assert my_func.call_count == 3


# =============================================================================
# User Model Tests
# =============================================================================

class TestUserEmailDescriptor:
    """Tests for ValidatedEmail descriptor."""
    
    def test_accepts_valid_email(self):
        """Test that valid email is accepted."""
        user = User("alice", "alice@example.com")
        assert user.email == "alice@example.com"
    
    def test_rejects_email_without_at(self):
        """Test that email without @ is rejected."""
        with pytest.raises(ValueError, match="@"):
            User("alice", "invalid-email")
    
    def test_rejects_email_without_domain(self):
        """Test that email without domain is rejected."""
        with pytest.raises(ValueError, match="domain"):
            User("alice", "alice@")
    
    def test_rejects_email_without_local(self):
        """Test that email without local part is rejected."""
        with pytest.raises(ValueError, match="local"):
            User("alice", "@example.com")
    
    def test_converts_to_lowercase(self):
        """Test that email is converted to lowercase."""
        user = User("alice", "ALICE@EXAMPLE.COM")
        assert user.email == "alice@example.com"


class TestUserUsernameDescriptor:
    """Tests for ValidatedUsername descriptor."""
    
    def test_accepts_valid_username(self):
        """Test that valid username is accepted."""
        user = User("alice_smith", "alice@test.com")
        assert user.username == "alice_smith"
    
    def test_rejects_short_username(self):
        """Test that short username is rejected."""
        with pytest.raises(ValueError, match="at least"):
            User("ab", "ab@test.com")
    
    def test_rejects_long_username(self):
        """Test that long username is rejected."""
        with pytest.raises(ValueError, match="at most"):
            User("a" * 31, "test@test.com")
    
    def test_rejects_invalid_characters(self):
        """Test that username with invalid chars is rejected."""
        with pytest.raises(ValueError, match="letters, numbers"):
            User("alice@smith", "test@test.com")
    
    def test_converts_to_lowercase(self):
        """Test that username is converted to lowercase."""
        user = User("ALICE", "alice@test.com")
        assert user.username == "alice"


class TestUserPermissions:
    """Tests for role-based permissions."""
    
    def test_admin_has_all_permissions(self):
        """Test that admin has all permissions."""
        admin = User("admin", "admin@test.com", Role.ADMIN)
        for perm in Permission:
            assert admin.has_permission(perm)
    
    def test_manager_has_correct_permissions(self):
        """Test that manager has expected permissions."""
        manager = User("mgr", "mgr@test.com", Role.MANAGER)
        assert manager.has_permission(Permission.CREATE_PROJECT)
        assert manager.has_permission(Permission.ASSIGN_TASK)
        assert not manager.has_permission(Permission.DELETE_PROJECT)
    
    def test_member_has_limited_permissions(self):
        """Test that member has limited permissions."""
        member = User("mem", "mem@test.com", Role.MEMBER)
        assert member.has_permission(Permission.CREATE_TASK)
        assert member.has_permission(Permission.VIEW_ALL)
        assert not member.has_permission(Permission.ASSIGN_TASK)
        assert not member.has_permission(Permission.DELETE_TASK)
    
    def test_viewer_has_readonly_permissions(self):
        """Test that viewer has only view permission."""
        viewer = User("view", "view@test.com", Role.VIEWER)
        assert viewer.has_permission(Permission.VIEW_ALL)
        assert not viewer.has_permission(Permission.CREATE_TASK)


class TestUserSerialization:
    """Tests for user serialization."""
    
    def test_to_dict(self):
        """Test that user serializes to dict correctly."""
        user = User("alice", "alice@test.com", Role.MANAGER)
        data = user.to_dict()
        
        assert data["username"] == "alice"
        assert data["email"] == "alice@test.com"
        assert data["role"] == "MANAGER"
    
    def test_from_dict(self):
        """Test that user deserializes from dict correctly."""
        data = {"username": "bob", "email": "bob@test.com", "role": "MEMBER"}
        user = User.from_dict(data)
        
        assert user.username == "bob"
        assert user.email == "bob@test.com"
        assert user.role == Role.MEMBER
    
    def test_equality(self):
        """Test that users are equal by username."""
        u1 = User("alice", "a@test.com", Role.ADMIN)
        u2 = User("alice", "b@test.com", Role.MEMBER)
        u3 = User("bob", "c@test.com", Role.ADMIN)
        
        assert u1 == u2
        assert u1 != u3


# =============================================================================
# Task Model Tests
# =============================================================================

class TestTaskDescriptors:
    """Tests for Task descriptor validation."""
    
    def test_validates_title_length(self):
        """Test that title length is validated."""
        Task("Valid Title")  # Should succeed
        
        with pytest.raises(ValueError, match="at least"):
            Task("AB")  # Too short
        
        with pytest.raises(ValueError, match="at most"):
            Task("A" * 101)  # Too long
    
    def test_validates_description_length(self):
        """Test that description length is validated."""
        task = Task("Title", description="A" * 1000)  # Max length
        assert len(task.description) == 1000
        
        with pytest.raises(ValueError, match="at most"):
            Task("Title", description="A" * 1001)  # Too long
    
    def test_validates_priority(self):
        """Test that priority is validated."""
        task = Task("Title", priority=Priority.HIGH)
        assert task.priority == Priority.HIGH
        
        task.priority = "LOW"
        assert task.priority == Priority.LOW
    
    def test_validates_deadline(self):
        """Test that deadline accepts datetime or ISO string."""
        dt = datetime(2024, 12, 31, 23, 59)
        task = Task("Title", deadline=dt)
        assert task.deadline == dt
        
        task2 = Task("Title", deadline="2024-12-31T23:59:00")
        assert task2.deadline.year == 2024


class TestTaskStatusWorkflow:
    """Tests for task status transitions."""
    
    def test_valid_transitions(self):
        """Test that valid transitions work."""
        task = Task("Test")
        assert task.status == Status.BACKLOG
        
        task.transition_to(Status.TODO)
        assert task.status == Status.TODO
        
        task.transition_to(Status.IN_PROGRESS)
        assert task.status == Status.IN_PROGRESS
        
        task.transition_to(Status.REVIEW)
        assert task.status == Status.REVIEW
        
        task.transition_to(Status.DONE)
        assert task.status == Status.DONE
    
    def test_invalid_transition_raises(self):
        """Test that invalid transitions raise error."""
        task = Task("Test")
        task.transition_to(Status.TODO)
        
        with pytest.raises(ValueError, match="Cannot transition"):
            task.transition_to(Status.DONE)  # Can't skip IN_PROGRESS/REVIEW
    
    def test_terminal_states(self):
        """Test that terminal states have no outgoing transitions."""
        done_task = Task("Done Task")
        done_task.transition_to(Status.TODO)
        done_task.transition_to(Status.IN_PROGRESS)
        done_task.transition_to(Status.REVIEW)
        done_task.transition_to(Status.DONE)
        
        assert len(VALID_TRANSITIONS[Status.DONE]) == 0
        
        with pytest.raises(ValueError):
            done_task.transition_to(Status.BACKLOG)
    
    def test_start_progress_shortcut(self):
        """Test start_progress shortcut method."""
        task = Task("Test")
        task.start_progress()
        assert task.status == Status.IN_PROGRESS
    
    def test_complete_shortcut_for_normal_priority(self):
        """Test complete shortcut for non-critical tasks."""
        task = Task("Test", priority=Priority.MEDIUM)
        task.transition_to(Status.TODO)
        task.transition_to(Status.IN_PROGRESS)
        task.transition_to(Status.REVIEW)
        task.complete()
        assert task.status == Status.DONE
    
    def test_complete_shortcut_for_critical_priority(self):
        """Test that critical tasks must go through review."""
        task = Task("Critical", priority=Priority.CRITICAL)
        task.start_progress()
        
        # Should go to REVIEW first
        assert task.status == Status.IN_PROGRESS
        task.complete()
        assert task.status == Status.REVIEW
        
        # Now can complete
        task.complete()
        assert task.status == Status.DONE
    
    def test_cancel_works_from_non_terminal(self):
        """Test that cancel works from non-terminal states."""
        task = Task("Test")
        task.transition_to(Status.TODO)
        task.transition_to(Status.IN_PROGRESS)
        task.cancel()
        assert task.status == Status.CANCELLED
    
    def test_cannot_cancel_terminal_task(self):
        """Test that cancel fails on terminal tasks."""
        task = Task("Test")
        task.transition_to(Status.TODO)
        task.transition_to(Status.IN_PROGRESS)
        task.transition_to(Status.REVIEW)
        task.transition_to(Status.DONE)
        
        with pytest.raises(ValueError, match="Cannot cancel"):
            task.cancel()


class TestTaskAssignment:
    """Tests for task assignment."""
    
    def test_assign_to_user(self):
        """Test that task can be assigned to user."""
        task = Task("Test")
        user = User("alice", "alice@test.com")
        
        task.assign_to(user)
        assert task.assignee == user
    
    def test_unassign_removes_user(self):
        """Test that unassign removes assignee."""
        task = Task("Test")
        user = User("alice", "alice@test.com")
        
        task.assign_to(user)
        task.unassign()
        assert task.assignee is None


class TestTaskTags:
    """Tests for task tags."""
    
    def test_add_tag(self):
        """Test that tags can be added."""
        task = Task("Test")
        task.add_tag("urgent")
        assert "urgent" in task.tags
    
    def test_add_tag_normalizes_case(self):
        """Test that tags are normalized to lowercase."""
        task = Task("Test")
        task.add_tag("URGENT")
        assert "urgent" in task.tags
    
    def test_remove_tag(self):
        """Test that tags can be removed."""
        task = Task("Test")
        task.add_tag("urgent")
        task.remove_tag("urgent")
        assert "urgent" not in task.tags
    
    def test_rejects_empty_tag(self):
        """Test that empty tags are rejected."""
        task = Task("Test")
        with pytest.raises(ValueError):
            task.add_tag("")


class TestTaskOverdue:
    """Tests for overdue detection."""
    
    def test_overdue_when_past_deadline(self):
        """Test that task is overdue when past deadline."""
        past = datetime.now() - timedelta(days=1)
        task = Task("Late", deadline=past)
        assert task.is_overdue()
    
    def test_not_overdue_when_before_deadline(self):
        """Test that task is not overdue when before deadline."""
        future = datetime.now() + timedelta(days=1)
        task = Task("Future", deadline=future)
        assert not task.is_overdue()
    
    def test_not_overdue_when_no_deadline(self):
        """Test that task without deadline is not overdue."""
        task = Task("No deadline")
        assert not task.is_overdue()
    
    def test_not_overdue_when_done(self):
        """Test that done tasks are not overdue."""
        past = datetime.now() - timedelta(days=1)
        task = Task("Done Late", deadline=past)
        task.transition_to(Status.TODO)
        task.transition_to(Status.IN_PROGRESS)
        task.transition_to(Status.REVIEW)
        task.transition_to(Status.DONE)
        assert not task.is_overdue()


class TestTaskSerialization:
    """Tests for task serialization."""
    
    def test_to_dict(self):
        """Test that task serializes to dict."""
        task = Task("Test Task", priority=Priority.HIGH)
        task.add_tag("test")
        
        data = task.to_dict()
        
        assert data["title"] == "Test Task"
        assert data["priority"] == "HIGH"
        assert "test" in data["tags"]
        assert "task_id" in data
    
    def test_from_dict(self):
        """Test that task deserializes from dict."""
        data = {
            "task_id": "abc123",
            "title": "Test",
            "description": "Description",
            "priority": "MEDIUM",
            "status": "TODO",
            "deadline": None,
            "assignee": None,
            "tags": ["tag1"],
            "created_at": datetime.now().isoformat(),
            "modified_at": datetime.now().isoformat(),
        }
        
        task = Task.from_dict(data)
        assert task.task_id == "abc123"
        assert task.title == "Test"


# =============================================================================
# Project Model Tests
# =============================================================================

class TestProjectCreation:
    """Tests for project creation."""
    
    def test_create_project(self):
        """Test that project can be created."""
        owner = User("owner", "owner@test.com", Role.ADMIN)
        project = Project("My Project", "Description", owner)
        
        assert project.name == "My Project"
        assert project.description == "Description"
        assert project.owner == owner
        assert project.status == ProjectStatus.PLANNING
    
    def test_owner_added_as_member(self):
        """Test that owner is automatically added as member."""
        owner = User("owner", "owner@test.com", Role.ADMIN)
        project = Project("Test", owner=owner)
        
        assert owner in project.get_members()
        assert project.get_member_role(owner) == Role.ADMIN


class TestProjectMembers:
    """Tests for project member management."""
    
    def test_add_member(self):
        """Test that members can be added."""
        owner = User("owner", "owner@test.com", Role.ADMIN)
        project = Project("Test", owner=owner)
        
        member = User("member", "member@test.com", Role.MEMBER)
        project.add_member(member, Role.MEMBER)
        
        assert member in project.get_members()
        assert project.get_member_role(member) == Role.MEMBER
    
    def test_cannot_add_duplicate_member(self):
        """Test that duplicate members are rejected."""
        owner = User("owner", "owner@test.com", Role.ADMIN)
        project = Project("Test", owner=owner)
        
        with pytest.raises(ValueError, match="already a member"):
            project.add_member(owner, Role.MANAGER)
    
    def test_remove_member(self):
        """Test that members can be removed."""
        owner = User("owner", "owner@test.com", Role.ADMIN)
        project = Project("Test", owner=owner)
        
        member = User("member", "member@test.com", Role.MEMBER)
        project.add_member(member, Role.MEMBER)
        project.remove_member(member)
        
        assert member not in project.get_members()
    
    def test_cannot_remove_owner(self):
        """Test that owner cannot be removed."""
        owner = User("owner", "owner@test.com", Role.ADMIN)
        project = Project("Test", owner=owner)
        
        with pytest.raises(ValueError, match="Cannot remove"):
            project.remove_member(owner)
    
    def test_get_members_by_role(self):
        """Test filtering members by role."""
        owner = User("owner", "owner@test.com", Role.ADMIN)
        project = Project("Test", owner=owner)
        
        mgr1 = User("mgr1", "m1@test.com", Role.MANAGER)
        mgr2 = User("mgr2", "m2@test.com", Role.MANAGER)
        project.add_member(mgr1, Role.MANAGER)
        project.add_member(mgr2, Role.MANAGER)
        
        managers = project.get_members_by_role(Role.MANAGER)
        assert len(managers) == 2
        assert mgr1 in managers
        assert mgr2 in managers


class TestProjectTasks:
    """Tests for project task management."""
    
    def test_add_task(self):
        """Test that tasks can be added to project."""
        owner = User("owner", "owner@test.com")
        project = Project("Test", owner=owner)
        
        task = Task("Task 1")
        project.add_task(task)
        
        assert task in project.get_tasks()
    
    def test_remove_task(self):
        """Test that tasks can be removed from project."""
        owner = User("owner", "owner@test.com")
        project = Project("Test", owner=owner)
        
        task = Task("Task 1")
        project.add_task(task)
        project.remove_task(task)
        
        assert task not in project.get_tasks()
    
    def test_get_task_by_id(self):
        """Test retrieving task by ID."""
        owner = User("owner", "owner@test.com")
        project = Project("Test", owner=owner)
        
        task = Task("Task 1")
        project.add_task(task)
        
        retrieved = project.get_task(task.task_id)
        assert retrieved == task
    
    def test_get_tasks_by_status(self):
        """Test filtering tasks by status."""
        owner = User("owner", "owner@test.com")
        project = Project("Test", owner=owner)
        
        task1 = Task("Task 1")
        task2 = Task("Task 2")
        task2.start_progress()
        
        project.add_task(task1)
        project.add_task(task2)
        
        todo_tasks = project.get_tasks_by_status(Status.BACKLOG)
        assert task1 in todo_tasks
        assert task2 not in todo_tasks
    
    def test_get_tasks_by_priority(self):
        """Test filtering tasks by priority."""
        owner = User("owner", "owner@test.com")
        project = Project("Test", owner=owner)
        
        task1 = Task("Low", priority=Priority.LOW)
        task2 = Task("High", priority=Priority.HIGH)
        
        project.add_task(task1)
        project.add_task(task2)
        
        high_tasks = project.get_tasks_by_priority(Priority.HIGH)
        assert task2 in high_tasks
        assert task1 not in high_tasks
    
    def test_get_tasks_for_user(self):
        """Test getting tasks assigned to user."""
        owner = User("owner", "owner@test.com")
        member = User("member", "member@test.com")
        project = Project("Test", owner=owner)
        
        task = Task("Assigned")
        task.assign_to(member)
        project.add_task(task)
        
        member_tasks = project.get_tasks_for_user(member)
        assert task in member_tasks
    
    def test_get_overdue_tasks(self):
        """Test getting overdue tasks."""
        owner = User("owner", "owner@test.com")
        project = Project("Test", owner=owner)
        
        past = datetime.now() - timedelta(days=1)
        overdue_task = Task("Overdue", deadline=past)
        current_task = Task("Current")
        
        project.add_task(overdue_task)
        project.add_task(current_task)
        
        overdue = project.get_overdue_tasks()
        assert overdue_task in overdue
        assert current_task not in overdue


class TestProjectStatus:
    """Tests for project status management."""
    
    def test_activate_project(self):
        """Test activating a project."""
        owner = User("owner", "owner@test.com")
        project = Project("Test", owner=owner)
        
        project.activate()
        assert project.status == ProjectStatus.ACTIVE
    
    def test_hold_project(self):
        """Test putting project on hold."""
        owner = User("owner", "owner@test.com")
        project = Project("Test", owner=owner)
        
        project.hold()
        assert project.status == ProjectStatus.ON_HOLD
    
    def test_complete_project(self):
        """Test completing a project."""
        owner = User("owner", "owner@test.com")
        project = Project("Test", owner=owner)
        
        project.complete()
        assert project.status == ProjectStatus.COMPLETED
    
    def test_archive_project(self):
        """Test archiving a project."""
        owner = User("owner", "owner@test.com")
        project = Project("Test", owner=owner)
        
        project.archive()
        assert project.status == ProjectStatus.ARCHIVED


class TestProjectStatistics:
    """Tests for project statistics."""
    
    def test_statistics(self):
        """Test that statistics are calculated correctly."""
        owner = User("owner", "owner@test.com")
        project = Project("Test", owner=owner)
        
        task1 = Task("Task 1", priority=Priority.HIGH)
        task2 = Task("Task 2", priority=Priority.LOW)
        task2.start_progress()
        
        project.add_task(task1)
        project.add_task(task2)
        
        stats = project.get_statistics()
        
        assert stats["total_tasks"] == 2
        assert stats["by_priority"]["HIGH"] == 1
        assert stats["by_priority"]["LOW"] == 1
        assert stats["by_status"]["BACKLOG"] == 1
        assert stats["by_status"]["IN_PROGRESS"] == 1
        assert stats["member_count"] == 1


# =============================================================================
# Storage Tests
# =============================================================================

def _get_test_dir():
    """Get a test directory that works on Windows."""
    test_dir = Path(tempfile.gettempdir()) / "task_system_tests"
    test_dir.mkdir(exist_ok=True)
    return test_dir


class TestStorageBasics:
    """Tests for basic storage operations."""
    
    def test_exists_when_file_missing(self):
        """Test exists returns False when file missing."""
        test_dir = _get_test_dir()
        storage = Storage(test_dir / "nonexistent.json")
        assert not storage.exists()
    
    def test_exists_when_file_present(self):
        """Test exists returns True when file exists."""
        test_dir = _get_test_dir()
        filepath = test_dir / "data.json"
        filepath.write_text("{}")
        storage = Storage(filepath)
        assert storage.exists()
        filepath.unlink()
    
    def test_save_and_load(self):
        """Test saving and loading data."""
        test_dir = _get_test_dir()
        filepath = test_dir / "save_load.json"
        
        # Clean up any existing file
        if filepath.exists():
            filepath.unlink()
        
        storage = Storage(filepath)
        
        user = User("alice", "alice@test.com", Role.ADMIN)
        owner = User("owner", "owner@test.com", Role.ADMIN)
        project = Project("Test", owner=owner)
        
        storage.save([project], [user, owner])
        
        loaded_projects, loaded_users = storage.load()
        
        assert len(loaded_projects) == 1
        assert len(loaded_users) == 2
        assert loaded_users[0].username == "alice"
        
        filepath.unlink()
    
    def test_load_or_init_creates_empty(self):
        """Test load_or_init returns empty when no file."""
        test_dir = _get_test_dir()
        filepath = test_dir / "new.json"
        if filepath.exists():
            filepath.unlink()
        
        storage = Storage(filepath)
        projects, users = storage.load_or_init()
        
        assert projects == []
        assert users == []
    
    def test_load_raises_when_missing(self):
        """Test load raises error when file missing."""
        test_dir = _get_test_dir()
        filepath = test_dir / "missing.json"
        if filepath.exists():
            filepath.unlink()
        
        storage = Storage(filepath)
        
        with pytest.raises(StorageError, match="not found"):
            storage.load()


class TestStorageBackup:
    """Tests for storage backup."""
    
    def test_backup_creates_file(self):
        """Test backup creates backup file."""
        test_dir = _get_test_dir()
        filepath = test_dir / "backup_test.json"
        filepath.write_text('{"version": "1.0"}')
        
        storage = Storage(filepath)
        backup_path = storage.backup()
        
        assert Path(backup_path).exists()
        
        # Cleanup
        filepath.unlink()
        Path(backup_path).unlink()
    
    def test_backup_raises_when_no_file(self):
        """Test backup raises when no file to backup."""
        test_dir = _get_test_dir()
        storage = Storage(test_dir / "missing_for_backup.json")
        
        with pytest.raises(StorageError, match="Cannot backup"):
            storage.backup()


class TestStorageClear:
    """Tests for storage clear."""
    
    def test_clear_removes_file(self):
        """Test clear removes storage file."""
        test_dir = _get_test_dir()
        filepath = test_dir / "clear_test.json"
        filepath.write_text("{}")
        
        storage = Storage(filepath)
        storage.clear()
        
        assert not filepath.exists()


class TestTransaction:
    """Tests for transaction support."""
    
    def test_transaction_saves_on_success(self):
        """Test transaction commits on success."""
        test_dir = _get_test_dir()
        filepath = test_dir / "txn_success.json"
        if filepath.exists():
            filepath.unlink()
        
        storage = Storage(filepath)
        owner = User("owner", "owner@test.com", Role.ADMIN)
        project = Project("Test", owner=owner)
        
        with storage.transaction() as txn:
            txn.save_project(project)
            txn.save_user(owner)
        
        # Verify saved
        projects, users = storage.load()
        assert len(projects) == 1
        assert len(users) == 1
        
        filepath.unlink()
    
    def test_transaction_rolls_back_on_error(self):
        """Test transaction does not save on error."""
        test_dir = _get_test_dir()
        filepath = test_dir / "txn_rollback.json"
        if filepath.exists():
            filepath.unlink()
        
        storage = Storage(filepath)
        owner = User("owner", "owner@test.com", Role.ADMIN)
        project = Project("Test", owner=owner)
        
        try:
            with storage.transaction() as txn:
                txn.save_project(project)
                txn.save_user(owner)
                raise ValueError("Intentional error")
        except ValueError:
            pass
        
        # Verify not saved
        assert not storage.exists()
    
    def test_transaction_get_projects(self):
        """Test getting projects from transaction."""
        test_dir = _get_test_dir()
        filepath = test_dir / "txn_get.json"
        if filepath.exists():
            filepath.unlink()
        
        storage = Storage(filepath)
        owner = User("owner", "owner@test.com", Role.ADMIN)
        project = Project("Test", owner=owner)
        
        with storage.transaction() as txn:
            txn.save_project(project)
            projects = txn.get_projects()
            assert len(projects) == 1
    
    def test_transaction_delete_project(self):
        """Test deleting project in transaction."""
        test_dir = _get_test_dir()
        filepath = test_dir / "txn_delete.json"
        if filepath.exists():
            filepath.unlink()
        
        storage = Storage(filepath)
        owner = User("owner", "owner@test.com", Role.ADMIN)
        project = Project("Test", owner=owner)
        
        # First save
        with storage.transaction() as txn:
            txn.save_project(project)
            txn.save_user(owner)
        
        # Then delete
        with storage.transaction() as txn:
            txn.delete_project(project.project_id)
        
        projects, _ = storage.load()
        assert len(projects) == 0
        
        filepath.unlink()
