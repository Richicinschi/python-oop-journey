"""Problem 05: Sort Data

Topic: Built-in Functions - sorted()
Difficulty: Easy

Write functions that sort data in various ways.

Function Signature:
    - sort_ascending(numbers: list[int]) -> list[int]
    - sort_descending(numbers: list[int]) -> list[int]
    - sort_by_length(strings: list[str]) -> list[str]
    - sort_by_last_letter(strings: list[str]) -> list[str]
    - sort_tuples_by_second_item(tuples: list[tuple[str, int]]) -> list[tuple[str, int]]

Requirements:
    - Each function sorts using sorted() with appropriate key
    - Return a new list, don't modify the original
    - Use key parameter for custom sorting

Behavior Notes:
    - sorted() returns a new sorted list
    - reverse=True for descending order
    - key=function for custom sort order
    - Original list should be unchanged

Examples:
    >>> sort_ascending([3, 1, 4, 1, 5])
    [1, 1, 3, 4, 5]
    
    >>> sort_descending([3, 1, 4, 1, 5])
    [5, 4, 3, 1, 1]
    
    >>> sort_by_length(["aaa", "bb", "c", "dddd"])
    ['c', 'bb', 'aaa', 'dddd']
    
    >>> sort_by_last_letter(["cat", "bed", "car"])
    ['bed', 'car', 'cat']  # d, r, t
    
    >>> sort_tuples_by_second_item([("b", 2), ("a", 3), ("c", 1)])
    [('c', 1), ('b', 2), ('a', 3)]

Input Validation:
    - You may assume inputs contain comparable elements

"""

from __future__ import annotations


def sort_ascending(numbers: list[int]) -> list[int]:
    """Sort numbers in ascending order.

    Args:
        numbers: List of integers.

    Returns:
        New list sorted in ascending order.
    """
    raise NotImplementedError("Implement sort_ascending")


def sort_descending(numbers: list[int]) -> list[int]:
    """Sort numbers in descending order.

    Args:
        numbers: List of integers.

    Returns:
        New list sorted in descending order.
    """
    raise NotImplementedError("Implement sort_descending")


def sort_by_length(strings: list[str]) -> list[str]:
    """Sort strings by their length.

    Args:
        strings: List of strings.

    Returns:
        New list sorted by string length.
    """
    raise NotImplementedError("Implement sort_by_length")


def sort_by_last_letter(strings: list[str]) -> list[str]:
    """Sort strings by their last letter.

    Args:
        strings: List of strings.

    Returns:
        New list sorted by last character.
    """
    raise NotImplementedError("Implement sort_by_last_letter")


def sort_tuples_by_second_item(tuples: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Sort tuples by their second element.

    Args:
        tuples: List of (str, int) tuples.

    Returns:
        New list sorted by second element of each tuple.
    """
    raise NotImplementedError("Implement sort_tuples_by_second_item")
