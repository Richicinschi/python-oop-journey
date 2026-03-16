"""Problem 02: Append and Get Length

Topic: Lists - Modifying and Measuring
Difficulty: Easy

Write a function that appends an item to a list and returns the new length.

Function Signature:
    def append_and_length(items: list[str], new_item: str) -> int

Requirements:
    - Append new_item to the items list (modifies in-place)
    - Return the new length of the list after appending
    - Works with empty lists

Behavior Notes:
    - list.append() adds item to the end (modifies original list)
    - len() returns the number of elements
    - The return value is the length AFTER appending

Examples:
    >>> append_and_length(["a", "b"], "c")
    3
    # List is now ["a", "b", "c"]
    
    >>> append_and_length([], "first")
    1
    # List is now ["first"]
    
    >>> append_and_length(["x"], "")
    2
    # Empty string is a valid item

Input Validation:
    - You may assume items is a list of strings
    - new_item is a string (could be empty)

"""

from __future__ import annotations


def append_and_length(items: list[str], new_item: str) -> int:
    """Append new_item to items and return the new length.

    Args:
        items: A list of strings.
        new_item: The string to append.

    Returns:
        The new length of the list after appending.
    """
    raise NotImplementedError("Implement append_and_length")
