"""Problem 03: Pure Counter - Solution."""

from __future__ import annotations


def increment_counter(current: int, step: int = 1) -> int:
    """Return the incremented counter value.

    This is a pure function - it doesn't modify any external state,
    it only returns a new value based on the inputs.

    Args:
        current: The current counter value.
        step: How much to increment by (default 1).

    Returns:
        The new counter value (current + step).
    """
    return current + step


def decrement_counter(current: int, step: int = 1) -> int:
    """Return the decremented counter value.

    This is a pure function - it doesn't modify any external state.

    Args:
        current: The current counter value.
        step: How much to decrement by (default 1).

    Returns:
        The new counter value (current - step).
    """
    return current - step


def reset_counter() -> int:
    """Return the initial counter value.

    Returns:
        The initial counter value (0).
    """
    return 0
