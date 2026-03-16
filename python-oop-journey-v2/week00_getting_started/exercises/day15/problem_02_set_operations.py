"""Problem 02: Set Operations

Topic: Sets - Mathematical Operations
Difficulty: Easy

Write a function that performs basic set operations on two lists.

Function Signature:
    def set_operations(list1: list[int], list2: list[int]) -> dict[str, set[int]]

Requirements:
    - Return a dictionary with three set operations:
      - 'union': all elements in either set
      - 'intersection': elements common to both
      - 'difference': elements in list1 but not in list2

Behavior Notes:
    - Convert lists to sets first
    - Use set operators: | for union, & for intersection, - for difference
    - Or use methods: union(), intersection(), difference()

Examples:
    >>> set_operations([1, 2, 3], [2, 3, 4])
    {'union': {1, 2, 3, 4}, 'intersection': {2, 3}, 'difference': {1}}
    
    No overlap:
    >>> set_operations([1, 2], [3, 4])
    {'union': {1, 2, 3, 4}, 'intersection': set(), 'difference': {1, 2}}
    
    Empty lists:
    >>> set_operations([], [1, 2])
    {'union': {1, 2}, 'intersection': set(), 'difference': set()}

Input Validation:
    - You may assume both are lists of integers

"""

from __future__ import annotations


def set_operations(list1: list[int], list2: list[int]) -> dict[str, set[int]]:
    """Perform set operations on two lists.

    Args:
        list1: First list of integers.
        list2: Second list of integers.

    Returns:
        A dictionary with 'union', 'intersection', and 'difference' sets.
    """
    raise NotImplementedError("Implement set_operations")
