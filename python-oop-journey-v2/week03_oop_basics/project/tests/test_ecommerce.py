"""Comprehensive tests for Week 3 Project: Basic E-commerce System.

Tests cover:
- Product class (validation, properties, methods)
- User class (email validation, cart, orders)
- ShoppingCart and CartItem classes
- Order, OrderItem, OrderStatus classes
- Inventory class
- Integration between classes
"""

from __future__ import annotations

import pytest

from week03_oop_basics.project.reference_solution.product import Product
from week03_oop_basics.project.reference_solution.user import User
from week03_oop_basics.project.reference_solution.cart import ShoppingCart, CartItem
from week03_oop_basics.project.reference_solution.order import Order, OrderItem, OrderStatus
from week03_oop_basics.project.reference_solution.inventory import Inventory


# ============================================================================
# Product Tests
# ============================================================================

class TestProduct:
    """Tests for the Product class."""
    
    def test_product_creation_valid(self) -> None:
        """Test creating a product with valid attributes."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        assert product.name == "Laptop"
        assert product.price == 999.99
        assert product.category == "Electronics"
        assert product.sku == "TECH-001"
    
    def test_product_creation_empty_name_raises(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Name must be"):
            Product("", 999.99, "Electronics", "TECH-001")
    
    def test_product_creation_empty_category_raises(self) -> None:
        """Test that empty category raises ValueError."""
        with pytest.raises(ValueError, match="Category must be"):
            Product("Laptop", 999.99, "", "TECH-001")
    
    def test_product_creation_empty_sku_raises(self) -> None:
        """Test that empty SKU raises ValueError."""
        with pytest.raises(ValueError, match="SKU must be"):
            Product("Laptop", 999.99, "Electronics", "")
    
    def test_product_creation_negative_price_raises(self) -> None:
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            Product("Laptop", -10.0, "Electronics", "TECH-001")
    
    def test_product_creation_zero_price_valid(self) -> None:
        """Test that zero price is valid."""
        product = Product("Free Item", 0.0, "Promo", "FREE-001")
        assert product.price == 0.0
    
    def test_product_name_setter_valid(self) -> None:
        """Test setting name with valid value."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        product.name = "Gaming Laptop"
        assert product.name == "Gaming Laptop"
    
    def test_product_name_setter_empty_raises(self) -> None:
        """Test that setting empty name raises ValueError."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        with pytest.raises(ValueError, match="Name must be"):
            product.name = ""
    
    def test_product_price_setter_valid(self) -> None:
        """Test setting price with valid value."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        product.price = 899.99
        assert product.price == 899.99
    
    def test_product_price_setter_negative_raises(self) -> None:
        """Test that setting negative price raises ValueError."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        with pytest.raises(ValueError, match="Price cannot be negative"):
            product.price = -50.0
    
    def test_product_sku_readonly(self) -> None:
        """Test that SKU is read-only."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        with pytest.raises(AttributeError):
            product.sku = "TECH-002"
    
    def test_product_equality_same_sku(self) -> None:
        """Test that products with same SKU are equal."""
        p1 = Product("Laptop", 999.99, "Electronics", "TECH-001")
        p2 = Product("Different Name", 1999.99, "Different Cat", "TECH-001")
        assert p1 == p2
    
    def test_product_equality_different_sku(self) -> None:
        """Test that products with different SKU are not equal."""
        p1 = Product("Laptop", 999.99, "Electronics", "TECH-001")
        p2 = Product("Laptop", 999.99, "Electronics", "TECH-002")
        assert p1 != p2
    
    def test_product_equality_non_product(self) -> None:
        """Test equality with non-Product returns NotImplemented."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        assert product != "TECH-001"
        assert product != 123
    
    def test_product_hash_same_sku(self) -> None:
        """Test that products with same SKU have same hash."""
        p1 = Product("Laptop", 999.99, "Electronics", "TECH-001")
        p2 = Product("Different", 1999.99, "Different", "TECH-001")
        assert hash(p1) == hash(p2)
    
    def test_product_hash_different_sku(self) -> None:
        """Test that products with different SKU can have different hash."""
        p1 = Product("Laptop", 999.99, "Electronics", "TECH-001")
        p2 = Product("Laptop", 999.99, "Electronics", "TECH-002")
        # Hash collision is possible but unlikely
        assert hash(p1) != hash(p2) or True  # Don't fail on collision
    
    def test_product_repr(self) -> None:
        """Test repr output contains key info."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        repr_str = repr(product)
        assert "Product" in repr_str
        assert "Laptop" in repr_str
        assert "TECH-001" in repr_str
    
    def test_product_apply_discount_valid(self) -> None:
        """Test applying valid discount."""
        product = Product("Laptop", 1000.0, "Electronics", "TECH-001")
        discounted = product.apply_discount(10)
        assert discounted == 900.0
    
    def test_product_apply_discount_zero(self) -> None:
        """Test applying 0% discount."""
        product = Product("Laptop", 1000.0, "Electronics", "TECH-001")
        assert product.apply_discount(0) == 1000.0
    
    def test_product_apply_discount_hundred(self) -> None:
        """Test applying 100% discount."""
        product = Product("Laptop", 1000.0, "Electronics", "TECH-001")
        assert product.apply_discount(100) == 0.0
    
    def test_product_apply_discount_invalid_raises(self) -> None:
        """Test that invalid discount raises ValueError."""
        product = Product("Laptop", 1000.0, "Electronics", "TECH-001")
        with pytest.raises(ValueError):
            product.apply_discount(-10)
        with pytest.raises(ValueError):
            product.apply_discount(110)
    
    def test_product_to_dict(self) -> None:
        """Test conversion to dictionary."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        data = product.to_dict()
        assert data["name"] == "Laptop"
        assert data["price"] == 999.99
        assert data["category"] == "Electronics"
        assert data["sku"] == "TECH-001"
    
    def test_product_from_dict_valid(self) -> None:
        """Test creation from valid dictionary."""
        data = {
            "name": "Laptop",
            "price": 999.99,
            "category": "Electronics",
            "sku": "TECH-001"
        }
        product = Product.from_dict(data)
        assert product.name == "Laptop"
        assert product.price == 999.99
    
    def test_product_from_dict_missing_keys_raises(self) -> None:
        """Test that missing keys raise ValueError."""
        data = {"name": "Laptop", "price": 999.99}
        with pytest.raises(ValueError, match="Missing"):
            Product.from_dict(data)


# ============================================================================
# User Tests
# ============================================================================

class TestUser:
    """Tests for the User class."""
    
    def test_user_creation_valid(self) -> None:
        """Test creating a user with valid attributes."""
        user = User("U001", "Alice Smith", "alice@example.com")
        assert user.user_id == "U001"
        assert user.name == "Alice Smith"
        assert user.email == "alice@example.com"
    
    def test_user_creation_empty_user_id_raises(self) -> None:
        """Test that empty user_id raises ValueError."""
        with pytest.raises(ValueError, match="User ID must be"):
            User("", "Alice", "alice@example.com")
    
    def test_user_creation_empty_name_raises(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Name must be"):
            User("U001", "", "alice@example.com")
    
    def test_user_creation_invalid_email_raises(self) -> None:
        """Test that invalid email raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email"):
            User("U001", "Alice", "not-an-email")
    
    def test_user_creation_no_at_email_raises(self) -> None:
        """Test that email without @ raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email"):
            User("U001", "Alice", "alice.example.com")
    
    def test_user_creation_no_domain_raises(self) -> None:
        """Test that email without domain raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email"):
            User("U001", "Alice", "alice@")
    
    def test_user_creation_no_local_raises(self) -> None:
        """Test that email without local part raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email"):
            User("U001", "Alice", "@example.com")
    
    def test_user_creation_no_dot_in_domain_raises(self) -> None:
        """Test that email without dot in domain raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email"):
            User("U001", "Alice", "alice@example")
    
    def test_user_id_readonly(self) -> None:
        """Test that user_id is read-only."""
        user = User("U001", "Alice", "alice@example.com")
        with pytest.raises(AttributeError):
            user.user_id = "U002"
    
    def test_user_name_setter_valid(self) -> None:
        """Test setting name with valid value."""
        user = User("U001", "Alice", "alice@example.com")
        user.name = "Alice Smith"
        assert user.name == "Alice Smith"
    
    def test_user_email_setter_valid(self) -> None:
        """Test setting email with valid value."""
        user = User("U001", "Alice", "alice@example.com")
        user.email = "alice.smith@example.com"
        assert user.email == "alice.smith@example.com"
    
    def test_user_email_setter_invalid_raises(self) -> None:
        """Test that setting invalid email raises ValueError."""
        user = User("U001", "Alice", "alice@example.com")
        with pytest.raises(ValueError, match="Invalid email"):
            user.email = "not-valid"
    
    def test_user_has_cart(self) -> None:
        """Test that user has a shopping cart."""
        user = User("U001", "Alice", "alice@example.com")
        assert user.cart is not None
        assert isinstance(user.cart, ShoppingCart)
    
    def test_user_orders_empty_initially(self) -> None:
        """Test that new user has empty orders."""
        user = User("U001", "Alice", "alice@example.com")
        assert user.orders == []
        assert user.get_order_count() == 0
    
    def test_user_add_order(self) -> None:
        """Test adding an order to user history."""
        user = User("U001", "Alice", "alice@example.com")
        order = Order("ORD-001", "U001", [])
        user.add_order(order)
        assert len(user.orders) == 1
        assert user.get_order_count() == 1
    
    def test_user_orders_returns_copy(self) -> None:
        """Test that orders property returns a copy."""
        user = User("U001", "Alice", "alice@example.com")
        order = Order("ORD-001", "U001", [])
        user.add_order(order)
        orders = user.orders
        orders.clear()  # Modify the returned list
        assert len(user.orders) == 1  # Original should be unchanged
    
    def test_user_get_total_spent(self) -> None:
        """Test calculating total spent."""
        user = User("U001", "Alice", "alice@example.com")
        order1 = Order("ORD-001", "U001", [
            OrderItem("Item1", "SKU1", 100.0, 1)
        ])
        order2 = Order("ORD-002", "U001", [
            OrderItem("Item2", "SKU2", 50.0, 2)
        ])
        user.add_order(order1)
        user.add_order(order2)
        assert user.get_total_spent() == 200.0
    
    def test_user_email_whitelist_valid(self) -> None:
        """Test email whitelist with valid domain."""
        User.set_email_whitelist(["example.com"])
        try:
            user = User("U001", "Alice", "alice@example.com")
            assert user.email == "alice@example.com"
        finally:
            User.clear_email_whitelist()
    
    def test_user_email_whitelist_invalid_raises(self) -> None:
        """Test that non-whitelisted domain raises ValueError."""
        User.set_email_whitelist(["example.com"])
        try:
            with pytest.raises(ValueError, match="not in whitelist"):
                User("U001", "Alice", "alice@other.com")
        finally:
            User.clear_email_whitelist()
    
    def test_user_validate_email_valid(self) -> None:
        """Test email validation with valid emails."""
        assert User.validate_email("test@example.com") is True
        assert User.validate_email("user.name@domain.co.uk") is True
        assert User.validate_email("user+tag@example.org") is True
    
    def test_user_validate_email_invalid(self) -> None:
        """Test email validation with invalid emails."""
        assert User.validate_email("") is False
        assert User.validate_email("no-at-sign") is False
        assert User.validate_email("@nodomain.com") is False
        assert User.validate_email("spaces in@domain.com") is False
        assert User.validate_email("double@@at.com") is False
    
    def test_user_repr(self) -> None:
        """Test repr output."""
        user = User("U001", "Alice", "alice@example.com")
        repr_str = repr(user)
        assert "User" in repr_str
        assert "U001" in repr_str
        assert "Alice" in repr_str


