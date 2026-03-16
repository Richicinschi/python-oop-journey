"""Reference solution for Problem 09: Counted Decorator."""

from __future__ import annotations

from functools import wraps
from typing import Callable, Any


def counted(func: Callable) -> Callable:
    """A decorator that counts function calls.
    
    Adds a `call_count` attribute to the function that tracks
    how many times it has been called.
    
    Args:
        func: The function to decorate
        
    Returns:
        The wrapper function with call counting
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        wrapper.call_count += 1
        return func(*args, **kwargs)
    
    wrapper.call_count = 0
    return wrapper


# Example usage for testing
@counted
def increment(x: int) -> int:
    """Increment a number."""
    return x + 1


@counted
def greet(name: str, greeting: str = "Hello") -> str:
    """Greet someone."""
    return f"{greeting}, {name}!"


@counted
def factorial(n: int) -> int:
    """Calculate factorial."""
    if n < 2:
        return 1 if n >= 0 else 0
    return n * factorial(n - 1)
