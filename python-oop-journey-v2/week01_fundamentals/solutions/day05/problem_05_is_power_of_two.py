"""Reference solution for Problem 05: Is Power of Two."""

from __future__ import annotations


def is_power_of_two(n: int) -> bool:
    """Check if a number is a power of two.

    Args:
        n: The integer to check.

    Returns:
        True if n is a power of two (n = 2^k for some k >= 0), False otherwise.
    """
    if n <= 0:
        return False

    # Keep dividing by 2 as long as n is even
    while n % 2 == 0:
        n //= 2

    # If we end up with 1, it was a power of two
    return n == 1
