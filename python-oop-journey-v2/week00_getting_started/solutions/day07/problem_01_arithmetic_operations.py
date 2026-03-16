"""Reference solution for Problem 01."""

from __future__ import annotations


def arithmetic_operations(a: int | float, b: int | float) -> dict[str, int | float]:
    """Solve the problem."""
    return {
        'sum': a + b,
        'difference': a - b,
        'product': a * b,
        'quotient': round(a / b, 2) if b != 0 else 0
    }
