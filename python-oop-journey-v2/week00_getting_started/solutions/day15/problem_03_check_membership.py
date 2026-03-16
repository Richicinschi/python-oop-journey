"""Reference solution for Problem 03: Check Membership."""

from __future__ import annotations


def check_membership(data: set[str], item: str) -> bool:
    """Check if an item exists in a set.

    Args:
        data: A set of strings
        item: The item to search for

    Returns:
        True if item is in the set, False otherwise
    """
    return item in data
