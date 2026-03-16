"""Problem 07: Subsets

Topic: Recursion, Backtracking
Difficulty: Medium

Generate all subsets (the power set) of a list of elements.

A subset is any combination of elements from the original list, including:
- The empty set []
- All individual elements
- All possible combinations
- The full set itself

Example:
    subsets([1, 2]) → [[], [1], [2], [1, 2]]
    subsets([1, 2, 3]) → [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]

Requirements:
    - Use recursion to build subsets
    - Return a list of all subsets
    - Each subset should be a list
    - The empty list is always a subset
    - The order of subsets in the result does not matter

Hint: For each element, you have two choices: include it or exclude it.
"""

from __future__ import annotations


def subsets(items: list) -> list[list]:
    """Generate all subsets (power set) of items.
    
    Args:
        items: A list of elements (can be any type)
        
    Returns:
        A list of all possible subsets, where each subset
        is a list containing some (or none) of the elements
        
    Examples:
        >>> sorted(subsets([1, 2]), key=len)
        [[], [1], [2], [1, 2]]
        >>> len(subsets([1, 2, 3]))
        8
        >>> subsets([])
        [[]]
    """
    raise NotImplementedError("Implement subsets")
