"""Problem 01: Flatten Nested List

Topic: List Comprehensions, Nested Structures
Difficulty: Easy

Flatten a nested list (list of lists) into a single flat list using
a list comprehension.
"""

from __future__ import annotations


def flatten_nested_list(nested: list[list[int]]) -> list[int]:
    """Flatten a nested list into a single list.

    Args:
        nested: A list of lists containing integers.

    Returns:
        A single flat list with all integers in row-major order.

    Example:
        >>> flatten_nested_list([[1, 2], [3, 4], [5, 6]])
        [1, 2, 3, 4, 5, 6]
        >>> flatten_nested_list([[1], [2, 3], [], [4]])
        [1, 2, 3, 4]
    """
    raise NotImplementedError("Implement flatten_nested_list")
