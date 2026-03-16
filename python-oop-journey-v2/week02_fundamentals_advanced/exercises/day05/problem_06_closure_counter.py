"""Problem 06: Closure Counter

Implement counters and stateful functions using closures
to maintain private state between function calls.
"""

from __future__ import annotations

from typing import Callable


def create_counter(start: int = 0, step: int = 1) -> Callable[[], int]:
    """Create a counter that increments by step each call.

    Args:
        start: Initial value of the counter.
        step: Amount to increment by each call.

    Returns:
        A function that returns the next counter value on each call.

    Example:
        >>> counter = create_counter(10, 2)
        >>> counter()
        10
        >>> counter()
        12
        >>> counter()
        14
    """
    raise NotImplementedError("Implement create_counter")


def create_multi_counter(n: int) -> Callable[[int], int]:
    """Create a counter with multiple independent channels.

    Args:
        n: Number of independent counters.

    Returns:
        A function that takes a channel index (0 to n-1) and returns
        the next value for that channel.

    Example:
        >>> mc = create_multi_counter(3)
        >>> mc(0)  # Channel 0
        0
        >>> mc(1)  # Channel 1
        0
        >>> mc(0)  # Channel 0 again
        1
        >>> mc(1)  # Channel 1 again
        1
    """
    raise NotImplementedError("Implement create_multi_counter")


def create_rate_limiter(max_calls: int, window_seconds: int) -> Callable[[], bool]:
    """Create a rate limiter that allows max_calls per window.

    Args:
        max_calls: Maximum number of calls allowed.
        window_seconds: Time window in seconds (simulated).

    Returns:
        A function that returns True if the call is allowed,
        False if rate limit is exceeded.

    Note: For this exercise, each "call" to the limiter represents
    one second passing. So window_seconds represents the number of
    calls before the window resets.

    Example:
        >>> limiter = create_rate_limiter(3, 5)
        >>> limiter()  # Call 1 of 3
        True
        >>> limiter()  # Call 2 of 3
        True
        >>> limiter()  # Call 3 of 3
        True
        >>> limiter()  # Exceeded limit
        False
    """
    raise NotImplementedError("Implement create_rate_limiter")


def make_multiplier_of(n: int) -> Callable[[int], int]:
    """Create a multiplier function that multiplies by n.

    Args:
        n: The multiplier value.

    Returns:
        A function that takes a value and returns value * n.

    Example:
        >>> double = make_multiplier_of(2)
        >>> triple = make_multiplier_of(3)
        >>> double(5)
        10
        >>> triple(5)
        15
    """
    raise NotImplementedError("Implement make_multiplier_of")
