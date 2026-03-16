"""Reference solution for Problem 05: Fix Off By One."""

from __future__ import annotations


def sum_evens(n: int) -> int:
    """Sum all even numbers from 0 to n (inclusive).

    Args:
        n: The upper bound (inclusive)

    Returns:
        Sum of even numbers from 0 to n
    """
    if n < 0:
        return 0
    
    # Fixed: range should start at 0 and go to n+1 to include n
    total = 0
    for i in range(0, n + 1):
        if i % 2 == 0:
            total += i
    return total
