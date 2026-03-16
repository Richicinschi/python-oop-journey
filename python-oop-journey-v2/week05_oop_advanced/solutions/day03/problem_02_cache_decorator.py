"""Reference solution for Problem 02: Cache Decorator."""

from __future__ import annotations

from functools import wraps
from typing import Callable, Any, Hashable


def cache(func: Callable) -> Callable:
    """A decorator that caches function results.
    
    Uses a dictionary to store results keyed by arguments.
    Only works with hashable arguments.
    
    Args:
        func: The function to decorate
        
    Returns:
        The wrapper function with caching
    """
    _cache: dict = {}
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Create a cache key from args and kwargs
        key = (args, tuple(sorted(kwargs.items())))
        if key not in _cache:
            _cache[key] = func(*args, **kwargs)
        return _cache[key]
    return wrapper


# Example usage for testing
@cache
def fibonacci(n: int) -> int:
    """Calculate fibonacci number (slow without cache)."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@cache
def greet(name: str, greeting: str = "Hello") -> str:
    """Greet someone."""
    return f"{greeting}, {name}!"
