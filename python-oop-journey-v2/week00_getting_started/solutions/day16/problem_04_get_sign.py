"""Problem 04: Get Sign - Solution."""

from __future__ import annotations


def get_sign(number: int) -> str:
    """Return the sign of a number.

    Args:
        number: The integer to check.

    Returns:
        "positive" if number > 0, "negative" if number < 0,
        "zero" if number == 0.
    """
    if number > 0:
        return "positive"
    if number < 0:
        return "negative"
    return "zero"
