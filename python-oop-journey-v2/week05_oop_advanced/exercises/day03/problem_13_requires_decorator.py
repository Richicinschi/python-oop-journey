"""Problem 13: Requires Decorator

Topic: Check Permissions
Difficulty: Medium

Create a decorator that checks if a user has required permissions.

This demonstrates inspecting function signatures to find specific parameters
and performing authorization checks. Common pattern in web frameworks and
APIs for access control.

Example:
    >>> class User:
    ...     def __init__(self, name: str, permissions: set[str]):
    ...         self.name = name
    ...         self.permissions = permissions
    
    >>> @requires({"admin"})
    ... def delete_database(user: User):
    ...     return "Database deleted"
    
    >>> admin = User("Alice", {"admin", "read", "write"})
    >>> delete_database(admin)
    'Database deleted'
    
    >>> guest = User("Bob", {"read"})
    >>> delete_database(guest)  # Raises PermissionError
    Traceback (most recent call last):
        ...
    PermissionError: User lacks required permissions: {'admin'}

    >>> @requires({"read", "write"})
    ... def save_document(user: User, document: str):
    ...     return f"Saved: {document}"
    
    >>> user = User("Charlie", {"read", "write", "admin"})
    >>> save_document(user, "report.txt")
    'Saved: report.txt'

Behavior Notes:
    - Finds the 'user' parameter by name in the function signature
    - Checks if user.permissions (a set) contains all required permissions
    - Raises PermissionError if any required permission is missing
    - Error message: "User lacks required permissions: {missing_permissions}"
    - Calls the function normally if user has all permissions

Edge Cases:
    - User must have ALL required permissions (AND logic, not OR)
    - The 'user' parameter can be positional or keyword
    - Missing 'user' parameter should raise TypeError naturally
    - Extra user permissions are fine (user can have superset)
    - Empty permissions set in @requires({}) allows any user
"""

from __future__ import annotations

from functools import wraps
from typing import Callable, Any, Set


def requires(permissions: Set[str]) -> Callable:
    """A decorator that checks user permissions.
    
    The decorated function must have a 'user' parameter with a 'permissions'
    attribute that is a set of permission strings.
    
    Raises PermissionError if user lacks any required permission.
    
    Args:
        permissions: Set of required permission strings
        
    Returns:
        A decorator function
    """
    raise NotImplementedError("Implement the requires decorator")


class User:
    """A user with permissions for testing the requires decorator."""
    
    def __init__(self, name: str, permissions: Set[str]) -> None:
        """Initialize a user.
        
        Args:
            name: The user's name
            permissions: Set of permission strings
        """
        raise NotImplementedError("Implement User.__init__")


# Hints for Requires Decorator (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to inspect the function's arguments at runtime. The user parameter could
# be positional or keyword.
#
# Hint 2 - Structural plan:
# - Use inspect.signature or **kwargs to find the user argument
# - Check if user.permissions (a set) is a superset of required permissions
# - Raise PermissionError if not
#
# Hint 3 - Edge-case warning:
# What if user is not passed? The function signature might not even have it.
# Consider using *args, **kwargs in your wrapper and searching for user in kwargs
# or by position.
