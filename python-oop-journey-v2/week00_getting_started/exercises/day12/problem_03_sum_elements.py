"""Problem 03: Sum List Elements

Topic: Lists - Aggregation
Difficulty: Easy

Write a function that calculates the sum of all elements in a list.

Function Signature:
    def sum_elements(numbers: list[int]) -> int

Requirements:
    - Return the sum of all integers in the list
    - Return 0 for an empty list
    - Handle negative numbers correctly

Behavior Notes:
    - Empty list sum is 0 (identity for addition)
    - Negative numbers reduce the sum
    - You can use sum() built-in or loop manually

Examples:
    >>> sum_elements([1, 2, 3, 4])
    10
    
    >>> sum_elements([10, -5, 3])
    8
    
    Empty list:
    >>> sum_elements([])
    0
    
    Single element:
    >>> sum_elements([42])
    42
    
    All negative:
    >>> sum_elements([-1, -2, -3])
    -6

Input Validation:
    - You may assume numbers is a list of integers
    - List may be empty

"""

from __future__ import annotations


def sum_elements(numbers: list[int]) -> int:
    """Calculate the sum of all elements in a list.

    Args:
        numbers: A list of integers.

    Returns:
        The sum of all elements (0 for empty list).
    """
    raise NotImplementedError("Implement sum_elements")
