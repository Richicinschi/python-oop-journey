"""Reference solution for Problem 11: Is Palindrome Number."""

from __future__ import annotations


def is_palindrome_number(x: int) -> bool:
    """Check if an integer is a palindrome.

    Solves without converting to string by reversing half the number.

    Args:
        x: Integer to check

    Returns:
        True if x is a palindrome, False otherwise
    """
    # Negative numbers are not palindromes
    if x < 0:
        return False

    # Numbers ending in 0 (except 0 itself) are not palindromes
    if x % 10 == 0 and x != 0:
        return False

    reversed_half = 0
    while x > reversed_half:
        reversed_half = reversed_half * 10 + x % 10
        x //= 10

    # For even-length numbers: x == reversed_half
    # For odd-length numbers: x == reversed_half // 10 (middle digit doesn't matter)
    return x == reversed_half or x == reversed_half // 10
