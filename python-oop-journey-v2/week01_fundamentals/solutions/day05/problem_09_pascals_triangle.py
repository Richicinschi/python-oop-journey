"""Reference solution for Problem 09: Pascal's Triangle."""

from __future__ import annotations


def pascals_triangle(num_rows: int) -> list[list[int]]:
    """Generate the first num_rows of Pascal's triangle.

    Args:
        num_rows: Number of rows to generate.

    Returns:
        A list of lists representing Pascal's triangle.
    """
    if num_rows <= 0:
        return []

    triangle: list[list[int]] = []

    for i in range(num_rows):
        # Each row has i + 1 elements
        row: list[int] = [1] * (i + 1)

        # Fill in the middle elements (not first or last)
        # Each element is the sum of the two elements above it
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]

        triangle.append(row)

    return triangle
