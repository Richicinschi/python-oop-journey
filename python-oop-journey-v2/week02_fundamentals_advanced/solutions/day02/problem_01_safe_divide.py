"""Solution for Problem 01: Safe Divide."""

from __future__ import annotations


def safe_divide(a: float, b: float) -> float | str:
    """Safely divide a by b, handling division by zero.

    Args:
        a: The dividend (numerator)
        b: The divisor (denominator)

    Returns:
        The result of a / b as a float, or an error message string
    """
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Division by zero"
