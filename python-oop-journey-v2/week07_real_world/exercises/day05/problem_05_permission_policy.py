"""Problem 05: Permission Policy

Topic: Policy-based authorization, permission checking, role-based access
Difficulty: Medium

Implement a permission checking system using the Policy pattern.
This allows flexible, composable authorization rules.

HINTS AND DEBUGGING:

HINT 1 (Conceptual):
The Policy pattern encapsulates authorization rules into interchangeable,
composable objects. Instead of scattered if-statements:
    if user.is_admin or (user.id == resource.owner_id):
        # allow access

You create reusable policy objects:
    policy = AdminPolicy() | OwnerPolicy()
    if policy.check(user, resource):
        # allow access

Key insight: Policies are composable using Python's bitwise operators:
- & (AND): Both policies must pass
- | (OR): Either policy must pass  
- ~ (NOT): Inverts the policy result

HINT 2 (Structural):

PermissionPolicy (Abstract Base):
- check(user, resource) -> bool
- __and__(other) -> AndPolicy
- __or__(other) -> OrPolicy
- __invert__() -> NotPolicy

Concrete Policies (implement check()):
- OwnerPolicy: resource.is_owner(user.user_id)
- RolePolicy: any(role in user.roles for role in required_roles)
- PermissionPolicyConcrete: any(p in user.permissions for p in required)
- PublicResourcePolicy: resource.is_public
- AllowedUserPolicy: resource.is_allowed(user.user_id)
- AdminPolicy: user.is_admin

Composite Policies:
- AndPolicy: checks left AND right
- OrPolicy: checks left OR right
- NotPolicy: inverts wrapped policy

PermissionChecker (Service):
- authorized(user, resource, policy) -> bool
- has_permission(user, permission) -> bool
- is_owner(user, resource) -> bool
- owner_or_admin() -> Policy (convenience method)
- can_read, can_write, can_delete -> check specific permissions

HINT 3 (Edge Cases):
- Policy.check() with no resource: handle None gracefully
- User with multiple roles: any match passes RolePolicy
- User with multiple permissions: any match passes PermissionPolicy
- Public resource: allowed for any user (but still check resource exists)
- AllowedUserPolicy: User must be in resource.allowed_users set
- can_read logic: admin OR owner OR public OR (allowed_user AND has READ permission)
- can_write logic: admin OR (owner AND has WRITE permission)

DEBUGGING - Common Policy Pattern Mistakes:

1. Not implementing operator overloading:
   # WRONG - can't compose policies
   policy1 = OwnerPolicy()
   policy2 = AdminPolicy()
   combined = policy1 | policy2  # TypeError!
   
   # RIGHT - implement __or__, __and__, __invert__
   class PermissionPolicy(ABC):
       def __or__(self, other):
           return OrPolicy(self, other)
       # ... similar for __and__, __invert__

2. Composite policies not evaluating lazily:
   # AND should short-circuit
   def check(self, user, resource):
       return self.left.check(user, resource) and self.right.check(user, resource)
   
   # Python's 'and' already short-circuits, so this is correct

3. Forgetting to handle None resource:
   # Some policies require a resource, others don't
   def check(self, user, resource=None):
       if resource is None:
           return False  # or True depending on policy
       return resource.is_owner(user.user_id)

4. Confusing roles with permissions:
   # Role: "admin", "user", "editor" (who you are)
   # Permission: READ, WRITE, DELETE (what you can do)
   # A role usually implies certain permissions

5. Not using frozenset for roles/permissions:
   # Use frozenset instead of set for immutability
   # Use set operations: required_roles & user.roles
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, ClassVar


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
    """Abstract base for permission policies.
    
    The Policy pattern encapsulates authorization rules into
    interchangeable, composable objects.
    
    Example:
        >>> policy = OwnerPolicy()
        >>> if policy.check(user, resource):
        ...     # Allow action
    """
    
    @abstractmethod
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if user passes this policy.
        
        Args:
            user: User requesting access
            resource: Optional resource being accessed
            
        Returns:
            True if policy allows access
        """
        raise NotImplementedError("Implement check")
    
    def __and__(self, other: PermissionPolicy) -> PermissionPolicy:
        """Combine with AND logic.
        
        Returns a new policy that passes only if both policies pass.
        """
        raise NotImplementedError("Implement __and__")
    
    def __or__(self, other: PermissionPolicy) -> PermissionPolicy:
        """Combine with OR logic.
        
        Returns a new policy that passes if either policy passes.
        """
        raise NotImplementedError("Implement __or__")
    
    def __invert__(self) -> PermissionPolicy:
        """Negate this policy.
        
        Returns a new policy that inverts the result.
        """
        raise NotImplementedError("Implement __invert__")


class OwnerPolicy(PermissionPolicy):
    """Policy: User must be the resource owner."""
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if user owns the resource."""
        raise NotImplementedError("Implement OwnerPolicy.check")


class RolePolicy(PermissionPolicy):
    """Policy: User must have one of the specified roles."""
    
    def __init__(self, required_roles: set[str]) -> None:
        """Initialize with required roles.
        
        Args:
            required_roles: Set of allowed roles
        """
        raise NotImplementedError("Implement __init__")
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if user has any required role."""
        raise NotImplementedError("Implement RolePolicy.check")


