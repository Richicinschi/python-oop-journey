"""Problem 03: Divide with Remainder

Topic: Division operators, multiple return values
Difficulty: Easy

Write a function that performs division and returns both the quotient and remainder.

Use floor division (//) and modulo (%) operators.

Examples:
    >>> divide_with_remainder(10, 3)
    (3, 1)
    >>> divide_with_remainder(17, 5)
    (3, 2)
    >>> divide_with_remainder(20, 4)
    (5, 0)

Requirements:
    - Return a tuple of (quotient, remainder)
    - quotient = dividend // divisor
    - remainder = dividend % divisor
    - Assume divisor is not zero
"""

from __future__ import annotations


def divide_with_remainder(dividend: int, divisor: int) -> tuple[int, int]:
    """Return quotient and remainder of division.

    Args:
        dividend: The number to be divided
        divisor: The number to divide by (non-zero)

    Returns:
        A tuple of (quotient, remainder)

    Raises:
        ZeroDivisionError: If divisor is zero
    """
    raise NotImplementedError("Implement divide_with_remainder")
