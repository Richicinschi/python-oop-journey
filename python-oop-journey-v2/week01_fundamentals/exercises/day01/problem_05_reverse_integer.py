"""Problem 05: Reverse Integer

Topic: Integer manipulation, loops
Difficulty: Medium

Write a function that reverses the digits of a 32-bit signed integer.

If reversing the integer causes the value to go outside the signed
32-bit integer range [-2³¹, 2³¹ - 1], return 0.

Examples:
    >>> reverse_integer(123)
    321
    >>> reverse_integer(-456)
    -654
    >>> reverse_integer(120)
    21
    >>> reverse_integer(1534236469)
    0  # Overflow

Requirements:
    - Handle positive and negative numbers
    - Remove trailing zeros in the result
    - Return 0 for overflow cases
    - 32-bit range: [-2147483648, 2147483647]
"""

from __future__ import annotations


def reverse_integer(x: int) -> int:
    """Reverse the digits of a 32-bit signed integer.

    Args:
        x: 32-bit signed integer to reverse

    Returns:
        Reversed integer, or 0 if overflow occurs
    """
    raise NotImplementedError("Implement reverse_integer")
