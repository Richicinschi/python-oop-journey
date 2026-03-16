"""Problem 01: Create and Access List

Topic: Lists - Creating and Indexing
Difficulty: Easy

Write a function that creates a list and accesses elements by index.

Function Signature:
    def create_and_access(numbers: list[int], index: int) -> int | None

Requirements:
    - Return the element at the given index
    - Return None if index is out of range (negative or too large)
    - Handle empty list gracefully

Behavior Notes:
    - Python lists are 0-indexed (first element is at index 0)
    - IndexError occurs when accessing beyond list bounds
    - Negative indices count from the end (-1 is last element)
    - But for this exercise, treat negative indices as invalid (return None)

Examples:
    >>> create_and_access([10, 20, 30], 0)
    10
    
    >>> create_and_access([10, 20, 30], 2)
    30
    
    Index out of range:
    >>> create_and_access([10, 20], 5)
    None
    
    Negative index (treat as invalid for this exercise):
    >>> create_and_access([10, 20], -1)
    None
    
    Empty list:
    >>> create_and_access([], 0)
    None

Input Validation:
    - You may assume numbers is a list of integers
    - index may be any integer (positive, negative, or zero)
    - Return None for any invalid index

"""

from __future__ import annotations


def create_and_access(numbers: list[int], index: int) -> int | None:
    """Return the element at the given index, or None if index is out of range.

    Args:
        numbers: A list of integers.
        index: The index to access.

    Returns:
        The element at the index, or None if index is invalid.
    """
    raise NotImplementedError("Implement create_and_access")
