"""Problem 04: Find Maximum

Topic: Lists - Finding Extremes
Difficulty: Easy

Write a function that finds the maximum value in a list.

Function Signature:
    def find_max(numbers: list[int]) -> int | None

Requirements:
    - Return the largest integer in the list
    - Return None for an empty list
    - Handle negative numbers correctly

Behavior Notes:
    - Compare all elements to find the largest
    - None signals "no maximum" for empty list
    - Works with all negative numbers
    - You can use max() built-in or loop manually

Examples:
    >>> find_max([1, 5, 3, 9, 2])
    9
    
    >>> find_max([-5, -2, -10])
    -2
    
    Single element:
    >>> find_max([42])
    42
    
    Empty list:
    >>> find_max([])
    None

Input Validation:
    - You may assume numbers is a list of integers
    - Return None for empty list

"""

from __future__ import annotations


def find_max(numbers: list[int]) -> int | None:
    """Find the maximum value in a list.

    Args:
        numbers: A list of integers.

    Returns:
        The maximum value, or None if list is empty.
    """
    raise NotImplementedError("Implement find_max")
