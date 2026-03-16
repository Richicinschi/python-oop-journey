"""Problem 03: Enumerate Items

Topic: Built-in Functions - enumerate()
Difficulty: Easy

Write a function that returns indexed items using enumerate().

Function Signature:
    def enumerate_items(items: list[str]) -> list[tuple[int, str]]

Requirements:
    - Use enumerate() to get index and value pairs
    - Return a list of (index, value) tuples
    - Start index at 0

Behavior Notes:
    - enumerate() adds a counter to an iterable
    - Returns (index, value) tuples
    - Default start is 0, but can be changed with start parameter

Examples:
    >>> enumerate_items(["a", "b", "c"])
    [(0, 'a'), (1, 'b'), (2, 'c')]
    
    Single item:
    >>> enumerate_items(["solo"])
    [(0, 'solo')]
    
    Empty list:
    >>> enumerate_items([])
    []

Input Validation:
    - You may assume items is a list of strings

"""

from __future__ import annotations


def enumerate_items(items: list[str]) -> list[tuple[int, str]]:
    """Return indexed items using enumerate().

    Args:
        items: A list of strings.

    Returns:
        A list of (index, value) tuples.
    """
    raise NotImplementedError("Implement enumerate_items")
