"""Problem 03: Find First Divisible

Topic: While Loops, Break
Difficulty: Easy

Write a function that finds the first number >= start that is divisible by divisor.

Examples:
    >>> find_first_divisible(10, 7)
    14
    >>> find_first_divisible(1, 5)
    5
    >>> find_first_divisible(15, 5)
    15
    >>> find_first_divisible(100, 25)
    100

Requirements:
    - Use a while loop with break
    - Return the first divisible number
    - divisor will always be positive
"""

from __future__ import annotations


def find_first_divisible(start: int, divisor: int) -> int:
    """Find the first number >= start divisible by divisor.

    Args:
        start: Starting number (inclusive)
        divisor: Number to check divisibility by

    Returns:
        First number >= start that is divisible by divisor
    """
    raise NotImplementedError("Implement find_first_divisible")
