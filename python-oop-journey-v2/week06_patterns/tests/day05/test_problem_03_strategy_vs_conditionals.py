"""Tests for Problem 03: Strategy vs Conditionals."""

from __future__ import annotations

from decimal import Decimal

import pytest

from week06_patterns.solutions.day05.problem_03_strategy_vs_conditionals import (
    BulkOrderDiscount,
    DiscountCalculator,
    DiscountStrategy,
    OrderContext,
    PremiumCustomerDiscount,
    RegularCustomerDiscount,
    StrategyRegistry,
    VipCustomerDiscount,
)


class TestOrderContext:
    """Tests for OrderContext dataclass."""
    
    def test_context_creation(self) -> None:
        context = OrderContext(
            customer_id="C001",
            customer_type="regular",
            order_total=Decimal("150.00"),
            item_count=3,
            items=[],
        )
        assert context.customer_id == "C001"
        assert context.order_total == Decimal("150.00")


class TestRegularCustomerDiscount:
    """Tests for RegularCustomerDiscount strategy."""
    
    def test_discount_name(self) -> None:
        strategy = RegularCustomerDiscount()
        assert strategy.get_discount_name() == "regular"
    
    def test_discount_description(self) -> None:
        strategy = RegularCustomerDiscount()
        assert "5%" in strategy.get_description()
    
    def test_no_discount_under_threshold(self) -> None:
        strategy = RegularCustomerDiscount()
        context = OrderContext("C001", "regular", Decimal("50.00"), 1, [])
        
        discount = strategy.calculate_discount(context)
        assert discount == Decimal("0")
    
    def test_discount_over_threshold(self) -> None:
        strategy = RegularCustomerDiscount()
        context = OrderContext("C001", "regular", Decimal("100.00"), 1, [])
        
        discount = strategy.calculate_discount(context)
        assert discount == Decimal("5.00")  # 5% of 100
    
    def test_discount_calculated_correctly(self) -> None:
        strategy = RegularCustomerDiscount()
        context = OrderContext("C001", "regular", Decimal("200.00"), 1, [])
        
        discount = strategy.calculate_discount(context)
        assert discount == Decimal("10.00")  # 5% of 200


class TestPremiumCustomerDiscount:
    """Tests for PremiumCustomerDiscount strategy."""
    
    def test_discount_name(self) -> None:
        strategy = PremiumCustomerDiscount()
        assert strategy.get_discount_name() == "premium"
    
    def test_base_discount(self) -> None:
        strategy = PremiumCustomerDiscount()
        context = OrderContext("C001", "premium", Decimal("100.00"), 1, [])
        
        discount = strategy.calculate_discount(context)
        assert discount == Decimal("10.00")  # 10% base
    
    def test_tiered_discount(self) -> None:
        strategy = PremiumCustomerDiscount()
        # $1000 order = 10% + 4% (2 tiers of $500) = 14%
        context = OrderContext("C001", "premium", Decimal("1000.00"), 1, [])
        
        discount = strategy.calculate_discount(context)
        assert discount == Decimal("140.00")  # 14% of 1000


class TestVipCustomerDiscount:
    """Tests for VipCustomerDiscount strategy."""
    
    def test_discount_name(self) -> None:
        strategy = VipCustomerDiscount()
        assert strategy.get_discount_name() == "vip"
    
    def test_base_vip_discount(self) -> None:
        strategy = VipCustomerDiscount()
        context = OrderContext("C001", "vip", Decimal("500.00"), 1, [])
        
        discount = strategy.calculate_discount(context)
        assert discount == Decimal("100.00")  # 20% of 500
    
    def test_bonus_discount_over_1000(self) -> None:
        strategy = VipCustomerDiscount()
        context = OrderContext("C001", "vip", Decimal("1001.00"), 1, [])
        
        discount = strategy.calculate_discount(context)
        # 20% + 5% = 25%
        expected = Decimal("1001.00") * Decimal("0.25")
        assert discount == expected


class TestBulkOrderDiscount:
    """Tests for BulkOrderDiscount strategy."""
    
    def test_discount_name(self) -> None:
        strategy = BulkOrderDiscount()
        assert strategy.get_discount_name() == "bulk"
    
    def test_tier_30_percent_for_100_items(self) -> None:
        strategy = BulkOrderDiscount()
        context = OrderContext("C001", "bulk", Decimal("1000.00"), 100, [])
        
        discount = strategy.calculate_discount(context)
        assert discount == Decimal("300.00")  # 30% of 1000
    
    def test_tier_20_percent_for_50_items(self) -> None:
        strategy = BulkOrderDiscount()
        context = OrderContext("C001", "bulk", Decimal("1000.00"), 50, [])
        
        discount = strategy.calculate_discount(context)
        assert discount == Decimal("200.00")  # 20% of 1000
    
    def test_tier_10_percent_for_20_items(self) -> None:
        strategy = BulkOrderDiscount()
        context = OrderContext("C001", "bulk", Decimal("1000.00"), 20, [])
        
        discount = strategy.calculate_discount(context)
        assert discount == Decimal("100.00")  # 10% of 1000
    
    def test_tier_5_percent_for_few_items(self) -> None:
        strategy = BulkOrderDiscount()
        context = OrderContext("C001", "bulk", Decimal("1000.00"), 5, [])
        
        discount = strategy.calculate_discount(context)
        assert discount == Decimal("50.00")  # 5% of 1000


