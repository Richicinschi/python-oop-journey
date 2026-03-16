"""Problem 05: Reverse List

Topic: Lists - Reversing
Difficulty: Easy

Write a function that returns a new list with elements in reverse order.

Function Signature:
    def reverse_list(items: list[str]) -> list[str]

Requirements:
    - Return a NEW list with elements in reverse order
    - Do NOT modify the original list
    - Empty list returns empty list

Behavior Notes:
    - Return a copy, don't reverse in-place
    - Original list should remain unchanged
    - You can use slicing [::-1] or reversed()

Examples:
    >>> reverse_list(["a", "b", "c"])
    ['c', 'b', 'a']
    
    >>> reverse_list(["one"])
    ['one']
    
    Empty list:
    >>> reverse_list([])
    []
    
    Original unchanged:
    >>> original = ["a", "b", "c"]
    >>> reversed_list = reverse_list(original)
    >>> original
    ['a', 'b', 'c']  # unchanged

Input Validation:
    - You may assume items is a list of strings
    - Return empty list for empty input

Important:
    - Return a new list, don't modify the input list

"""

from __future__ import annotations


def reverse_list(items: list[str]) -> list[str]:
    """Return a new list with elements in reverse order.

    Args:
        items: A list of strings.

    Returns:
        A new list with elements reversed.
    """
    raise NotImplementedError("Implement reverse_list")
