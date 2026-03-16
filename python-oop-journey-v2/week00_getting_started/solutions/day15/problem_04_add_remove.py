"""Reference solution for Problem 04: Add and Remove."""

from __future__ import annotations


def add_and_remove(data: set[int], to_add: int, to_remove: int) -> set[int]:
    """Add an element to a set and remove another element.

    Args:
        data: A set of integers (modified in place)
        to_add: The element to add to the set
        to_remove: The element to remove from the set

    Returns:
        The modified set
    """
    data.add(to_add)
    data.discard(to_remove)
    return data
