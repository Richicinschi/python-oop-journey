"""Problem 05: Fraction Number

Topic: Magic Methods - Arithmetic and Comparison with Simplification
Difficulty: Medium

Implement a fraction class with automatic simplification.

Hints:
    - Hint 1: Use math.gcd() to simplify: divide both num and denom by gcd
    - Hint 2: Ensure positive denominator: if denom < 0, flip signs of both
    - Hint 3: Compare fractions by cross-multiplication: a/b < c/d iff a*d < c*b
"""

from __future__ import annotations

import math


class FractionNumber:
    """Represents a rational number with automatic simplification.
    
    The fraction is always stored in its simplest form with a positive denominator.
    
    Attributes:
        numerator: The numerator of the fraction.
        denominator: The denominator of the fraction (always positive).
    
    Example:
        >>> f1 = FractionNumber(2, 4)  # Automatically simplifies to 1/2
        >>> f1.numerator, f1.denominator
        (1, 2)
        >>> f2 = FractionNumber(1, 3)
        >>> f1 + f2
        FractionNumber(5, 6)
    """
    
    def __init__(self, numerator: int, denominator: int) -> None:
        """Initialize a fraction and simplify it.
        
        Args:
            numerator: The numerator.
            denominator: The denominator (must not be zero).
        
        Raises:
            ZeroDivisionError: If denominator is zero.
        """
        raise NotImplementedError("Implement __init__")
    
    def _simplify(self) -> None:
        """Simplify the fraction to lowest terms and ensure positive denominator."""
        raise NotImplementedError("Implement _simplify")
    
    def __add__(self, other: FractionNumber) -> FractionNumber:
        """Add two fractions.
        
        Args:
            other: The fraction to add.
        
        Returns:
            A new FractionNumber with the sum.
        
        Raises:
            TypeError: If other is not a FractionNumber.
        """
        raise NotImplementedError("Implement __add__")
    
    def __sub__(self, other: FractionNumber) -> FractionNumber:
        """Subtract one fraction from another."""
        raise NotImplementedError("Implement __sub__")
    
    def __mul__(self, other: FractionNumber) -> FractionNumber:
        """Multiply two fractions."""
        raise NotImplementedError("Implement __mul__")
    
    def __truediv__(self, other: FractionNumber) -> FractionNumber:
        """Divide one fraction by another.
        
        Raises:
            ZeroDivisionError: If other fraction is zero.
        """
        raise NotImplementedError("Implement __truediv__")
    
    def __eq__(self, other: object) -> bool:
        """Check if two fractions are equal."""
        raise NotImplementedError("Implement __eq__")
    
    def __lt__(self, other: FractionNumber) -> bool:
        """Check if this fraction is less than other."""
        raise NotImplementedError("Implement __lt__")
    
    def __le__(self, other: FractionNumber) -> bool:
        """Check if this fraction is less than or equal to other."""
        raise NotImplementedError("Implement __le__")
    
    def __gt__(self, other: FractionNumber) -> bool:
        """Check if this fraction is greater than other."""
        raise NotImplementedError("Implement __gt__")
    
    def __ge__(self, other: FractionNumber) -> bool:
        """Check if this fraction is greater than or equal to other."""
        raise NotImplementedError("Implement __ge__")
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        raise NotImplementedError("Implement __repr__")
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        raise NotImplementedError("Implement __str__")
    
    def to_float(self) -> float:
        """Convert the fraction to a float."""
        raise NotImplementedError("Implement to_float")
