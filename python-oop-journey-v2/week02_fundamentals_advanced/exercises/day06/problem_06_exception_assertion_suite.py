"""Problem 06: Exception Assertion Suite

Topic: Testing exception raising with pytest.raises
Difficulty: Medium

Create functions with validation and write comprehensive exception tests.

Your task:
    1. Implement validation functions that raise specific exceptions
    2. Write tests using pytest.raises to verify exception behavior
    3. Test both exception type and exception message

Example:
    >>> validate_positive_integer("age", 25)
    25
    >>> validate_positive_integer("age", -5)
    Traceback (most recent call last):
        ...
    ValueError: age must be a positive integer, got -5
    >>> divide_safely(10, 0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: Cannot divide 10 by zero
"""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


class ValidationError(ValueError):
    """Raised when validation fails."""
    pass


class NotFoundError(LookupError):
    """Raised when an item is not found."""
    pass


def validate_positive_integer(name: str, value: int) -> int:
    """Validate that value is a positive integer.

    Args:
        name: Name of the field being validated (for error messages).
        value: The value to validate.

    Returns:
        The validated value.

    Raises:
        TypeError: If value is not an integer.
        ValidationError: If value is not positive.
    """
    # TODO: Implement validation with proper error messages
    raise NotImplementedError("Implement validate_positive_integer")


def validate_email(email: str) -> str:
    """Validate an email address format.

    Args:
        email: The email address to validate.

    Returns:
        The validated email address.

    Raises:
        ValidationError: If email format is invalid.
    """
    # TODO: Implement email validation
    raise NotImplementedError("Implement validate_email")


def divide_safely(dividend: float, divisor: float) -> float:
    """Safely divide two numbers with detailed error messages.

    Args:
        dividend: The number to divide.
        divisor: The number to divide by.

    Returns:
        The quotient.

    Raises:
        TypeError: If inputs are not numbers.
        ZeroDivisionError: If divisor is zero (with custom message).
    """
    # TODO: Implement safe division
    raise NotImplementedError("Implement divide_safely")


def find_in_list(items: list[T], predicate) -> T:
    """Find the first item matching a predicate.

    Args:
        items: List to search.
        predicate: Function that returns True for matching items.

    Returns:
        The first matching item.

    Raises:
        NotFoundError: If no item matches the predicate.
        TypeError: If items is not a list or predicate is not callable.
    """
    # TODO: Implement find with proper exceptions
    raise NotImplementedError("Implement find_in_list")


def parse_positive_float(value: str) -> float:
    """Parse a string as a positive float.

    Args:
        value: The string to parse.

    Returns:
        The parsed positive float.

    Raises:
        TypeError: If value is not a string.
        ValidationError: If string cannot be parsed or is not positive.
    """
    # TODO: Implement parsing with validation
    raise NotImplementedError("Implement parse_positive_float")


# TODO: Write tests using pytest.raises() to verify:
# 1. The correct exception type is raised
# 2. The exception message contains expected content
# 3. Use match parameter to check message patterns
# 4. Test both the exception and successful cases
#
# Example:
# def test_validate_positive_integer_negative():
#     with pytest.raises(ValidationError, match="must be a positive integer"):
#         validate_positive_integer("age", -5)