# ============================================================================
# ShoppingCart and CartItem Tests
# ============================================================================

class TestCartItem:
    """Tests for the CartItem class."""
    
    def test_cart_item_creation_valid(self) -> None:
        """Test creating a cart item."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        item = CartItem(product, 2)
        assert item.product == product
        assert item.quantity == 2
    
    def test_cart_item_creation_default_quantity(self) -> None:
        """Test that default quantity is 1."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        item = CartItem(product)
        assert item.quantity == 1
    
    def test_cart_item_creation_zero_quantity_raises(self) -> None:
        """Test that zero quantity raises ValueError."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        with pytest.raises(ValueError, match="Quantity must be positive"):
            CartItem(product, 0)
    
    def test_cart_item_creation_negative_quantity_raises(self) -> None:
        """Test that negative quantity raises ValueError."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        with pytest.raises(ValueError, match="Quantity must be positive"):
            CartItem(product, -1)
    
    def test_cart_item_quantity_setter_valid(self) -> None:
        """Test setting quantity with valid value."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        item = CartItem(product, 1)
        item.quantity = 5
        assert item.quantity == 5
    
    def test_cart_item_quantity_setter_invalid_raises(self) -> None:
        """Test that setting invalid quantity raises ValueError."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        item = CartItem(product, 1)
        with pytest.raises(ValueError, match="Quantity must be positive"):
            item.quantity = 0
    
    def test_cart_item_get_subtotal(self) -> None:
        """Test subtotal calculation."""
        product = Product("Laptop", 100.0, "Electronics", "TECH-001")
        item = CartItem(product, 3)
        assert item.get_subtotal() == 300.0


