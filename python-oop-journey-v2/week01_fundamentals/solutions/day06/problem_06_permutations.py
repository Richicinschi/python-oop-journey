"""Reference solution for Problem 06: Permutations."""

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
    # Base case: empty list has one permutation - the empty list
    if len(items) <= 1:
        return [items[:]]  # Return a copy to avoid aliasing issues
    
    result = []
    
    # For each item, place it first and permute the rest
    for i, item in enumerate(items):
        # Get remaining items (everything except items[i])
        remaining = items[:i] + items[i + 1:]
        
        # Recursively get all permutations of remaining items
        for perm in permutations(remaining):
            result.append([item] + perm)
    
    return result
