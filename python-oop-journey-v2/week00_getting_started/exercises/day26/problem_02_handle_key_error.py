"""Problem 02: Handle KeyError

Topic: Common Exceptions
Difficulty: Easy

Write a function that safely retrieves a value from a dictionary.

If the key doesn't exist, return a default value.
If the input is not a dictionary, return None.

Examples:
    >>> safe_dict_get({"name": "Alice"}, "name", "Unknown")
    'Alice'
    >>> safe_dict_get({"name": "Alice"}, "age", 0)
    0
    >>> safe_dict_get("not a dict", "key", "default")
    None

Requirements:
    - Return the value if key exists
    - Return default if key is missing
    - Return None if data is not a dictionary
"""

from __future__ import annotations


def safe_dict_get(data: dict, key: str, default: any) -> any:
    """Safely get a value from a dictionary.

    Args:
        data: The dictionary to access
        key: The key to look up
        default: Value to return if key not found

    Returns:
        The value, default, or None if data isn't a dict
    """
    raise NotImplementedError("Implement safe_dict_get")
