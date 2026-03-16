"""Reference solution for Problem 06: Exception Assertion Suite."""

from __future__ import annotations

from typing import List, TypeVar

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
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
    if value <= 0:
        raise ValidationError(f"{name} must be a positive integer, got {value}")
    return value


def validate_email(email: str) -> str:
    """Validate an email address format.

    Args:
        email: The email address to validate.

    Returns:
        The validated email address.

    Raises:
        ValidationError: If email format is invalid.
    """
    if not isinstance(email, str):
        raise ValidationError("Email must be a string")
    if "@" not in email:
        raise ValidationError(f"Invalid email format: {email}")
    parts = email.split("@")
    if len(parts) != 2 or not parts[0] or "." not in parts[1]:
        raise ValidationError(f"Invalid email format: {email}")
    if " " in email:
        raise ValidationError(f"Email cannot contain spaces: {email}")
    return email


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
    if not isinstance(dividend, (int, float)):
        raise TypeError(f"Dividend must be a number, got {type(dividend).__name__}")
    if not isinstance(divisor, (int, float)):
        raise TypeError(f"Divisor must be a number, got {type(divisor).__name__}")
    if divisor == 0:
        raise ZeroDivisionError(f"Cannot divide {dividend} by zero")
    return dividend / divisor


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
    if not isinstance(items, list):
        raise TypeError(f"items must be a list, got {type(items).__name__}")
    if not callable(predicate):
        raise TypeError(f"predicate must be callable, got {type(predicate).__name__}")

    for item in items:
        if predicate(item):
            return item
    raise NotFoundError("No item matches the predicate")


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
    if not isinstance(value, str):
        raise TypeError(f"Value must be a string, got {type(value).__name__}")
    try:
        result = float(value)
    except ValueError as e:
        raise ValidationError(f"Cannot parse '{value}' as a float") from e
    if result <= 0:
        raise ValidationError(f"Value must be positive, got {result}")
    return result