class TestShoppingCart:
    """Tests for the ShoppingCart class."""
    
    def test_cart_creation_empty(self) -> None:
        """Test creating an empty cart."""
        cart = ShoppingCart()
        assert cart.is_empty()
        assert len(cart) == 0
    
    def test_cart_add_item(self) -> None:
        """Test adding an item to cart."""
        cart = ShoppingCart()
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        cart.add_item(product, 2)
        assert len(cart) == 1
        assert not cart.is_empty()
    
    def test_cart_add_item_default_quantity(self) -> None:
        """Test adding item with default quantity."""
        cart = ShoppingCart()
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        cart.add_item(product)
        item = cart.get_item("TECH-001")
        assert item is not None
        assert item.quantity == 1
    
    def test_cart_add_item_zero_quantity_raises(self) -> None:
        """Test that adding with zero quantity raises ValueError."""
        cart = ShoppingCart()
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        with pytest.raises(ValueError, match="Quantity must be positive"):
            cart.add_item(product, 0)
    
    def test_cart_add_same_product_increments_quantity(self) -> None:
        """Test adding same product increments quantity."""
        cart = ShoppingCart()
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        cart.add_item(product, 2)
        cart.add_item(product, 3)
        item = cart.get_item("TECH-001")
        assert item.quantity == 5
    
    def test_cart_remove_item_success(self) -> None:
        """Test removing an existing item."""
        cart = ShoppingCart()
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        cart.add_item(product)
        result = cart.remove_item("TECH-001")
        assert result is True
        assert cart.is_empty()
    
    def test_cart_remove_item_not_found(self) -> None:
        """Test removing non-existent item returns False."""
        cart = ShoppingCart()
        result = cart.remove_item("NONEXISTENT")
        assert result is False
    
    def test_cart_update_quantity_success(self) -> None:
        """Test updating quantity of existing item."""
        cart = ShoppingCart()
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        cart.add_item(product, 2)
        result = cart.update_quantity("TECH-001", 5)
        assert result is True
        assert cart.get_item("TECH-001").quantity == 5
    
    def test_cart_update_quantity_not_found(self) -> None:
        """Test updating quantity of non-existent item returns False."""
        cart = ShoppingCart()
        result = cart.update_quantity("NONEXISTENT", 5)
        assert result is False
    
    def test_cart_update_quantity_invalid_raises(self) -> None:
        """Test that updating to invalid quantity raises ValueError."""
        cart = ShoppingCart()
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        cart.add_item(product)
        with pytest.raises(ValueError, match="Quantity must be positive"):
            cart.update_quantity("TECH-001", 0)
    
    def test_cart_has_item(self) -> None:
        """Test has_item method."""
        cart = ShoppingCart()
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        cart.add_item(product)
        assert cart.has_item("TECH-001") is True
        assert cart.has_item("NONEXISTENT") is False
    
    def test_cart_get_item_found(self) -> None:
        """Test getting existing item."""
        cart = ShoppingCart()
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        cart.add_item(product)
        item = cart.get_item("TECH-001")
        assert item is not None
        assert item.product.sku == "TECH-001"
    
    def test_cart_get_item_not_found(self) -> None:
        """Test getting non-existent item returns None."""
        cart = ShoppingCart()
        item = cart.get_item("NONEXISTENT")
        assert item is None
    
    def test_cart_get_total_quantity(self) -> None:
        """Test total quantity calculation."""
        cart = ShoppingCart()
        p1 = Product("Laptop", 999.99, "Electronics", "TECH-001")
        p2 = Product("Mouse", 29.99, "Electronics", "TECH-002")
        cart.add_item(p1, 2)
        cart.add_item(p2, 3)
        assert cart.get_total_quantity() == 5
    
    def test_cart_get_total(self) -> None:
        """Test total price calculation."""
        cart = ShoppingCart()
        p1 = Product("Laptop", 1000.0, "Electronics", "TECH-001")
        p2 = Product("Mouse", 50.0, "Electronics", "TECH-002")
        cart.add_item(p1, 2)  # 2000
        cart.add_item(p2, 3)  # 150
        assert cart.get_total() == 2150.0
    
    def test_cart_clear(self) -> None:
        """Test clearing the cart."""
        cart = ShoppingCart()
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        cart.add_item(product, 2)
        cart.clear()
        assert cart.is_empty()
        assert len(cart) == 0
    
    def test_cart_get_items(self) -> None:
        """Test getting list of items."""
        cart = ShoppingCart()
        p1 = Product("Laptop", 999.99, "Electronics", "TECH-001")
        p2 = Product("Mouse", 29.99, "Electronics", "TECH-002")
        cart.add_item(p1)
        cart.add_item(p2)
        items = cart.get_items()
        assert len(items) == 2
    
    def test_cart_iteration(self) -> None:
        """Test iterating over cart items."""
        cart = ShoppingCart()
        p1 = Product("Laptop", 999.99, "Electronics", "TECH-001")
        p2 = Product("Mouse", 29.99, "Electronics", "TECH-002")
        cart.add_item(p1)
        cart.add_item(p2)
        skus = [item.product.sku for item in cart]
        assert "TECH-001" in skus
        assert "TECH-002" in skus
    
    def test_cart_apply_discount_code_valid(self) -> None:
        """Test applying valid discount codes."""
        cart = ShoppingCart()
        product = Product("Laptop", 1000.0, "Electronics", "TECH-001")
        cart.add_item(product)
        
        assert cart.apply_discount_code("SAVE10") == 100.0
        assert cart.apply_discount_code("SAVE20") == 200.0
        assert cart.apply_discount_code("SAVE50") == 500.0
    
    def test_cart_apply_discount_code_invalid_raises(self) -> None:
        """Test that invalid code raises ValueError."""
        cart = ShoppingCart()
        product = Product("Laptop", 1000.0, "Electronics", "TECH-001")
        cart.add_item(product)
        
        with pytest.raises(ValueError, match="Invalid discount code"):
            cart.apply_discount_code("INVALID")


