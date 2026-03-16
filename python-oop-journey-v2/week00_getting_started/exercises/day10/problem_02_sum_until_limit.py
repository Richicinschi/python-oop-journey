"""Problem 02: Sum Until Limit

Topic: While Loops, Accumulation
Difficulty: Easy

Write a function that sums numbers starting from 1 until the sum exceeds the limit.
Returns a tuple of (count, total) where count is how many numbers were added.

Examples:
    >>> sum_until_limit(10)
    (4, 10)  # 1 + 2 + 3 + 4 = 10
    >>> sum_until_limit(15)
    (5, 15)  # 1 + 2 + 3 + 4 + 5 = 15
    >>> sum_until_limit(5)
    (2, 3)   # 1 + 2 = 3 (next would be 6 > 5)

Requirements:
    - Use a while loop
    - Return tuple of (count, total)
    - Sum while total <= limit
"""

from __future__ import annotations


def sum_until_limit(limit: int) -> tuple[int, int]:
    """Sum numbers from 1 until sum exceeds limit.

    Args:
        limit: Maximum sum allowed

    Returns:
        Tuple of (count, total) where count is numbers added and total is their sum
    """
    raise NotImplementedError("Implement sum_until_limit")
