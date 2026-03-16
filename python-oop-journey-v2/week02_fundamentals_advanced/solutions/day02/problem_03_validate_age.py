"""Solution for Problem 03: Validate Age with Custom Exception."""

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
    if not 1 <= age <= 150:
        raise InvalidAgeError(f"Age must be between 1 and 150, got {age}")
    return age
