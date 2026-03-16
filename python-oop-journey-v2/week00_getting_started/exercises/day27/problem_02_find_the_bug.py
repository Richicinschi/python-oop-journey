"""Problem 02: Find The Bug

Topic: Debugging Basics
Difficulty: Easy

The function below has a bug. Identify and fix it.

The function should return the maximum value in a list.

Examples:
    >>> find_max([1, 5, 3, 9, 2])
    9
    >>> find_max([-5, -2, -10])
    -2
    >>> find_max([5])
    5

Requirements:
    - Return the maximum value
    - Handle single-element lists
    - Handle negative numbers
"""

from __future__ import annotations


def find_max(numbers: list) -> int | None:
    """Find the maximum value in a list.

    Args:
        numbers: A list of numbers

    Returns:
        The maximum value, or None if list is empty
    """
    # Bug: This function doesn't work correctly for all cases
    if not numbers:
        return None
    
    max_val = 0  # <-- Bug is here
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val
