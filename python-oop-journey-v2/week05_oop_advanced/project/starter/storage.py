"""Data persistence layer.

Implement JSON-based storage with transaction support.
"""

from __future__ import annotations

import json
import os
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
    """JSON file-based storage for projects, tasks, and users.
    
    Provides load/save functionality and transaction support.
    
    TODO: Implement Storage class with:
    1. File path management
    2. JSON serialization/deserialization
    3. Data integrity
    """
    
    def __init__(self, filepath: str | Path) -> None:
        raise NotImplementedError("Implement Storage.__init__")
    
    def exists(self) -> bool:
        """Check if storage file exists.
        
        TODO: Return True if file exists.
        """
        raise NotImplementedError("Implement exists")
    
    def save(
        self,
        projects: list[Project],
        users: list[User],
    ) -> None:
        """Save all data to file atomically.
        
        TODO:
        1. Serialize projects and users to dicts
        2. Write to temp file
        3. Rename to target (atomic on most systems)
        """
        raise NotImplementedError("Implement save")
    
    def load(self) -> tuple[list[Project], list[User]]:
        """Load all data from file.
        
        TODO:
        1. Read JSON from file
        2. Deserialize users first (for reference resolution)
        3. Deserialize projects and tasks
        4. Return (projects, users)
        
        Raises StorageError if file not found or corrupted.
        """
        raise NotImplementedError("Implement load")
    
    def load_or_init(self) -> tuple[list[Project], list[User]]:
        """Load data or return empty collections.
        
        TODO: Try to load, return ([], []) if file doesn't exist.
        """
        raise NotImplementedError("Implement load_or_init")
    
    def backup(self, backup_path: str | Path | None = None) -> str:
        """Create backup of current data file.
        
        TODO: Copy current file to backup location, return path.
        """
        raise NotImplementedError("Implement backup")
    
    def clear(self) -> None:
        """Delete storage file if exists.
        
        TODO: Remove file if it exists.
        """
        raise NotImplementedError("Implement clear")
    
    @contextmanager
    def transaction(
        self,
    ) -> Generator[Transaction, None, None]:
        """Context manager for atomic storage operations.
        
        Usage:
            with storage.transaction() as txn:
                txn.save_project(project)
                txn.save_user(user)
            # Auto-committed on success
            # Auto-rolled back on exception
        
        TODO: Implement transaction context manager that:
        1. Loads current state
        2. Yields Transaction object
        3. Saves on successful exit
        4. Does NOT save on exception (rollback)
        """
        raise NotImplementedError("Implement transaction")


class Transaction:
    """Transaction object for batch operations.
    
    Collects changes and applies them on commit.
    
    TODO: Implement Transaction class with:
    1. Reference to Storage
    2. Buffers for projects and users
    3. Methods to queue changes
    4. Commit method
    """
    
    def __init__(self, storage: Storage) -> None:
        raise NotImplementedError("Implement Transaction.__init__")
    
    def save_project(self, project: Project) -> None:
        """Queue project for saving.
        
        TODO: Add/replace project in buffer.
        """
        raise NotImplementedError("Implement save_project")
    
    def delete_project(self, project_id: str) -> None:
        """Queue project for deletion.
        
        TODO: Mark project for removal.
        """
        raise NotImplementedError("Implement delete_project")
    
    def save_user(self, user: User) -> None:
        """Queue user for saving.
        
        TODO: Add/replace user in buffer.
        """
        raise NotImplementedError("Implement save_user")
    
    def delete_user(self, username: str) -> None:
        """Queue user for deletion.
        
        TODO: Mark user for removal.
        """
        raise NotImplementedError("Implement delete_user")
    
    def commit(self) -> None:
        """Apply all queued changes to storage.
        
        TODO: Merge buffers with current data and save.
        """
        raise NotImplementedError("Implement commit")
    
    def get_projects(self) -> list[Project]:
        """Get current projects including pending changes.
        
        TODO: Return merged view.
        """
        raise NotImplementedError("Implement get_projects")
    
    def get_users(self) -> list[User]:
        """Get current users including pending changes.
        
        TODO: Return merged view.
        """
        raise NotImplementedError("Implement get_users")
