"""Problem 03: Validate Age with Custom Exception

Topic: Custom Exceptions
Difficulty: Easy

Create a custom exception class and use it to validate age values.

Examples:
    >>> validate_age(25)
    25
    >>> validate_age(0)
    Traceback (most recent call last):
        ...
    InvalidAgeError: Age must be between 1 and 150, got 0
    >>> validate_age(200)
    Traceback (most recent call last):
        ...
    InvalidAgeError: Age must be between 1 and 150, got 200

Requirements:
    - Create InvalidAgeError exception class inheriting from ValueError
    - Valid age is between 1 and 150 (inclusive)
    - Raise InvalidAgeError with descriptive message for invalid ages
    - Return the age if valid
"""

from __future__ import annotations


class InvalidAgeError(ValueError):
    """Raised when an age value is invalid."""
    pass


def validate_age(age: int) -> int:
    """Validate that age is within acceptable range.

    Args:
        age: The age value to validate

    Returns:
        The age if valid

    Raises:
        InvalidAgeError: If age is not between 1 and 150
    """
    raise NotImplementedError("Implement validate_age")
