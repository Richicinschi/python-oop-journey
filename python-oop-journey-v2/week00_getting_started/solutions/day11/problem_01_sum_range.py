"""Reference solution for Problem 01: Sum Range."""

from __future__ import annotations


def sum_range(start: int, end: int) -> int:
    """Sum all integers from start to end (inclusive).

    Args:
        start: Starting number
        end: Ending number

    Returns:
        Sum of all integers from start to end, or 0 if start > end
    """
    if start > end:
        return 0

    total = 0
    for i in range(start, end + 1):
        total += i
    return total
