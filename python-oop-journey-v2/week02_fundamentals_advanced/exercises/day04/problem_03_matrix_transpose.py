"""Problem 03: Matrix Transpose

Topic: List Comprehensions, 2D Arrays
Difficulty: Easy

Transpose a matrix (2D list) using a list comprehension.
The transpose of a matrix swaps its rows and columns.
"""

from __future__ import annotations


def matrix_transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Transpose a matrix using list comprehension.

    Args:
        matrix: A 2D list representing a matrix.
            Assumes all rows have equal length.

    Returns:
        The transposed matrix where rows become columns.

    Example:
        >>> matrix_transpose([[1, 2, 3], [4, 5, 6]])
        [[1, 4], [2, 5], [3, 6]]
        >>> matrix_transpose([[1, 2], [3, 4], [5, 6]])
        [[1, 3, 5], [2, 4, 6]]
    """
    raise NotImplementedError("Implement matrix_transpose")
