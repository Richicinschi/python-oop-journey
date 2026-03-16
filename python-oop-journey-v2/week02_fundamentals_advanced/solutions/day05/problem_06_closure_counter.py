"""Problem 06: Closure Counter - Solution

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
    count = start - step  # Start one step behind so first call returns 'start'

    def counter() -> int:
        nonlocal count
        count += step
        return count

    return counter


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
    # Initialize counters for each channel to -1 so first call returns 0
    counts = [-1] * n

    def counter(channel: int) -> int:
        if not 0 <= channel < n:
            raise ValueError(f"Channel must be between 0 and {n-1}")
        counts[channel] += 1
        return counts[channel]

    return counter


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
    # For this simplified model:
    # - We track calls in fixed windows of size window_seconds
    # - Each window can have up to max_calls calls
    # - When we enter a new window, the counter resets
    calls_in_current_window = 0
    window_call_count = 0  # Count calls to track window boundaries

    def limiter() -> bool:
        nonlocal calls_in_current_window, window_call_count

        window_call_count += 1

        # Check if we're starting a new window
        # Windows are: [1, window_seconds], [window_seconds+1, 2*window_seconds], etc.
        if (window_call_count - 1) % window_seconds == 0 and window_call_count > 1:
            # Start of a new window (after the first)
            calls_in_current_window = 0

        if calls_in_current_window < max_calls:
            calls_in_current_window += 1
            return True
        return False

    return limiter


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
    def multiplier(x: int) -> int:
        return x * n

    return multiplier
