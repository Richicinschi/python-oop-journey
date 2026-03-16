"""Problem 02: Invert Dictionary

Topic: Dictionary Comprehensions
Difficulty: Easy

Invert a dictionary by swapping its keys and values using a
dictionary comprehension.
"""

from __future__ import annotations


def invert_dictionary(original: dict[str, int]) -> dict[int, str]:
    """Invert a dictionary, swapping keys and values.

    Args:
        original: A dictionary with string keys and integer values.
            Assumes all values are unique.

    Returns:
        A new dictionary with integer keys and string values.

    Example:
        >>> invert_dictionary({"a": 1, "b": 2, "c": 3})
        {1: 'a', 2: 'b', 3: 'c'}
        >>> invert_dictionary({"x": 10})
        {10: 'x'}
    """
    raise NotImplementedError("Implement invert_dictionary")
