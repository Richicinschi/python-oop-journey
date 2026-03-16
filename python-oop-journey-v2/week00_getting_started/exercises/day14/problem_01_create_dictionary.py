"""Problem 01: Create Dictionary

Topic: Dictionaries - Creating and Basic Operations
Difficulty: Easy

Write a function that creates a dictionary from keys and values.

Function Signature:
    def create_dictionary(keys: list[str], values: list[int]) -> dict[str, int]

Requirements:
    - Create a dictionary mapping keys to values
    - If lists have different lengths, only use pairs that exist
    - Return an empty dict if both lists are empty

Behavior Notes:
    - Use zip() to pair keys with values
    - dict() constructor or dict comprehension
    - Extra keys or values are ignored

Examples:
    >>> create_dictionary(["a", "b", "c"], [1, 2, 3])
    {'a': 1, 'b': 2, 'c': 3}
    
    Different lengths (extra key ignored):
    >>> create_dictionary(["a", "b", "c"], [1, 2])
    {'a': 1, 'b': 2}
    
    Different lengths (extra value ignored):
    >>> create_dictionary(["a", "b"], [1, 2, 3])
    {'a': 1, 'b': 2}
    
    Empty lists:
    >>> create_dictionary([], [])
    {}

Input Validation:
    - You may assume keys is a list of strings
    - You may assume values is a list of integers

"""

from __future__ import annotations


def create_dictionary(keys: list[str], values: list[int]) -> dict[str, int]:
    """Create a dictionary from keys and values.

    Args:
        keys: List of keys (strings).
        values: List of values (integers).

    Returns:
        A dictionary mapping keys to values.
    """
    raise NotImplementedError("Implement create_dictionary")
