"""Reference solution for Problem 02: Set Operations."""

from __future__ import annotations


def set_operations(set1: set[int], set2: set[int]) -> dict[str, set[int]]:
    """Perform union, intersection, and difference operations on two sets.

    Args:
        set1: First set of integers
        set2: Second set of integers

    Returns:
        A dictionary with keys 'union', 'intersection', and 'difference'
        containing the respective set operations results
    """
    return {
        "union": set1 | set2,
        "intersection": set1 & set2,
        "difference": set1 - set2,
    }
