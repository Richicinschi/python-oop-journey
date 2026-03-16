"""Reference solution for Problem 03: Tuple Statistics."""

from __future__ import annotations


def tuple_statistics(nums: tuple[int, ...]) -> tuple[int, int, int] | None:
    """Return min, max, and count of elements in a tuple.

    Args:
        nums: A tuple of integers (can be any length)

    Returns:
        A tuple of (minimum, maximum, count), or None if empty
    """
    if not nums:
        return None
    
    return min(nums), max(nums), len(nums)
