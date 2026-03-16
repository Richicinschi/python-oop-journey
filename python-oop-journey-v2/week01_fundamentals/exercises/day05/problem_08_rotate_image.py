"""Problem 08: Rotate Image

Topic: Nested loops, matrix manipulation, in-place operations
Difficulty: Medium

You are given an n x n 2D matrix representing an image, rotate the image by 
90 degrees (clockwise).

You have to rotate the image in-place, which means you have to modify the 
input 2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.

Example:
Input: [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]]
Output: [[7, 4, 1],
         [8, 5, 2],
         [9, 6, 3]]
"""

from __future__ import annotations


def rotate_image(matrix: list[list[int]]) -> None:
    """Rotate the matrix by 90 degrees clockwise (in-place).

    Args:
        matrix: An n x n 2D list of integers.

    Returns:
        None (modifies matrix in-place).

    Example:
        >>> matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        >>> rotate_image(matrix)
        >>> matrix
        [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    """
    raise NotImplementedError("Implement rotate_image")