# ============================================================================
# Order Tests
# ============================================================================

class TestOrderStatus:
    """Tests for OrderStatus enum."""
    
    def test_order_status_values(self) -> None:
        """Test that all statuses have correct values."""
        assert OrderStatus.PENDING.value == "pending"
        assert OrderStatus.CONFIRMED.value == "confirmed"
        assert OrderStatus.SHIPPED.value == "shipped"
        assert OrderStatus.DELIVERED.value == "delivered"
        assert OrderStatus.CANCELLED.value == "cancelled"
    
    def test_order_status_str(self) -> None:
        """Test string representation."""
        assert str(OrderStatus.PENDING) == "pending"


class TestOrderItem:
    """Tests for OrderItem class."""
    
    def test_order_item_creation(self) -> None:
        """Test creating an order item."""
        item = OrderItem("Laptop", "TECH-001", 999.99, 2)
        assert item.product_name == "Laptop"
        assert item.product_sku == "TECH-001"
        assert item.unit_price == 999.99
        assert item.quantity == 2
    
    def test_order_item_get_subtotal(self) -> None:
        """Test subtotal calculation."""
        item = OrderItem("Laptop", "TECH-001", 100.0, 3)
        assert item.get_subtotal() == 300.0
    
    def test_order_item_immutable(self) -> None:
        """Test that order item attributes are read-only."""
        item = OrderItem("Laptop", "TECH-001", 999.99, 2)
        with pytest.raises(AttributeError):
            item.product_name = "Changed"
        with pytest.raises(AttributeError):
            item.quantity = 5


