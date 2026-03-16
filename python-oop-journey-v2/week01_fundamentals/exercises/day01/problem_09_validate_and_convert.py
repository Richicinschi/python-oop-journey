"""Problem 09: Validate and Convert

Topic: Type conversion, error handling
Difficulty: Medium

Write a function that validates whether a string can be converted to an integer
and returns the converted value or None if invalid.

Examples:
    >>> validate_and_convert("123")
    123
    >>> validate_and_convert("-456")
    -456
    >>> validate_and_convert("12.34")
    None
    >>> validate_and_convert("abc")
    None
    >>> validate_and_convert("")
    None

Requirements:
    - Return the integer value if the string represents a valid integer
    - Return None if the string cannot be converted to an integer
    - Handle positive and negative numbers
    - Handle empty strings
    - Whitespace should be stripped before validation
"""

from __future__ import annotations


def validate_and_convert(value: str) -> int | None:
    """Validate and convert a string to an integer.

    Args:
        value: String to validate and convert

    Returns:
        Integer value if valid, None otherwise
    """
    raise NotImplementedError("Implement validate_and_convert")
