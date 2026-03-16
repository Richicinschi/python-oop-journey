"""Reference solution for Problem 04: Error Description."""

from __future__ import annotations


def describe_error(error_type: str) -> str:
    """Return a human-friendly description of an error type.

    Args:
        error_type: The name of the error type

    Returns:
        A description of what the error means
    """
    descriptions = {
        "ZeroDivisionError": "Cannot divide a number by zero",
        "NameError": "Variable name is not defined",
        "TypeError": "Operation applied to wrong type",
        "ValueError": "Right type but inappropriate value",
        "IndexError": "Sequence index out of range",
        "KeyError": "Dictionary key not found",
        "AttributeError": "Object has no such attribute",
    }
    return descriptions.get(error_type, "Unknown error type")
