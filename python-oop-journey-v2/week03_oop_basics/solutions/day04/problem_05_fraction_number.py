"""Reference solution for Problem 05: Fraction Number."""

from __future__ import annotations

import math


class FractionNumber:
    """Represents a rational number with automatic simplification.
    
    The fraction is always stored in its simplest form with a positive denominator.
    
    Attributes:
        numerator: The numerator of the fraction.
        denominator: The denominator of the fraction (always positive).
    """
    
    def __init__(self, numerator: int, denominator: int) -> None:
        """Initialize a fraction and simplify it.
        
        Args:
            numerator: The numerator.
            denominator: The denominator (must not be zero).
        
        Raises:
            ZeroDivisionError: If denominator is zero.
        """
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        self.numerator = numerator
        self.denominator = denominator
        self._simplify()
    
    def _simplify(self) -> None:
        """Simplify the fraction to lowest terms and ensure positive denominator."""
        # Ensure positive denominator
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator
        
        # Simplify using GCD
        gcd = math.gcd(abs(self.numerator), abs(self.denominator))
        if gcd > 1:
            self.numerator //= gcd
            self.denominator //= gcd
    
    def __add__(self, other: FractionNumber) -> FractionNumber:
        """Add two fractions.
        
        Args:
            other: The fraction to add.
        
        Returns:
            A new FractionNumber with the sum.
        
        Raises:
            TypeError: If other is not a FractionNumber.
        """
        if not isinstance(other, FractionNumber):
            return NotImplemented
        new_num = self.numerator * other.denominator + other.numerator * self.denominator
        new_den = self.denominator * other.denominator
        return FractionNumber(new_num, new_den)
    
    def __sub__(self, other: FractionNumber) -> FractionNumber:
        """Subtract one fraction from another."""
        if not isinstance(other, FractionNumber):
            return NotImplemented
        new_num = self.numerator * other.denominator - other.numerator * self.denominator
        new_den = self.denominator * other.denominator
        return FractionNumber(new_num, new_den)
    
    def __mul__(self, other: FractionNumber) -> FractionNumber:
        """Multiply two fractions."""
        if not isinstance(other, FractionNumber):
            return NotImplemented
        new_num = self.numerator * other.numerator
        new_den = self.denominator * other.denominator
        return FractionNumber(new_num, new_den)
    
    def __truediv__(self, other: FractionNumber) -> FractionNumber:
        """Divide one fraction by another.
        
        Raises:
            ZeroDivisionError: If other fraction is zero.
        """
        if not isinstance(other, FractionNumber):
            return NotImplemented
        if other.numerator == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        new_num = self.numerator * other.denominator
        new_den = self.denominator * other.numerator
        return FractionNumber(new_num, new_den)
    
    def __eq__(self, other: object) -> bool:
        """Check if two fractions are equal."""
        if not isinstance(other, FractionNumber):
            return NotImplemented
        return (
            self.numerator == other.numerator
            and self.denominator == other.denominator
        )
    
    def __lt__(self, other: FractionNumber) -> bool:
        """Check if this fraction is less than other."""
        if not isinstance(other, FractionNumber):
            return NotImplemented
        # Compare by cross-multiplication to avoid floating point
        return self.numerator * other.denominator < other.numerator * self.denominator
    
    def __le__(self, other: FractionNumber) -> bool:
        """Check if this fraction is less than or equal to other."""
        if not isinstance(other, FractionNumber):
            return NotImplemented
        return self.numerator * other.denominator <= other.numerator * self.denominator
    
    def __gt__(self, other: FractionNumber) -> bool:
        """Check if this fraction is greater than other."""
        if not isinstance(other, FractionNumber):
            return NotImplemented
        return self.numerator * other.denominator > other.numerator * self.denominator
    
    def __ge__(self, other: FractionNumber) -> bool:
        """Check if this fraction is greater than or equal to other."""
        if not isinstance(other, FractionNumber):
            return NotImplemented
        return self.numerator * other.denominator >= other.numerator * self.denominator
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        return f"FractionNumber({self.numerator}, {self.denominator})"
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return f"{self.numerator}/{self.denominator}"
    
    def to_float(self) -> float:
        """Convert the fraction to a float."""
        return self.numerator / self.denominator
