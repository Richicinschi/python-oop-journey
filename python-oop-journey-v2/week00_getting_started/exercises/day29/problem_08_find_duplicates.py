"""Problem 08: Find Duplicates Efficiently

Topic: Sets, dictionaries, algorithm efficiency
Difficulty: Medium

Create efficient functions to find duplicates in collections.

Required functions:
- find_duplicates(items): Find all items that appear more than once
- find_first_duplicate(items): Find first item that appears twice
- count_duplicates(items): Count occurrences of each duplicate
- remove_duplicates_keep_order(items): Remove duplicates preserving order

Efficiency considerations:
- Use sets for O(1) lookup when appropriate
- Avoid O(n²) approaches for large lists

Example:
    >>> find_duplicates([1, 2, 3, 2, 4, 3, 5])
    {2, 3}
    >>> find_first_duplicate([1, 2, 3, 2, 4, 3])
    2
    >>> count_duplicates([1, 2, 2, 3, 3, 3])
    {2: 2, 3: 3}
    >>> remove_duplicates_keep_order([1, 2, 1, 3, 2, 4])
    [1, 2, 3, 4]
"""

from __future__ import annotations


def find_duplicates(items: list) -> set:
    """Find all items that appear more than once.

    Args:
        items: List of items (must be hashable)

    Returns:
        Set of items that appear multiple times
    """
    raise NotImplementedError("Implement find_duplicates")


def find_first_duplicate(items: list) -> any:
    """Find the first item that appears twice.

    Args:
        items: List of items (must be hashable)

    Returns:
        First duplicate item found, or None if no duplicates
    """
    raise NotImplementedError("Implement find_first_duplicate")


def count_duplicates(items: list) -> dict[any, int]:
    """Count occurrences of each duplicate item.

    Args:
        items: List of items (must be hashable)

    Returns:
        Dictionary mapping duplicate items to their occurrence counts
    """
    raise NotImplementedError("Implement count_duplicates")


def remove_duplicates_keep_order(items: list) -> list:
    """Remove duplicates while preserving original order.

    Args:
        items: List of items (must be hashable)

    Returns:
        List with duplicates removed, first occurrence kept
    """
    raise NotImplementedError("Implement remove_duplicates_keep_order")
