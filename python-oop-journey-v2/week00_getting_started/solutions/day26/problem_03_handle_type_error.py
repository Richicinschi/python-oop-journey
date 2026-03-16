"""Reference solution for Problem 03: Handle TypeError."""

from __future__ import annotations


def safe_concat(a: any, b: any) -> str:
    """Safely concatenate two values as strings.

    Args:
        a: First value
        b: Second value

    Returns:
        Concatenated string representation
    """
    return str(a) + str(b)
