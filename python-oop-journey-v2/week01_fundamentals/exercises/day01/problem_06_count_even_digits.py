"""Problem 06: Count Even Digits

Topic: Digit extraction, conditionals
Difficulty: Easy

Write a function that counts how many even digits are in a given integer.

Even digits are: 0, 2, 4, 6, 8

Examples:
    >>> count_even_digits(12345)
    2  # Digits 2 and 4 are even
    >>> count_even_digits(24680)
    5  # All digits are even
    >>> count_even_digits(13579)
    0  # No even digits
    >>> count_even_digits(-2468)
    4  # Negative sign is not a digit

Requirements:
    - Count only even digits (0, 2, 4, 6, 8)
    - Handle negative numbers (ignore the minus sign)
    - Zero counts as an even digit
"""

from __future__ import annotations


def count_even_digits(n: int) -> int:
    """Count the number of even digits in an integer.

    Args:
        n: Integer to analyze

    Returns:
        Count of even digits (0, 2, 4, 6, 8)
    """
    raise NotImplementedError("Implement count_even_digits")
