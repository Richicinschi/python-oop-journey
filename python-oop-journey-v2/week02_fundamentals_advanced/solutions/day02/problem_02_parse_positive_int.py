"""Solution for Problem 02: Parse Positive Integer."""

from __future__ import annotations


def parse_positive_int(value: str) -> int | str:
    """Parse a string to a positive integer.

    Args:
        value: The string to parse

    Returns:
        The positive integer if valid, or an error message string
    """
    try:
        parsed = int(value.strip())
        if parsed <= 0:
            return "Error: Value must be positive"
        return parsed
    except ValueError:
        return "Error: Invalid integer format"
