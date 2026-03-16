"""Problem 06: Comparison Ready Money

Topic: Dataclasses with ordering
Difficulty: Medium

Create a Money dataclass that supports comparison operations (ordering)
and implements proper equality semantics for monetary values.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from typing import Self


@dataclass(order=True)
class Money:
    """Monetary value with proper comparison support.
    
    Uses amount_cents internally for precise integer arithmetic
    to avoid floating-point errors common with money calculations.
    
    Attributes:
        amount_cents: Amount in smallest currency unit (cents, pence, etc.)
        currency: ISO 4217 currency code (default: "USD")
        _normalized: Internal sort key (auto-generated)
    
    Comparison Logic:
        - Only Money with same currency can be compared
        - Comparisons use amount_cents for precision
        - Equality considers both amount AND currency
    """
    
    amount_cents: int
    currency: str = field(default="USD", compare=False)
    _normalized: tuple[str, int] = field(init=False, repr=False)
    
    def __post_init__(self) -> None:
        """Set up the normalized sort key."""
        raise NotImplementedError("Implement Money.__post_init__")
    
    @classmethod
    def from_decimal(cls, amount: Decimal | float | str, currency: str = "USD") -> Money:
        """Create Money from decimal/float/string amount.
        
        Args:
            amount: Amount in main currency unit (e.g., dollars, euros)
            currency: ISO 4217 currency code
            
        Returns:
            Money instance with appropriate amount_cents
        """
        raise NotImplementedError("Implement Money.from_decimal")
    
    @classmethod
    def zero(cls, currency: str = "USD") -> Money:
        """Create zero amount in given currency.
        
        Args:
            currency: Currency code
            
        Returns:
            Money with zero amount
        """
        raise NotImplementedError("Implement Money.zero")
    
    @classmethod
    def parse(cls, amount_str: str, currency: str = "USD") -> Money:
        """Parse money from string like "$10.50" or "€20,00".
        
        Args:
            amount_str: String representation of amount
            currency: Currency code (overrides any in string if provided)
            
        Returns:
            Parsed Money instance
        """
        raise NotImplementedError("Implement Money.parse")
    
    def to_decimal(self) -> Decimal:
        """Convert to Decimal for display.
        
        Returns:
            Decimal amount in main currency unit
        """
        raise NotImplementedError("Implement Money.to_decimal")
    
    def format(self, symbol: bool = True) -> str:
        """Format money for display.
        
        Args:
            symbol: Whether to include currency symbol
            
        Returns:
            Formatted string like "$10.50" or "10.50 USD"
        """
        raise NotImplementedError("Implement Money.format")
    
    def add(self, other: Money) -> Money:
        """Add two Money amounts (must be same currency).
        
        Args:
            other: Money to add
            
        Returns:
            New Money with sum
            
        Raises:
            ValueError: If currencies don't match
        """
        raise NotImplementedError("Implement Money.add")
    
    def subtract(self, other: Money) -> Money:
        """Subtract other from this amount (must be same currency).
        
        Args:
            other: Money to subtract
            
        Returns:
            New Money with difference
            
        Raises:
            ValueError: If currencies don't match
        """
        raise NotImplementedError("Implement Money.subtract")
    
    def multiply(self, factor: float | Decimal) -> Money:
        """Multiply by a scalar factor.
        
        Args:
            factor: Multiplication factor
            
        Returns:
            New Money with multiplied amount
        """
        raise NotImplementedError("Implement Money.multiply")
    
    def allocate(self, ratios: list[int]) -> list[Money]:
        """Allocate money according to ratios (no penny lost).
        
        Used for splitting bills, distributing amounts, etc.
        
        Args:
            ratios: List of allocation ratios
            
        Returns:
            List of Money instances totaling to original amount
        """
        raise NotImplementedError("Implement Money.allocate")
    
    def is_zero(self) -> bool:
        """Check if amount is zero.
        
        Returns:
            True if amount_cents == 0
        """
        raise NotImplementedError("Implement Money.is_zero")
    
    def is_positive(self) -> bool:
        """Check if amount is positive.
        
        Returns:
            True if amount_cents > 0
        """
        raise NotImplementedError("Implement Money.is_positive")
    
    def is_negative(self) -> bool:
        """Check if amount is negative.
        
        Returns:
            True if amount_cents < 0
        """
        raise NotImplementedError("Implement Money.is_negative")
    
    def abs(self) -> Money:
        """Return absolute value.
        
        Returns:
            New Money with positive amount
        """
        raise NotImplementedError("Implement Money.abs")
    
    def with_currency(self, new_currency: str, exchange_rate: float) -> Money:
        """Convert to different currency.
        
        Args:
            new_currency: Target currency code
            exchange_rate: Rate to multiply by (new/old)
            
        Returns:
            New Money in target currency
        """
        raise NotImplementedError("Implement Money.with_currency")


@dataclass(order=True)
class PriceRange:
    """A price range with minimum and maximum prices.
    
    Supports ordering based on minimum price.
    
    Attributes:
        min_price: Lower bound of range
        max_price: Upper bound of range
        _sort_key: Internal sort key (auto-generated)
    """
    
    min_price: Money = field(compare=True)
    max_price: Money = field(compare=False)
    _sort_key: tuple[int, str] = field(init=False, repr=False)
    
    def __post_init__(self) -> None:
        """Set up sort key and validate."""
        raise NotImplementedError("Implement PriceRange.__post_init__")
    
    def contains(self, price: Money) -> bool:
        """Check if price falls within this range.
        
        Args:
            price: Price to check
            
        Returns:
            True if min_price <= price <= max_price
        """
        raise NotImplementedError("Implement PriceRange.contains")
    
    def overlaps(self, other: PriceRange) -> bool:
        """Check if this range overlaps with another.
        
        Args:
            other: Another price range
            
        Returns:
            True if ranges overlap (share at least one price)
        """
        raise NotImplementedError("Implement PriceRange.overlaps")
    
    def midpoint(self) -> Money:
        """Calculate midpoint of range.
        
        Returns:
            Money at the middle of the range
        """
        raise NotImplementedError("Implement PriceRange.midpoint")


# Hints for Comparison-Ready Money (Medium):
# 
# Hint 1 - Conceptual nudge:
# Use @dataclass(order=True) to enable comparison operators. You need to implement
# rich comparison methods (__lt__, __le__, __gt__, __ge__, __eq__).
#
# Hint 2 - Structural plan:
# - Implement __lt__ comparing amounts (same currency) or converted amounts
# - Use functools.total_ordering if you only want to implement __eq__ and one other
# - For operations like addition, return a new Money instance
# - Ensure currency compatibility before operations
#
# Hint 3 - Edge-case warning:
# Comparison between different currencies is tricky. Either raise an error or
# implement a conversion mechanism. Also, watch for floating-point precision
# issues with amounts.
