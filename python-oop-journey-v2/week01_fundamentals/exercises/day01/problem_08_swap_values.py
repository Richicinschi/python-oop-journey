"""Problem 08: Swap Values

Topic: Tuple unpacking, multiple assignment
Difficulty: Easy

Write a function that swaps two values using tuple unpacking.

Return the values in a tuple in reversed order.

Examples:
    >>> swap_values(5, 10)
    (10, 5)
    >>> swap_values('a', 'b')
    ('b', 'a')
    >>> a, b = swap_values(1, 2)
    >>> print(a, b)
    2 1

Requirements:
    - Use tuple unpacking to swap values (no temporary variable)
    - Return a tuple with values in swapped order
    - Work with any types (int, str, etc.)
"""

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
    raise NotImplementedError("Implement swap_values")
