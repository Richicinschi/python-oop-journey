"""Problem 01: Identify Error Type

Topic: Understanding Errors
Difficulty: Easy

Write a function that identifies what type of error would occur in a given scenario.

The function should return the error type name as a string for these scenarios:
- "division_by_zero" → "ZeroDivisionError"
- "undefined_variable" → "NameError"
- "wrong_type" → "TypeError"
- "index_too_big" → "IndexError"
- "key_not_found" → "KeyError"
- "invalid_conversion" → "ValueError"

Examples:
    >>> identify_error("division_by_zero")
    'ZeroDivisionError'
    >>> identify_error("undefined_variable")
    'NameError'

Requirements:
    - Return the exact error type name as a string
    - Handle all six scenarios listed above
"""

from __future__ import annotations


def identify_error(scenario: str) -> str:
    """Return the error type name for a given scenario.

    Args:
        scenario: A string describing an error scenario

    Returns:
        The name of the Python exception type as a string
    """
    raise NotImplementedError("Implement identify_error")
