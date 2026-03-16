"""Reference solution for Problem 05: Find Common Elements."""

from __future__ import annotations


def find_common(list1: list[int], list2: list[int]) -> list[int]:
    """Find common elements between two lists.

    Args:
        list1: First list of integers
        list2: Second list of integers

    Returns:
        A sorted list of elements common to both input lists
    """
    common = set(list1) & set(list2)
    return sorted(common)
