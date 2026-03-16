"""Reference solution for Problem 02: Lookup Value."""

from __future__ import annotations


def lookup_value(data: dict[str, int], key: str, default: int) -> int:
    """Look up a value in a dictionary with a default fallback.

    Args:
        data: A dictionary mapping strings to integers
        key: The key to look up
        default: The value to return if key is not found

    Returns:
        The value associated with key, or default if not found
    """
    return data.get(key, default)
