"""Reference solution for Problem 05."""

from __future__ import annotations


def calculate_remainder_and_quotient(dividend: int, divisor: int) -> dict[str, int]:
    """Solve the problem."""
    return {
        'quotient': dividend // divisor,
        'remainder': dividend % divisor
    }
