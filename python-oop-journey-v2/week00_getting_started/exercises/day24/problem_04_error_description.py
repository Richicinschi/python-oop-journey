"""Problem 04: Error Description

Topic: Understanding Error Messages
Difficulty: Easy

Write a function that returns a human-friendly description of common errors.

Given an error type name, return a helpful explanation:
- "ZeroDivisionError" → "Cannot divide a number by zero"
- "NameError" → "Variable name is not defined"
- "TypeError" → "Operation applied to wrong type"
- "ValueError" → "Right type but inappropriate value"
- "IndexError" → "Sequence index out of range"
- "KeyError" → "Dictionary key not found"
- "AttributeError" → "Object has no such attribute"

Examples:
    >>> describe_error("ZeroDivisionError")
    'Cannot divide a number by zero'
    >>> describe_error("NameError")
    'Variable name is not defined'

Requirements:
    - Return a helpful description for common error types
    - Return "Unknown error type" for unrecognized errors
"""

from __future__ import annotations


def describe_error(error_type: str) -> str:
    """Return a human-friendly description of an error type.

    Args:
        error_type: The name of the error type

    Returns:
        A description of what the error means
    """
    raise NotImplementedError("Implement describe_error")
