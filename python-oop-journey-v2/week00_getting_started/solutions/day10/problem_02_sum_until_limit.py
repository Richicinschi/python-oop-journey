"""Reference solution for Problem 02: Sum Until Limit."""

from __future__ import annotations


def sum_until_limit(limit: int) -> tuple[int, int]:
    """Sum numbers from 1 until sum exceeds limit.

    Args:
        limit: Maximum sum allowed

    Returns:
        Tuple of (count, total) where count is numbers added and total is their sum
    """
    total = 0
    count = 0
    current = 1

    while total + current <= limit:
        total += current
        count += 1
        current += 1

    return count, total
