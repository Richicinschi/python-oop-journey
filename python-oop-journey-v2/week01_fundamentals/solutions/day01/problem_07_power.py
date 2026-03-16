"""Reference solution for Problem 07: Power."""

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
    # Handle negative exponent
    if exponent < 0:
        base = 1 / base
        exponent = -exponent

    result = 1.0
    current_base = base

    while exponent > 0:
        # If exponent is odd, multiply result by current base
        if exponent % 2 == 1:
            result *= current_base

        # Square the base and halve the exponent
        current_base *= current_base
        exponent //= 2

    return result
