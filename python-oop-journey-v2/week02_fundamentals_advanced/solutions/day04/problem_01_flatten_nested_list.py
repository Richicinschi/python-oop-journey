"""Reference solution for Problem 01: Flatten Nested List."""

from __future__ import annotations


def flatten_nested_list(nested: list[list[int]]) -> list[int]:
    """Flatten a nested list into a single list.

    Uses a nested list comprehension to iterate through each sublist
    and then each element within those sublists.

    Args:
        nested: A list of lists containing integers.

    Returns:
        A single flat list with all integers in row-major order.
    """
    return [item for sublist in nested for item in sublist]
