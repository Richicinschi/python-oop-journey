"""Reference solution for Problem 05: Invert Dictionary."""

from __future__ import annotations


def invert_dictionary(original: dict[str, int]) -> dict[int, str]:
    """Invert a dictionary, swapping keys and values.

    Args:
        original: A dictionary mapping strings to integers

    Returns:
        A new dictionary with values as keys and keys as values.
        If duplicate values exist, the last key wins.
    """
    inverted = {}
    for key, value in original.items():
        inverted[value] = key
    return inverted
