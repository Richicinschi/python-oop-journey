"""Problem 03: Strategy vs Conditionals

Topic: Pattern Tradeoffs and Anti-patterns
Difficulty: Medium

Convert a class with complex if-elif-else conditional chains into
the Strategy pattern for better extensibility and testability.

The `DiscountCalculator` uses a long chain of conditionals to
calculate discounts based on customer type. This makes it hard to:
- Add new customer types
- Test each discount type independently
- Reuse discount logic elsewhere

Your task: Apply the Strategy pattern to make discount strategies
interchangeable and independently testable.

Classes to implement:
- DiscountStrategy (abstract base)
- RegularCustomerDiscount
- PremiumCustomerDiscount
- VipCustomerDiscount
- BulkOrderDiscount
- DiscountCalculator (uses strategies)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Any


# BEFORE: The conditional approach (do not modify - for reference)
class ConditionalDiscountCalculator:
    """Discount calculator using if-elif chains.
    
    Problems:
    - Adding new customer types requires modifying this class
    - Violates Open/Closed Principle
    - Hard to test each discount type independently
    - Discount logic mixed with validation logic
    """
    
    def calculate_discount(
        self,
        customer_type: str,
        order_total: Decimal,
        item_count: int,
    ) -> Decimal:
        """Calculate discount based on customer type."""
        if customer_type == "regular":
            # Regular customers: 5% discount on orders over $100
            if order_total >= Decimal("100"):
                return order_total * Decimal("0.05")
            return Decimal("0")
        
        elif customer_type == "premium":
            # Premium customers: 10% base + 2% per $500, max 25%
            base_discount = order_total * Decimal("0.10")
            bonus_discount = min(
                (order_total // Decimal("500")) * Decimal("0.02") * order_total,
                order_total * Decimal("0.15")  # max 15% bonus
            )
            return base_discount + bonus_discount
        
        elif customer_type == "vip":
            # VIP customers: 20% base + 5% if order > $1000
            discount = order_total * Decimal("0.20")
            if order_total > Decimal("1000"):
                discount += order_total * Decimal("0.05")
            return discount
        
        elif customer_type == "bulk":
            # Bulk orders: tiered discount based on item count
            if item_count >= 100:
                return order_total * Decimal("0.30")
            elif item_count >= 50:
                return order_total * Decimal("0.20")
            elif item_count >= 20:
                return order_total * Decimal("0.10")
            else:
                return order_total * Decimal("0.05")
        
        else:
            raise ValueError(f"Unknown customer type: {customer_type}")
    
    def get_discount_description(self, customer_type: str) -> str:
        """Get human-readable discount description."""
        descriptions = {
            "regular": "5% on orders over $100",
            "premium": "10-25% tiered",
            "vip": "20-25% based on order size",
            "bulk": "5-30% based on quantity",
        }
        return descriptions.get(customer_type, "No discount available")


# AFTER: Your Strategy pattern implementation (implement these)

@dataclass
class OrderContext:
    """Context object containing order information."""
    customer_id: str
    customer_type: str
    order_total: Decimal
    item_count: int
    items: list[dict[str, Any]]


class DiscountStrategy(ABC):
    """Abstract base class for discount strategies.
    
    Each concrete strategy implements a specific discount calculation.
    This allows:
    - Adding new discounts without modifying existing code
    - Testing each strategy independently
    - Reusing strategies in different contexts
    """
    
    @abstractmethod
    def calculate_discount(self, context: OrderContext) -> Decimal:
        """Calculate discount amount for the given order.
        
        Args:
            context: Order information
        
        Returns:
            Discount amount (not percentage)
        """
        raise NotImplementedError("Implement calculate_discount")
    
    @abstractmethod
    def get_description(self) -> str:
        """Get human-readable description of this discount."""
        raise NotImplementedError("Implement get_description")
    
    @abstractmethod
    def get_discount_name(self) -> str:
        """Get short name/identifier for this discount type."""
        raise NotImplementedError("Implement get_discount_name")


class RegularCustomerDiscount(DiscountStrategy):
    """Regular customers: 5% discount on orders over $100."""
    
    def calculate_discount(self, context: OrderContext) -> Decimal:
        """Calculate regular customer discount."""
        raise NotImplementedError("Implement calculate_discount")
    
    def get_description(self) -> str:
        """Get discount description."""
        raise NotImplementedError("Implement get_description")
    
    def get_discount_name(self) -> str:
        """Get discount name."""
        raise NotImplementedError("Implement get_discount_name")


class PremiumCustomerDiscount(DiscountStrategy):
    """Premium customers: 10% base + 2% per $500, max 25%."""
    
    def calculate_discount(self, context: OrderContext) -> Decimal:
        """Calculate premium customer discount."""
        raise NotImplementedError("Implement calculate_discount")
    
    def get_description(self) -> str:
        """Get discount description."""
        raise NotImplementedError("Implement get_description")
    
    def get_discount_name(self) -> str:
        """Get discount name."""
        raise NotImplementedError("Implement get_discount_name")


class VipCustomerDiscount(DiscountStrategy):
    """VIP customers: 20% base + 5% if order > $1000."""
    
    def calculate_discount(self, context: OrderContext) -> Decimal:
        """Calculate VIP customer discount."""
        raise NotImplementedError("Implement calculate_discount")
    
    def get_description(self) -> str:
        """Get discount description."""
        raise NotImplementedError("Implement get_description")
    
    def get_discount_name(self) -> str:
        """Get discount name."""
        raise NotImplementedError("Implement get_discount_name")


class BulkOrderDiscount(DiscountStrategy):
    """Bulk orders: tiered discount based on item count.
    
    - 100+ items: 30%
    - 50-99 items: 20%
    - 20-49 items: 10%
    - <20 items: 5%
    """
    
    def calculate_discount(self, context: OrderContext) -> Decimal:
        """Calculate bulk order discount."""
        raise NotImplementedError("Implement calculate_discount")
    
    def get_description(self) -> str:
        """Get discount description."""
        raise NotImplementedError("Implement get_description")
    
    def get_discount_name(self) -> str:
        """Get discount name."""
        raise NotImplementedError("Implement get_discount_name")


class DiscountCalculator:
    """Calculator that uses Strategy pattern for extensible discounts.
    
    This class is now open for extension (add new strategies)
    but closed for modification (no changes needed to add strategies).
    """
    
    def __init__(self, default_strategy: DiscountStrategy | None = None) -> None:
        """Initialize with optional default strategy.
        
        Args:
            default_strategy: Strategy to use if none specified
        """
        raise NotImplementedError("Implement __init__")
    
    def set_strategy(self, strategy: DiscountStrategy) -> None:
        """Change the discount strategy at runtime.
        
        Args:
            strategy: New strategy to use
        """
        raise NotImplementedError("Implement set_strategy")
    
    def calculate_discount(self, context: OrderContext) -> Decimal:
        """Calculate discount using current strategy.
        
        Args:
            context: Order information
        
        Returns:
            Discount amount
        """
        raise NotImplementedError("Implement calculate_discount")
    
    def get_discount_description(self) -> str:
        """Get description of current strategy."""
        raise NotImplementedError("Implement get_discount_description")
    
    def get_strategy_name(self) -> str:
        """Get name of current strategy."""
        raise NotImplementedError("Implement get_strategy_name")


class StrategyRegistry:
    """Registry for managing available discount strategies.
    
    Allows lookup of strategies by name, enabling configuration-driven
    strategy selection.
    """
    
    def __init__(self) -> None:
        raise NotImplementedError("Implement __init__")
    
    def register(self, name: str, strategy: DiscountStrategy) -> None:
        """Register a strategy with a name."""
        raise NotImplementedError("Implement register")
    
    def get(self, name: str) -> DiscountStrategy | None:
        """Get strategy by name."""
        raise NotImplementedError("Implement get")
    
    def list_strategies(self) -> list[str]:
        """List all registered strategy names."""
        raise NotImplementedError("Implement list_strategies")
    
    def create_calculator(self, name: str) -> DiscountCalculator | None:
        """Create a calculator with the named strategy."""
        raise NotImplementedError("Implement create_calculator")
