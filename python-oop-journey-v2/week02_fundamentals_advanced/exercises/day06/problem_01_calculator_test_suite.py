"""Problem 01: Calculator Test Suite

Topic: Writing comprehensive tests
Difficulty: Easy

Write tests for a Calculator class that supports basic arithmetic operations.

Your task:
    1. Read the Calculator class implementation below
    2. Create comprehensive tests covering:
       - Normal cases (positive numbers, negative numbers, zero)
       - Edge cases (very large numbers, floating point)
       - Error cases (division by zero)

Example usage of the Calculator:
    >>> calc = Calculator()
    >>> calc.add(2, 3)
    5
    >>> calc.divide(10, 2)
    5.0
    >>> calc.divide(5, 0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: Cannot divide by zero
"""

from __future__ import annotations


class Calculator:
    """Simple calculator with basic arithmetic operations."""

    def add(self, a: float, b: float) -> float:
        """Return the sum of a and b."""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Return the difference of a and b."""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Return the product of a and b."""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Return the quotient of a divided by b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    def power(self, base: float, exponent: float) -> float:
        """Return base raised to the power of exponent."""
        return base ** exponent

    def absolute(self, value: float) -> float:
        """Return the absolute value."""
        return abs(value)


# TODO: Write tests for the Calculator class in the corresponding test file.
# The test file should import this Calculator and test all its methods.
