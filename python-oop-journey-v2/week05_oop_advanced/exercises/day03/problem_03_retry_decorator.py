"""Problem 03: Retry Decorator

Topic: Retry on Failure
Difficulty: Medium

Create a parameterized decorator that retries a function on specified exceptions.

This demonstrates parameterized decorators - decorators that accept arguments
and return the actual decorator. Useful for handling transient failures in
network calls, database operations, or flaky external services.

Example:
    >>> @retry(max_attempts=3, delay=0.1, exceptions=(ConnectionError,))
    ... def fetch_data(url: str) -> str:
    ...     # Simulates flaky network
    ...     import random
    ...     if random.random() < 0.7:
    ...         raise ConnectionError("Network error")
    ...     return f"Data from {url}"
    
    >>> fetch_data("http://api.example.com")  # May retry up to 3 times
    'Data from http://api.example.com'

    >>> call_count = 0
    >>> @retry(max_attempts=3, delay=0.01)
    ... def might_fail():
    ...     global call_count
    ...     call_count += 1
    ...     if call_count < 3:
    ...         raise ValueError("Not yet")
    ...     return "Success!"
    
    >>> might_fail()  # Retries twice, succeeds on third attempt
    'Success!'

Behavior Notes:
    - Calls the function up to max_attempts times
    - Waits 'delay' seconds between attempts (use time.sleep)
    - Only catches exceptions specified in the 'exceptions' tuple
    - Returns immediately on first successful call
    - If all attempts fail, raises the last exception

Edge Cases:
    - If max_attempts is 1, the function is called once (no retries)
    - If delay is 0, retries immediately without waiting
    - Exceptions not in the tuple propagate immediately (no retry)
    - The original exception is preserved and re-raised after final failure
"""

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
    raise NotImplementedError("Implement the retry decorator")


# Hints for Retry Decorator (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to catch specific exceptions and retry the function call. Use a loop
# with a try/except block.
#
# Hint 2 - Structural plan:
# - Outer function (factory) takes max_attempts, delay, exceptions
# - Decorator receives the function, returns wrapper
# - Wrapper uses a for loop for attempts
# - Try to call the function, return result on success
# - On exception, sleep for delay, then retry
# - If all attempts fail, re-raise the last exception
#
# Hint 3 - Edge-case warning:
# What if delay is 0? You might still want a small backoff. Also, what if the
# decorated function is a generator? The retry logic becomes more complex.
