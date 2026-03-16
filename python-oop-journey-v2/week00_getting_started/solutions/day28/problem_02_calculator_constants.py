"""Reference solution for Problem 02: Calculator Module with Constants."""

from __future__ import annotations

# Module-level constants
PI: float = 3.14159
E: float = 2.71828
GOLDEN_RATIO: float = 1.61803


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b


def divide(a: float, b: float) -> float | None:
    """Return the quotient of two numbers.

    Returns None if division by zero.
    """
    if b == 0:
        return None
    return a / b


def circle_area(radius: float) -> float:
    """Calculate the area of a circle given its radius.

    Formula: PI * radius^2
    """
    return PI * radius * radius
