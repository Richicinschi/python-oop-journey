"""Problem 03: Strategy vs Conditionals - Solution.

Uses Strategy pattern to replace conditional chains with interchangeable algorithms.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass
class OrderContext:
    """Context object containing order information."""
    customer_id: str
    customer_type: str
    order_total: Decimal
    item_count: int
    items: list[dict[str, Any]]


class DiscountStrategy(ABC):
    """Abstract base class for discount strategies."""
    
    @abstractmethod
    def calculate_discount(self, context: OrderContext) -> Decimal:
        raise NotImplementedError
    
    @abstractmethod
    def get_description(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_discount_name(self) -> str:
        raise NotImplementedError


class RegularCustomerDiscount(DiscountStrategy):
    """Regular customers: 5% discount on orders over $100."""
    
    def calculate_discount(self, context: OrderContext) -> Decimal:
        if context.order_total >= Decimal("100"):
            return context.order_total * Decimal("0.05")
        return Decimal("0")
    
    def get_description(self) -> str:
        return "5% discount on orders over $100"
    
    def get_discount_name(self) -> str:
        return "regular"


class PremiumCustomerDiscount(DiscountStrategy):
    """Premium customers: 10% base + 2% per $500, max 25%."""
    
    def calculate_discount(self, context: OrderContext) -> Decimal:
        base_discount = context.order_total * Decimal("0.10")
        tier_bonus = min(
            (context.order_total // Decimal("500")) * Decimal("0.02"),
            Decimal("0.15"),
        )
        return context.order_total * (Decimal("0.10") + tier_bonus)
    
    def get_description(self) -> str:
        return "10-25% tiered discount"
    
    def get_discount_name(self) -> str:
        return "premium"


class VipCustomerDiscount(DiscountStrategy):
    """VIP customers: 20% base + 5% if order > $1000."""
    
    def calculate_discount(self, context: OrderContext) -> Decimal:
        discount = context.order_total * Decimal("0.20")
        if context.order_total > Decimal("1000"):
            discount += context.order_total * Decimal("0.05")
        return discount
    
    def get_description(self) -> str:
        return "20-25% based on order size"
    
    def get_discount_name(self) -> str:
        return "vip"


class BulkOrderDiscount(DiscountStrategy):
    """Bulk orders: tiered discount based on item count."""
    
    def calculate_discount(self, context: OrderContext) -> Decimal:
        if context.item_count >= 100:
            rate = Decimal("0.30")
        elif context.item_count >= 50:
            rate = Decimal("0.20")
        elif context.item_count >= 20:
            rate = Decimal("0.10")
        else:
            rate = Decimal("0.05")
        return context.order_total * rate
    
    def get_description(self) -> str:
        return "5-30% based on quantity"
    
    def get_discount_name(self) -> str:
        return "bulk"


class DiscountCalculator:
    """Calculator that uses Strategy pattern for extensible discounts."""
    
    def __init__(self, default_strategy: DiscountStrategy | None = None) -> None:
        self._strategy = default_strategy
    
    def set_strategy(self, strategy: DiscountStrategy) -> None:
        """Change the discount strategy at runtime."""
        self._strategy = strategy
    
    def calculate_discount(self, context: OrderContext) -> Decimal:
        """Calculate discount using current strategy."""
        if self._strategy is None:
            return Decimal("0")
        return self._strategy.calculate_discount(context)
    
    def get_discount_description(self) -> str:
        """Get description of current strategy."""
        if self._strategy is None:
            return "No discount"
        return self._strategy.get_description()
    
    def get_strategy_name(self) -> str:
        """Get name of current strategy."""
        if self._strategy is None:
            return "none"
        return self._strategy.get_discount_name()


class StrategyRegistry:
    """Registry for managing available discount strategies."""
    
    def __init__(self) -> None:
        self._strategies: dict[str, DiscountStrategy] = {}
    
    def register(self, name: str, strategy: DiscountStrategy) -> None:
        """Register a strategy with a name."""
        self._strategies[name] = strategy
    
    def get(self, name: str) -> DiscountStrategy | None:
        """Get strategy by name."""
        return self._strategies.get(name)
    
    def list_strategies(self) -> list[str]:
        """List all registered strategy names."""
        return list(self._strategies.keys())
    
    def create_calculator(self, name: str) -> DiscountCalculator | None:
        """Create a calculator with the named strategy."""
        strategy = self.get(name)
        if strategy:
            return DiscountCalculator(strategy)
        return None
