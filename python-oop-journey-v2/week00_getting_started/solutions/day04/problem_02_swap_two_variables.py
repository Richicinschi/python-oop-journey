"""Reference solution for Problem 02."""

from __future__ import annotations


def swap_two_variables(a: int | str, b: int | str) -> tuple[int | str, int | str]:
    """Solve the problem."""
    temp = a
    a = b
    b = temp
    return (a, b)
