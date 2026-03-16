"""Reference solution for Problem 01: Count Down."""

from __future__ import annotations


def count_down(n: int) -> list[int]:
    """Count down from n to 1.

    Args:
        n: Starting number

    Returns:
        List of integers from n down to 1
    """
    result: list[int] = []
    current = n
    while current > 0:
        result.append(current)
        current -= 1
    return result
