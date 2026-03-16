"""Reference solution for Problem 02: Print Pattern."""

from __future__ import annotations


def print_pattern(n: int) -> list[str]:
    """Generate a triangle pattern of asterisks.

    Args:
        n: Number of rows

    Returns:
        List of strings, each containing asterisks for that row
    """
    result: list[str] = []
    for i in range(1, n + 1):
        row = ""
        for j in range(i):
            row += "*"
        result.append(row)
    return result
