"""Reference solution for Problem 05: Binary Search Recursive."""

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
    # Initialize right on first call
    if right is None:
        right = len(arr) - 1
    
    # Base case: target not found
    if left > right:
        return -1
    
    # Find middle index
    mid = (left + right) // 2
    
    # Check if target is at mid
    if arr[mid] == target:
        return mid
    
    # Search left half
    if arr[mid] > target:
        return binary_search(arr, target, left, mid - 1)
    
    # Search right half
    return binary_search(arr, target, mid + 1, right)
