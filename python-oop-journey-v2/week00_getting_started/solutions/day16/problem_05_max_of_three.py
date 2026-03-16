"""Problem 05: Max of Three - Solution."""

from __future__ import annotations


def max_of_three(a: int, b: int, c: int) -> int:
    """Return the maximum of three integers.

    Args:
        a: First integer.
        b: Second integer.
        c: Third integer.

    Returns:
        The largest of the three integers.
    """
    if a >= b and a >= c:
        return a
    if b >= a and b >= c:
        return b
    return c
