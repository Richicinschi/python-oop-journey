"""Problem 03: Audit Enabled Models.

Implement audit and versioning mixins for data models.

Classes to implement:
- Auditable: Mixin that tracks who made what changes
- Versioned: Mixin that tracks version history
- Model: Base class with id and data
- User: A user model with audit and versioning

Example:
    >>> user = User(1, "alice", {"email": "alice@example.com"})
    >>> user.update({"email": "new@example.com"}, "admin")
    >>> user.version
    2
    >>> len(user.get_audit_trail()) > 0
    True
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


class Auditable:
    """Mixin that tracks audit information.
    
    Attributes:
        _audit_trail: List of audit entries.
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the auditable mixin."""
        super().__init__(*args, **kwargs)
        self._audit_trail: list[dict[str, Any]] = []
    
    def audit(self, action: str, user: str, details: dict[str, Any] | None = None) -> None:
        """Record an audit entry.
        
        Args:
            action: The action performed.
            user: Who performed the action.
            details: Optional additional details.
        """
        entry: dict[str, Any] = {
            "timestamp": datetime.now(),
            "action": action,
            "user": user
        }
        if details:
            entry["details"] = details
        self._audit_trail.append(entry)
    
    def get_audit_trail(self) -> list[dict[str, Any]]:
        """Get a copy of the audit trail.
        
        Returns:
            List of audit entry dictionaries.
        """
        return self._audit_trail.copy()
    
    def get_changes_by_user(self, user: str) -> list[dict[str, Any]]:
        """Get all changes made by a specific user.
        
        Args:
            user: The username to filter by.
        
        Returns:
            List of audit entries by the specified user.
        """
        return [entry for entry in self._audit_trail if entry.get("user") == user]


class Versioned:
    """Mixin that tracks version history.
    
    Attributes:
        _version: Current version number.
        _version_history: List of version history entries.
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the versioned mixin."""
        super().__init__(*args, **kwargs)
        self._version: int = 1
        self._version_history: list[dict[str, Any]] = []
    
    @property
    def version(self) -> int:
        """Get the current version.
        
        Returns:
            The current version number.
        """
        return self._version
    
    def bump_version(self, changes_description: str) -> None:
        """Increment version and record changes.
        
        Args:
            changes_description: Description of the changes.
        """
        self._version_history.append({
            "version": self._version,
            "description": changes_description,
            "timestamp": datetime.now()
        })
        self._version += 1
    
    def get_version_history(self) -> list[dict[str, Any]]:
        """Get the version history.
        
        Returns:
            List of version history entries.
        """
        return self._version_history.copy()
    
    def rollback_to_version(self, target_version: int) -> bool:
        """Check if rollback to a version is possible (doesn't actually rollback).
        
        Args:
            target_version: The version to rollback to.
        
        Returns:
            True if target_version < current version and >= 1, False otherwise.
        """
        return 1 <= target_version < self._version


class Model(Auditable, Versioned):
    """Base model class with audit and versioning.
    
    Attributes:
        id: The model's unique identifier.
        _data: The model's data dictionary.
        _audit_trail: From Auditable.
        _version: From Versioned.
    
    Args:
        id: The model's unique identifier.
        data: The initial data dictionary.
    """
    
    def __init__(self, id: int, data: dict[str, Any]) -> None:
        """Initialize a model.
        
        Args:
            id: The model's unique identifier.
            data: The initial data dictionary.
        """
        super().__init__()
        self.id = id
        self._data = data.copy()
        self.audit("created", "system", {"initial_data": data})
    
    def get_data(self) -> dict[str, Any]:
        """Get a copy of the data.
        
        Returns:
            Copy of the internal data dictionary.
        """
        return self._data.copy()
    
    def update(self, changes: dict[str, Any], user: str) -> None:
        """Update the data and record audit/version.
        
        Args:
            changes: Dictionary of changes to apply.
            user: Who is making the changes.
        """
        old_values = {k: self._data.get(k) for k in changes.keys()}
        self._data.update(changes)
        self.audit("updated", user, {"changes": changes, "old_values": old_values})
        self.bump_version(f"Updated: {list(changes.keys())}")


class User(Model):
    """A user model with username and profile data.
    
    Attributes:
        id: The user's unique identifier.
        username: The user's username.
        _data: The user's profile data.
    
    Args:
        id: The user's unique identifier.
        username: The user's username.
        profile: The user's profile data.
    """
    
    def __init__(self, id: int, username: str, profile: dict[str, Any]) -> None:
        """Initialize a user.
        
        Args:
            id: The user's unique identifier.
            username: The user's username.
            profile: The user's profile data.
        """
        data = {"username": username, **profile, "active": True}
        super().__init__(id, data)
    
    @property
    def username(self) -> str:
        """Get the username.
        
        Returns:
            The username from data.
        """
        return self._data.get("username", "")
    
    def deactivate(self, admin_user: str) -> None:
        """Deactivate the user account.
        
        Args:
            admin_user: The admin performing the deactivation.
        """
        self._data["active"] = False
        self.audit("deactivated", admin_user)
        self.bump_version("User deactivated")
    
    def is_active(self) -> bool:
        """Check if the user is active.
        
        Returns:
            True if user is active, False otherwise.
        """
        return self._data.get("active", True)
