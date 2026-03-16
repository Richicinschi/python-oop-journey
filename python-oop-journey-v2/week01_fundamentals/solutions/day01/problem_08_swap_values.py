"""Reference solution for Problem 08: Swap Values."""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def swap_values(a: T, b: T) -> tuple[T, T]:
    """Swap two values using tuple unpacking.

    Args:
        a: First value
        b: Second value

    Returns:
        A tuple with values swapped: (b, a)
    """
    a, b = b, a  # Tuple unpacking swap
    return (a, b)
