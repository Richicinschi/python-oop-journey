"""Reference solution for Problem 06: Count Even Digits."""

from __future__ import annotations


def count_even_digits(n: int) -> int:
    """Count the number of even digits in an integer.

    Args:
        n: Integer to analyze

    Returns:
        Count of even digits (0, 2, 4, 6, 8)
    """
    # Special case: 0 has one even digit (0 itself)
    if n == 0:
        return 1

    count = 0
    n = abs(n)  # Handle negative numbers

    while n > 0:
        digit = n % 10
        if digit % 2 == 0:
            count += 1
        n //= 10

    return count
