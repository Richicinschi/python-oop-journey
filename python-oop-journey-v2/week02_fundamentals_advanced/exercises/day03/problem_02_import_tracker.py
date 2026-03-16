"""Problem 02: Import Tracker

Topic: Decorators with module state, function metadata
Difficulty: Easy

Create a decorator that tracks how many times functions have been called.
The tracker should store call counts in module-level state and provide
utilities to query and reset statistics.

Requirements:
    - Create a @track_calls decorator that counts function calls
    - Provide get_call_count(func) to get count for a specific function
    - Provide get_all_call_counts() to get dict of all counts
    - Provide reset_call_counts() to reset all counters
    - The decorator must preserve function metadata

Example:
    @track_calls
    def greet(name):
        return f"Hello, {name}!"
    
    greet("Alice")
    greet("Bob")
    print(get_call_count(greet))  # 2
    
    reset_call_counts()
    print(get_call_count(greet))  # 0
"""

from __future__ import annotations

from functools import wraps
from typing import Callable, TypeVar

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
    raise NotImplementedError("Implement track_calls decorator")


def get_call_count(func: Callable) -> int:
    """Get the call count for a specific function.
    
    Args:
        func: The function to query
        
    Returns:
        Number of times the function has been called
    """
    raise NotImplementedError("Implement get_call_count")


def get_all_call_counts() -> dict[str, int]:
    """Get all call counts as a dictionary.
    
    Returns:
        Dictionary mapping function names to call counts
    """
    raise NotImplementedError("Implement get_all_call_counts")


def reset_call_counts() -> None:
    """Reset all call counts to zero."""
    raise NotImplementedError("Implement reset_call_counts")
