"""Problem 04: Even Square Map

Topic: List Comprehensions, Functional Style
Difficulty: Easy

Square all even numbers from a list using a list comprehension
with a filtering condition.
"""

from __future__ import annotations


def even_square_map(numbers: list[int]) -> list[int]:
    """Return squares of all even numbers in the input list.

    Args:
        numbers: A list of integers.

    Returns:
        A list containing squares of even numbers only,
        in the same order as they appeared.

    Example:
        >>> even_square_map([1, 2, 3, 4, 5, 6])
        [4, 16, 36]
        >>> even_square_map([1, 3, 5])
        []
        >>> even_square_map([2, 4, 6])
        [4, 16, 36]
    """
    raise NotImplementedError("Implement even_square_map")
