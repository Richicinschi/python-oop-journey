"""Reference solution for Problem 07: Subsets."""

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
    # Base case: empty list has one subset - the empty subset
    if not items:
        return [[]]
    
    # Recursive case: get all subsets of the rest
    first = items[0]
    rest_subsets = subsets(items[1:])
    
    # For each subset of the rest, create two subsets:
    # 1. The subset without 'first'
    # 2. The subset with 'first' added
    result = []
    for subset in rest_subsets:
        # Exclude first
        result.append(subset[:])
        # Include first
        result.append([first] + subset)
    
    return result
