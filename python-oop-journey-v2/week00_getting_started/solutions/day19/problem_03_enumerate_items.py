"""Problem 03: Enumerate Items - Solution."""

from __future__ import annotations


def add_indices(items: list[str]) -> list[tuple[int, str]]:
    """Add zero-based indices to each item.

    Args:
        items: List of strings to enumerate.

    Returns:
        List of (index, item) tuples.
    """
    return list(enumerate(items))


def add_numbered_labels(items: list[str], start: int = 1) -> list[tuple[int, str]]:
    """Add numbered labels starting from 'start'.

    Args:
        items: List of strings to enumerate.
        start: Starting number (default 1).

    Returns:
        List of (number, item) tuples.
    """
    return list(enumerate(items, start))


def find_item_index(items: list[str], target: str) -> int:
    """Find the index of a target item.

    Args:
        items: List of strings to search.
        target: The item to find.

    Returns:
        The index of the target, or -1 if not found.
    """
    for index, item in enumerate(items):
        if item == target:
            return index
    return -1


def create_numbered_string(items: list[str]) -> str:
    """Create a numbered string like "1. item1, 2. item2".

    Args:
        items: List of strings to format.

    Returns:
        A formatted string with numbered items.
    """
    if not items:
        return ""

    parts = [f"{i}. {item}" for i, item in enumerate(items, 1)]
    return ", ".join(parts)
