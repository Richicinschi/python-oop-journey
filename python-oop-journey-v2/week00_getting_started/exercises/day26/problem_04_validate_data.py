"""Problem 04: Validate Data

Topic: Common Exceptions
Difficulty: Medium

Write a function that validates user data from a dictionary.

Check for required fields and valid types. Return a list of error messages.

Required fields:
- "name": must be a string
- "age": must be convertible to int (>= 0)
- "email": must be a string containing "@"

Examples:
    >>> validate_data({"name": "Alice", "age": "30", "email": "a@test.com"})
    []
    >>> validate_data({"name": "", "age": "-5", "email": "invalid"})
    ['name cannot be empty', 'age must be non-negative', 'email must contain @']

Requirements:
    - Check all three required fields exist
    - Validate name is non-empty string
    - Validate age is non-negative integer
    - Validate email contains @
    - Return list of all validation errors
"""

from __future__ import annotations


def validate_data(data: dict) -> list:
    """Validate user data and return list of errors.

    Args:
        data: Dictionary containing user data

    Returns:
        List of error message strings (empty if valid)
    """
    raise NotImplementedError("Implement validate_data")
