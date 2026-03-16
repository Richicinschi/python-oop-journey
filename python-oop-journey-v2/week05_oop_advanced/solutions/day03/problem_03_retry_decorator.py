"""Reference solution for Problem 03: Retry Decorator."""

from __future__ import annotations

from functools import wraps
from time import sleep
from typing import Callable, Any, Type, Tuple


def retry(
    max_attempts: int = 3,
    delay: float = 0.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """A decorator that retries a function on specified exceptions.
    
    Args:
        max_attempts: Maximum number of attempts before giving up
        delay: Seconds to wait between attempts
        exceptions: Tuple of exception types to catch and retry
        
    Returns:
        A decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1 and delay > 0:
                        sleep(delay)
            
            # Re-raise the last exception if all attempts failed
            if last_exception:
                raise last_exception
            return None  # Should never reach here
        
        return wrapper
    return decorator


# Example usage for testing
class FlakyCounter:
    """Counter for testing retry decorator."""
    count: int = 0


@retry(max_attempts=3, delay=0.01)
def flaky_function() -> str:
    """A function that fails first 2 times."""
    FlakyCounter.count += 1
    if FlakyCounter.count < 3:
        raise RuntimeError(f"Attempt {FlakyCounter.count} failed")
    return "Success!"


@retry(max_attempts=2, exceptions=(ValueError,))
def specific_exception_only(x: int) -> int:
    """Only retry on ValueError."""
    if x < 0:
        raise ValueError("Negative value")
    return x * 2
