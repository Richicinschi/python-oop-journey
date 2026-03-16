"""Problem 02: Calculator Module with Constants

Topic: Module-level constants and functions
Difficulty: Easy

Create a calculator module that includes mathematical constants
and basic arithmetic operations.

Required constants:
- PI: 3.14159
- E: 2.71828
- GOLDEN_RATIO: 1.61803

Required functions:
- add(a, b): Addition
- subtract(a, b): Subtraction
- multiply(a, b): Multiplication
- divide(a, b): Division (handle division by zero)
- circle_area(radius): Calculate area using PI

Example usage:
    >>> from calculator_constants import PI, add, circle_area
    >>> add(5, 3)
    8
    >>> circle_area(2)
    12.56636
"""

from __future__ import annotations

# Define module-level constants
PI: float = 0.0  # TODO: Set to 3.14159
E: float = 0.0  # TODO: Set to 2.71828
GOLDEN_RATIO: float = 0.0  # TODO: Set to 1.61803


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    raise NotImplementedError("Implement add")


def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers."""
    raise NotImplementedError("Implement subtract")


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    raise NotImplementedError("Implement multiply")


def divide(a: float, b: float) -> float | None:
    """Return the quotient of two numbers.

    Returns None if division by zero.
    """
    raise NotImplementedError("Implement divide")


def circle_area(radius: float) -> float:
    """Calculate the area of a circle given its radius.

    Formula: PI * radius^2
    """
    raise NotImplementedError("Implement circle_area")
