"""Reference solution for Problem 05: Counter."""

from __future__ import annotations


class Counter:
    """A simple counter class that can be incremented and decremented."""

    def __init__(self, start_value: int = 0) -> None:
        """Initialize counter with optional start value.
        
        Args:
            start_value: Initial count value (default 0)
        """
        self._initial_value = start_value
        self._count = start_value

    def increment(self) -> int:
        """Increment the counter by 1 and return the new count."""
        self._count += 1
        return self._count

    def decrement(self) -> int:
        """Decrement the counter by 1 and return the new count."""
        self._count -= 1
        return self._count

    def reset(self) -> None:
        """Reset the counter to its initial value."""
        self._count = self._initial_value

    def get_count(self) -> int:
        """Return the current count."""
        return self._count

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        return f"Counter(count={self._count})"

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"Counter(start_value={self._initial_value}, current={self._count})"
