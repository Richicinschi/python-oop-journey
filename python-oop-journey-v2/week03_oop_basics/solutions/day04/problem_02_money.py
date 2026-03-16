"""Reference solution for Problem 02: Money."""

from __future__ import annotations


class Money:
    """Represents an amount of money with currency.
    
    All amounts are stored internally as cents (integer) to avoid
    floating-point precision issues.
    
    Attributes:
        amount_cents: The amount in the smallest currency unit (e.g., cents).
        currency: The three-letter currency code (e.g., 'USD', 'EUR').
    """
    
    def __init__(self, dollars: int, cents: int, currency: str) -> None:
        """Initialize money with dollars, cents, and currency.
        
        Args:
            dollars: The whole dollar amount (can be negative).
            cents: The cents amount (0-99, can span across dollars).
            currency: The three-letter currency code.
        """
        self._currency = currency.upper()
        # Normalize to total cents
        total_cents = dollars * 100 + cents
        self._amount_cents = total_cents
    
    @property
    def dollars(self) -> int:
        """Return the whole dollar portion."""
        return self._amount_cents // 100
    
    @property
    def cents(self) -> int:
        """Return the cents portion (0-99, preserves sign of total)."""
        abs_cents = abs(self._amount_cents) % 100
        return abs_cents if self._amount_cents >= 0 else -abs_cents
    
    @property
    def currency(self) -> str:
        """Return the currency code."""
        return self._currency
    
    def _check_currency(self, other: Money) -> None:
        """Verify that currencies match."""
        if self._currency != other._currency:
            raise ValueError(
                f"Cannot operate on different currencies: {self._currency} and {other._currency}"
            )
    
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
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        total_cents = self._amount_cents + other._amount_cents
        return Money(total_cents // 100, total_cents % 100, self._currency)
    
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
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        total_cents = self._amount_cents - other._amount_cents
        return Money(total_cents // 100, total_cents % 100, self._currency)
    
    def __eq__(self, other: object) -> bool:
        """Check if two money amounts are equal (value and currency)."""
        if not isinstance(other, Money):
            return NotImplemented
        return (
            self._amount_cents == other._amount_cents
            and self._currency == other._currency
        )
    
    def __lt__(self, other: Money) -> bool:
        """Check if this money is less than other (same currency only).
        
        Raises:
            ValueError: If currencies don't match.
            TypeError: If other is not Money.
        """
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return self._amount_cents < other._amount_cents
    
    def __le__(self, other: Money) -> bool:
        """Check if this money is less than or equal to other."""
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return self._amount_cents <= other._amount_cents
    
    def __gt__(self, other: Money) -> bool:
        """Check if this money is greater than other."""
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return self._amount_cents > other._amount_cents
    
    def __ge__(self, other: Money) -> bool:
        """Check if this money is greater than or equal to other."""
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return self._amount_cents >= other._amount_cents
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        return f"Money({self.dollars}, {abs(self.cents)}, {self._currency!r})"
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        abs_cents = abs(self._amount_cents)
        abs_dollars = abs_cents // 100
        cents_only = abs_cents % 100
        sign = "-" if self._amount_cents < 0 else ""
        return f"{sign}{self._currency} {abs_dollars}.{cents_only:02d}"
