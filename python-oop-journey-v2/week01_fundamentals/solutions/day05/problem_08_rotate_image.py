"""Reference solution for Problem 08: Rotate Image."""

from __future__ import annotations


def rotate_image(matrix: list[list[int]]) -> None:
    """Rotate the matrix by 90 degrees clockwise (in-place).

    Args:
        matrix: An n x n 2D list of integers.

    Returns:
        None (modifies matrix in-place).
    """
    if not matrix or not matrix[0]:
        return

    n = len(matrix)

    # Step 1: Transpose the matrix (swap across diagonal)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: Reverse each row
    for i in range(n):
        matrix[i].reverse()
