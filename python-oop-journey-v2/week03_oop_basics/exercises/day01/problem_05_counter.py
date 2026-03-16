"""Problem 05: Counter

Topic: Simple state manipulation
Difficulty: Easy

Create a Counter class that can be incremented and decremented.

Examples:
    >>> counter = Counter()
    >>> counter.get_count()
    0
    >>> counter.increment()
    1
    >>> counter.increment()
    2
    >>> counter.decrement()
    1
    >>> counter.reset()
    >>> counter.get_count()
    0
    >>> counter2 = Counter(10)
    >>> counter2.get_count()
    10

Requirements:
    - __init__ takes optional start_value (int, default 0)
    - increment() increases count by 1, returns new count
    - decrement() decreases count by 1, returns new count
    - reset() resets count to initial value
    - get_count() returns current count
"""

from __future__ import annotations


class Counter:
    """A simple counter class that can be incremented and decremented."""

    def __init__(self, start_value: int = 0) -> None:
        """Initialize counter with optional start value."""
        raise NotImplementedError("Initialize count and initial_value")

    def increment(self) -> int:
        """Increment the counter by 1 and return the new count."""
        raise NotImplementedError("Implement increment method")

    def decrement(self) -> int:
        """Decrement the counter by 1 and return the new count."""
        raise NotImplementedError("Implement decrement method")

    def reset(self) -> None:
        """Reset the counter to its initial value."""
        raise NotImplementedError("Implement reset method")

    def get_count(self) -> int:
        """Return the current count."""
        raise NotImplementedError("Implement get_count method")

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        raise NotImplementedError("Implement __str__ method")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        raise NotImplementedError("Implement __repr__ method")
