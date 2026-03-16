"""Problem 04: First and Last Elements

Topic: Tuples - Indexing
Difficulty: Easy

Write a function that returns the first and last elements of a tuple.

Function Signature:
    def first_last(items: tuple[str, ...]) -> tuple[str, str] | None

Requirements:
    - Return a tuple of (first_element, last_element)
    - Return None if the tuple is empty
    - Works with single-element tuples (first == last)

Behavior Notes:
    - Use index [0] for first element
    - Use index [-1] for last element
    - Single element: both first and last are that element
    - Empty tuple: return None

Examples:
    >>> first_last(("a", "b", "c", "d"))
    ('a', 'd')
    
    Single element:
    >>> first_last(("solo",))
    ('solo', 'solo')
    
    Two elements:
    >>> first_last(("first", "last"))
    ('first', 'last')
    
    Empty tuple:
    >>> first_last(())
    None

Input Validation:
    - You may assume items is a tuple of strings
    - Return None for empty tuple

"""

from __future__ import annotations


def first_last(items: tuple[str, ...]) -> tuple[str, str] | None:
    """Return the first and last elements of a tuple.

    Args:
        items: A tuple of strings.

    Returns:
        A tuple of (first, last), or None if empty.
    """
    raise NotImplementedError("Implement first_last")
