"""Problem 04: Add and Remove from Set

Topic: Sets - Modification
Difficulty: Easy

Write a function that adds and removes items from a set based on instructions.

Function Signature:
    def modify_set(
        original: set[str], 
        to_add: list[str], 
        to_remove: list[str]
    ) -> set[str]

Requirements:
    - Start with a copy of the original set
    - Add all items from to_add
    - Remove all items from to_remove
    - Return the modified set
    - Don't modify the original set

Behavior Notes:
    - Make a copy first to avoid modifying original
    - Use set.add() for single items
    - Use set.remove() or discard() for removal
    - discard() won't raise error if item doesn't exist

Examples:
    >>> modify_set({"a", "b"}, ["c"], ["a"])
    {'b', 'c'}
    
    Add existing item (no change):
    >>> modify_set({"a", "b"}, ["a"], [])
    {'a', 'b'}
    
    Remove non-existent (should not error):
    >>> modify_set({"a", "b"}, [], ["z"])
    {'a', 'b'}
    
    Empty operations:
    >>> modify_set({"a", "b"}, [], [])
    {'a', 'b'}

Input Validation:
    - You may assume original is a set of strings
    - to_add and to_remove are lists of strings

"""

from __future__ import annotations


def modify_set(original: set[str], to_add: list[str], to_remove: list[str]) -> set[str]:
    """Add and remove items from a set.

    Args:
        original: The starting set.
        to_add: Items to add.
        to_remove: Items to remove.

    Returns:
        A new set with modifications applied.
    """
    raise NotImplementedError("Implement modify_set")
