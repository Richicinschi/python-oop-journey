"""Reference solution for Problem 02."""

from __future__ import annotations


def compare_numbers(a: int | float, b: int | float) -> dict[str, bool]:
    """Solve the problem."""
    return {
        'greater': a > b,
        'equal': a == b,
        'less': a < b
    }
