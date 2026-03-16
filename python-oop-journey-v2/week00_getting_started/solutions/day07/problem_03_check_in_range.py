"""Reference solution for Problem 03."""

from __future__ import annotations


def check_in_range(value: int | float, min_val: int | float, max_val: int | float) -> bool:
    """Solve the problem."""
    return min_val <= value <= max_val
