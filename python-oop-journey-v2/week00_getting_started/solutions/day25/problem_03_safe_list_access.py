"""Reference solution for Problem 03: Safe List Access."""

from __future__ import annotations


def safe_get(data: list, index: int) -> any:
    """Safely get an element from a list.

    Args:
        data: The list to access
        index: The index to retrieve

    Returns:
        The element at index, or None if access fails
    """
    # Only accept list/tuple types, not strings or other subscriptables
    if not isinstance(data, (list, tuple)):
        return None
    
    try:
        return data[index]
    except IndexError:
        return None