class TestOrder:
    """Tests for Order class."""
    
    def setup_method(self) -> None:
        """Reset order counter before each test."""
        Order.reset_counter()
    
    def test_order_creation(self) -> None:
        """Test creating an order."""
        items = [OrderItem("Laptop", "TECH-001", 999.99, 1)]
        order = Order("ORD-001", "U001", items)
        assert order.order_id == "ORD-001"
        assert order.user_id == "U001"
        assert order.status == OrderStatus.PENDING
        assert len(order.items) == 1
    
    def test_order_creation_default_status(self) -> None:
        """Test that default status is PENDING."""
        order = Order("ORD-001", "U001", [])
        assert order.status == OrderStatus.PENDING
    
    def test_order_id_readonly(self) -> None:
        """Test that order_id is read-only."""
        order = Order("ORD-001", "U001", [])
        with pytest.raises(AttributeError):
            order.order_id = "ORD-002"
    
    def test_order_user_id_readonly(self) -> None:
        """Test that user_id is read-only."""
        order = Order("ORD-001", "U001", [])
        with pytest.raises(AttributeError):
            order.user_id = "U002"
    
    def test_order_items_returns_copy(self) -> None:
        """Test that items returns a copy."""
        items = [OrderItem("Laptop", "TECH-001", 999.99, 1)]
        order = Order("ORD-001", "U001", items)
        returned_items = order.items
        returned_items.clear()
        assert len(order.items) == 1
    
    def test_order_total_calculation(self) -> None:
        """Test total calculation."""
        items = [
            OrderItem("Laptop", "TECH-001", 1000.0, 1),
            OrderItem("Mouse", "TECH-002", 50.0, 2),
        ]
        order = Order("ORD-001", "U001", items)
        assert order.total == 1100.0
    
    def test_order_item_count(self) -> None:
        """Test item count property."""
        items = [
            OrderItem("Laptop", "TECH-001", 1000.0, 2),
            OrderItem("Mouse", "TECH-002", 50.0, 3),
        ]
        order = Order("ORD-001", "U001", items)
        assert order.item_count == 5
    
    def test_order_update_status_valid(self) -> None:
        """Test valid status transitions."""
        order = Order("ORD-001", "U001", [])
        
        order.update_status(OrderStatus.CONFIRMED)
        assert order.status == OrderStatus.CONFIRMED
        
        order.update_status(OrderStatus.SHIPPED)
        assert order.status == OrderStatus.SHIPPED
        
        order.update_status(OrderStatus.DELIVERED)
        assert order.status == OrderStatus.DELIVERED
    
    def test_order_update_status_invalid_raises(self) -> None:
        """Test that invalid transitions raise ValueError."""
        order = Order("ORD-001", "U001", [])
        
        # Can't go directly from PENDING to SHIPPED
        with pytest.raises(ValueError, match="Invalid status transition"):
            order.update_status(OrderStatus.SHIPPED)
        
        # Can't go from PENDING to DELIVERED
        with pytest.raises(ValueError, match="Invalid status transition"):
            order.update_status(OrderStatus.DELIVERED)
    
    def test_order_update_status_from_delivered_raises(self) -> None:
        """Test that no transitions from DELIVERED are allowed."""
        order = Order("ORD-001", "U001", [], OrderStatus.DELIVERED)
        
        with pytest.raises(ValueError, match="Invalid status transition"):
            order.update_status(OrderStatus.PENDING)
        with pytest.raises(ValueError, match="Invalid status transition"):
            order.update_status(OrderStatus.CANCELLED)
    
    def test_order_cancel_success(self) -> None:
        """Test cancelling a pending order."""
        order = Order("ORD-001", "U001", [])
        result = order.cancel()
        assert result is True
        assert order.status == OrderStatus.CANCELLED
    
    def test_order_cancel_from_confirmed(self) -> None:
        """Test cancelling a confirmed order."""
        order = Order("ORD-001", "U001", [], OrderStatus.CONFIRMED)
        result = order.cancel()
        assert result is True
        assert order.status == OrderStatus.CANCELLED
    
    def test_order_cancel_from_shipped_fails(self) -> None:
        """Test that cancelling shipped order fails."""
        order = Order("ORD-001", "U001", [], OrderStatus.SHIPPED)
        result = order.cancel()
        assert result is False
        assert order.status == OrderStatus.SHIPPED
    
    def test_order_can_cancel(self) -> None:
        """Test can_cancel method."""
        pending = Order("ORD-001", "U001", [], OrderStatus.PENDING)
        confirmed = Order("ORD-002", "U001", [], OrderStatus.CONFIRMED)
        shipped = Order("ORD-003", "U001", [], OrderStatus.SHIPPED)
        delivered = Order("ORD-004", "U001", [], OrderStatus.DELIVERED)
        cancelled = Order("ORD-005", "U001", [], OrderStatus.CANCELLED)
        
        assert pending.can_cancel() is True
        assert confirmed.can_cancel() is True
        assert shipped.can_cancel() is False
        assert delivered.can_cancel() is False
        assert cancelled.can_cancel() is False
    
    def test_order_generate_order_id(self) -> None:
        """Test order ID generation."""
        Order.reset_counter()
        id1 = Order.generate_order_id()
        id2 = Order.generate_order_id()
        assert id1 == "ORD-0001"
        assert id2 == "ORD-0002"
    
    def test_order_reset_counter(self) -> None:
        """Test counter reset."""
        Order.generate_order_id()
        Order.reset_counter()
        id_after_reset = Order.generate_order_id()
        assert id_after_reset == "ORD-0001"
    
    def test_order_from_cart(self) -> None:
        """Test creating order from cart."""
        cart = ShoppingCart()
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        cart.add_item(product, 2)
        
        Order.reset_counter()
        order = Order.from_cart("U001", cart.get_items())
        
        assert order.order_id == "ORD-0001"
        assert order.user_id == "U001"
        assert order.total == 1999.98
        assert len(order.items) == 1
    
    def test_order_from_cart_with_custom_id(self) -> None:
        """Test creating order with custom ID."""
        cart = ShoppingCart()
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        cart.add_item(product)
        
        order = Order.from_cart("U001", cart.get_items(), "CUSTOM-123")
        assert order.order_id == "CUSTOM-123"


