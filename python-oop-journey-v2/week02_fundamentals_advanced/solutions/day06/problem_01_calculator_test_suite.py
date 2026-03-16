"""Reference solution for Problem 01: Calculator Test Suite."""

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
