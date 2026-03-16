"""Problem 01: Refactor God Object

Topic: Pattern Tradeoffs and Anti-patterns
Difficulty: Medium

Refactor a God Object that does too much into smaller, focused classes.

The `MegaStoreManager` class below is a classic God Object - it handles:
- Inventory management
- Customer management  
- Order processing
- Payment handling
- Reporting

Your task: Break this into separate service classes that each have
a single responsibility, then compose them.

Classes to implement:
- InventoryService - manages products and stock
- CustomerService - manages customer data
- PaymentService - handles payments
- OrderService - coordinates orders (uses composition of other services)

The refactored OrderService should use dependency injection to receive
the other services, making it testable and loosely coupled.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Any


# BEFORE: The God Object (do not modify - for reference)
class MegaStoreManager:
    """This is the God Object we're refactoring.
    
    It does WAY too much - inventory, customers, orders, payments, reports.
    This makes it hard to test, maintain, and extend.
    """
    
    def __init__(self) -> None:
        self._products: dict[str, dict[str, Any]] = {}
        self._customers: dict[str, dict[str, str]] = {}
        self._orders: dict[str, dict[str, Any]] = {}
        self._payments: list[dict[str, Any]] = []
    
    # Product management
    def add_product(self, sku: str, name: str, price: Decimal, stock: int) -> None:
        self._products[sku] = {"name": name, "price": price, "stock": stock}
    
    def get_product(self, sku: str) -> dict[str, Any] | None:
        return self._products.get(sku)
    
    def update_stock(self, sku: str, quantity: int) -> bool:
        if sku in self._products:
            self._products[sku]["stock"] += quantity
            return True
        return False
    
    def check_stock(self, sku: str) -> int:
        return self._products.get(sku, {}).get("stock", 0)
    
    # Customer management
    def add_customer(self, customer_id: str, name: str, email: str) -> None:
        self._customers[customer_id] = {"name": name, "email": email}
    
    def get_customer(self, customer_id: str) -> dict[str, str] | None:
        return self._customers.get(customer_id)
    
    # Order processing
    def create_order(self, order_id: str, customer_id: str, items: list[tuple[str, int]]) -> dict[str, Any] | None:
        if customer_id not in self._customers:
            return None
        
        total = Decimal("0")
        order_items = []
        
        for sku, qty in items:
            product = self._products.get(sku)
            if not product or product["stock"] < qty:
                return None
            total += product["price"] * qty
            order_items.append({"sku": sku, "qty": qty, "price": product["price"]})
        
        self._orders[order_id] = {
            "customer_id": customer_id,
            "items": order_items,
            "total": total,
            "status": "pending"
        }
        return self._orders[order_id]
    
    def process_payment(self, order_id: str, method: str) -> dict[str, Any] | None:
        order = self._orders.get(order_id)
        if not order:
            return None
        
        # Deduct stock
        for item in order["items"]:
            self._products[item["sku"]]["stock"] -= item["qty"]
        
        order["status"] = "paid"
        payment = {"order_id": order_id, "amount": order["total"], "method": method}
        self._payments.append(payment)
        return payment
    
    def generate_inventory_report(self) -> list[dict[str, Any]]:
        return [
            {"sku": sku, "name": data["name"], "stock": data["stock"]}
            for sku, data in self._products.items()
        ]
    
    def generate_sales_report(self) -> dict[str, Any]:
        total_sales = sum(p["amount"] for p in self._payments)
        return {"total_sales": total_sales, "order_count": len(self._payments)}


# AFTER: Your refactored classes (implement these)

@dataclass
class Product:
    """Product data class."""
    sku: str
    name: str
    price: Decimal
    stock: int


@dataclass
class Customer:
    """Customer data class."""
    customer_id: str
    name: str
    email: str


@dataclass
class Order:
    """Order data class."""
    order_id: str
    customer_id: str
    items: list[dict[str, Any]]
    total: Decimal
    status: str


class InventoryService:
    """Manages products and stock levels.
    
    Responsibilities:
    - Add/remove products
    - Update stock levels
    - Check product availability
    """
    
    def __init__(self) -> None:
        raise NotImplementedError("Implement __init__")
    
    def add_product(self, product: Product) -> None:
        """Add a product to inventory."""
        raise NotImplementedError("Implement add_product")
    
    def get_product(self, sku: str) -> Product | None:
        """Get product by SKU."""
        raise NotImplementedError("Implement get_product")
    
    def update_stock(self, sku: str, quantity: int) -> bool:
        """Update stock by adding quantity (can be negative)."""
        raise NotImplementedError("Implement update_stock")
    
    def check_stock(self, sku: str) -> int:
        """Get current stock level."""
        raise NotImplementedError("Implement check_stock")
    
    def reserve_stock(self, sku: str, quantity: int) -> bool:
        """Reserve stock for an order. Returns True if successful."""
        raise NotImplementedError("Implement reserve_stock")
    
    def get_all_products(self) -> list[Product]:
        """Get all products."""
        raise NotImplementedError("Implement get_all_products")


class CustomerService:
    """Manages customer data.
    
    Responsibilities:
    - Register customers
    - Retrieve customer information
    """
    
    def __init__(self) -> None:
        raise NotImplementedError("Implement __init__")
    
    def register_customer(self, customer: Customer) -> None:
        """Register a new customer."""
        raise NotImplementedError("Implement register_customer")
    
    def get_customer(self, customer_id: str) -> Customer | None:
        """Get customer by ID."""
        raise NotImplementedError("Implement get_customer")
    
    def customer_exists(self, customer_id: str) -> bool:
        """Check if customer exists."""
        raise NotImplementedError("Implement customer_exists")


class PaymentResult:
    """Result of a payment attempt."""
    
    def __init__(self, success: bool, amount: Decimal, method: str, message: str) -> None:
        raise NotImplementedError("Implement __init__")


class PaymentService:
    """Handles payment processing.
    
    Responsibilities:
    - Process payments
    - Track payment history
    """
    
    def __init__(self) -> None:
        raise NotImplementedError("Implement __init__")
    
    def process_payment(self, order_id: str, amount: Decimal, method: str) -> PaymentResult:
        """Process a payment."""
        raise NotImplementedError("Implement process_payment")
    
    def get_total_sales(self) -> Decimal:
        """Get total of all successful payments."""
        raise NotImplementedError("Implement get_total_sales")
    
    def get_payment_count(self) -> int:
        """Get count of successful payments."""
        raise NotImplementedError("Implement get_payment_count")


class OrderService:
    """Coordinates order workflow using composed services.
    
    Uses dependency injection to receive InventoryService, CustomerService,
    and PaymentService, making it loosely coupled and testable.
    """
    
    def __init__(
        self,
        inventory: InventoryService,
        customers: CustomerService,
        payments: PaymentService,
    ) -> None:
        raise NotImplementedError("Implement __init__")
    
    def create_order(
        self,
        order_id: str,
        customer_id: str,
        items: list[tuple[str, int]],
    ) -> Order | None:
        """Create an order if customer exists and stock is available.
        
        Args:
            order_id: Unique order identifier
            customer_id: Customer placing the order
            items: List of (sku, quantity) tuples
        
        Returns:
            Order object or None if creation fails
        """
        raise NotImplementedError("Implement create_order")
    
    def process_order_payment(self, order: Order, method: str) -> PaymentResult:
        """Process payment for an order and update stock.
        
        Args:
            order: The order to pay for
            method: Payment method string
        
        Returns:
            PaymentResult with success/failure info
        """
        raise NotImplementedError("Implement process_order_payment")
    
    def get_inventory_report(self) -> list[Product]:
        """Get current inventory status."""
        raise NotImplementedError("Implement get_inventory_report")
    
    def get_sales_report(self) -> dict[str, Any]:
        """Get sales summary."""
        raise NotImplementedError("Implement get_sales_report")
