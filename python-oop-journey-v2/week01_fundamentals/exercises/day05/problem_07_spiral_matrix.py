"""Problem 07: Spiral Matrix

Topic: Nested loops, boundary tracking, 2D traversal
Difficulty: Medium

Given an m x n matrix, return all elements of the matrix in spiral order 
(clockwise, starting from the top-left corner).

Example:
Input: [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]]
Output: [1, 2, 3, 6, 9, 8, 7, 4, 5]
"""

from __future__ import annotations


def spiral_matrix(matrix: list[list[int]]) -> list[int]:
    """Return elements of matrix in spiral order.

    Args:
        matrix: A 2D list of integers (m x n).

    Returns:
        A list of integers in spiral order.

    Example:
        >>> spiral_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        [1, 2, 3, 6, 9, 8, 7, 4, 5]
        >>> spiral_matrix([[1, 2, 3, 4], [5, 6, 7, 8]])
        [1, 2, 3, 4, 8, 7, 6, 5]
    """
    raise NotImplementedError("Implement spiral_matrix")
