"""Reference solution for Problem 01: Remove Duplicates."""

from __future__ import annotations


def remove_duplicates(items: list[str]) -> set[str]:
    """Remove duplicates from a list by converting to a set.

    Args:
        items: A list of strings that may contain duplicates

    Returns:
        A set containing only unique elements from the list
    """
    return set(items)
