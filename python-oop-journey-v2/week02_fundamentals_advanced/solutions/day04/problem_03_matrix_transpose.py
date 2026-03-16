"""Reference solution for Problem 03: Matrix Transpose."""

from __future__ import annotations


def matrix_transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Transpose a matrix using list comprehension.

    The transpose is computed by using zip(*matrix) to group elements
    by column index, then converting each tuple back to a list.

    Args:
        matrix: A 2D list representing a matrix.
            Assumes all rows have equal length.

    Returns:
        The transposed matrix where rows become columns.
    """
    if not matrix:
        return []
    return [list(row) for row in zip(*matrix)]
