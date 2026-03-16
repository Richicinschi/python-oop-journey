"""Reference solution for Problem 03: Divide with Remainder."""

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
    if divisor == 0:
        raise ZeroDivisionError("Cannot divide by zero")

    quotient = dividend // divisor
    remainder = dividend % divisor
    return (quotient, remainder)
