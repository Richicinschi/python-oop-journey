"""Reference solution for Problem 04: First and Last."""

from __future__ import annotations


def first_last(items: tuple[str, ...]) -> tuple[str, str] | None:
    """Return the first and last elements of a tuple.

    Args:
        items: A tuple of strings

    Returns:
        A tuple of (first_element, last_element), or None if empty
    """
    if not items:
        return None
    
    return items[0], items[-1]
