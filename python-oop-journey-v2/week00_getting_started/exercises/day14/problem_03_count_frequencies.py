"""Problem 03: Count Frequencies

Topic: Dictionaries - Counting
Difficulty: Easy

Write a function that counts the frequency of each item in a list.

Function Signature:
    def count_frequencies(items: list[str]) -> dict[str, int]

Requirements:
    - Return a dictionary with each unique item as key
    - Value is the count of how many times it appears
    - Return empty dict for empty list

Behavior Notes:
    - Iterate through items and count occurrences
    - Use dict.get() or setdefault() for counting
    - Or use collections.Counter (but simple loop is fine)

Examples:
    >>> count_frequencies(["a", "b", "a", "c", "a", "b"])
    {'a': 3, 'b': 2, 'c': 1}
    
    >>> count_frequencies(["x", "x", "x"])
    {'x': 3}
    
    Empty list:
    >>> count_frequencies([])
    {}
    
    All unique:
    >>> count_frequencies(["a", "b", "c"])
    {'a': 1, 'b': 1, 'c': 1}

Input Validation:
    - You may assume items is a list of strings

"""

from __future__ import annotations


def count_frequencies(items: list[str]) -> dict[str, int]:
    """Count the frequency of each item in a list.

    Args:
        items: A list of strings.

    Returns:
        A dictionary mapping each item to its frequency.
    """
    raise NotImplementedError("Implement count_frequencies")