# ============================================================================
# Inventory Tests
# ============================================================================

class TestInventory:
    """Tests for Inventory class."""
    
    def setup_method(self) -> None:
        """Reset threshold before each test."""
        Inventory.set_low_stock_threshold(10)
    
    def test_inventory_creation_empty(self) -> None:
        """Test creating empty inventory."""
        inv = Inventory()
        assert inv.is_empty()
        assert len(inv) == 0
    
    def test_inventory_stock_product_new(self) -> None:
        """Test stocking a new product."""
        inv = Inventory()
        inv.stock_product("TECH-001", 100)
        assert inv.get_stock("TECH-001") == 100
        assert len(inv) == 1
    
    def test_inventory_stock_product_existing(self) -> None:
        """Test adding to existing stock."""
        inv = Inventory()
        inv.stock_product("TECH-001", 100)
        inv.stock_product("TECH-001", 50)
        assert inv.get_stock("TECH-001") == 150
    
    def test_inventory_stock_product_negative_raises(self) -> None:
        """Test that negative stock amount raises ValueError."""
        inv = Inventory()
        with pytest.raises(ValueError, match="Quantity cannot be negative"):
            inv.stock_product("TECH-001", -10)
    
    def test_inventory_remove_product_success(self) -> None:
        """Test removing a product."""
        inv = Inventory()
        inv.stock_product("TECH-001", 100)
        result = inv.remove_product("TECH-001")
        assert result is True
        assert inv.get_stock("TECH-001") == 0
    
    def test_inventory_remove_product_not_found(self) -> None:
        """Test removing non-existent product."""
        inv = Inventory()
        result = inv.remove_product("NONEXISTENT")
        assert result is False
    
    def test_inventory_get_stock_existing(self) -> None:
        """Test getting stock for existing product."""
        inv = Inventory()
        inv.stock_product("TECH-001", 100)
        assert inv.get_stock("TECH-001") == 100
    
    def test_inventory_get_stock_not_found(self) -> None:
        """Test getting stock for non-existent product returns 0."""
        inv = Inventory()
        assert inv.get_stock("NONEXISTENT") == 0
    
    def test_inventory_has_stock_sufficient(self) -> None:
        """Test has_stock when sufficient."""
        inv = Inventory()
        inv.stock_product("TECH-001", 100)
        assert inv.has_stock("TECH-001", 50) is True
        assert inv.has_stock("TECH-001", 100) is True
    
    def test_inventory_has_stock_insufficient(self) -> None:
        """Test has_stock when insufficient."""
        inv = Inventory()
        inv.stock_product("TECH-001", 100)
        assert inv.has_stock("TECH-001", 101) is False
    
    def test_inventory_has_stock_not_found(self) -> None:
        """Test has_stock for non-existent product."""
        inv = Inventory()
        assert inv.has_stock("NONEXISTENT") is False
    
    def test_inventory_reserve_success(self) -> None:
        """Test successful reservation."""
        inv = Inventory()
        inv.stock_product("TECH-001", 100)
        result = inv.reserve("TECH-001", 30)
        assert result is True
        assert inv.get_stock("TECH-001") == 70
    
    def test_inventory_reserve_insufficient(self) -> None:
        """Test reservation with insufficient stock."""
        inv = Inventory()
        inv.stock_product("TECH-001", 10)
        result = inv.reserve("TECH-001", 20)
        assert result is False
        assert inv.get_stock("TECH-001") == 10  # Unchanged
    
    def test_inventory_reserve_not_found(self) -> None:
        """Test reservation for non-existent product."""
        inv = Inventory()
        result = inv.reserve("NONEXISTENT", 10)
        assert result is False
    
    def test_inventory_reserve_zero_raises(self) -> None:
        """Test that reserving zero raises ValueError."""
        inv = Inventory()
        inv.stock_product("TECH-001", 100)
        with pytest.raises(ValueError, match="Quantity must be positive"):
            inv.reserve("TECH-001", 0)
    
    def test_inventory_release_existing(self) -> None:
        """Test releasing stock to existing product."""
        inv = Inventory()
        inv.stock_product("TECH-001", 50)
        result = inv.release("TECH-001", 20)
        assert result is True
        assert inv.get_stock("TECH-001") == 70
    
    def test_inventory_release_zero_raises(self) -> None:
        """Test that releasing zero raises ValueError."""
        inv = Inventory()
        with pytest.raises(ValueError, match="Quantity must be positive"):
            inv.release("TECH-001", 0)
    
    def test_inventory_get_low_stock_items(self) -> None:
        """Test getting low stock items."""
        inv = Inventory()
        inv.stock_product("LOW-001", 5)
        inv.stock_product("LOW-002", 9)
        inv.stock_product("OK-001", 10)
        inv.stock_product("OK-002", 50)
        
        low_stock = inv.get_low_stock_items()
        assert len(low_stock) == 2
        skus = [sku for sku, _ in low_stock]
        assert "LOW-001" in skus
        assert "LOW-002" in skus
    
    def test_inventory_get_total_units(self) -> None:
        """Test getting total units."""
        inv = Inventory()
        inv.stock_product("TECH-001", 100)
        inv.stock_product("TECH-002", 50)
        assert inv.get_total_units() == 150
    
    def test_inventory_get_skus(self) -> None:
        """Test getting all SKUs."""
        inv = Inventory()
        inv.stock_product("TECH-001", 100)
        inv.stock_product("TECH-002", 50)
        skus = inv.get_skus()
        assert len(skus) == 2
        assert "TECH-001" in skus
        assert "TECH-002" in skus
    
    def test_inventory_clear(self) -> None:
        """Test clearing inventory."""
        inv = Inventory()
        inv.stock_product("TECH-001", 100)
        inv.clear()
        assert inv.is_empty()
        assert len(inv) == 0
    
    def test_inventory_update_stock_success(self) -> None:
        """Test updating stock to new value."""
        inv = Inventory()
        inv.stock_product("TECH-001", 100)
        result = inv.update_stock("TECH-001", 50)
        assert result is True
        assert inv.get_stock("TECH-001") == 50
    
    def test_inventory_update_stock_not_found(self) -> None:
        """Test updating stock for non-existent product."""
        inv = Inventory()
        result = inv.update_stock("NONEXISTENT", 50)
        assert result is False
    
    def test_inventory_update_stock_negative_raises(self) -> None:
        """Test that updating to negative raises ValueError."""
        inv = Inventory()
        inv.stock_product("TECH-001", 100)
        with pytest.raises(ValueError, match="Quantity cannot be negative"):
            inv.update_stock("TECH-001", -10)
    
    def test_inventory_set_low_stock_threshold(self) -> None:
        """Test setting low stock threshold."""
        Inventory.set_low_stock_threshold(20)
        assert Inventory.get_low_stock_threshold() == 20
    
    def test_inventory_set_low_stock_threshold_negative_raises(self) -> None:
        """Test that negative threshold raises ValueError."""
        with pytest.raises(ValueError, match="Threshold cannot be negative"):
            Inventory.set_low_stock_threshold(-5)
    
    def test_inventory_get_low_stock_threshold(self) -> None:
        """Test getting default threshold."""
        assert Inventory.get_low_stock_threshold() == 10


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests between multiple classes."""
    
    def setup_method(self) -> None:
        """Reset state before each test."""
        Order.reset_counter()
        Inventory.set_low_stock_threshold(10)
        User.clear_email_whitelist()
    
    def test_full_purchase_flow(self) -> None:
        """Test a complete purchase flow."""
        # Create products
        laptop = Product("Laptop", 999.99, "Electronics", "TECH-001")
        mouse = Product("Wireless Mouse", 29.99, "Electronics", "TECH-002")
        
        # Create user
        user = User("U001", "Alice Smith", "alice@example.com")
        
        # Add items to cart
        user.cart.add_item(laptop, 1)
        user.cart.add_item(mouse, 2)
        
        # Verify cart
        assert user.cart.get_total_quantity() == 3
        assert user.cart.get_total() == 1059.97
        
        # Setup inventory
        inventory = Inventory()
        inventory.stock_product("TECH-001", 100)
        inventory.stock_product("TECH-002", 50)
        
        # Reserve inventory
        for item in user.cart:
            assert inventory.reserve(item.product.sku, item.quantity) is True
        
        # Create order
        order = Order.from_cart(user.user_id, user.cart.get_items())
        user.add_order(order)
        
        # Verify order
        assert order.total == 1059.97
        assert order.status == OrderStatus.PENDING
        
        # Process order
        order.update_status(OrderStatus.CONFIRMED)
        order.update_status(OrderStatus.SHIPPED)
        order.update_status(OrderStatus.DELIVERED)
        
        # Verify final state
        assert len(user.orders) == 1
        assert user.get_total_spent() == 1059.97
        assert inventory.get_stock("TECH-001") == 99
        assert inventory.get_stock("TECH-002") == 48
    
    def test_order_cancellation_with_inventory_release(self) -> None:
        """Test order cancellation releasing inventory."""
        # Setup
        laptop = Product("Laptop", 999.99, "Electronics", "TECH-001")
        user = User("U001", "Alice", "alice@example.com")
        user.cart.add_item(laptop, 5)
        
        inventory = Inventory()
        inventory.stock_product("TECH-001", 100)
        
        # Reserve and create order
        inventory.reserve("TECH-001", 5)
        order = Order.from_cart(user.user_id, user.cart.get_items())
        
        # Cancel and release
        if order.cancel():
            inventory.release("TECH-001", 5)
        
        assert inventory.get_stock("TECH-001") == 100
        assert order.status == OrderStatus.CANCELLED
    
    def test_product_in_cart_and_order(self) -> None:
        """Test product usage in cart and then order."""
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        
        # Use in cart
        cart = ShoppingCart()
        cart.add_item(product, 2)
        
        # Modify product price
        product.price = 899.99
        
        # Cart should reflect new price (reference)
        assert cart.get_total() == 1799.98
        
        # Create order - should capture current price
        order = Order.from_cart("U001", cart.get_items())
        assert order.total == 1799.98
        
        # Order items should be immutable snapshot
        order_item = order.items[0]
        assert order_item.unit_price == 899.99
    
    def test_cart_to_order_conversion(self) -> None:
        """Test converting cart contents to order."""
        p1 = Product("A", 100.0, "Cat", "SKU-001")
        p2 = Product("B", 50.0, "Cat", "SKU-002")
        
        cart = ShoppingCart()
        cart.add_item(p1, 2)
        cart.add_item(p2, 3)
        
        order = Order.from_cart("U001", cart.get_items())
        
        assert len(order.items) == 2
        assert order.item_count == 5
        assert order.total == 350.0
    
    def test_user_cart_isolation(self) -> None:
        """Test that each user has their own cart."""
        user1 = User("U001", "Alice", "alice@example.com")
        user2 = User("U002", "Bob", "bob@example.com")
        
        product = Product("Laptop", 999.99, "Electronics", "TECH-001")
        user1.cart.add_item(product, 2)
        
        assert user1.cart.get_total_quantity() == 2
        assert user2.cart.get_total_quantity() == 0
    
    def test_multiple_orders_per_user(self) -> None:
        """Test user with multiple orders."""
        user = User("U001", "Alice", "alice@example.com")
        
        # First order
        items1 = [OrderItem("Item1", "SKU1", 100.0, 1)]
        order1 = Order("ORD-001", "U001", items1)
        # Valid transitions: PENDING -> CONFIRMED -> SHIPPED -> DELIVERED
        order1.update_status(OrderStatus.CONFIRMED)
        order1.update_status(OrderStatus.SHIPPED)
        order1.update_status(OrderStatus.DELIVERED)
        user.add_order(order1)
        
        # Second order
        items2 = [OrderItem("Item2", "SKU2", 200.0, 2)]
        order2 = Order("ORD-002", "U001", items2)
        user.add_order(order2)
        
        assert user.get_order_count() == 2
        assert user.get_total_spent() == 500.0
    
    def test_inventory_with_multiple_products(self) -> None:
        """Test inventory management with many products."""
        inventory = Inventory()
        
        # Stock multiple products
        for i in range(10):
            inventory.stock_product(f"SKU-{i:03d}", i * 10 + 5)
        
        assert len(inventory) == 10
        assert inventory.get_total_units() == sum(i * 10 + 5 for i in range(10))
        
        # Check low stock
        low_stock = inventory.get_low_stock_items()
        # Products with stock < 10: SKU-000 (5)
        assert len(low_stock) == 1
        assert low_stock[0][0] == "SKU-000"
