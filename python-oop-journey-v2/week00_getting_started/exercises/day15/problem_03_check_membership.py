"""Problem 03: Check Membership

Topic: Sets - Membership Testing
Difficulty: Easy

Write a function that checks if any items from one list exist in another.

Function Signature:
    def has_common_items(group1: list[str], group2: list[str]) -> bool

Requirements:
    - Return True if at least one item from group1 is in group2
    - Return False if there are no common items
    - Empty lists should return False

Behavior Notes:
    - Sets have O(1) membership testing vs O(n) for lists
    - Convert group2 to a set for efficient lookup
    - Any common item makes the result True

Examples:
    >>> has_common_items(["a", "b", "c"], ["c", "d", "e"])
    True
    
    No common items:
    >>> has_common_items(["a", "b"], ["c", "d"])
    False
    
    One empty list:
    >>> has_common_items(["a", "b"], [])
    False
    
    Both empty:
    >>> has_common_items([], [])
    False

Input Validation:
    - You may assume both are lists of strings

Implementation Hint:
    - Convert group2 to a set for O(1) lookups
    - Check if any item from group1 is in the set

"""

from __future__ import annotations


def has_common_items(group1: list[str], group2: list[str]) -> bool:
    """Check if any items from group1 exist in group2.

    Args:
        group1: First list of strings.
        group2: Second list of strings.

    Returns:
        True if there's at least one common item, False otherwise.
    """
    raise NotImplementedError("Implement has_common_items")
