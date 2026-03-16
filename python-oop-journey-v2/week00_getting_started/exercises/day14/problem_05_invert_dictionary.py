"""Problem 05: Invert Dictionary

Topic: Dictionaries - Transformation
Difficulty: Easy

Write a function that inverts a dictionary (swaps keys and values).

Function Signature:
    def invert_dictionary(original: dict[str, int]) -> dict[int, str]

Requirements:
    - Return a new dictionary with values as keys and keys as values
    - If values are not unique, later keys overwrite earlier ones
    - Original dictionary should not be modified

Behavior Notes:
    - Iterate through items and swap key/value
    - Duplicate values: last key wins (standard dict behavior)
    - Create a new dictionary, don't modify original

Examples:
    >>> invert_dictionary({"a": 1, "b": 2, "c": 3})
    {1: 'a', 2: 'b', 3: 'c'}
    
    Duplicate values (last wins):
    >>> invert_dictionary({"a": 1, "b": 2, "c": 1})
    {1: 'c', 2: 'b'}
    
    Single pair:
    >>> invert_dictionary({"key": 42})
    {42: 'key'}
    
    Empty:
    >>> invert_dictionary({})
    {}

Input Validation:
    - You may assume original has string keys and int values
    - Values may not be unique

"""

from __future__ import annotations


def invert_dictionary(original: dict[str, int]) -> dict[int, str]:
    """Invert a dictionary (swap keys and values).

    Args:
        original: The dictionary to invert.

    Returns:
        A new dictionary with swapped keys and values.
    """
    raise NotImplementedError("Implement invert_dictionary")
