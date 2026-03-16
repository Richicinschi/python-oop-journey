"""Reference solution for Problem 08: Combination Sum."""

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
    result: list[list[int]] = []
    
    def backtrack(
        start_index: int,
        current_combination: list[int],
        remaining_target: int
    ) -> None:
        """Helper function for recursive backtracking.
        
        Args:
            start_index: Index in candidates to start from
            current_combination: Current combination being built
            remaining_target: Target minus sum of current_combination
        """
        # Base case: found a valid combination
        if remaining_target == 0:
            result.append(current_combination[:])  # Add a copy
            return
        
        # Base case: target exceeded
        if remaining_target < 0:
            return
        
        # Try each candidate from start_index
        for i in range(start_index, len(candidates)):
            candidate = candidates[i]
            
            # Include this candidate and continue (can reuse same index)
            current_combination.append(candidate)
            backtrack(i, current_combination, remaining_target - candidate)
            current_combination.pop()  # Backtrack
    
    backtrack(0, [], target)
    return result
