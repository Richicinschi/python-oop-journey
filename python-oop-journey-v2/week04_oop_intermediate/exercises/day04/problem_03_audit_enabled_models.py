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
        # TODO: Initialize _audit_trail as empty list and call super().__init__
        raise NotImplementedError("Initialize _audit_trail")
    
    def audit(self, action: str, user: str, details: dict[str, Any] | None = None) -> None:
        """Record an audit entry.
        
        Args:
            action: The action performed.
            user: Who performed the action.
            details: Optional additional details.
        """
        # TODO: Append dict with timestamp, action, user, details to _audit_trail
        raise NotImplementedError("Append audit entry")
    
    def get_audit_trail(self) -> list[dict[str, Any]]:
        """Get a copy of the audit trail.
        
        Returns:
            List of audit entry dictionaries.
        """
        # TODO: Return a copy of _audit_trail
        raise NotImplementedError("Return copy of audit trail")
    
    def get_changes_by_user(self, user: str) -> list[dict[str, Any]]:
        """Get all changes made by a specific user.
        
        Args:
            user: The username to filter by.
        
        Returns:
            List of audit entries by the specified user.
        """
        # TODO: Return list of entries where entry['user'] == user
        raise NotImplementedError("Return changes by user")


class Versioned:
    """Mixin that tracks version history.
    
    Attributes:
        _version: Current version number.
        _version_history: List of version history entries.
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # TODO: Initialize _version to 1, _version_history to empty list, call super().__init__
        raise NotImplementedError("Initialize version tracking")
    
    @property
    def version(self) -> int:
        """Get the current version.
        
        Returns:
            The current version number.
        """
        # TODO: Return _version
        raise NotImplementedError("Return version")
    
    def bump_version(self, changes_description: str) -> None:
        """Increment version and record changes.
        
        Args:
            changes_description: Description of the changes.
        """
        # TODO: Record current version + changes to history, then increment _version
        raise NotImplementedError("Bump version and record")
    
    def get_version_history(self) -> list[dict[str, Any]]:
        """Get the version history.
        
        Returns:
            List of version history entries.
        """
        # TODO: Return a copy of _version_history
        raise NotImplementedError("Return version history")
    
    def rollback_to_version(self, target_version: int) -> bool:
        """Check if rollback to a version is possible (doesn't actually rollback).
        
        Args:
            target_version: The version to rollback to.
        
        Returns:
            True if target_version < current version and >= 1, False otherwise.
        """
        # TODO: Return True if 1 <= target_version < _version
        raise NotImplementedError("Check rollback feasibility")


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
        # TODO: Call super().__init__ to trigger MRO, then set id and _data
        # TODO: Audit the creation
        raise NotImplementedError("Initialize model")
    
    def get_data(self) -> dict[str, Any]:
        """Get a copy of the data.
        
        Returns:
            Copy of the internal data dictionary.
        """
        # TODO: Return _data.copy()
        raise NotImplementedError("Return data copy")
    
    def update(self, changes: dict[str, Any], user: str) -> None:
        """Update the data and record audit/version.
        
        Args:
            changes: Dictionary of changes to apply.
            user: Who is making the changes.
        """
        # TODO: Update _data with changes, audit the change, bump version
        raise NotImplementedError("Update and record")


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
        # TODO: Initialize with id and data containing username and profile
        raise NotImplementedError("Initialize user")
    
    @property
    def username(self) -> str:
        """Get the username.
        
        Returns:
            The username from data.
        """
        # TODO: Return self._data.get('username', '')
        raise NotImplementedError("Return username")
    
    def deactivate(self, admin_user: str) -> None:
        """Deactivate the user account.
        
        Args:
            admin_user: The admin performing the deactivation.
        """
        # TODO: Set _data['active'] = False and record audit
        raise NotImplementedError("Deactivate user")
    
    def is_active(self) -> bool:
        """Check if the user is active.
        
        Returns:
            True if user is active, False otherwise.
        """
        # TODO: Return _data.get('active', True)
        raise NotImplementedError("Check active status")
