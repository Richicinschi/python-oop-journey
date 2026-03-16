"""Problem 01: Count Items

Topic: Built-in Functions - len() and count
Difficulty: Easy

Write a function that counts different types of items in a collection.

Function Signature:
    def count_items(data: list | tuple | str) -> dict[str, int]

Requirements:
    - Return a dictionary with 'total', 'unique', and 'repeated' counts
    - 'total' is the total number of items (use len())
    - 'unique' is the number of unique items (use set())
    - 'repeated' is how many items appear more than once

Behavior Notes:
    - len() works on lists, tuples, and strings
    - set() removes duplicates
    - Count occurrences to find repeats

Examples:
    >>> count_items(["a", "b", "a", "c", "b"])
    {'total': 5, 'unique': 3, 'repeated': 2}
    # Total: 5, Unique: {a,b,c}=3, Repeated: a,b = 2 items
    
    >>> count_items((1, 2, 3, 3, 3))
    {'total': 5, 'unique': 3, 'repeated': 1}
    
    String:
    >>> count_items("hello")
    {'total': 5, 'unique': 4, 'repeated': 1}  # 'l' repeats

Input Validation:
    - You may assume data is a list, tuple, or string

"""

from __future__ import annotations


def count_items(data: list | tuple | str) -> dict[str, int]:
    """Count total, unique, and repeated items.

    Args:
        data: A collection (list, tuple, or string).

    Returns:
        A dictionary with 'total', 'unique', and 'repeated' counts.
    """
    raise NotImplementedError("Implement count_items")
