"""Reference solution for Problem 02: Safe Convert."""

from __future__ import annotations


def safe_convert(value: str, default: int = 0) -> int:
    """Safely convert a string to an integer.

    Args:
        value: The string to convert
        default: The value to return if conversion fails

    Returns:
        The integer value or the default
    """
    try:
        return int(value)
    except ValueError:
        return default
    except TypeError:
        return default
