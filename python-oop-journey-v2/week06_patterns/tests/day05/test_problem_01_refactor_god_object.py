"""Tests for Problem 01: Refactor God Object."""

from __future__ import annotations

from decimal import Decimal

import pytest

from week06_patterns.solutions.day05.problem_01_refactor_god_object import (
    Customer,
    CustomerService,
    InventoryService,
    Order,
    OrderService,
    PaymentResult,
    PaymentService,
    Product,
)


class TestProduct:
    """Tests for Product dataclass."""
    
    def test_product_creation(self) -> None:
        product = Product("SKU001", "Widget", Decimal("19.99"), 100)
        assert product.sku == "SKU001"
        assert product.name == "Widget"
        assert product.price == Decimal("19.99")
        assert product.stock == 100


class TestInventoryService:
    """Tests for InventoryService."""
    
    def test_add_and_get_product(self) -> None:
        service = InventoryService()
        product = Product("SKU001", "Widget", Decimal("19.99"), 100)
        service.add_product(product)
        
        retrieved = service.get_product("SKU001")
        assert retrieved is not None
        assert retrieved.name == "Widget"
    
    def test_get_nonexistent_product(self) -> None:
        service = InventoryService()
        assert service.get_product("NONEXISTENT") is None
    
    def test_check_stock(self) -> None:
        service = InventoryService()
        product = Product("SKU001", "Widget", Decimal("19.99"), 100)
        service.add_product(product)
        
        assert service.check_stock("SKU001") == 100
        assert service.check_stock("NONEXISTENT") == 0
    
    def test_update_stock(self) -> None:
        service = InventoryService()
        product = Product("SKU001", "Widget", Decimal("19.99"), 100)
        service.add_product(product)
        
        assert service.update_stock("SKU001", -10) is True
        assert service.check_stock("SKU001") == 90
        
        assert service.update_stock("NONEXISTENT", 10) is False
    
    def test_reserve_stock(self) -> None:
        service = InventoryService()
        product = Product("SKU001", "Widget", Decimal("19.99"), 100)
        service.add_product(product)
        
        assert service.reserve_stock("SKU001", 30) is True
        assert service.check_stock("SKU001") == 70
        
        assert service.reserve_stock("SKU001", 100) is False
        assert service.reserve_stock("NONEXISTENT", 10) is False
    
    def test_get_all_products(self) -> None:
        service = InventoryService()
        service.add_product(Product("SKU001", "Widget", Decimal("19.99"), 100))
        service.add_product(Product("SKU002", "Gadget", Decimal("29.99"), 50))
        
        all_products = service.get_all_products()
        assert len(all_products) == 2


class TestCustomerService:
    """Tests for CustomerService."""
    
    def test_register_and_get_customer(self) -> None:
        service = CustomerService()
        customer = Customer("C001", "Alice Smith", "alice@example.com")
        service.register_customer(customer)
        
        retrieved = service.get_customer("C001")
        assert retrieved is not None
        assert retrieved.name == "Alice Smith"
        assert retrieved.email == "alice@example.com"
    
    def test_get_nonexistent_customer(self) -> None:
        service = CustomerService()
        assert service.get_customer("NONEXISTENT") is None
    
    def test_customer_exists(self) -> None:
        service = CustomerService()
        service.register_customer(Customer("C001", "Alice", "alice@example.com"))
        
        assert service.customer_exists("C001") is True
        assert service.customer_exists("NONEXISTENT") is False


class TestPaymentService:
    """Tests for PaymentService."""
    
    def test_process_payment(self) -> None:
        service = PaymentService()
        result = service.process_payment("ORDER001", Decimal("99.99"), "credit_card")
        
        assert isinstance(result, PaymentResult)
        assert result.success is True
        assert result.amount == Decimal("99.99")
        assert result.method == "credit_card"
    
    def test_get_total_sales(self) -> None:
        service = PaymentService()
        service.process_payment("ORDER001", Decimal("50.00"), "cash")
        service.process_payment("ORDER002", Decimal("75.00"), "card")
        
        assert service.get_total_sales() == Decimal("125.00")
    
    def test_get_payment_count(self) -> None:
        service = PaymentService()
        assert service.get_payment_count() == 0
        
        service.process_payment("ORDER001", Decimal("50.00"), "cash")
        assert service.get_payment_count() == 1


class TestOrderService:
    """Tests for OrderService."""
    
    @pytest.fixture
    def setup_service(self) -> OrderService:
        inventory = InventoryService()
        inventory.add_product(Product("SKU001", "Widget", Decimal("10.00"), 100))
        inventory.add_product(Product("SKU002", "Gadget", Decimal("20.00"), 50))
        
        customers = CustomerService()
        customers.register_customer(Customer("C001", "Alice", "alice@example.com"))
        
        payments = PaymentService()
        
        return OrderService(inventory, customers, payments)
    
    def test_create_order_success(self, setup_service: OrderService) -> None:
        service = setup_service
        order = service.create_order("ORDER001", "C001", [("SKU001", 5), ("SKU002", 2)])
        
        assert isinstance(order, Order)
        assert order.order_id == "ORDER001"
        assert order.customer_id == "C001"
        assert order.total == Decimal("90.00")  # 5*10 + 2*20
        assert order.status == "pending"
    
    def test_create_order_invalid_customer(self, setup_service: OrderService) -> None:
        service = setup_service
        order = service.create_order("ORDER001", "NONEXISTENT", [("SKU001", 5)])
        
        assert order is None
    
    def test_create_order_insufficient_stock(self, setup_service: OrderService) -> None:
        service = setup_service
        order = service.create_order("ORDER001", "C001", [("SKU001", 999)])
        
        assert order is None
    
    def test_process_order_payment(self, setup_service: OrderService) -> None:
        service = setup_service
        order = service.create_order("ORDER001", "C001", [("SKU001", 5)])
        assert order is not None
        
        result = service.process_order_payment(order, "credit_card")
        
        assert isinstance(result, PaymentResult)
        assert result.success is True
        assert order.status == "paid"
    
    def test_inventory_report(self, setup_service: OrderService) -> None:
        service = setup_service
        report = service.get_inventory_report()
        
        assert len(report) == 2
    
    def test_sales_report(self, setup_service: OrderService) -> None:
        service = setup_service
        order = service.create_order("ORDER001", "C001", [("SKU001", 5)])
        assert order is not None
        service.process_order_payment(order, "credit_card")
        
        report = service.get_sales_report()
        
        assert "total_sales" in report
        assert "order_count" in report
        assert report["order_count"] == 1


class TestRefactoringBenefits:
    """Tests demonstrating the benefits of the refactored design."""
    
    def test_services_are_independent(self) -> None:
        """Each service can be tested independently."""
        inventory = InventoryService()
        customers = CustomerService()
        
        # Inventory works without customers or payments
        inventory.add_product(Product("SKU001", "Widget", Decimal("10.00"), 100))
        assert inventory.check_stock("SKU001") == 100
        
        # Customer service works independently
        customers.register_customer(Customer("C001", "Alice", "alice@example.com"))
        assert customers.customer_exists("C001")
    
    def test_dependency_injection(self) -> None:
        """Services can be injected with different implementations."""
        # We could inject mock services for testing
        inventory = InventoryService()
        customers = CustomerService()
        payments = PaymentService()
        
        order_service = OrderService(inventory, customers, payments)
        
        # Verify composition (not inheritance)
        assert hasattr(order_service, "_inventory")
        assert hasattr(order_service, "_customers")
        assert hasattr(order_service, "_payments")
