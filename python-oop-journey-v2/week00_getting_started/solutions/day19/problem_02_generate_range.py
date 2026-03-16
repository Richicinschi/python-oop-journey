"""Problem 02: Generate Range - Solution."""

from __future__ import annotations


def get_numbers_up_to(n: int) -> list[int]:
    """Return a list of numbers from 0 to n-1.

    Args:
        n: The upper limit (exclusive).

    Returns:
        List of integers from 0 to n-1.
    """
    return list(range(n))


def get_numbers_between(start: int, end: int) -> list[int]:
    """Return a list of numbers from start to end-1.

    Args:
        start: The starting number (inclusive).
        end: The ending number (exclusive).

    Returns:
        List of integers from start to end-1.
    """
    return list(range(start, end))


def get_even_numbers_up_to(n: int) -> list[int]:
    """Return a list of even numbers from 0 to n-1.

    Args:
        n: The upper limit (exclusive).

    Returns:
        List of even integers from 0 to n-1.
    """
    return list(range(0, n, 2))


def get_countdown(start: int) -> list[int]:
    """Return a countdown list from start to 1.

    Args:
        start: The number to start counting down from.

    Returns:
        List of integers from start down to 1.
    """
    return list(range(start, 0, -1))
