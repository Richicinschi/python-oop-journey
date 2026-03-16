"""Problem 03: Is Even - Solution."""

from __future__ import annotations


def is_even(number: int) -> bool:
    """Determine if a number is even.

    Args:
        number: The integer to check.

    Returns:
        True if the number is even, False otherwise.
    """
    return number % 2 == 0
