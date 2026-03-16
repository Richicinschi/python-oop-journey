"""Reference solution for Problem 02: Is In Range."""

from __future__ import annotations


def is_in_range(value: int, min_val: int, max_val: int) -> bool:
    """Check if value is within the inclusive range [min_val, max_val].

    Args:
        value: The number to check
        min_val: The minimum value of the range (inclusive)
        max_val: The maximum value of the range (inclusive)

    Returns:
        True if value is within range, False otherwise
    """
    return min_val <= value <= max_val
