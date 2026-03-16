"""Problem 05: Binary Search Recursive

Topic: Recursion, Divide and Conquer
Difficulty: Easy

Implement binary search algorithm using recursion to find the index of a target
value in a sorted list.

Binary search works by:
1. Comparing the target with the middle element
2. If equal, return the middle index
3. If target is smaller, search the left half
4. If target is larger, search the right half

Example:
    binary_search([1, 2, 3, 4, 5], 3) → 2
    binary_search([1, 2, 3, 4, 5], 6) → -1 (not found)
    binary_search([], 5) → -1 (not found)

Requirements:
    - Use recursion to search subarrays
    - Return the index of target if found, -1 otherwise
    - The input array is guaranteed to be sorted
    - Do NOT modify the input array (use index parameters)
"""

from __future__ import annotations


def binary_search(arr: list[int], target: int, left: int = 0, right: int | None = None) -> int:
    """Find the index of target in sorted array using recursive binary search.
    
    Args:
        arr: A sorted list of integers in ascending order
        target: The value to search for
        left: The left index of the current search range (default 0)
        right: The right index of the current search range (default len(arr) - 1)
        
    Returns:
        The index of target if found, -1 otherwise
        
    Examples:
        >>> binary_search([1, 2, 3, 4, 5], 3)
        2
        >>> binary_search([1, 2, 3, 4, 5], 6)
        -1
        >>> binary_search([], 5)
        -1
    """
    raise NotImplementedError("Implement binary_search")
