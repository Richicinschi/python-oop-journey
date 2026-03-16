"""Reference solution for Problem 05: Reverse List."""

from __future__ import annotations


def reverse_list(items: list[str]) -> list[str]:
    """Return a new list with elements in reverse order.

    Args:
        items: A list of strings

    Returns:
        A new list with elements reversed
    """
    reversed_items = []
    for i in range(len(items) - 1, -1, -1):
        reversed_items.append(items[i])
    return reversed_items
