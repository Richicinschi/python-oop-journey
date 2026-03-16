"""Reference solution for Problem 05: Enumerate Names."""

from __future__ import annotations


def enumerate_names(names: list[str]) -> list[str]:
    """Format names with their position numbers.

    Args:
        names: List of names

    Returns:
        List of formatted strings like "1. Name"
    """
    result: list[str] = []
    for index, name in enumerate(names, start=1):
        result.append(f"{index}. {name}")
    return result
