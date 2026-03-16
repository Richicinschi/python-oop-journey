"""Problem 03: Count Primes

Topic: Nested loops, Sieve of Eratosthenes, algorithm efficiency
Difficulty: Medium

Write a function that counts the number of prime numbers less than a non-negative 
integer n using the Sieve of Eratosthenes algorithm.

The Sieve of Eratosthenes works by iteratively marking the multiples of each 
prime number starting from 2.
"""

from __future__ import annotations


def count_primes(n: int) -> int:
    """Count the number of primes less than n.

    Args:
        n: A non-negative integer.

    Returns:
        The count of prime numbers strictly less than n.

    Example:
        >>> count_primes(10)
        4  # Primes: 2, 3, 5, 7
        >>> count_primes(0)
        0
        >>> count_primes(2)
        0
    """
    raise NotImplementedError("Implement count_primes")
