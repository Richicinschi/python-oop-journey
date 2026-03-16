"""Reference solution for Problem 04: Is Perfect Square."""

from __future__ import annotations

import math


def is_perfect_square(n: int) -> bool:
    """Check if a number is a perfect square.

    A perfect square is an integer that is the square of an integer.
    Negative numbers are not perfect squares.

    Args:
        n: Integer to check

    Returns:
        True if n is a perfect square, False otherwise
    """
    if n < 0:
        return False

    root = int(math.isqrt(n))
    return root * root == n
