"""Reference solution for Problem 01: Check Equality."""

from __future__ import annotations


def check_equality(a: int | str | float, b: int | str | float) -> bool:
    """Check if two values are equal.

    Args:
        a: First value to compare
        b: Second value to compare

    Returns:
        True if a equals b, False otherwise
    """
    return a == b
