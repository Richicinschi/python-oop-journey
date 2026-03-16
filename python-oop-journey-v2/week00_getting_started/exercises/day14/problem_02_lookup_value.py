"""Problem 02: Lookup Value

Topic: Dictionaries - Accessing Values
Difficulty: Easy

Write a function that looks up a value in a dictionary with a default.

Function Signature:
    def lookup_value(data: dict[str, int], key: str, default: int) -> int

Requirements:
    - Return the value for the given key if it exists
    - Return default if key is not in dictionary
    - Do not modify the original dictionary

Behavior Notes:
    - Use dict.get(key, default) or check with 'in'
    - Return existing value if key present
    - Return default if key missing

Examples:
    >>> lookup_value({"a": 1, "b": 2}, "a", 0)
    1
    
    >>> lookup_value({"a": 1, "b": 2}, "c", 0)
    0
    
    >>> lookup_value({"a": 1, "b": 2}, "c", -1)
    -1
    
    Empty dictionary:
    >>> lookup_value({}, "key", 100)
    100

Input Validation:
    - You may assume data is a dict with string keys and int values
    - key is a string
    - default is an integer

"""

from __future__ import annotations


def lookup_value(data: dict[str, int], key: str, default: int) -> int:
    """Look up a value in a dictionary with a default.

    Args:
        data: The dictionary to search.
        key: The key to look up.
        default: Value to return if key not found.

    Returns:
        The value for key, or default if not found.
    """
    raise NotImplementedError("Implement lookup_value")
