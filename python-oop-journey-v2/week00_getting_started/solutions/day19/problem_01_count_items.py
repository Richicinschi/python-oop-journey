"""Problem 01: Count Items - Solution."""

from __future__ import annotations


def count_items(collection: list[str] | str | dict[str, int]) -> int:
    """Return the number of items in the collection.

    Args:
        collection: A list, string, or dictionary to count.

    Returns:
        The number of items in the collection.
    """
    return len(collection)


def is_empty(collection: list[str] | str | dict[str, int]) -> bool:
    """Check if a collection is empty.

    Args:
        collection: A list, string, or dictionary to check.

    Returns:
        True if the collection has no items, False otherwise.
    """
    return len(collection) == 0


def compare_lengths(
    collection1: list[str] | str,
    collection2: list[str] | str,
) -> str:
    """Compare the lengths of two collections.

    Args:
        collection1: First collection.
        collection2: Second collection.

    Returns:
        "first" if collection1 is longer,
        "second" if collection2 is longer,
        "equal" if they have the same length.
    """
    len1 = len(collection1)
    len2 = len(collection2)

    if len1 > len2:
        return "first"
    if len2 > len1:
        return "second"
    return "equal"
