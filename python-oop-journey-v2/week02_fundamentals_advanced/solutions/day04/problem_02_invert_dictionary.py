"""Reference solution for Problem 02: Invert Dictionary."""

from __future__ import annotations


def invert_dictionary(original: dict[str, int]) -> dict[int, str]:
    """Invert a dictionary, swapping keys and values.

    Uses a dictionary comprehension to create a new dictionary
    with values as keys and keys as values.

    Args:
        original: A dictionary with string keys and integer values.
            Assumes all values are unique.

    Returns:
        A new dictionary with integer keys and string values.
    """
    return {v: k for k, v in original.items()}