class TestDiscountCalculator:
    """Tests for DiscountCalculator."""
    
    def test_calculator_with_no_strategy(self) -> None:
        calculator = DiscountCalculator()
        context = OrderContext("C001", "any", Decimal("100.00"), 1, [])
        
        discount = calculator.calculate_discount(context)
        assert discount == Decimal("0")
    
    def test_calculator_with_strategy(self) -> None:
        calculator = DiscountCalculator(RegularCustomerDiscount())
        context = OrderContext("C001", "regular", Decimal("100.00"), 1, [])
        
        discount = calculator.calculate_discount(context)
        assert discount == Decimal("5.00")
    
    def test_set_strategy_at_runtime(self) -> None:
        calculator = DiscountCalculator()
        context = OrderContext("C001", "vip", Decimal("1000.00"), 1, [])
        
        # Start with no strategy
        assert calculator.calculate_discount(context) == Decimal("0")
        
        # Switch to VIP strategy
        calculator.set_strategy(VipCustomerDiscount())
        discount = calculator.calculate_discount(context)
        assert discount == Decimal("200.00")  # 20% of 1000
    
    def test_get_strategy_name(self) -> None:
        calculator = DiscountCalculator(RegularCustomerDiscount())
        assert calculator.get_strategy_name() == "regular"
    
    def test_get_discount_description(self) -> None:
        calculator = DiscountCalculator(RegularCustomerDiscount())
        assert "5%" in calculator.get_discount_description()


class TestStrategyRegistry:
    """Tests for StrategyRegistry."""
    
    def test_register_and_get_strategy(self) -> None:
        registry = StrategyRegistry()
        strategy = RegularCustomerDiscount()
        
        registry.register("regular", strategy)
        retrieved = registry.get("regular")
        
        assert retrieved is strategy
    
    def test_get_nonexistent_strategy(self) -> None:
        registry = StrategyRegistry()
        assert registry.get("nonexistent") is None
    
    def test_list_strategies(self) -> None:
        registry = StrategyRegistry()
        registry.register("regular", RegularCustomerDiscount())
        registry.register("vip", VipCustomerDiscount())
        
        strategies = registry.list_strategies()
        assert "regular" in strategies
        assert "vip" in strategies
    
    def test_create_calculator(self) -> None:
        registry = StrategyRegistry()
        registry.register("premium", PremiumCustomerDiscount())
        
        calculator = registry.create_calculator("premium")
        assert calculator is not None
        assert isinstance(calculator, DiscountCalculator)
        
        # Test the calculator works
        context = OrderContext("C001", "premium", Decimal("100.00"), 1, [])
        assert calculator.calculate_discount(context) == Decimal("10.00")
    
    def test_create_calculator_with_unknown_strategy(self) -> None:
        registry = StrategyRegistry()
        calculator = registry.create_calculator("unknown")
        assert calculator is None


class TestStrategyPatternBenefits:
    """Tests demonstrating Strategy pattern benefits."""
    
    def test_strategies_are_interchangeable(self) -> None:
        """Different strategies can be used with same calculator."""
        context = OrderContext("C001", "any", Decimal("100.00"), 1, [])
        
        strategies = [
            RegularCustomerDiscount(),
            PremiumCustomerDiscount(),
            VipCustomerDiscount(),
            BulkOrderDiscount(),
        ]
        
        for strategy in strategies:
            calculator = DiscountCalculator(strategy)
            result = calculator.calculate_discount(context)
            assert isinstance(result, Decimal)
    
    def test_strategies_independent_and_testable(self) -> None:
        """Each strategy can be tested independently."""
        # Test just RegularCustomerDiscount without other code
        regular = RegularCustomerDiscount()
        context = OrderContext("C001", "regular", Decimal("200.00"), 1, [])
        
        discount = regular.calculate_discount(context)
        assert discount == Decimal("10.00")
    
    def test_open_closed_principle(self) -> None:
        """Can add new strategies without modifying existing code."""
        # Define a new custom strategy inline
        class CustomDiscount(DiscountStrategy):
            def calculate_discount(self, context: OrderContext) -> Decimal:
                return Decimal("99.99")
            
            def get_description(self) -> str:
                return "Custom discount"
            
            def get_discount_name(self) -> str:
                return "custom"
        
        # Use it without modifying any existing classes
        custom = CustomDiscount()
        calculator = DiscountCalculator(custom)
        
        context = OrderContext("C001", "any", Decimal("100.00"), 1, [])
        assert calculator.calculate_discount(context) == Decimal("99.99")
