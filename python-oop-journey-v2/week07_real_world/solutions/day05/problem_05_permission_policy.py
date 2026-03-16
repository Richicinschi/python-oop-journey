"""Reference solution for Problem 05: Permission Policy."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class Permission(Enum):
    """Standard permission types."""
    READ = auto()
    WRITE = auto()
    DELETE = auto()
    ADMIN = auto()


@dataclass(frozen=True)
class User:
    """User with permissions context."""
    user_id: int
    username: str
    roles: frozenset[str] = frozenset()
    permissions: frozenset[Permission] = frozenset()
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return "admin" in self.roles or Permission.ADMIN in self.permissions
    
    def has_role(self, role: str) -> bool:
        """Check if user has specific role."""
        return role in self.roles
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has specific permission."""
        return permission in self.permissions


@dataclass
class Resource:
    """Generic resource with ownership and access control."""
    resource_id: str
    resource_type: str
    owner_id: int
    is_public: bool = False
    allowed_users: frozenset[int] = frozenset()
    
    def is_owner(self, user_id: int) -> bool:
        """Check if user owns this resource."""
        return self.owner_id == user_id
    
    def is_allowed(self, user_id: int) -> bool:
        """Check if user is in allowed list."""
        return user_id in self.allowed_users


class PermissionPolicy(ABC):
    """Abstract base for permission policies."""
    
    @abstractmethod
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if user passes this policy."""
        raise NotImplementedError("Implement check")
    
    def __and__(self, other: PermissionPolicy) -> PermissionPolicy:
        """Combine with AND logic."""
        return AndPolicy(self, other)
    
    def __or__(self, other: PermissionPolicy) -> PermissionPolicy:
        """Combine with OR logic."""
        return OrPolicy(self, other)
    
    def __invert__(self) -> PermissionPolicy:
        """Negate this policy."""
        return NotPolicy(self)


class OwnerPolicy(PermissionPolicy):
    """Policy: User must be the resource owner."""
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if user owns the resource."""
        if resource is None:
            return False
        return resource.is_owner(user.user_id)


class RolePolicy(PermissionPolicy):
    """Policy: User must have one of the specified roles."""
    
    def __init__(self, required_roles: set[str]) -> None:
        """Initialize with required roles."""
        self._required_roles = frozenset(required_roles)
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if user has any required role."""
        return bool(self._required_roles & user.roles)


class PermissionPolicyConcrete(PermissionPolicy):
    """Policy: User must have one of the specified permissions."""
    
    def __init__(self, required_permissions: set[Permission]) -> None:
        """Initialize with required permissions."""
        self._required_permissions = frozenset(required_permissions)
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if user has any required permission."""
        return bool(self._required_permissions & user.permissions)


class PublicResourcePolicy(PermissionPolicy):
    """Policy: Resource must be marked as public."""
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if resource is public."""
        if resource is None:
            return False
        return resource.is_public


class AllowedUserPolicy(PermissionPolicy):
    """Policy: User must be in resource's allowed list."""
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if user is explicitly allowed."""
        if resource is None:
            return False
        return resource.is_allowed(user.user_id)


class AdminPolicy(PermissionPolicy):
    """Policy: User must be an admin."""
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if user is admin."""
        return user.is_admin


class AndPolicy(PermissionPolicy):
    """Combines two policies with AND logic."""
    
    def __init__(self, left: PermissionPolicy, right: PermissionPolicy) -> None:
        self._left = left
        self._right = right
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        return (
            self._left.check(user, resource) and
            self._right.check(user, resource)
        )


class OrPolicy(PermissionPolicy):
    """Combines two policies with OR logic."""
    
    def __init__(self, left: PermissionPolicy, right: PermissionPolicy) -> None:
        self._left = left
        self._right = right
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        return (
            self._left.check(user, resource) or
            self._right.check(user, resource)
        )


class NotPolicy(PermissionPolicy):
    """Negates a policy."""
    
    def __init__(self, policy: PermissionPolicy) -> None:
        self._policy = policy
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        return not self._policy.check(user, resource)


class PermissionChecker:
    """Service for checking permissions using policies."""
    
    def authorized(
        self,
        user: User,
        resource: Resource | None,
        policy: PermissionPolicy,
    ) -> bool:
        """Check if user is authorized by policy."""
        return policy.check(user, resource)
    
    def has_permission(self, user: User, permission: Permission) -> bool:
        """Check if user has specific permission."""
        return user.has_permission(permission)
    
    def is_owner(self, user: User, resource: Resource) -> bool:
        """Check if user owns resource."""
        return resource.is_owner(user.user_id)
    
    def owner_or_admin(self) -> PermissionPolicy:
        """Get policy requiring ownership OR admin role."""
        return OwnerPolicy() | AdminPolicy()
    
    def can_read(self, user: User, resource: Resource) -> bool:
        """Check read access.
        
        Allows if:
        - User is admin, OR
        - User is owner, OR
        - Resource is public, OR
        - User has READ permission and is in allowed list
        """
        # Admin can read everything
        if user.is_admin:
            return True
        
        # Owner can read their own
        if resource.is_owner(user.user_id):
            return True
        
        # Public resources are readable
        if resource.is_public:
            return True
        
        # Allowed users with READ permission
        if (
            resource.is_allowed(user.user_id) and
            user.has_permission(Permission.READ)
        ):
            return True
        
        return False
    
    def can_write(self, user: User, resource: Resource) -> bool:
        """Check write access.
        
        Allows if:
        - User is admin, OR
        - User is owner AND has WRITE permission
        """
        # Admin can write everything
        if user.is_admin:
            return True
        
        # Owner with WRITE permission
        if (
            resource.is_owner(user.user_id) and
            user.has_permission(Permission.WRITE)
        ):
            return True
        
        return False
    
    def can_delete(self, user: User, resource: Resource) -> bool:
        """Check delete access.
        
        Allows if:
        - User is admin, OR
        - User is owner AND has DELETE permission
        """
        # Admin can delete everything
        if user.is_admin:
            return True
        
        # Owner with DELETE permission
        if (
            resource.is_owner(user.user_id) and
            user.has_permission(Permission.DELETE)
        ):
            return True
        
        return False
