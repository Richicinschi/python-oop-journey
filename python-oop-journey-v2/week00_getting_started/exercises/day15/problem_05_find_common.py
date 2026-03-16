"""Problem 05: Find Common Elements

Topic: Sets - Finding Overlaps
Difficulty: Easy

Write a function that finds elements common to all given lists.

Function Signature:
    def find_common(*lists: list[int]) -> set[int]

Requirements:
    - Accept any number of lists as arguments
    - Return a set of elements that appear in ALL lists
    - Return empty set if no common elements
    - Return empty set if no lists provided

Behavior Notes:
    - *lists collects all arguments into a tuple of lists
    - Find intersection of all sets
    - If no arguments, return empty set

Examples:
    >>> find_common([1, 2, 3], [2, 3, 4], [3, 4, 5])
    {3}
    
    Two lists:
    >>> find_common([1, 2, 3], [2, 3, 4])
    {2, 3}
    
    No common:
    >>> find_common([1, 2], [3, 4], [5, 6])
    set()
    
    Single list:
    >>> find_common([1, 2, 3])
    {1, 2, 3}
    
    No arguments:
    >>> find_common()
    set()

Input Validation:
    - You may assume all arguments are lists of integers

Implementation Hint:
    - Convert each list to a set
    - Use set.intersection() or & operator
    - Handle the case of no arguments

"""

from __future__ import annotations


def find_common(*lists: list[int]) -> set[int]:
    """Find elements common to all given lists.

    Args:
        *lists: Any number of lists of integers.

    Returns:
        A set of elements common to all lists.
    """
    raise NotImplementedError("Implement find_common")
