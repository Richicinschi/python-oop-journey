"""Problem 04: Merge Dictionaries

Topic: Dictionaries - Combining
Difficulty: Easy

Write a function that merges two dictionaries.

Function Signature:
    def merge_dictionaries(dict1: dict[str, int], dict2: dict[str, int]) -> dict[str, int]

Requirements:
    - Return a new dictionary containing all key-value pairs from both
    - If a key exists in both, use the value from dict2 (dict2 wins)
    - Do not modify the original dictionaries

Behavior Notes:
    - Create a new dictionary
    - Copy dict1 first, then update with dict2
    - Or use unpacking: {**dict1, **dict2}
    - Original dicts should remain unchanged

Examples:
    >>> merge_dictionaries({"a": 1, "b": 2}, {"c": 3})
    {'a': 1, 'b': 2, 'c': 3}
    
    Key collision (dict2 wins):
    >>> merge_dictionaries({"a": 1, "b": 2}, {"b": 20, "c": 3})
    {'a': 1, 'b': 20, 'c': 3}
    
    Empty dicts:
    >>> merge_dictionaries({}, {})
    {}
    
    >>> merge_dictionaries({"a": 1}, {})
    {'a': 1}

Input Validation:
    - You may assume both are dictionaries with string keys and int values

"""

from __future__ import annotations


def merge_dictionaries(dict1: dict[str, int], dict2: dict[str, int]) -> dict[str, int]:
    """Merge two dictionaries.

    Args:
        dict1: First dictionary.
        dict2: Second dictionary (values take precedence).

    Returns:
        A new merged dictionary.
    """
    raise NotImplementedError("Implement merge_dictionaries")
