"""Reference solution for Problem 03: Find In List."""

from __future__ import annotations


def find_in_list(items: list[int], target: int) -> int:
    """Find the index of target in items.

    Args:
        items: List of integers to search
        target: Value to find

    Returns:
        Index of target, or -1 if not found
    """
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1
