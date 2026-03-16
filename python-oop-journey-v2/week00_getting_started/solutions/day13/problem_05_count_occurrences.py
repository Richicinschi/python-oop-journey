"""Reference solution for Problem 05: Count Occurrences."""

from __future__ import annotations


def count_occurrences(data: tuple[int, ...], target: int) -> int:
    """Count how many times a value appears in a tuple.

    Args:
        data: A tuple of integers
        target: The value to count

    Returns:
        The number of occurrences of target
    """
    return data.count(target)
