"""Reference solution for Problem 02: Handle KeyError."""

from __future__ import annotations


def safe_dict_get(data: dict, key: str, default: any) -> any:
    """Safely get a value from a dictionary.

    Args:
        data: The dictionary to access
        key: The key to look up
        default: Value to return if key not found

    Returns:
        The value, default, or None if data isn't a dict
    """
    if not isinstance(data, dict):
        return None
    
    try:
        return data[key]
    except KeyError:
        return default
