"""Reference solution for Problem 10: Rate Limit Decorator."""

from __future__ import annotations

from functools import wraps
from time import time
from typing import Callable, Any


def rate_limit(max_calls: int, period: float) -> Callable:
    """A decorator that limits function call rate.
    
    Allows at most `max_calls` within `period` seconds.
    Raises RuntimeError if rate limit is exceeded.
    
    Args:
        max_calls: Maximum number of calls allowed in the period
        period: Time period in seconds
        
    Returns:
        A decorator function
    """
    def decorator(func: Callable) -> Callable:
        # Track call timestamps
        call_times: list[float] = []
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_time = time()
            
            # Remove timestamps outside the current period
            cutoff_time = current_time - period
            call_times[:] = [t for t in call_times if t > cutoff_time]
            
            # Check if rate limit is exceeded
            if len(call_times) >= max_calls:
                raise RuntimeError(
                    f"Rate limit exceeded: {max_calls} calls per {period} seconds"
                )
            
            # Record this call and execute
            call_times.append(current_time)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Example usage for testing
@rate_limit(max_calls=3, period=1.0)
def api_call(endpoint: str) -> str:
    """Simulate an API call."""
    return f"Response from {endpoint}"


@rate_limit(max_calls=2, period=0.5)
def process_data(data: str) -> str:
    """Process some data."""
    return f"Processed: {data}"
