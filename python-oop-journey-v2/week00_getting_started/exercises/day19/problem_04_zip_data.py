"""Problem 04: Zip Data

Topic: Built-in Functions - zip()
Difficulty: Easy

Write a function that combines multiple lists using zip().

Function Signature:
    def zip_data(names: list[str], ages: list[int], cities: list[str]) -> list[tuple[str, int, str]]

Requirements:
    - Use zip() to combine the three lists
    - Return a list of tuples (name, age, city)
    - Stop at the shortest list (zip's default behavior)

Behavior Notes:
    - zip() pairs elements from multiple iterables
    - Stops when the shortest iterable is exhausted
    - Returns an iterator, convert to list

Examples:
    >>> zip_data(["Alice", "Bob"], [30, 25], ["NYC", "LA"])
    [('Alice', 30, 'NYC'), ('Bob', 25, 'LA')]
    
    Unequal lengths:
    >>> zip_data(["A", "B", "C"], [1, 2], ["X", "Y", "Z"])
    [('A', 1, 'X'), ('B', 2, 'Y')]  # Stops at shortest (ages)
    
    Empty lists:
    >>> zip_data([], [], [])
    []

Input Validation:
    - You may assume inputs are lists of appropriate types

"""

from __future__ import annotations


def zip_data(names: list[str], ages: list[int], cities: list[str]) -> list[tuple[str, int, str]]:
    """Combine multiple lists using zip().

    Args:
        names: List of names.
        ages: List of ages.
        cities: List of cities.

    Returns:
        A list of (name, age, city) tuples.
    """
    raise NotImplementedError("Implement zip_data")
