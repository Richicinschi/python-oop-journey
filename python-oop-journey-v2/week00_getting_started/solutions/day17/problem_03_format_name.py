"""Problem 03: Format Name - Solution."""

from __future__ import annotations


def format_name(first: str, last: str, middle: str | None = None) -> str:
    """Format a full name with optional middle name.

    Args:
        first: First name.
        last: Last name.
        middle: Middle name (optional). If None, not included.

    Returns:
        Formatted full name. With middle: "First Middle Last"
        Without middle: "First Last"
    """
    if middle:
        return f"{first} {middle} {last}"
    return f"{first} {last}"
