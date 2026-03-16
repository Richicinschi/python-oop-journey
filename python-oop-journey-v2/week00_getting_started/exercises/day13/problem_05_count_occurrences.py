"""Problem 05: Count Occurrences in Tuple

Topic: Tuples - Searching
Difficulty: Easy

Write a function that counts occurrences of a value in a tuple.

Function Signature:
    def count_in_tuple(items: tuple[str, ...], target: str) -> int

Requirements:
    - Return the number of times target appears in the tuple
    - Return 0 if target is not found
    - Case-sensitive comparison

Behavior Notes:
    - Use tuple.count() method
    - Case-sensitive: "A" != "a"
    - Empty tuple returns 0

Examples:
    >>> count_in_tuple(("a", "b", "a", "c", "a"), "a")
    3
    
    >>> count_in_tuple(("x", "y", "z"), "a")
    0
    
    Case-sensitive:
    >>> count_in_tuple(("A", "a", "A"), "a")
    1
    
    Empty tuple:
    >>> count_in_tuple((), "anything")
    0

Input Validation:
    - You may assume items is a tuple of strings
    - target is a string

"""

from __future__ import annotations


def count_in_tuple(items: tuple[str, ...], target: str) -> int:
    """Count occurrences of a value in a tuple.

    Args:
        items: A tuple of strings.
        target: The value to count.

    Returns:
        The number of occurrences (0 if not found).
    """
    raise NotImplementedError("Implement count_in_tuple")
