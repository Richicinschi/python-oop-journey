"""Project container for tasks.

Implement Project class with member management and task organization.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum, auto
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .task import Task
    from .user import User, Role


class ProjectStatus(Enum):
    """Project lifecycle states."""
    PLANNING = auto()
    ACTIVE = auto()
    ON_HOLD = auto()
    COMPLETED = auto()
    ARCHIVED = auto()


class Project:
    """Project containing tasks and members.
    
    Manages tasks, members with roles, and project lifecycle.
    
    TODO: Implement Project class with:
    1. Name and description attributes
    2. Owner and members dictionary (user -> role)
    3. Task collection
    4. Status workflow
    5. Methods for task and member management
    """
    
    def __init__(
        self,
        name: str,
        description: str = "",
        owner: User | None = None,
    ) -> None:
        raise NotImplementedError("Implement Project.__init__")
    
    @property
    def project_id(self) -> str:
        """Unique project identifier.
        
        TODO: Return unique ID (could be generated from name).
        """
        raise NotImplementedError("Implement project_id")
    
    # Member Management
    
    def add_member(self, user: User, role: Role) -> None:
        """Add member with role to project.
        
        TODO: Add user to members dict with role.
        Raise ValueError if user already member.
        """
        raise NotImplementedError("Implement add_member")
    
    def remove_member(self, user: User) -> None:
        """Remove member from project.
        
        TODO: Remove user from members, handle unassigning their tasks.
        """
        raise NotImplementedError("Implement remove_member")
    
    def get_member_role(self, user: User) -> Role | None:
        """Get user's role in project.
        
        TODO: Return role or None if not member.
        """
        raise NotImplementedError("Implement get_member_role")
    
    def is_member(self, user: User) -> bool:
        """Check if user is project member.
        
        TODO: Check membership.
        """
        raise NotImplementedError("Implement is_member")
    
    def get_members(self) -> list[User]:
        """Return all project members.
        
        TODO: Return list of member users.
        """
        raise NotImplementedError("Implement get_members")
    
    def get_members_by_role(self, role: Role) -> list[User]:
        """Return members with specific role.
        
        TODO: Filter members by role.
        """
        raise NotImplementedError("Implement get_members_by_role")
    
    # Task Management
    
    def add_task(self, task: Task) -> None:
        """Add task to project.
        
        TODO: Add task to collection, set task's project reference.
        """
        raise NotImplementedError("Implement add_task")
    
    def remove_task(self, task: Task) -> None:
        """Remove task from project.
        
        TODO: Remove task if present.
        """
        raise NotImplementedError("Implement remove_task")
    
    def get_task(self, task_id: str) -> Task | None:
        """Get task by ID.
        
        TODO: Find task by ID.
        """
        raise NotImplementedError("Implement get_task")
    
    def get_tasks(self) -> list[Task]:
        """Return all tasks.
        
        TODO: Return list of all tasks.
        """
        raise NotImplementedError("Implement get_tasks")
    
    def get_tasks_by_status(self, status: Any) -> list[Task]:
        """Filter tasks by status.
        
        TODO: Filter tasks by status.
        """
        raise NotImplementedError("Implement get_tasks_by_status")
    
    def get_tasks_by_priority(self, priority: Any) -> list[Task]:
        """Filter tasks by priority.
        
        TODO: Filter tasks by priority.
        """
        raise NotImplementedError("Implement get_tasks_by_priority")
    
    def get_tasks_for_user(self, user: User) -> list[Task]:
        """Get tasks assigned to user.
        
        TODO: Filter tasks by assignee.
        """
        raise NotImplementedError("Implement get_tasks_for_user")
    
    def get_overdue_tasks(self) -> list[Task]:
        """Get overdue tasks.
        
        TODO: Filter tasks where is_overdue() is True.
        """
        raise NotImplementedError("Implement get_overdue_tasks")
    
    # Status Management
    
    def activate(self) -> None:
        """Activate project.
        
        TODO: Change status to ACTIVE.
        """
        raise NotImplementedError("Implement activate")
    
    def hold(self) -> None:
        """Put project on hold.
        
        TODO: Change status to ON_HOLD.
        """
        raise NotImplementedError("Implement hold")
    
    def complete(self) -> None:
        """Mark project complete.
        
        TODO: Change status to COMPLETED.
        """
        raise NotImplementedError("Implement complete")
    
    def archive(self) -> None:
        """Archive project.
        
        TODO: Change status to ARCHIVED.
        """
        raise NotImplementedError("Implement archive")
    
    # Statistics
    
    def get_statistics(self) -> dict[str, Any]:
        """Return project statistics.
        
        TODO: Return dict with:
        - total tasks
        - tasks by status
        - tasks by priority
        - overdue count
        - member count
        """
        raise NotImplementedError("Implement get_statistics")
    
    # Serialization
    
    def to_dict(self) -> dict[str, Any]:
        """Serialize project to dictionary.
        
        TODO: Return dict with all project data.
        """
        raise NotImplementedError("Implement to_dict")
    
    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        users: dict[str, User],
        tasks: list[Task],
    ) -> Project:
        """Create Project from dictionary.
        
        TODO: Deserialize from dict, resolve user and task references.
        """
        raise NotImplementedError("Implement from_dict")
    
    def __repr__(self) -> str:
        raise NotImplementedError("Implement __repr__")
