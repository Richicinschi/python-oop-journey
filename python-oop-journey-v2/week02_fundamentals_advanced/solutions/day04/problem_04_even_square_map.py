"""Reference solution for Problem 04: Even Square Map."""

from __future__ import annotations


def even_square_map(numbers: list[int]) -> list[int]:
    """Return squares of all even numbers in the input list.

    Uses a list comprehension with a filtering condition to select
    only even numbers before squaring them.

    Args:
        numbers: A list of integers.

    Returns:
        A list containing squares of even numbers only,
        in the same order as they appeared.
    """
    return [x * x for x in numbers if x % 2 == 0]
