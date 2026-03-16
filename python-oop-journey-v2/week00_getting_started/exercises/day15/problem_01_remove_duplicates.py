"""Problem 01: Remove Duplicates

Topic: Sets - Deduplication
Difficulty: Easy

Write a function that removes duplicates from a list while preserving order.

Function Signature:
    def remove_duplicates(items: list[str]) -> list[str]

Requirements:
    - Return a new list with duplicates removed
    - Preserve the original order of first occurrences
    - Use a set to track seen items efficiently

Behavior Notes:
    - Sets have O(1) lookup, making deduplication efficient
    - Preserve order: first occurrence stays, subsequent duplicates removed
    - Return a list (not a set) to maintain order

Examples:
    >>> remove_duplicates(["a", "b", "a", "c", "b", "d"])
    ['a', 'b', 'c', 'd']
    
    No duplicates:
    >>> remove_duplicates(["x", "y", "z"])
    ['x', 'y', 'z']
    
    All duplicates:
    >>> remove_duplicates(["a", "a", "a"])
    ['a']
    
    Empty list:
    >>> remove_duplicates([])
    []

Input Validation:
    - You may assume items is a list of strings

Implementation Hint:
    - Use a set to track seen items
    - Build result list, only add if not in seen set

"""

from __future__ import annotations


def remove_duplicates(items: list[str]) -> list[str]:
    """Remove duplicates from a list while preserving order.

    Args:
        items: A list of strings.

    Returns:
        A new list with duplicates removed.
    """
    raise NotImplementedError("Implement remove_duplicates")
