"""Problem 01: Sum Range

Topic: For Loops, range()
Difficulty: Easy

Write a function that returns the sum of all integers from start to end (inclusive).

Examples:
    >>> sum_range(1, 5)
    15  # 1 + 2 + 3 + 4 + 5 = 15
    >>> sum_range(3, 3)
    3   # Single number
    >>> sum_range(1, 1)
    1

Requirements:
    - Use a for loop with range()
    - Handle the case where start > end (return 0)
"""

from __future__ import annotations


def sum_range(start: int, end: int) -> int:
    """Sum all integers from start to end (inclusive).

    Args:
        start: Starting number
        end: Ending number

    Returns:
        Sum of all integers from start to end, or 0 if start > end
    """
    raise NotImplementedError("Implement sum_range")
