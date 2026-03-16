"""Problem 09: Pascal's Triangle

Topic: Pattern recognition, dynamic building, nested loops
Difficulty: Medium

Given an integer num_rows, return the first num_rows of Pascal's triangle.

In Pascal's triangle, each number is the sum of the two numbers directly 
above it. The first and last elements of each row are always 1.

Example:
Input: 5
Output: [
     [1],
    [1, 1],
   [1, 2, 1],
  [1, 3, 3, 1],
 [1, 4, 6, 4, 1]
]
"""

from __future__ import annotations


def pascals_triangle(num_rows: int) -> list[list[int]]:
    """Generate the first num_rows of Pascal's triangle.

    Args:
        num_rows: Number of rows to generate.

    Returns:
        A list of lists representing Pascal's triangle.

    Example:
        >>> pascals_triangle(5)
        [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
        >>> pascals_triangle(1)
        [[1]]
    """
    raise NotImplementedError("Implement pascals_triangle")
