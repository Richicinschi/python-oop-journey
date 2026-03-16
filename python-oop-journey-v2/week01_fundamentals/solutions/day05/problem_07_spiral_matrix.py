"""Reference solution for Problem 07: Spiral Matrix."""

from __future__ import annotations


def spiral_matrix(matrix: list[list[int]]) -> list[int]:
    """Return elements of matrix in spiral order.

    Args:
        matrix: A 2D list of integers (m x n).

    Returns:
        A list of integers in spiral order.
    """
    if not matrix or not matrix[0]:
        return []

    result: list[int] = []
    rows, cols = len(matrix), len(matrix[0])

    # Define boundaries
    top, bottom = 0, rows - 1
    left, right = 0, cols - 1

    while top <= bottom and left <= right:
        # Traverse right along the top row
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1

        # Traverse down along the right column
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1

        # Traverse left along the bottom row (if there's still a row)
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1

        # Traverse up along the left column (if there's still a column)
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1

    return result
