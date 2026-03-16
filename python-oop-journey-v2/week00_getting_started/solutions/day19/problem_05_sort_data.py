"""Problem 05: Sort Data - Solution."""

from __future__ import annotations


def sort_ascending(numbers: list[int]) -> list[int]:
    """Sort numbers in ascending order.

    Args:
        numbers: List of integers to sort.

    Returns:
        New list with numbers sorted from smallest to largest.
    """
    return sorted(numbers)


def sort_descending(numbers: list[int]) -> list[int]:
    """Sort numbers in descending order.

    Args:
        numbers: List of integers to sort.

    Returns:
        New list with numbers sorted from largest to smallest.
    """
    return sorted(numbers, reverse=True)


def sort_by_length(strings: list[str]) -> list[str]:
    """Sort strings by their length.

    Args:
        strings: List of strings to sort.

    Returns:
        New list with strings sorted by length (shortest first).
    """
    return sorted(strings, key=len)


def sort_by_last_letter(strings: list[str]) -> list[str]:
    """Sort strings by their last letter.

    Args:
        strings: List of strings to sort.

    Returns:
        New list with strings sorted by last letter alphabetically.
    """
    return sorted(strings, key=lambda s: s[-1] if s else "")


def sort_tuples_by_second_item(tuples: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Sort tuples by their second element (the integer).

    Args:
        tuples: List of (string, int) tuples.

    Returns:
        New list sorted by the integer value.
    """
    return sorted(tuples, key=lambda x: x[1])
