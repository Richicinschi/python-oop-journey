"""Reference solution for Problem 01: Get Number Sign."""

from __future__ import annotations


def get_number_sign(n: int | float) -> str:
    """Return the sign of a number.

    Args:
        n: The number to check

    Returns:
        'positive' if n > 0, 'negative' if n < 0, 'zero' if n == 0
    """
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"
