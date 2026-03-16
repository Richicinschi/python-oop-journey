"""Reference solution for Problem 06: Comparison Ready Money."""

from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from typing import Self


@dataclass(order=True)
class Money:
    """Monetary value with proper comparison support."""
    
    amount_cents: int
    currency: str = field(default="USD", compare=False)
    _normalized: tuple[str, int] = field(init=False, repr=False)
    
    def __post_init__(self) -> None:
        """Set up the normalized sort key."""
        self._normalized = (self.currency, self.amount_cents)
    
    @classmethod
    def from_decimal(cls, amount: Decimal | float | str, currency: str = "USD") -> Money:
        """Create Money from decimal/float/string amount."""
        if isinstance(amount, str):
            amount = Decimal(amount)
        elif isinstance(amount, float):
            # Convert through string to avoid float precision issues
            amount = Decimal(str(amount))
        
        # Convert to cents and round
        cents = int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        return cls(amount_cents=cents, currency=currency)
    
    @classmethod
    def zero(cls, currency: str = "USD") -> Money:
        """Create zero amount in given currency."""
        return cls(amount_cents=0, currency=currency)
    
    @classmethod
    def parse(cls, amount_str: str, currency: str = "USD") -> Money:
        """Parse money from string like "$10.50" or "20.00"."""
        # Remove currency symbols and whitespace
        cleaned = amount_str.strip()
        for symbol in "$€£¥":
            cleaned = cleaned.replace(symbol, "")
        cleaned = cleaned.replace(",", "").strip()
        
        return cls.from_decimal(cleaned, currency)
    
    def to_decimal(self) -> Decimal:
        """Convert to Decimal for display."""
        return Decimal(self.amount_cents) / 100
    
    def format(self, symbol: bool = True) -> str:
        """Format money for display."""
        amount = self.to_decimal()
        amount_str = f"{amount:.2f}"
        
        if not symbol:
            return f"{amount_str} {self.currency}"
        
        # Add currency symbol
        symbols = {"USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"}
        curr_symbol = symbols.get(self.currency, self.currency)
        return f"{curr_symbol}{amount_str}"
    
    def add(self, other: Money) -> Money:
        """Add two Money amounts (must be same currency)."""
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot add {self.currency} and {other.currency}"
            )
        return Money(
            amount_cents=self.amount_cents + other.amount_cents,
            currency=self.currency
        )
    
    def subtract(self, other: Money) -> Money:
        """Subtract other from this amount (must be same currency)."""
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot subtract {other.currency} from {self.currency}"
            )
        return Money(
            amount_cents=self.amount_cents - other.amount_cents,
            currency=self.currency
        )
    
    def multiply(self, factor: float | Decimal) -> Money:
        """Multiply by a scalar factor."""
        if isinstance(factor, float):
            factor = Decimal(str(factor))
        
        new_cents = int((Decimal(self.amount_cents) * factor).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP
        ))
        return Money(amount_cents=new_cents, currency=self.currency)
    
    def allocate(self, ratios: list[int]) -> list[Money]:
        """Allocate money according to ratios (no penny lost)."""
        if not ratios:
            return []
        
        total_ratio = sum(ratios)
        if total_ratio == 0:
            return [Money.zero(self.currency) for _ in ratios]
        
        # Calculate allocations
        total = self.amount_cents
        allocations = []
        remainder = total
        
        for i, ratio in enumerate(ratios[:-1]):
            share = int((Decimal(total) * ratio / total_ratio).quantize(
                Decimal("1"), rounding=ROUND_HALF_UP
            ))
            allocations.append(Money(share, self.currency))
            remainder -= share
        
        # Last allocation gets the remainder to ensure sum equals total
        allocations.append(Money(remainder, self.currency))
        
        return allocations
    
    def is_zero(self) -> bool:
        """Check if amount is zero."""
        return self.amount_cents == 0
    
    def is_positive(self) -> bool:
        """Check if amount is positive."""
        return self.amount_cents > 0
    
    def is_negative(self) -> bool:
        """Check if amount is negative."""
        return self.amount_cents < 0
    
    def abs(self) -> Money:
        """Return absolute value."""
        return Money(abs(self.amount_cents), self.currency)
    
    def with_currency(self, new_currency: str, exchange_rate: float) -> Money:
        """Convert to different currency.
        
        Args:
            new_currency: Target currency code
            exchange_rate: Rate in dollars (new_currency / current_currency)
            
        Returns:
            New Money in target currency
        """
        # Convert cents to dollars, apply rate, then convert back to cents
        dollars = self.amount_cents / 100
        new_dollars = dollars * exchange_rate
        new_cents = int((new_dollars * 100))
        return Money(new_cents, new_currency)


@dataclass(order=True)
class PriceRange:
    """A price range with minimum and maximum prices."""
    
    min_price: Money = field(compare=True)
    max_price: Money = field(compare=False)
    _sort_key: tuple[int, str] = field(init=False, repr=False)
    
    def __post_init__(self) -> None:
        """Set up sort key and validate."""
        if self.min_price.currency != self.max_price.currency:
            raise ValueError("min_price and max_price must have same currency")
        
        if self.min_price.amount_cents > self.max_price.amount_cents:
            raise ValueError("min_price cannot be greater than max_price")
        
        self._sort_key = (self.min_price.amount_cents, self.min_price.currency)
    
    def contains(self, price: Money) -> bool:
        """Check if price falls within this range."""
        if price.currency != self.min_price.currency:
            return False
        return (
            self.min_price.amount_cents <= price.amount_cents <=
            self.max_price.amount_cents
        )
    
    def overlaps(self, other: PriceRange) -> bool:
        """Check if this range overlaps with another."""
        if self.min_price.currency != other.min_price.currency:
            return False
        
        return (
            self.min_price.amount_cents <= other.max_price.amount_cents and
            other.min_price.amount_cents <= self.max_price.amount_cents
        )
    
    def midpoint(self) -> Money:
        """Calculate midpoint of range."""
        mid_cents = (self.min_price.amount_cents + self.max_price.amount_cents) // 2
        return Money(mid_cents, self.min_price.currency)
