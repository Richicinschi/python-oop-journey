"""Problem 04: Is Perfect Square

Topic: Mathematical operations, boolean logic
Difficulty: Easy

Write a function that checks if a number is a perfect square.

A perfect square is an integer that is the square of an integer.
Examples: 0, 1, 4, 9, 16, 25, 36, ...

Examples:
    >>> is_perfect_square(16)
    True
    >>> is_perfect_square(25)
    True
    >>> is_perfect_square(26)
    False
    >>> is_perfect_square(0)
    True

Requirements:
    - Return True if n is a perfect square, False otherwise
    - Handle negative numbers (they are not perfect squares)
    - Zero is considered a perfect square (0 = 0²)
"""

from __future__ import annotations

import math


def is_perfect_square(n: int) -> bool:
    """Check if a number is a perfect square.

    Args:
        n: Integer to check

    Returns:
        True if n is a perfect square, False otherwise
    """
    raise NotImplementedError("Implement is_perfect_square")
