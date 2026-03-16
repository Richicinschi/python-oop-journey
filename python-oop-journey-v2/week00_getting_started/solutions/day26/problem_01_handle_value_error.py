"""Reference solution for Problem 01: Handle ValueError."""

from __future__ import annotations


def convert_number(value: str) -> int | float | None:
    """Convert a string to a number, handling ValueError.

    Args:
        value: The string to convert

    Returns:
        int if whole number, float if decimal, None if invalid
    """
    try:
        # Try int first
        return int(value)
    except ValueError:
        try:
            # Then try float
            return float(value)
        except ValueError:
            return None
