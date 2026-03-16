"""Reference solution for Problem 03: Sum List Elements.

This solution demonstrates two approaches:
1. Manual iteration (shown below) - good for learning loops
2. Built-in sum() - preferred in production code

The manual approach helps understand how aggregation works.
"""

from __future__ import annotations


def sum_elements(numbers: list[int]) -> int:
    """Calculate the sum of all elements in a list.

    Args:
        numbers: A list of integers

    Returns:
        The sum of all elements (0 for empty list)
    """
    # Initialize accumulator to 0 (identity for addition)
    total = 0
    
    # Iterate through each number and add to total
    for num in numbers:
        total += num  # Same as: total = total + num
    
    # Return the accumulated sum
    # For empty list, loop never runs and returns 0 (correct!)
    return total
    
    # Production alternative: return sum(numbers)
