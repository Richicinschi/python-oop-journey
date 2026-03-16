"""Reference solution for Problem 02: Swap Variables."""

from __future__ import annotations


def swap_variables(a: int, b: int) -> tuple[int, int]:
    """Swap two values using tuple unpacking.

    Args:
        a: First integer
        b: Second integer

    Returns:
        A tuple with values swapped (b, a)
    """
    a, b = b, a
    return a, b
