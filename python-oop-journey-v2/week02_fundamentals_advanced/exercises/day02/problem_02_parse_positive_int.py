"""Problem 02: Parse Positive Integer

Topic: Exception Handling, Validation
Difficulty: Easy

Write a function that parses a string to a positive integer with validation.

Examples:
    >>> parse_positive_int("42")
    42
    >>> parse_positive_int("-5")
    'Error: Value must be positive'
    >>> parse_positive_int("abc")
    'Error: Invalid integer format'
    >>> parse_positive_int("0")
    'Error: Value must be positive'

Requirements:
    - Return the integer if the string represents a positive integer (> 0)
    - Return specific error messages for different failure cases
    - Strip whitespace from the input before parsing
"""

from __future__ import annotations


def parse_positive_int(value: str) -> int | str:
    """Parse a string to a positive integer.

    Args:
        value: The string to parse

    Returns:
        The positive integer if valid, or an error message string
    """
    raise NotImplementedError("Implement parse_positive_int")
