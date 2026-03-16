"""Problem 10: Rate Limit Decorator

Topic: Limit Call Rate
Difficulty: Hard

Create a parameterized decorator that limits how often a function can be called.

This demonstrates maintaining state across function calls and implementing
rate limiting - an essential pattern for API clients, web scraping, and
preventing resource exhaustion. Uses a sliding window algorithm.

Example:
    >>> @rate_limit(max_calls=3, period=1.0)
    ... def api_call(endpoint: str) -> str:
    ...     return f"Response from {endpoint}"
    
    >>> api_call("/users")  # Success
    'Response from /users'
    >>> api_call("/posts")  # Success
    'Response from /posts'
    >>> api_call("/comments")  # Success
    'Response from /comments'
    >>> api_call("/stats")  # Raises RuntimeError (limit exceeded)
    Traceback (most recent call last):
        ...
    RuntimeError: Rate limit exceeded: 3 calls per 1.0 seconds

    >>> @rate_limit(max_calls=2, period=0.5)
    ... def process(data: str) -> str:
    ...     return f"Processed: {data}"
    
    >>> process("a")  # Success
    'Processed: a'
    >>> process("b")  # Success
    'Processed: b'
    >>> process("c")  # Raises RuntimeError
    Traceback (most recent call last):
        ...
    RuntimeError: Rate limit exceeded: 2 calls per 0.5 seconds

Behavior Notes:
    - Tracks call timestamps in a list stored in the closure
    - Before each call, removes timestamps older than 'period' seconds
    - If call count >= max_calls, raises RuntimeError with specific message
    - The message format is: "Rate limit exceeded: {max_calls} calls per {period} seconds"
    - Otherwise records the call and executes the function

Edge Cases:
    - Multiple decorated functions each have their own rate limit state
    - The same function called from different places shares the same limit
    - The sliding window uses time.time() for timestamps
    - Rate limit resets automatically after 'period' seconds of inactivity
    - Setting max_calls=0 should always raise RuntimeError
    - Very short periods (near 0) effectively disable rate limiting
"""

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
    raise NotImplementedError("Implement the rate_limit decorator")


# Hints for Rate Limit Decorator (Hard):
# 
# Hint 1 - Conceptual nudge:
# This needs a decorator factory (parameterized decorator). You need to track call
# times per decorated function.
#
# Hint 2 - Structural plan:
# - Outer function takes max_calls and period, returns actual decorator
# - Decorator receives the function, returns wrapper
# - Wrapper maintains a list of call timestamps
# - Before each call, remove timestamps older than period, then check count
# - Use time.time() for timestamps
#
# Hint 3 - Edge-case warning:
# Each decorated function needs its OWN call history. Don't use a shared list!
# Use a closure variable or function attribute. Also, preserve function metadata
# with @functools.wraps.
