"""Reference solution for Problem 02: Import Tracker."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar

# Module-level storage for call counts
_call_counts: dict[str, int] = {}

F = TypeVar("F", bound=Callable)


def track_calls(func: F) -> F:
    """Decorator that tracks how many times a function is called.
    
    Args:
        func: The function to track
        
    Returns:
        The wrapped function with call tracking
    """
    func_name = f"{func.__module__}.{func.__qualname__}"
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        _call_counts[func_name] = _call_counts.get(func_name, 0) + 1
        return func(*args, **kwargs)
    
    return wrapper  # type: ignore[return-value]


def get_call_count(func: Callable) -> int:
    """Get the call count for a specific function.
    
    Args:
        func: The function to query
        
    Returns:
        Number of times the function has been called
    """
    func_name = f"{func.__module__}.{func.__qualname__}"
    return _call_counts.get(func_name, 0)


def get_all_call_counts() -> dict[str, int]:
    """Get all call counts as a dictionary.
    
    Returns:
        Dictionary mapping function names to call counts
    """
    return dict(_call_counts)


def reset_call_counts() -> None:
    """Reset all call counts to zero."""
    _call_counts.clear()
