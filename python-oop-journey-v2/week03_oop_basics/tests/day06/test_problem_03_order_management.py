"""Tests for Problem 03: Order Management System."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day06.problem_03_order_management import (
    Customer,
    Order,
    OrderLine,
    OrderManager,
    OrderStatus,
    Product,
)


class TestProduct:
    """Tests for Product class."""
    
    def test_product_creation(self) -> None:
        """Test product initialization."""
        product = Product("SKU001", "Widget", 10.0, 100)
        assert product.sku == "SKU001"
        assert product.name == "Widget"
        assert product.price == 10.0
        assert product.stock_quantity == 100
    
    def test_is_available(self) -> None:
        """Test availability check."""
        product = Product("SKU001", "Widget", 10.0, 100)
        assert product.is_available(50) is True
        assert product.is_available(100) is True
        assert product.is_available(101) is False
    
    def test_reserve_stock_success(self) -> None:
        """Test successful stock reservation."""
        product = Product("SKU001", "Widget", 10.0, 100)
        assert product.reserve_stock(30) is True
        assert product.available_quantity == 70
    
    def test_reserve_stock_insufficient(self) -> None:
        """Test reservation with insufficient stock."""
        product = Product("SKU001", "Widget", 10.0, 100)
        assert product.reserve_stock(150) is False
        assert product.available_quantity == 100
    
    def test_release_stock(self) -> None:
        """Test releasing reserved stock."""
        product = Product("SKU001", "Widget", 10.0, 100)
        product.reserve_stock(30)
        product.release_stock(20)
        assert product.available_quantity == 90
    
    def test_confirm_sale(self) -> None:
        """Test confirming a sale."""
        product = Product("SKU001", "Widget", 10.0, 100)
        product.reserve_stock(30)
        product.confirm_sale(30)
        assert product.stock_quantity == 70
        assert product.available_quantity == 70


class TestCustomer:
    """Tests for Customer class."""
    
    def test_customer_creation(self) -> None:
        """Test customer initialization."""
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        assert customer.customer_id == "CUST001"
        assert customer.name == "Jane Doe"
        assert customer.email == "jane@example.com"


class TestOrderLine:
    """Tests for OrderLine class."""
    
    def test_order_line_creation(self) -> None:
        """Test order line initialization."""
        product = Product("SKU001", "Widget", 10.0, 100)
        line = OrderLine(product, 5)
        assert line.product == product
        assert line.quantity == 5
        assert line.unit_price == 10.0
    
    def test_order_line_subtotal(self) -> None:
        """Test subtotal calculation."""
        product = Product("SKU001", "Widget", 10.0, 100)
        line = OrderLine(product, 5)
        assert line.subtotal == 50.0
    
    def test_order_line_invalid_quantity(self) -> None:
        """Test that zero or negative quantity raises error."""
        product = Product("SKU001", "Widget", 10.0, 100)
        with pytest.raises(ValueError):
            OrderLine(product, 0)
        with pytest.raises(ValueError):
            OrderLine(product, -1)
    
    def test_can_fulfill(self) -> None:
        """Test fulfillment check."""
        product = Product("SKU001", "Widget", 10.0, 100)
        line = OrderLine(product, 50)
        assert line.can_fulfill() is True
        
        # Reserve most stock
        product.reserve_stock(60)
        assert line.can_fulfill() is False


class TestOrder:
    """Tests for Order class."""
    
    def test_order_creation(self) -> None:
        """Test order initialization."""
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        order = Order("ORD001", customer)
        assert order.order_id == "ORD001"
        assert order.customer == customer
        assert order.status == OrderStatus.PENDING
    
    def test_add_line(self) -> None:
        """Test adding lines to order."""
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        order = Order("ORD001", customer)
        product = Product("SKU001", "Widget", 10.0, 100)
        
        assert order.add_line(product, 5) is True
        assert len(order.lines) == 1
    
    def test_add_line_not_pending(self) -> None:
        """Test adding lines to non-pending order fails."""
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        order = Order("ORD001", customer)
        product = Product("SKU001", "Widget", 10.0, 100)
        
        # Simulate confirmed status
        order._set_status(OrderStatus.CONFIRMED)
        assert order.add_line(product, 5) is False
    
    def test_order_total(self) -> None:
        """Test order total calculation."""
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        order = Order("ORD001", customer)
        
        product1 = Product("SKU001", "Widget", 10.0, 100)
        product2 = Product("SKU002", "Gadget", 25.0, 50)
        
        order.add_line(product1, 2)  # 20.0
        order.add_line(product2, 3)  # 75.0
        
        assert order.total == 95.0
    
    def test_can_fulfill(self) -> None:
        """Test order fulfillment check."""
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        order = Order("ORD001", customer)
        
        product = Product("SKU001", "Widget", 10.0, 100)
        order.add_line(product, 50)
        
        assert order.can_fulfill() is True
        
        # Add another line that exceeds stock
        product2 = Product("SKU002", "Gadget", 25.0, 10)
        order.add_line(product2, 20)
        assert order.can_fulfill() is False


class TestOrderManager:
    """Tests for OrderManager class."""
    
    def test_create_order(self) -> None:
        """Test order creation."""
        manager = OrderManager()
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        
        order = manager.create_order("ORD001", customer)
        assert order.order_id == "ORD001"
        assert order.status == OrderStatus.PENDING
    
    def test_confirm_order_success(self) -> None:
        """Test successful order confirmation."""
        manager = OrderManager()
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        order = manager.create_order("ORD001", customer)
        
        product = Product("SKU001", "Widget", 10.0, 100)
        order.add_line(product, 10)
        
        assert manager.confirm_order(order) is True
        assert order.status == OrderStatus.CONFIRMED
        assert product.available_quantity == 90
    
    def test_confirm_order_insufficient_stock(self) -> None:
        """Test confirmation with insufficient stock."""
        manager = OrderManager()
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        order = manager.create_order("ORD001", customer)
        
        product = Product("SKU001", "Widget", 10.0, 5)
        order.add_line(product, 10)
        
        assert manager.confirm_order(order) is False
        assert order.status == OrderStatus.PENDING
    
    def test_confirm_non_pending_order(self) -> None:
        """Test confirming already confirmed order fails."""
        manager = OrderManager()
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        order = manager.create_order("ORD001", customer)
        
        product = Product("SKU001", "Widget", 10.0, 100)
        order.add_line(product, 10)
        
        manager.confirm_order(order)
        assert manager.confirm_order(order) is False
    
    def test_ship_order_success(self) -> None:
        """Test successful order shipment."""
        manager = OrderManager()
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        order = manager.create_order("ORD001", customer)
        
        product = Product("SKU001", "Widget", 10.0, 100)
        order.add_line(product, 10)
        
        manager.confirm_order(order)
        assert manager.ship_order(order) is True
        assert order.status == OrderStatus.SHIPPED
        assert product.stock_quantity == 90
    
    def test_ship_unconfirmed_order(self) -> None:
        """Test shipping unconfirmed order fails."""
        manager = OrderManager()
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        order = manager.create_order("ORD001", customer)
        
        assert manager.ship_order(order) is False
    
    def test_cancel_pending_order(self) -> None:
        """Test cancelling pending order."""
        manager = OrderManager()
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        order = manager.create_order("ORD001", customer)
        
        assert manager.cancel_order(order) is True
        assert order.status == OrderStatus.CANCELLED
    
    def test_cancel_confirmed_order(self) -> None:
        """Test cancelling confirmed order releases stock."""
        manager = OrderManager()
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        order = manager.create_order("ORD001", customer)
        
        product = Product("SKU001", "Widget", 10.0, 100)
        order.add_line(product, 10)
        
        manager.confirm_order(order)
        assert product.available_quantity == 90
        
        manager.cancel_order(order)
        assert order.status == OrderStatus.CANCELLED
        assert product.available_quantity == 100
    
    def test_cancel_shipped_order(self) -> None:
        """Test cancelling shipped order fails."""
        manager = OrderManager()
        customer = Customer("CUST001", "Jane Doe", "jane@example.com")
        order = manager.create_order("ORD001", customer)
        
        product = Product("SKU001", "Widget", 10.0, 100)
        order.add_line(product, 10)
        
        manager.confirm_order(order)
        manager.ship_order(order)
        
        assert manager.cancel_order(order) is False
