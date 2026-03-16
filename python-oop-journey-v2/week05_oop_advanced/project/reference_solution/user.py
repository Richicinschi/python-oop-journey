"""User model with role-based access control.

Reference implementation using descriptors for validation.
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
    """Descriptor for validated email addresses."""
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.private_name = f"_{name}"
    
    def __get__(self, instance: Any, owner: type) -> str | None:
        if instance is None:
            return None
        return getattr(instance, self.private_name, None)
    
    def __set__(self, instance: Any, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Email must be a string")
        
        value = value.strip()
        if "@" not in value:
            raise ValueError("Email must contain @")
        
        parts = value.split("@")
        if len(parts) != 2:
            raise ValueError("Invalid email format")
        
        local, domain = parts
        if not local or not domain:
            raise ValueError("Email must have local part and domain")
        if "." not in domain:
            raise ValueError("Email domain must contain a dot")
        
        setattr(instance, self.private_name, value.lower())


class ValidatedUsername:
    """Descriptor for validated usernames."""
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.private_name = f"_{name}"
    
    def __get__(self, instance: Any, owner: type) -> str | None:
        if instance is None:
            return None
        return getattr(instance, self.private_name, None)
    
    def __set__(self, instance: Any, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Username must be a string")
        
        value = value.strip()
        
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(value) > 30:
            raise ValueError("Username must be at most 30 characters")
        
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
        if not all(c in valid_chars for c in value):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        
        setattr(instance, self.private_name, value.lower())


class User:
    """User with role-based permissions."""
    
    username = ValidatedUsername()
    email = ValidatedEmail()
    
    def __init__(self, username: str, email: str, role: Role = Role.MEMBER) -> None:
        self.username = username
        self.email = email
        self.role = role
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has specific permission."""
        return permission in ROLE_PERMISSIONS.get(self.role, set())
    
    def to_dict(self) -> dict[str, Any]:
        """Serialize user to dictionary."""
        return {
            "username": self.username,
            "email": self.email,
            "role": self.role.name,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> User:
        """Create User from dictionary."""
        return cls(
            username=data["username"],
            email=data["email"],
            role=Role[data["role"]],
        )
    
    def __repr__(self) -> str:
        return f"User(username={self.username!r}, email={self.email!r}, role={self.role.name})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self.username == other.username
    
    def __hash__(self) -> int:
        return hash(self.username)
