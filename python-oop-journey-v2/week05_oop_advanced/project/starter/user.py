"""User model with role-based access control.

Implement User class with role validation using descriptors.
"""

from __future__ import annotations

from enum import Enum, auto
from typing import Any


class Role(Enum):
    """User roles with different permission levels."""
    ADMIN = auto()
    MANAGER = auto()
    MEMBER = auto()
    VIEWER = auto()


class Permission(Enum):
    """Available permissions in the system."""
    CREATE_PROJECT = auto()
    DELETE_PROJECT = auto()
    MANAGE_MEMBERS = auto()
    CREATE_TASK = auto()
    DELETE_TASK = auto()
    ASSIGN_TASK = auto()
    UPDATE_TASK = auto()
    VIEW_ALL = auto()


# Permission matrix mapping roles to permissions
ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.ADMIN: {
        Permission.CREATE_PROJECT, Permission.DELETE_PROJECT,
        Permission.MANAGE_MEMBERS, Permission.CREATE_TASK,
        Permission.DELETE_TASK, Permission.ASSIGN_TASK,
        Permission.UPDATE_TASK, Permission.VIEW_ALL,
    },
    Role.MANAGER: {
        Permission.CREATE_PROJECT, Permission.MANAGE_MEMBERS,
        Permission.CREATE_TASK, Permission.ASSIGN_TASK,
        Permission.UPDATE_TASK, Permission.VIEW_ALL,
    },
    Role.MEMBER: {
        Permission.CREATE_TASK, Permission.UPDATE_TASK,
        Permission.VIEW_ALL,
    },
    Role.VIEWER: {
        Permission.VIEW_ALL,
    },
}


class ValidatedEmail:
    """Descriptor for validated email addresses.
    
    Validates email format: must contain @ and domain.
    Stores in private attribute.
    
    TODO: Implement email descriptor that:
    1. Validates email contains '@'
    2. Validates domain part exists after '@'
    3. Stores in private attribute (e.g., _email)
    4. Returns stored value on get
    """
    raise NotImplementedError("Implement ValidatedEmail descriptor")


class ValidatedUsername:
    """Descriptor for validated usernames.
    
    Rules: 3-30 characters, alphanumeric and underscore only.
    
    TODO: Implement username descriptor that:
    1. Validates length 3-30
    2. Validates alphanumeric/underscore characters
    3. Stores in private attribute
    4. Returns stored value on get
    """
    raise NotImplementedError("Implement ValidatedUsername descriptor")


class User:
    """User with role-based permissions.
    
    Uses descriptors for email and username validation.
    
    TODO: Implement User class with:
    1. ValidatedUsername and ValidatedEmail descriptors
    2. Role assignment with validation
    3. Permission checking via has_permission method
    4. Serialization to/from dict
    """
    
    def __init__(self, username: str, email: str, role: Role = Role.MEMBER) -> None:
        raise NotImplementedError("Implement User.__init__")
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has specific permission.
        
        TODO: Check ROLE_PERMISSIONS matrix for user's role.
        """
        raise NotImplementedError("Implement has_permission")
    
    def to_dict(self) -> dict[str, Any]:
        """Serialize user to dictionary.
        
        TODO: Return dict with username, email, role.
        """
        raise NotImplementedError("Implement to_dict")
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> User:
        """Create User from dictionary.
        
        TODO: Deserialize from dict.
        """
        raise NotImplementedError("Implement from_dict")
    
    def __repr__(self) -> str:
        raise NotImplementedError("Implement __repr__")
    
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError("Implement __eq__")
