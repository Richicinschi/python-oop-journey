"""Data persistence layer.

Reference implementation of JSON-based storage with transaction support.
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generator

if TYPE_CHECKING:
    from .project import Project
    from .user import User


class StorageError(Exception):
    """Base exception for storage operations."""
    pass


class Storage:
    """JSON file-based storage for projects, tasks, and users."""
    
    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath)
        self._ensure_dir()
    
    def _ensure_dir(self) -> None:
        """Ensure parent directory exists."""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
    
    def exists(self) -> bool:
        """Check if storage file exists."""
        return self.filepath.exists()
    
    def save(
        self,
        projects: list[Project],
        users: list[User],
    ) -> None:
        """Save all data to file atomically."""
        data = {
            "version": "1.0",
            "projects": [p.to_dict() for p in projects],
            "users": [u.to_dict() for u in users],
        }
        
        # Write to temp file then rename for atomicity
        temp_fd, temp_path = tempfile.mkstemp(
            dir=self.filepath.parent,
            prefix=".tmp_",
            suffix=".json",
        )
        try:
            with os.fdopen(temp_fd, "w") as f:
                json.dump(data, f, indent=2)
            # Atomic rename
            shutil.move(temp_path, self.filepath)
        except Exception:
            # Clean up temp file on error
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise
    
    def load(self) -> tuple[list[Project], list[User]]:
        """Load all data from file."""
        if not self.exists():
            raise StorageError(f"Storage file not found: {self.filepath}")
        
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise StorageError(f"Invalid JSON in storage file: {e}")
        except Exception as e:
            raise StorageError(f"Failed to read storage file: {e}")
        
        # Deserialize users first (needed for project/task references)
        from .user import User
        users_data = data.get("users", [])
        users = [User.from_dict(u) for u in users_data]
        users_by_name = {u.username: u for u in users}
        
        # Deserialize projects
        from .project import Project
        projects_data = data.get("projects", [])
        projects = [Project.from_dict(p, users_by_name) for p in projects_data]
        
        return (projects, users)
    
    def load_or_init(self) -> tuple[list[Project], list[User]]:
        """Load data or return empty collections."""
        if self.exists():
            return self.load()
        return ([], [])
    
    def backup(self, backup_path: str | Path | None = None) -> str:
        """Create backup of current data file."""
        if not self.exists():
            raise StorageError("Cannot backup: storage file does not exist")
        
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.filepath.with_suffix(f".backup_{timestamp}.json")
        
        backup_path = Path(backup_path)
        shutil.copy2(self.filepath, backup_path)
        return str(backup_path)
    
    def clear(self) -> None:
        """Delete storage file if exists."""
        if self.filepath.exists():
            self.filepath.unlink()
    
    @contextmanager
    def transaction(
        self,
    ) -> Generator[Transaction, None, None]:
        """Context manager for atomic storage operations."""
        txn = Transaction(self)
        try:
            yield txn
            # Commit on successful exit
            txn.commit()
        except Exception:
            # Rollback (don't save) on exception
            raise


class Transaction:
    """Transaction object for batch operations."""
    
    def __init__(self, storage: Storage) -> None:
        self._storage = storage
        # Load current state
        self._projects, self._users = storage.load_or_init()
        
        # Create lookup dicts
        self._projects_by_id: dict[str, Project] = {
            p.project_id: p for p in self._projects
        }
        self._users_by_name: dict[str, User] = {
            u.username: u for u in self._users
        }
        
        # Track deletions
        self._deleted_projects: set[str] = set()
        self._deleted_users: set[str] = set()
    
    def save_project(self, project: Project) -> None:
        """Queue project for saving."""
        self._projects_by_id[project.project_id] = project
        self._deleted_projects.discard(project.project_id)
    
    def delete_project(self, project_id: str) -> None:
        """Queue project for deletion."""
        self._deleted_projects.add(project_id)
        if project_id in self._projects_by_id:
            del self._projects_by_id[project_id]
    
    def save_user(self, user: User) -> None:
        """Queue user for saving."""
        self._users_by_name[user.username] = user
        self._deleted_users.discard(user.username)
    
    def delete_user(self, username: str) -> None:
        """Queue user for deletion."""
        self._deleted_users.add(username)
        if username in self._users_by_name:
            del self._users_by_name[username]
    
    def commit(self) -> None:
        """Apply all queued changes to storage."""
        projects = list(self._projects_by_id.values())
        users = list(self._users_by_name.values())
        self._storage.save(projects, users)
    
    def get_projects(self) -> list[Project]:
        """Get current projects including pending changes."""
        return list(self._projects_by_id.values())
    
    def get_users(self) -> list[User]:
        """Get current users including pending changes."""
        return list(self._users_by_name.values())
    
    def get_project(self, project_id: str) -> Project | None:
        """Get project by ID."""
        return self._projects_by_id.get(project_id)
    
    def get_user(self, username: str) -> User | None:
        """Get user by username."""
        return self._users_by_name.get(username)


# Need datetime import
from datetime import datetime
