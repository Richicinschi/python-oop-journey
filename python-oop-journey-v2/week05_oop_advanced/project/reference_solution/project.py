"""Project container for tasks.

Reference implementation with member management and task organization.
"""

from __future__ import annotations

import uuid
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
    """Project containing tasks and members."""
    
    def __init__(
        self,
        name: str,
        description: str = "",
        owner: User | None = None,
    ) -> None:
        self._project_id = str(uuid.uuid4())[:8]
        self.name = name
        self.description = description
        self._owner = owner
        self._members: dict[User, Role] = {}
        self._tasks: dict[str, Task] = {}
        self.status = ProjectStatus.PLANNING
        self.created_at = datetime.now()
        self.modified_at = self.created_at
        
        # Add owner as member if provided
        if owner:
            from .user import Role
            self._members[owner] = Role.ADMIN
    
    @property
    def project_id(self) -> str:
        """Unique project identifier."""
        return self._project_id
    
    @property
    def owner(self) -> User | None:
        """Project owner."""
        return self._owner
    
    # Member Management
    
    def add_member(self, user: User, role: Role) -> None:
        """Add member with role to project."""
        if user in self._members:
            raise ValueError(f"User {user.username} is already a member")
        self._members[user] = role
        self._touch()
    
    def remove_member(self, user: User) -> None:
        """Remove member from project."""
        if user == self._owner:
            raise ValueError("Cannot remove project owner")
        if user not in self._members:
            raise ValueError(f"User {user.username} is not a member")
        
        # Unassign user's tasks
        for task in self._tasks.values():
            if task.assignee == user:
                task.unassign()
        
        del self._members[user]
        self._touch()
    
    def get_member_role(self, user: User) -> Role | None:
        """Get user's role in project."""
        return self._members.get(user)
    
    def is_member(self, user: User) -> bool:
        """Check if user is project member."""
        return user in self._members
    
    def get_members(self) -> list[User]:
        """Return all project members."""
        return list(self._members.keys())
    
    def get_members_by_role(self, role: Role) -> list[User]:
        """Return members with specific role."""
        return [user for user, r in self._members.items() if r == role]
    
    # Task Management
    
    def add_task(self, task: Task) -> None:
        """Add task to project."""
        self._tasks[task.task_id] = task
        self._touch()
    
    def remove_task(self, task: Task) -> None:
        """Remove task from project."""
        if task.task_id in self._tasks:
            del self._tasks[task.task_id]
            self._touch()
    
    def get_task(self, task_id: str) -> Task | None:
        """Get task by ID."""
        return self._tasks.get(task_id)
    
    def get_tasks(self) -> list[Task]:
        """Return all tasks."""
        return list(self._tasks.values())
    
    def get_tasks_by_status(self, status: Any) -> list[Task]:
        """Filter tasks by status."""
        from .task import Status
        if isinstance(status, str):
            status = Status[status]
        return [t for t in self._tasks.values() if t.status == status]
    
    def get_tasks_by_priority(self, priority: Any) -> list[Task]:
        """Filter tasks by priority."""
        from .task import Priority
        if isinstance(priority, str):
            priority = Priority[priority]
        return [t for t in self._tasks.values() if t.priority == priority]
    
    def get_tasks_for_user(self, user: User) -> list[Task]:
        """Get tasks assigned to user."""
        return [t for t in self._tasks.values() if t.assignee == user]
    
    def get_overdue_tasks(self) -> list[Task]:
        """Get overdue tasks."""
        return [t for t in self._tasks.values() if t.is_overdue()]
    
    # Status Management
    
    def activate(self) -> None:
        """Activate project."""
        self.status = ProjectStatus.ACTIVE
        self._touch()
    
    def hold(self) -> None:
        """Put project on hold."""
        self.status = ProjectStatus.ON_HOLD
        self._touch()
    
    def complete(self) -> None:
        """Mark project complete."""
        self.status = ProjectStatus.COMPLETED
        self._touch()
    
    def archive(self) -> None:
        """Archive project."""
        self.status = ProjectStatus.ARCHIVED
        self._touch()
    
    def _touch(self) -> None:
        """Update modified timestamp."""
        self.modified_at = datetime.now()
    
    # Statistics
    
    def get_statistics(self) -> dict[str, Any]:
        """Return project statistics."""
        from .task import Status, Priority
        
        tasks = list(self._tasks.values())
        
        by_status = {}
        for status in Status:
            count = len([t for t in tasks if t.status == status])
            by_status[status.name] = count
        
        by_priority = {}
        for priority in Priority:
            count = len([t for t in tasks if t.priority == priority])
            by_priority[priority.name] = count
        
        return {
            "total_tasks": len(tasks),
            "by_status": by_status,
            "by_priority": by_priority,
            "overdue": len([t for t in tasks if t.is_overdue()]),
            "member_count": len(self._members),
        }
    
    # Serialization
    
    def to_dict(self) -> dict[str, Any]:
        """Serialize project to dictionary."""
        return {
            "project_id": self._project_id,
            "name": self.name,
            "description": self.description,
            "owner": self._owner.username if self._owner else None,
            "members": {
                user.username: role.name for user, role in self._members.items()
            },
            "tasks": [t.to_dict() for t in self._tasks.values()],
            "status": self.status.name,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
        }
    
    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        users: dict[str, User],
        tasks: list[Task] | None = None,
    ) -> Project:
        """Create Project from dictionary."""
        # Resolve owner
        owner_username = data.get("owner")
        owner = users.get(owner_username) if owner_username else None
        
        project = cls.__new__(cls)
        project._project_id = data["project_id"]
        project.name = data["name"]
        project.description = data.get("description", "")
        project._owner = owner
        project.status = ProjectStatus[data["status"]]
        project.created_at = datetime.fromisoformat(data["created_at"])
        project.modified_at = datetime.fromisoformat(data["modified_at"])
        
        # Resolve members
        project._members = {}
        from .user import Role
        for username, role_name in data.get("members", {}).items():
            user = users.get(username)
            if user:
                project._members[user] = Role[role_name]
        
        # Add tasks
        project._tasks = {}
        task_list = tasks if tasks else []
        for task_data in data.get("tasks", []):
            task = Task.from_dict(task_data, users)
            project._tasks[task.task_id] = task
        
        return project
    
    def __repr__(self) -> str:
        return f"Project({self._project_id!r}, name={self.name!r}, status={self.status.name})"
