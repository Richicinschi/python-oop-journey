"""Reference solution for Problem 04."""

from __future__ import annotations


def logical_and_or(a: bool, b: bool) -> dict[str, bool]:
    """Solve the problem."""
    return {
        'and': a and b,
        'or': a or b
    }
