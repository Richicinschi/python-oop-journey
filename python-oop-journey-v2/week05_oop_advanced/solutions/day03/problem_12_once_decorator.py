"""Reference solution for Problem 12: Once Decorator."""

from __future__ import annotations

from functools import wraps
from typing import Callable, Any


def once(func: Callable) -> Callable:
    """A decorator that ensures a function runs only once.
    
    Subsequent calls return the result from the first call without
    re-executing the function.
    
    Args:
        func: The function to decorate
        
    Returns:
        The wrapper function that runs only once
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if not wrapper.has_run:
            wrapper.has_run = True
            try:
                wrapper.result = func(*args, **kwargs)
            except Exception as e:
                wrapper.exception = e
                raise
        elif hasattr(wrapper, 'exception'):
            raise wrapper.exception
        return wrapper.result
    
    wrapper.has_run = False
    wrapper.result = None
    return wrapper


# Example usage for testing
call_count = 0


@once
def initialize() -> str:
    """Initialize something (should only run once)."""
    global call_count
    call_count += 1
    return f"Initialized (call #{call_count})"


@once
def expensive_computation(x: int) -> int:
    """An expensive computation (should only run once)."""
    global call_count
    call_count += 1
    # Simulate expensive operation
    return x * x * x


@once
def configure(settings: dict[str, Any]) -> dict[str, Any]:
    """Configure with settings (should only run once)."""
    global call_count
    call_count += 1
    return settings.copy()
