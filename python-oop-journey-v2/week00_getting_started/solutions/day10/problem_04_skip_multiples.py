"""Reference solution for Problem 04: Skip Multiples."""

from __future__ import annotations


def skip_multiples(n: int, k: int) -> int:
    """Sum numbers from 1 to n, skipping multiples of k.

    Args:
        n: Upper bound (inclusive)
        k: Multiple to skip

    Returns:
        Sum of numbers from 1 to n, excluding multiples of k
    """
    total = 0
    current = 1
    while current <= n:
        if current % k == 0:
            current += 1
            continue
        total += current
        current += 1
    return total
