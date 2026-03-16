"""Problem 08: Combination Sum

Topic: Recursion, Backtracking
Difficulty: Medium

Find all unique combinations of candidates where the chosen numbers sum to target.
Each number in candidates may be used multiple times.

Example:
    combination_sum([2, 3, 6, 7], 7) → [[2, 2, 3], [7]]
    combination_sum([2, 3, 5], 8) → [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    combination_sum([2], 1) → [] (no combination possible)

Requirements:
    - Use recursion with backtracking
    - Return a list of all valid combinations
    - Each combination should be a sorted list (or maintain input order)
    - Each number can be used unlimited times
    - Combinations should be unique (no duplicates in result)
    - Return empty list if no valid combinations exist

Hint: At each step, decide whether to include the current number (and stay at
same index since it can be reused) or exclude it and move to next index.
"""

from __future__ import annotations


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """Find all unique combinations that sum to target.
    
    Each number in candidates may be used multiple times.
    
    Args:
        candidates: A list of distinct positive integers
        target: The target sum to achieve
        
    Returns:
        A list of all unique combinations that sum to target
        
    Examples:
        >>> sorted(combination_sum([2, 3, 6, 7], 7))
        [[2, 2, 3], [7]]
        >>> combination_sum([2], 1)
        []
        >>> combination_sum([], 5)
        []
    """
    raise NotImplementedError("Implement combination_sum")
