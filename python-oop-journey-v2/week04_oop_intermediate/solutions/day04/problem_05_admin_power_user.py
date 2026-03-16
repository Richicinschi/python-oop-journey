r"""Problem 05: Admin Power User (Diamond Inheritance).

Demonstrate the diamond problem and MRO with user roles.

Inheritance hierarchy::

        User
       /    \
    Admin  PowerUser
       \    /
      SuperAdmin

Classes to implement:
- User: Base user class with name and email
- Admin: User with admin privileges
- PowerUser: User with elevated permissions
- SuperAdmin: Inherits from both Admin and PowerUser

Example:
    >>> sa = SuperAdmin("alice", "alice@example.com")
    >>> sa.can_administer()
    True
    >>> sa.can_access_power_features()
    True
    >>> sa.get_permissions()
    ['read', 'write', 'admin', 'power']
"""

from __future__ import annotations

from typing import Any


class User:
    """Base user class.
    
    Attributes:
        name: The user's name.
        email: The user's email address.
    
    Args:
        name: The user's name.
        email: The user's email address.
    """
    
    def __init__(self, name: str, email: str) -> None:
        """Initialize a user.
        
        Args:
            name: The user's name.
            email: The user's email address.
        """
        self.name = name
        self.email = email
        self._permissions: list[str] = ["read"]
    
    def get_permissions(self) -> list[str]:
        """Get the user's permissions.
        
        Returns:
            List of permission strings.
        """
        return self._permissions.copy()
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission.
        
        Args:
            permission: The permission to check.
        
        Returns:
            True if user has the permission, False otherwise.
        """
        return permission in self._permissions
    
    def describe(self) -> str:
        """Return user description.
        
        Returns:
            Description string.
        """
        return f"User({self.name}, {self.email})"


class Admin(User):
    """User with admin privileges.
    
    Adds 'write' and 'admin' permissions.
    
    Attributes:
        name: The user's name.
        email: The user's email address.
        admin_level: The admin level (default 1).
    
    Args:
        name: The user's name.
        email: The user's email address.
        admin_level: The admin level.
    """
    
    def __init__(self, name: str, email: str, admin_level: int = 1) -> None:
        """Initialize an admin.
        
        Args:
            name: The user's name.
            email: The user's email address.
            admin_level: The admin level.
        """
        super().__init__(name, email)
        self.admin_level = admin_level
        # Add admin permissions (avoid duplicates)
        for perm in ["write", "admin"]:
            if perm not in self._permissions:
                self._permissions.append(perm)
    
    def can_administer(self) -> bool:
        """Check if user can administer.
        
        Returns:
            True (Admin can always administer).
        """
        return True
    
    def get_admin_info(self) -> dict[str, Any]:
        """Get admin information.
        
        Returns:
            Dictionary with admin info.
        """
        return {"level": self.admin_level, "can_administer": True}


class PowerUser(User):
    """User with elevated permissions.
    
    Adds 'write' and 'power' permissions.
    
    Attributes:
        name: The user's name.
        email: The user's email address.
        power_level: The power level (default 1).
    
    Args:
        name: The user's name.
        email: The user's email address.
        power_level: The power level.
    """
    
    def __init__(self, name: str, email: str, power_level: int = 1) -> None:
        """Initialize a power user.
        
        Args:
            name: The user's name.
            email: The user's email address.
            power_level: The power level.
        """
        super().__init__(name, email)
        self.power_level = power_level
        # Add power permissions (avoid duplicates)
        for perm in ["write", "power"]:
            if perm not in self._permissions:
                self._permissions.append(perm)
    
    def can_access_power_features(self) -> bool:
        """Check if user can access power features.
        
        Returns:
            True (PowerUser can always access power features).
        """
        return True
    
    def get_power_info(self) -> dict[str, Any]:
        """Get power user information.
        
        Returns:
            Dictionary with power user info.
        """
        return {"level": self.power_level, "can_access_power": True}


class SuperAdmin(Admin, PowerUser):
    """User with both admin and power privileges.
    
    This creates a diamond inheritance pattern:
    User -> Admin -> SuperAdmin
    User -> PowerUser -> SuperAdmin
    
    Attributes:
        name: The user's name.
        email: The user's email address.
        admin_level: The admin level.
        power_level: The power level.
    
    Args:
        name: The user's name.
        email: The user's email address.
        admin_level: The admin level (default 2).
        power_level: The power level (default 2).
    """
    
    def __init__(
        self,
        name: str,
        email: str,
        admin_level: int = 2,
        power_level: int = 2
    ) -> None:
        """Initialize a super admin.
        
        Args:
            name: The user's name.
            email: The user's email address.
            admin_level: The admin level (default 2).
            power_level: The power level (default 2).
        """
        # Admin is first in MRO, so call super() with Admin's signature
        super().__init__(name, email, admin_level)
        # Set power_level manually (PowerUser's __init__ won't be called via super())
        self.power_level = power_level
        # Ensure all permissions are present
        for perm in ["write", "power"]:
            if perm not in self._permissions:
                self._permissions.append(perm)
    
    def get_all_capabilities(self) -> dict[str, Any]:
        """Get all capabilities.
        
        Returns:
            Dictionary with all capabilities info.
        """
        return {
            "name": self.name,
            "email": self.email,
            "admin_level": self.admin_level,
            "power_level": self.power_level,
            "permissions": self.get_permissions()
        }
    
    def is_super_admin(self) -> bool:
        """Check if this is a super admin.
        
        Returns:
            True.
        """
        return True
