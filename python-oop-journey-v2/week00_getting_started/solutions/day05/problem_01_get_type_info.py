"""Reference solution for Problem 01."""

from __future__ import annotations


def get_type_info(value: int | float | str | bool) -> str:
    """Solve the problem."""
    return type(value).__name__
