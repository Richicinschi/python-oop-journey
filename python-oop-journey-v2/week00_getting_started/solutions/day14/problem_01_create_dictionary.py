"""Reference solution for Problem 01: Create Dictionary."""

from __future__ import annotations


def create_dictionary(keys: list[str], values: list[int]) -> dict[str, int]:
    """Create a dictionary from two lists - keys and values.

    Args:
        keys: A list of strings to use as keys
        values: A list of integers to use as values

    Returns:
        A dictionary mapping keys to values. If lists have different lengths,
        only pair up to the shorter length.
    """
    result = {}
    for i in range(min(len(keys), len(values))):
        result[keys[i]] = values[i]
    return result
