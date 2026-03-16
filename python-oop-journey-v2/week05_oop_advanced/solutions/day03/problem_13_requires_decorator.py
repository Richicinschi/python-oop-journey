"""Reference solution for Problem 13: Requires Decorator."""

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
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Find user argument
            user = kwargs.get('user')
            
            # If not in kwargs, look in positional args
            if user is None and args:
                # Check each positional arg for permissions attribute
                for arg in args:
                    if hasattr(arg, 'permissions'):
                        user = arg
                        break
            
            if user is None:
                raise PermissionError("No user provided")
            
            # Check permissions
            if not hasattr(user, 'permissions'):
                raise PermissionError("User has no permissions attribute")
            
            user_perms = set(user.permissions)
            missing = permissions - user_perms
            
            if missing:
                raise PermissionError(
                    f"Missing permissions: {', '.join(missing)}"
                )
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


class User:
    """A user with permissions for testing the requires decorator."""
    
    def __init__(self, name: str, permissions: Set[str]) -> None:
        """Initialize a user.
        
        Args:
            name: The user's name
            permissions: Set of permission strings
        """
        self.name = name
        self.permissions = permissions
    
    def __repr__(self) -> str:
        return f"User({self.name}, permissions={self.permissions})"


# Example usage for testing
@requires({"read"})
def read_data(user: User) -> str:
    """Read data (requires 'read' permission)."""
    return f"Data for {user.name}"


@requires({"write", "admin"})
def write_data(user: User, content: str) -> str:
    """Write data (requires 'write' and 'admin' permissions)."""
    return f"Wrote '{content}' for {user.name}"


@requires({"delete"})
def delete_resource(user: User, resource_id: int) -> str:
    """Delete a resource (requires 'delete' permission)."""
    return f"Deleted resource {resource_id}"
