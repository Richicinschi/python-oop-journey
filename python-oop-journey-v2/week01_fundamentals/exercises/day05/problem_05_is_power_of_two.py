"""Problem 05: Is Power of Two

Topic: Mathematical loops, bitwise thinking
Difficulty: Easy

Write a function that returns True if a given integer is a power of two.
A number is a power of two if it can be written as 2^k where k is a non-negative 
integer.

Note: Solve this using loops/iteration, not bit manipulation.
"""

from __future__ import annotations


def is_power_of_two(n: int) -> bool:
    """Check if a number is a power of two.

    Args:
        n: The integer to check.

    Returns:
        True if n is a power of two (n = 2^k for some k >= 0), False otherwise.

    Example:
        >>> is_power_of_two(1)
        True   # 2^0 = 1
        >>> is_power_of_two(16)
        True   # 2^4 = 16
        >>> is_power_of_two(3)
        False
        >>> is_power_of_two(0)
        False
    """
    raise NotImplementedError("Implement is_power_of_two")
