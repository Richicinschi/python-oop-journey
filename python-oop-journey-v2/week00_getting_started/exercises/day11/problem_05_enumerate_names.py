"""Problem 05: Enumerate Names

Topic: For Loops, enumerate()
Difficulty: Easy

Write a function that formats a list of names with their positions.
Returns a list of formatted strings like "1. Alice", "2. Bob", etc.

Examples:
    >>> enumerate_names(["Alice", "Bob", "Charlie"])
    ['1. Alice', '2. Bob', '3. Charlie']
    >>> enumerate_names(["Solo"])
    ['1. Solo']
    >>> enumerate_names([])
    []

Requirements:
    - Use enumerate() with start=1
    - Format each item as "N. Name"
    - Return list of formatted strings
"""

from __future__ import annotations


def enumerate_names(names: list[str]) -> list[str]:
    """Format names with their position numbers.

    Args:
        names: List of names

    Returns:
        List of formatted strings like "1. Name"
    """
    raise NotImplementedError("Implement enumerate_names")
