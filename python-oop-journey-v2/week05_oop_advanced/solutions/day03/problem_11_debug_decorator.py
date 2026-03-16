"""Reference solution for Problem 11: Debug Decorator."""

from __future__ import annotations

from functools import wraps
from typing import Callable, Any


def debug(func: Callable) -> Callable:
    """A decorator that prints debug information about function calls.
    
    Prints:
    - Function name and signature
    - Arguments (args and kwargs)
    - Return value
    
    Format:
    "DEBUG: Calling <func_name>(<args_repr>)"
    "DEBUG: <func_name> returned <result_repr>"
    
    Args:
        func: The function to decorate
        
    Returns:
        The wrapper function with debug output
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Format arguments
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        
        print(f"DEBUG: Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"DEBUG: {func.__name__} returned {result!r}")
        
        return result
    
    return wrapper


# Example usage for testing
@debug
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@debug
def greet(name: str, greeting: str = "Hello") -> str:
    """Greet someone."""
    return f"{greeting}, {name}!"


@debug
def create_user(username: str, age: int, active: bool = True) -> dict[str, Any]:
    """Create a user dictionary."""
    return {
        "username": username,
        "age": age,
        "active": active
    }
