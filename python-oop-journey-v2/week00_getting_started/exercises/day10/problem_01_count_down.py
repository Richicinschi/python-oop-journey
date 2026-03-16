"""Problem 01: Count Down

Topic: While Loops
Difficulty: Easy

Write a function that counts down from n to 1 and returns a list of numbers.

Examples:
    >>> count_down(5)
    [5, 4, 3, 2, 1]
    >>> count_down(3)
    [3, 2, 1]
    >>> count_down(1)
    [1]
    >>> count_down(0)
    []

Requirements:
    - Use a while loop
    - Return a list of integers
    - If n <= 0, return empty list
"""

from __future__ import annotations


def count_down(n: int) -> list[int]:
    """Count down from n to 1.

    Args:
        n: Starting number

    Returns:
        List of integers from n down to 1
    """
    raise NotImplementedError("Implement count_down")
