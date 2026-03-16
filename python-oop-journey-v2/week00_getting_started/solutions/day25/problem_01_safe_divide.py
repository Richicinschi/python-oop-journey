"""Reference solution for Problem 01: Safe Divide."""

from __future__ import annotations


def safe_divide(a: float, b: float) -> float | None:
    """Safely divide two numbers, handling errors gracefully.

    Args:
        a: The dividend
        b: The divisor

    Returns:
        The quotient as float, 0 if division by zero, None if invalid input
    """
    try:
        result = a / b
    except ZeroDivisionError:
        return 0
    except TypeError:
        return None
    else:
        return float(result)
