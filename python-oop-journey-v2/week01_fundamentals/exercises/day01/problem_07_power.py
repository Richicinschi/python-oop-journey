"""Problem 07: Power

Topic: Loops, efficient computation
Difficulty: Medium

Implement a function to calculate base^exponent without using the ** operator.

Implement an efficient O(log n) solution using exponentiation by squaring.

Examples:
    >>> power(2, 3)
    8
    >>> power(5, 0)
    1
    >>> power(2, -2)
    0.25
    >>> power(0, 5)
    0

Requirements:
    - Do NOT use ** operator or math.pow()
    - Handle positive, zero, and negative exponents
    - 0^0 should return 1 (mathematical convention in programming)
    - Return float for negative exponents
"""

from __future__ import annotations


def power(base: float, exponent: int) -> float:
    """Calculate base raised to the power of exponent.

    Uses exponentiation by squaring for O(log n) time complexity.

    Args:
        base: The base number
        exponent: The exponent (can be negative)

    Returns:
        base^exponent as a float
    """
    raise NotImplementedError("Implement power")
