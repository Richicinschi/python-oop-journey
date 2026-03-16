"""Reference solution for Problem 03: Count Primes."""

from __future__ import annotations


def count_primes(n: int) -> int:
    """Count the number of primes less than n using Sieve of Eratosthenes.

    Args:
        n: A non-negative integer.

    Returns:
        The count of prime numbers strictly less than n.
    """
    if n <= 2:
        return 0

    # Create a boolean array "is_prime[0..n-1]" and initialize
    # all entries as True. A value in is_prime[i] will
    # finally be False if i is Not a prime, else True.
    is_prime = [True] * n
    is_prime[0] = False
    is_prime[1] = False

    # Use Sieve of Eratosthenes
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            # Mark all multiples of i as not prime
            for j in range(i * i, n, i):
                is_prime[j] = False

    # Count primes
    return sum(is_prime)
