"""Reference solution for Problem 08: Deprecated Decorator."""

from __future__ import annotations

from functools import wraps
from typing import Callable, Any, Optional
import warnings


def deprecated(message: Optional[str] = None) -> Callable:
    """A decorator that marks functions as deprecated.
    
    Emits a DeprecationWarning when the decorated function is called.
    Optionally includes a custom message.
    
    Args:
        message: Optional custom deprecation message
        
    Returns:
        A decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warning_msg = message if message else f"{func.__name__} is deprecated"
            warnings.warn(
                warning_msg,
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Example usage for testing
@deprecated()
def old_function() -> str:
    """An old function that is deprecated."""
    return "I am old"


@deprecated("Use new_function() instead")
def another_old_function() -> str:
    """Another deprecated function with custom message."""
    return "I am also old"


@deprecated("Will be removed in v2.0")
def calculate_legacy(x: int, y: int) -> int:
    """A legacy calculation function."""
    return x + y
