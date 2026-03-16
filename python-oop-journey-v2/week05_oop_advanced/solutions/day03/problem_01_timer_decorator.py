"""Reference solution for Problem 01: Timer Decorator."""

from __future__ import annotations

from functools import wraps
from time import perf_counter
from typing import Callable, Any


def timer(func: Callable) -> Callable:
    """A decorator that times function execution.
    
    Prints the elapsed time with 4 decimal places in the format:
    "<function_name> took <elapsed_time:.4f} seconds"
    
    Args:
        func: The function to decorate
        
    Returns:
        The wrapper function that times execution
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper


# Example usage for testing
@timer
def slow_function() -> str:
    """A slow function for testing."""
    import time
    time.sleep(0.01)
    return "Done"


@timer
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
