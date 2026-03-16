"""Problem 06: Permutations

Topic: Recursion, Backtracking
Difficulty: Medium

Generate all permutations (all possible arrangements) of a list of elements.

Example:
    permutations([1, 2]) → [[1, 2], [2, 1]]
    permutations([1, 2, 3]) → [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    permutations([]) → [[]]

Requirements:
    - Use recursion to build permutations
    - Return a list of all permutations
    - Each permutation should be a list
    - For empty input, return [[]] (list containing one empty list)
    - The order of permutations in the result does not matter

Hint: For each element, place it first and recursively permute the rest.
"""

from __future__ import annotations


def permutations(items: list) -> list[list]:
    """Generate all permutations of items.
    
    Args:
        items: A list of elements (can be any type)
        
    Returns:
        A list of all possible permutations, where each permutation
        is a list containing all elements in some order
        
    Examples:
        >>> sorted(permutations([1, 2]))
        [[1, 2], [2, 1]]
        >>> permutations([])
        [[]]
        >>> len(permutations([1, 2, 3]))
        6
    """
    raise NotImplementedError("Implement permutations")
