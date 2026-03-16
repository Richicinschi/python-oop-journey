"""Problem 11: Is Palindrome Number

Topic: Digit manipulation, comparison
Difficulty: Medium

Write a function to determine if a given integer is a palindrome.

A palindrome reads the same forwards and backwards.

Examples:
    >>> is_palindrome_number(121)
    True
    >>> is_palindrome_number(-121)
    False  # Negative sign makes it not a palindrome
    >>> is_palindrome_number(10)
    False  # Reads 01 backwards
    >>> is_palindrome_number(0)
    True

Requirements:
    - Return True if the number is a palindrome, False otherwise
    - Negative numbers are NOT palindromes
    - Numbers ending in 0 (except 0 itself) are NOT palindromes
    - Do NOT convert the number to a string (solve mathematically)
"""

from __future__ import annotations


def is_palindrome_number(x: int) -> bool:
    """Check if an integer is a palindrome.

    Solves without converting to string.

    Args:
        x: Integer to check

    Returns:
        True if x is a palindrome, False otherwise
    """
    raise NotImplementedError("Implement is_palindrome_number")
