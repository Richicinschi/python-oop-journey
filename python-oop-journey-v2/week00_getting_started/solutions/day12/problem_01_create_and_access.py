"""Reference solution for Problem 01: Create and Access List."""

from __future__ import annotations


def create_and_access(numbers: list[int], index: int) -> int | None:
    """Return the element at the given index, or None if index is out of range.

    Args:
        numbers: A list of integers
        index: The index to access

    Returns:
        The element at the index, or None if index is invalid
    """
    if index < 0 or index >= len(numbers):
        return None
    return numbers[index]
