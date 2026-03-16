"""Problem 04: Skip Multiples

Topic: While Loops, Continue
Difficulty: Easy

Write a function that sums numbers from 1 to n, skipping multiples of k.

Examples:
    >>> skip_multiples(10, 3)
    37  # 1 + 2 + 4 + 5 + 7 + 8 + 10 = 37 (skip 3, 6, 9)
    >>> skip_multiples(10, 2)
    25  # 1 + 3 + 5 + 7 + 9 = 25 (skip even numbers)
    >>> skip_multiples(5, 10)
    15  # 1 + 2 + 3 + 4 + 5 = 15 (no multiples of 10 to skip)

Requirements:
    - Use a while loop with continue
    - Use modulo operator to check multiples
    - Return the sum
"""

from __future__ import annotations


def skip_multiples(n: int, k: int) -> int:
    """Sum numbers from 1 to n, skipping multiples of k.

    Args:
        n: Upper bound (inclusive)
        k: Multiple to skip

    Returns:
        Sum of numbers from 1 to n, excluding multiples of k
    """
    raise NotImplementedError("Implement skip_multiples")
