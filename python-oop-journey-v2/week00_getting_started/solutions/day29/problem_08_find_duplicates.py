"""Reference solution for Problem 08: Find Duplicates Efficiently."""

from __future__ import annotations
from collections import Counter


def find_duplicates(items: list) -> set:
    """Find all items that appear more than once.

    Args:
        items: List of items (must be hashable)

    Returns:
        Set of items that appear multiple times
    """
    counts = Counter(items)
    return {item for item, count in counts.items() if count > 1}


def find_first_duplicate(items: list) -> any:
    """Find the first item that appears twice.

    Args:
        items: List of items (must be hashable)

    Returns:
        First duplicate item found, or None if no duplicates
    """
    seen = set()
    for item in items:
        if item in seen:
            return item
        seen.add(item)
    return None


def count_duplicates(items: list) -> dict[any, int]:
    """Count occurrences of each duplicate item.

    Args:
        items: List of items (must be hashable)

    Returns:
        Dictionary mapping duplicate items to their occurrence counts
    """
    counts = Counter(items)
    return {item: count for item, count in counts.items() if count > 1}


def remove_duplicates_keep_order(items: list) -> list:
    """Remove duplicates while preserving original order.

    Args:
        items: List of items (must be hashable)

    Returns:
        List with duplicates removed, first occurrence kept
    """
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