class PermissionPolicyConcrete(PermissionPolicy):
    """Policy: User must have one of the specified permissions."""
    
    def __init__(self, required_permissions: set[Permission]) -> None:
        """Initialize with required permissions.
        
        Args:
            required_permissions: Set of required permissions
        """
        raise NotImplementedError("Implement __init__")
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if user has any required permission."""
        raise NotImplementedError("Implement PermissionPolicyConcrete.check")


class PublicResourcePolicy(PermissionPolicy):
    """Policy: Resource must be marked as public."""
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if resource is public."""
        raise NotImplementedError("Implement PublicResourcePolicy.check")


class AllowedUserPolicy(PermissionPolicy):
    """Policy: User must be in resource's allowed list."""
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if user is explicitly allowed."""
        raise NotImplementedError("Implement AllowedUserPolicy.check")


class AdminPolicy(PermissionPolicy):
    """Policy: User must be an admin (short for RolePolicy({"admin"}))."""
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        """Check if user is admin."""
        raise NotImplementedError("Implement AdminPolicy.check")


# Composite policies (for __and__, __or__, __invert__)
class AndPolicy(PermissionPolicy):
    """Combines two policies with AND logic."""
    
    def __init__(self, left: PermissionPolicy, right: PermissionPolicy) -> None:
        raise NotImplementedError("Implement __init__")
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        raise NotImplementedError("Implement AndPolicy.check")


class OrPolicy(PermissionPolicy):
    """Combines two policies with OR logic."""
    
    def __init__(self, left: PermissionPolicy, right: PermissionPolicy) -> None:
        raise NotImplementedError("Implement __init__")
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        raise NotImplementedError("Implement OrPolicy.check")


class NotPolicy(PermissionPolicy):
    """Negates a policy."""
    
    def __init__(self, policy: PermissionPolicy) -> None:
        raise NotImplementedError("Implement __init__")
    
    def check(self, user: User, resource: Resource | None = None) -> bool:
        raise NotImplementedError("Implement NotPolicy.check")


class PermissionChecker:
    """Service for checking permissions using policies.
    
    Provides a convenient API for authorization checks with
    support for common patterns like ownership, roles, and
    permission-based access.
    
    Example:
        >>> checker = PermissionChecker()
        >>> policy = checker.owner_or_admin()
        >>> if checker.authorized(user, resource, policy):
        ...     # Perform action
        
        >>> # Direct permission check
        >>> if checker.has_permission(user, Permission.WRITE):
        ...     # Allow write
    """
    
    def authorized(
        self,
        user: User,
        resource: Resource | None,
        policy: PermissionPolicy,
    ) -> bool:
        """Check if user is authorized by policy.
        
        Args:
            user: User to check
            resource: Optional resource being accessed
            policy: Policy to evaluate
            
        Returns:
            True if policy passes
        """
        raise NotImplementedError("Implement authorized")
    
    def has_permission(self, user: User, permission: Permission) -> bool:
        """Check if user has specific permission.
        
        Args:
            user: User to check
            permission: Required permission
            
        Returns:
            True if user has permission
        """
        raise NotImplementedError("Implement has_permission")
    
    def is_owner(self, user: User, resource: Resource) -> bool:
        """Check if user owns resource.
        
        Args:
            user: User to check
            resource: Resource to check ownership of
            
        Returns:
            True if user is owner
        """
        raise NotImplementedError("Implement is_owner")
    
    def owner_or_admin(self) -> PermissionPolicy:
        """Get policy requiring ownership OR admin role.
        
        Returns:
            Composed policy (OwnerPolicy | AdminPolicy)
        """
        raise NotImplementedError("Implement owner_or_admin")
    
    def can_read(self, user: User, resource: Resource) -> bool:
        """Check read access.
        
        Allows if:
        - User is admin, OR
        - User is owner, OR
        - Resource is public, OR
        - User has READ permission and is in allowed list
        
        Args:
            user: User requesting access
            resource: Resource being accessed
            
        Returns:
            True if read is allowed
        """
        raise NotImplementedError("Implement can_read")
    
    def can_write(self, user: User, resource: Resource) -> bool:
        """Check write access.
        
        Allows if:
        - User is admin, OR
        - User is owner AND has WRITE permission
        
        Args:
            user: User requesting access
            resource: Resource being accessed
            
        Returns:
            True if write is allowed
        """
        raise NotImplementedError("Implement can_write")
    
    def can_delete(self, user: User, resource: Resource) -> bool:
        """Check delete access.
        
        Allows if:
        - User is admin, OR
        - User is owner AND has DELETE permission
        
        Args:
            user: User requesting access
            resource: Resource being accessed
            
        Returns:
            True if delete is allowed
        """
        raise NotImplementedError("Implement can_delete")
