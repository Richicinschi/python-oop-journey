"""Reference solution for Problem 09: Validate and Convert."""

from __future__ import annotations


def validate_and_convert(value: str) -> int | None:
    """Validate and convert a string to an integer.

    Args:
        value: String to validate and convert

    Returns:
        Integer value if valid, None otherwise
    """
    if not value or not isinstance(value, str):
        return None

    stripped = value.strip()

    if not stripped:
        return None

    try:
        return int(stripped)
    except ValueError:
        return None
