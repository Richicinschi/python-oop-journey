"""Problem 02: Is Prime

Topic: Loops, conditionals, mathematical operations
Difficulty: Easy

Write a function that determines whether a given integer is a prime number.
A prime number is a natural number greater than 1 that has no positive 
divisors other than 1 and itself.
"""

from __future__ import annotations


def is_prime(n: int) -> bool:
    """Check if a number is prime.

    Args:
        n: The integer to check.

    Returns:
        True if n is prime, False otherwise.

    Example:
        >>> is_prime(2)
        True
        >>> is_prime(17)
        True
        >>> is_prime(4)
        False
        >>> is_prime(1)
        False
    """
    raise NotImplementedError("Implement is_prime")
