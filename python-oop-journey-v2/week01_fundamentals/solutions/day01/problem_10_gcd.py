"""Reference solution for Problem 10: GCD."""

from __future__ import annotations


def gcd(a: int, b: int) -> int:
    """Calculate the Greatest Common Divisor using Euclidean algorithm.

    The Euclidean algorithm:
        gcd(a, b) = gcd(b, a % b)
        gcd(a, 0) = |a|

    Args:
        a: First integer
        b: Second integer

    Returns:
        The GCD of a and b (always non-negative)
    """
    # Handle negative inputs by taking absolute values
    a, b = abs(a), abs(b)

    # Special case: gcd(0, 0) = 0
    if a == 0 and b == 0:
        return 0

    # Euclidean algorithm (iterative)
    while b != 0:
        a, b = b, a % b

    return a
