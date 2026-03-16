"""Problem 10: GCD - Greatest Common Divisor

Topic: Algorithms, Euclidean algorithm
Difficulty: Medium

Write a function to compute the Greatest Common Divisor (GCD) of two integers
using the Euclidean algorithm.

The Euclidean algorithm:
    gcd(a, b) = gcd(b, a % b)
    gcd(a, 0) = |a|

Examples:
    >>> gcd(48, 18)
    6
    >>> gcd(56, 98)
    14
    >>> gcd(0, 5)
    5
    >>> gcd(0, 0)
    0

Requirements:
    - Implement the Euclidean algorithm iteratively or recursively
    - Handle negative numbers (return GCD of absolute values)
    - gcd(0, 0) should return 0
    - The result should always be non-negative

Hints:
    - The Euclidean algorithm: gcd(a, b) = gcd(b, a % b)
    - Keep applying this until b becomes 0
    - When b is 0, the GCD is |a|
    - Don't forget to handle negative inputs by taking absolute values first
"""

from __future__ import annotations


def gcd(a: int, b: int) -> int:
    """Calculate the Greatest Common Divisor using Euclidean algorithm.

    Args:
        a: First integer
        b: Second integer

    Returns:
        The GCD of a and b (always non-negative)
    """
    raise NotImplementedError("Implement gcd")
