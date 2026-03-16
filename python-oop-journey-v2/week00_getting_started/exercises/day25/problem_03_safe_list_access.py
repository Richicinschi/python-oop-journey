"""Problem 03: Safe List Access

Topic: Try and Except
Difficulty: Medium

Write a function that safely accesses an element in a list.

Handle both IndexError (index out of range) and TypeError (not subscriptable).

Examples:
    >>> safe_get([1, 2, 3], 1)
    2
    >>> safe_get([1, 2, 3], 10)
    None
    >>> safe_get("not a list", 0)
    None

Requirements:
    - Return the element at the given index when successful
    - Return None if index is out of range
    - Return None if the data is not a list/tuple
"""

from __future__ import annotations


def safe_get(data: list, index: int) -> any:
    """Safely get an element from a list.

    Args:
        data: The list to access
        index: The index to retrieve

    Returns:
        The element at index, or None if access fails
    """
    raise NotImplementedError("Implement safe_get")
