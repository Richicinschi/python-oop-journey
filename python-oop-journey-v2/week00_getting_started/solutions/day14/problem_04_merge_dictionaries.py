"""Reference solution for Problem 04: Merge Dictionaries."""

from __future__ import annotations


def merge_dictionaries(dict1: dict[str, int], dict2: dict[str, int]) -> dict[str, int]:
    """Merge two dictionaries. If a key exists in both, use the value from dict2.

    Args:
        dict1: First dictionary
        dict2: Second dictionary

    Returns:
        A new dictionary containing all keys from both dictionaries
    """
    result = dict1.copy()
    for key, value in dict2.items():
        result[key] = value
    return result
