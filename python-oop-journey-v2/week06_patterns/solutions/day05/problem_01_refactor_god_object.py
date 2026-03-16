"""Problem 01: Refactor God Object - Solution.

Refactors MegaStoreManager into focused service classes using composition.

WHY COMPOSITION OVER GOD OBJECT?
The God Object anti-pattern concentrates too much responsibility in one class,
making it:
- Hard to test (many dependencies to mock)
- Hard to maintain (changes affect everything)
- Hard to reuse (can't use just inventory logic without the whole class)

COMPOSITION BENEFITS:
- Single Responsibility: Each service does one thing well
- Testability: Services can be tested in isolation with mock dependencies
- Flexibility: Services can be composed differently for different use cases
- Dependency Injection: OrderService receives its dependencies, making
the relationships explicit and easy to change

This refactoring demonstrates the principle: "Favor composition over inheritance."
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Any


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
    """Manages products and stock levels."""
    
    def __init__(self) -> None:
        self._products: dict[str, Product] = {}
    
    def add_product(self, product: Product) -> None:
        """Add a product to inventory."""
        self._products[product.sku] = product
    
    def get_product(self, sku: str) -> Product | None:
        """Get product by SKU."""
        return self._products.get(sku)
    
    def update_stock(self, sku: str, quantity: int) -> bool:
        """Update stock by adding quantity (can be negative)."""
        if sku in self._products:
            self._products[sku].stock += quantity
            return True
        return False
    
    def check_stock(self, sku: str) -> int:
        """Get current stock level."""
        product = self._products.get(sku)
        return product.stock if product else 0
    
    def reserve_stock(self, sku: str, quantity: int) -> bool:
        """Reserve stock for an order. Returns True if successful."""
        product = self._products.get(sku)
        if product and product.stock >= quantity:
            product.stock -= quantity
            return True
        return False
    
    def get_all_products(self) -> list[Product]:
        """Get all products."""
        return list(self._products.values())


class CustomerService:
    """Manages customer data."""
    
    def __init__(self) -> None:
        self._customers: dict[str, Customer] = {}
    
    def register_customer(self, customer: Customer) -> None:
        """Register a new customer."""
        self._customers[customer.customer_id] = customer
    
    def get_customer(self, customer_id: str) -> Customer | None:
        """Get customer by ID."""
        return self._customers.get(customer_id)
    
    def customer_exists(self, customer_id: str) -> bool:
        """Check if customer exists."""
        return customer_id in self._customers


class PaymentResult:
    """Result of a payment attempt."""
    
    def __init__(self, success: bool, amount: Decimal, method: str, message: str) -> None:
        self.success = success
        self.amount = amount
        self.method = method
        self.message = message


class PaymentService:
    """Handles payment processing."""
    
    def __init__(self) -> None:
        self._payments: list[dict[str, Any]] = []
    
    def process_payment(self, order_id: str, amount: Decimal, method: str) -> PaymentResult:
        """Process a payment."""
        payment = {"order_id": order_id, "amount": amount, "method": method}
        self._payments.append(payment)
        return PaymentResult(
            success=True,
            amount=amount,
            method=method,
            message=f"Payment of {amount} processed via {method}",
        )
    
    def get_total_sales(self) -> Decimal:
        """Get total of all successful payments."""
        return sum(p["amount"] for p in self._payments)
    
    def get_payment_count(self) -> int:
        """Get count of successful payments."""
        return len(self._payments)


class OrderService:
    """Coordinates order workflow using composed services.
    
    This class demonstrates dependency injection - it receives its dependencies
    through the constructor rather than creating them internally. This makes
    the class:
    - Testable: Pass mock services for unit testing
    - Flexible: Swap implementations without code changes
    - Explicit: Dependencies are visible in the constructor signature
    """
    
    def __init__(
        self,
        inventory: InventoryService,
        customers: CustomerService,
        payments: PaymentService,
    ) -> None:
        self._inventory = inventory
        self._customers = customers
        self._payments = payments
        self._orders: dict[str, Order] = {}
    
    def create_order(
        self,
        order_id: str,
        customer_id: str,
        items: list[tuple[str, int]],
    ) -> Order | None:
        """Create an order if customer exists and stock is available."""
        if not self._customers.customer_exists(customer_id):
            return None
        
        total = Decimal("0")
        order_items = []
        
        for sku, qty in items:
            product = self._inventory.get_product(sku)
            if not product or product.stock < qty:
                return None
            total += product.price * qty
            order_items.append({"sku": sku, "qty": qty, "price": product.price})
        
        order = Order(
            order_id=order_id,
            customer_id=customer_id,
            items=order_items,
            total=total,
            status="pending",
        )
        self._orders[order_id] = order
        return order
    
    def process_order_payment(self, order: Order, method: str) -> PaymentResult:
        """Process payment for an order and update stock."""
        # Reserve stock
        for item in order.items:
            self._inventory.reserve_stock(item["sku"], item["qty"])
        
        order.status = "paid"
        return self._payments.process_payment(order.order_id, order.total, method)
    
    def get_inventory_report(self) -> list[Product]:
        """Get current inventory status."""
        return self._inventory.get_all_products()
    
    def get_sales_report(self) -> dict[str, Any]:
        """Get sales summary."""
        return {
            "total_sales": self._payments.get_total_sales(),
            "order_count": self._payments.get_payment_count(),
        }
