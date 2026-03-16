"""Reference solution for Problem 03: Find First Divisible."""

from __future__ import annotations


def find_first_divisible(start: int, divisor: int) -> int:
    """Find the first number >= start divisible by divisor.

    Args:
        start: Starting number (inclusive)
        divisor: Number to check divisibility by

    Returns:
        First number >= start that is divisible by divisor
    """
    current = start
    while True:
        if current % divisor == 0:
            return current
        current += 1
