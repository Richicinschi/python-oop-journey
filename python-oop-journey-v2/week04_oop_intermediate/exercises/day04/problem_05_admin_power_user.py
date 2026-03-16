r"""Problem 05: Admin Power User (Diamond Inheritance).

Demonstrate the diamond problem and MRO with user roles.

Inheritance hierarchy:
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

Hints:
    Hint 1: This is a diamond inheritance problem. SuperAdmin's MRO will be:
    SuperAdmin -> Admin -> PowerUser -> User -> object
    Use SuperAdmin.__mro__ to verify. Call super().__init__() with name, email,
    and admin_level in SuperAdmin.__init__, then set power_level manually.
    
    Hint 2: In Admin and PowerUser __init__, accept **kwargs and pass them to
    super().__init__(**kwargs). This enables cooperative multiple inheritance.
    Both should add their permissions to the parent's permission list.
    
    Hint 3: For get_permissions(), make sure to return a COPY of the permissions
    list (use self._permissions.copy()), not the original. This prevents external
    code from modifying the internal list. SuperAdmin needs all four permissions
    without duplicates.
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
        # TODO: Set name and email, initialize _permissions with ["read"]
        raise NotImplementedError("Initialize user")
    
    def get_permissions(self) -> list[str]:
        """Get the user's permissions.
        
        Returns:
            List of permission strings.
        """
        # TODO: Return copy of _permissions
        raise NotImplementedError("Return permissions")
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission.
        
        Args:
            permission: The permission to check.
        
        Returns:
            True if user has the permission, False otherwise.
        """
        # TODO: Return True if permission in _permissions
        raise NotImplementedError("Check permission")
    
    def describe(self) -> str:
        """Return user description.
        
        Returns:
            Description string.
        """
        # TODO: Return f"User({self.name}, {self.email})"
        raise NotImplementedError("Return description")


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
        # TODO: Call super().__init__(name, email), then set admin_level,
        # add "write" and "admin" to _permissions if not present
        raise NotImplementedError("Initialize admin")
    
    def can_administer(self) -> bool:
        """Check if user can administer.
        
        Returns:
            True (Admin can always administer).
        """
        # TODO: Return True
        raise NotImplementedError("Return True")
    
    def get_admin_info(self) -> dict[str, Any]:
        """Get admin information.
        
        Returns:
            Dictionary with admin info.
        """
        # TODO: Return {"level": self.admin_level, "can_administer": True}
        raise NotImplementedError("Return admin info")


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
        # TODO: Call super().__init__(name, email), then set power_level,
        # add "write" and "power" to _permissions if not present
        raise NotImplementedError("Initialize power user")
    
    def can_access_power_features(self) -> bool:
        """Check if user can access power features.
        
        Returns:
            True (PowerUser can always access power features).
        """
        # TODO: Return True
        raise NotImplementedError("Return True")
    
    def get_power_info(self) -> dict[str, Any]:
        """Get power user information.
        
        Returns:
            Dictionary with power user info.
        """
        # TODO: Return {"level": self.power_level, "can_access_power": True}
        raise NotImplementedError("Return power info")


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
        # TODO: Call super().__init__ with name, email, admin_level
        # Then set power_level manually
        raise NotImplementedError("Initialize super admin")
    
    def get_all_capabilities(self) -> dict[str, Any]:
        """Get all capabilities.
        
        Returns:
            Dictionary with all capabilities info.
        """
        # TODO: Return dict with admin_level, power_level, permissions
        raise NotImplementedError("Return all capabilities")
    
    def is_super_admin(self) -> bool:
        """Check if this is a super admin.
        
        Returns:
            True.
        """
        # TODO: Return True
        raise NotImplementedError("Return True")
