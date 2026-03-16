"""Problem 02: Money

Topic: Magic Methods - Arithmetic and Comparison
Difficulty: Easy

Implement a Money class with currency handling, arithmetic, and comparison operations.
"""

from __future__ import annotations


class Money:
    """Represents an amount of money with currency.
    
    All amounts are stored internally as cents (integer) to avoid
    floating-point precision issues.
    
    Attributes:
        amount_cents: The amount in the smallest currency unit (e.g., cents).
        currency: The three-letter currency code (e.g., 'USD', 'EUR').
    
    Example:
        >>> m1 = Money(10, 50, 'USD')  # $10.50
        >>> m2 = Money(5, 25, 'USD')   # $5.25
        >>> m1 + m2
        Money(15, 75, 'USD')
        >>> m1 > m2
        True
    """
    
    def __init__(self, dollars: int, cents: int, currency: str) -> None:
        """Initialize money with dollars, cents, and currency.
        
        Args:
            dollars: The whole dollar amount (can be negative).
            cents: The cents amount (0-99, can span across dollars).
            currency: The three-letter currency code.
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def dollars(self) -> int:
        """Return the whole dollar portion."""
        raise NotImplementedError("Implement dollars property")
    
    @property
    def cents(self) -> int:
        """Return the cents portion (0-99)."""
        raise NotImplementedError("Implement cents property")
    
    def __add__(self, other: Money) -> Money:
        """Add two money amounts (same currency only).
        
        Args:
            other: The money to add.
        
        Returns:
            A new Money instance with the sum.
        
        Raises:
            ValueError: If currencies don't match.
            TypeError: If other is not Money.
        """
        raise NotImplementedError("Implement __add__")
    
    def __sub__(self, other: Money) -> Money:
        """Subtract one money amount from another (same currency only).
        
        Args:
            other: The money to subtract.
        
        Returns:
            A new Money instance with the difference.
        
        Raises:
            ValueError: If currencies don't match.
            TypeError: If other is not Money.
        """
        raise NotImplementedError("Implement __sub__")
    
    def __eq__(self, other: object) -> bool:
        """Check if two money amounts are equal (value and currency)."""
        raise NotImplementedError("Implement __eq__")
    
    def __lt__(self, other: Money) -> bool:
        """Check if this money is less than other (same currency only).
        
        Raises:
            ValueError: If currencies don't match.
            TypeError: If other is not Money.
        """
        raise NotImplementedError("Implement __lt__")
    
    def __le__(self, other: Money) -> bool:
        """Check if this money is less than or equal to other."""
        raise NotImplementedError("Implement __le__")
    
    def __gt__(self, other: Money) -> bool:
        """Check if this money is greater than other."""
        raise NotImplementedError("Implement __gt__")
    
    def __ge__(self, other: Money) -> bool:
        """Check if this money is greater than or equal to other."""
        raise NotImplementedError("Implement __ge__")
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        raise NotImplementedError("Implement __repr__")
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        raise NotImplementedError("Implement __str__")
