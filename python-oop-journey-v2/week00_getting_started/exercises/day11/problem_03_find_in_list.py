"""Problem 03: Find In List

Topic: For Loops, Iterating lists, Break
Difficulty: Easy

Write a function that finds the index of a target value in a list.
Returns -1 if not found.

Examples:
    >>> find_in_list([1, 2, 3, 4, 5], 3)
    2
    >>> find_in_list([10, 20, 30], 10)
    0
    >>> find_in_list([1, 2, 3], 5)
    -1
    >>> find_in_list([], 1)
    -1

Requirements:
    - Use a for loop with enumerate()
    - Use break when target is found
    - Return -1 if target not in list
"""

from __future__ import annotations


def find_in_list(items: list[int], target: int) -> int:
    """Find the index of target in items.

    Args:
        items: List of integers to search
        target: Value to find

    Returns:
        Index of target, or -1 if not found
    """
    raise NotImplementedError("Implement find_in_list")
