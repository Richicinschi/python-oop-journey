"""Reference solution for Problem 03: Find Maximum."""

from __future__ import annotations


def find_maximum(a: int | float, b: int | float, c: int | float) -> int | float:
    """Find the maximum of three numbers.

    Args:
        a: First number
        b: Second number
        c: Third number

    Returns:
        The maximum value among a, b, and c
    """
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c
