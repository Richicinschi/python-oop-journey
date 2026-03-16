"""Reference solution for Problem 02: Is Prime."""

from __future__ import annotations


def is_prime(n: int) -> bool:
    """Check if a number is prime.

    Args:
        n: The integer to check.

    Returns:
        True if n is prime, False otherwise.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # Only check odd divisors up to square root of n
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True
