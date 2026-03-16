# Week 3, Day 6: Class Design Principles

## Learning Objectives

- Understand the Single Responsibility Principle (SRP) and why it matters
- Learn to design cohesive classes with focused responsibilities
- Apply encapsulation to protect internal state
- Practice designing for change and extensibility
- Recognize common design mistakes and how to avoid them

---

## 1. Single Responsibility Principle

> **A class should have only one reason to change.**

Each class should do one thing and do it well. When a class has multiple responsibilities, those responsibilities become coupled, leading to fragile code.

### Bad Example: God Object
```python
from __future__ import annotations


class SystemManager:  # Too many responsibilities!
    """Handles users, orders, inventory, payments, and reports."""
    
    def create_user(self, name: str) -> None: ...
    def delete_user(self, user_id: int) -> None: ...
    def place_order(self, user_id: int, items: list) -> None: ...
    def cancel_order(self, order_id: int) -> None: ...
    def check_inventory(self, product_id: int) -> int: ...
    def restock(self, product_id: int, amount: int) -> None: ...
    def process_payment(self, order_id: int, amount: float) -> None: ...
    def generate_sales_report(self) -> dict: ...
    def generate_inventory_report(self) -> dict: ...
```

### Good Example: Separated Responsibilities
```python
from __future__ import annotations


class UserService:
    """Manages user lifecycle."""
    def create_user(self, name: str) -> User: ...
    def delete_user(self, user_id: int) -> None: ...


class OrderService:
    """Manages order lifecycle."""
    def place_order(self, user_id: int, items: list) -> Order: ...
    def cancel_order(self, order_id: int) -> None: ...


class InventoryService:
    """Manages product inventory."""
    def check_stock(self, product_id: int) -> int: ...
    def restock(self, product_id: int, amount: int) -> None: ...
```

---

## 2. Cohesion and Coupling

### High Cohesion
Cohesion measures how closely the responsibilities of a class are related.

**High cohesion** (good):
- Methods work together to achieve a single purpose
- Class has a clear, focused role
- Easy to understand and maintain

### Low Coupling
Coupling measures how much classes depend on each other.

**Low coupling** (good):
- Classes interact through well-defined interfaces
- Changes in one class don't cascade to others
- Easy to test in isolation

### Example: Well-Designed Classes
```python
from __future__ import annotations
from typing import Protocol


class PaymentProcessor(Protocol):
    """Interface for payment processing."""
    def process(self, amount: float) -> bool: ...


class Order:
    """Represents a customer order - high cohesion."""
    
    def __init__(self, order_id: str, customer_id: str) -> None:
        self.order_id = order_id
        self.customer_id = customer_id
        self.items: list[OrderItem] = []
        self._total: float = 0.0
    
    def add_item(self, product: Product, quantity: int) -> None:
        """Add an item to the order."""
        self.items.append(OrderItem(product, quantity))
        self._calculate_total()
    
    def _calculate_total(self) -> None:
        """Recalculate order total."""
        self._total = sum(item.subtotal for item in self.items)
    
    @property
    def total(self) -> float:
        return self._total


class CheckoutService:
    """Processes order checkout - low coupling via protocol."""
    
    def __init__(self, payment_processor: PaymentProcessor) -> None:
        self.payment_processor = payment_processor
    
    def checkout(self, order: Order) -> bool:
        """Process checkout for an order."""
        return self.payment_processor.process(order.total)
```

---

## 3. Designing for Change

### Information Hiding
Protect internal implementation details so they can change without affecting clients.

```python
from __future__ import annotations


class BankAccount:
    """Bank account with hidden implementation details."""
    
    def __init__(self, account_number: str) -> None:
        self._account_number = account_number
        self._balance = 0.0
        self._transaction_history: list[Transaction] = []
    
    def deposit(self, amount: float) -> None:
        """Deposit money - implementation can change."""
        self._validate_amount(amount)
        self._balance += amount
        self._record_transaction("deposit", amount)
    
    def get_balance(self) -> float:
        """Public interface - stable contract."""
        return self._balance
    
    def _validate_amount(self, amount: float) -> None:
        """Private implementation detail - can change."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
    
    def _record_transaction(self, type_: str, amount: float) -> None:
        """Private implementation detail."""
        self._transaction_history.append(Transaction(type_, amount))
```

### Dependency Injection
Pass dependencies rather than creating them internally:

```python
# Bad: Hard-coded dependency
class OrderProcessor:
    def __init__(self) -> None:
        self.tax_calculator = TaxCalculator()  # Hard to test!

# Good: Injected dependency
class OrderProcessor:
    def __init__(self, tax_calculator: TaxCalculator) -> None:
        self.tax_calculator = tax_calculator  # Easy to mock
```

---

## 4. Tell, Don't Ask

Don't ask an object for its data and then operate on it. Instead, tell the object what to do.

### Violating the Principle
```python
# Bad: Asking for data
def process_discount(order: Order, customer: Customer) -> None:
    if customer.is_premium:
        order.total *= 0.9  # Operating on internal data
```

### Following the Principle
```python
# Good: Telling objects what to do
class Order:
    def apply_discount(self, percentage: float) -> None:
        self._total *= (1 - percentage)

class Customer:
    def get_discount_rate(self) -> float:
        return 0.1 if self._is_premium else 0.0

def process_discount(order: Order, customer: Customer) -> None:
    order.apply_discount(customer.get_discount_rate())
```

---

## 5. Common Design Mistakes

### 1. Anemic Domain Model
Classes with only data (getters/setters) and no behavior:

```python
# Bad: Just a data holder
class User:
    def __init__(self) -> None:
        self.name = ""
        self.email = ""
    
    def get_name(self) -> str: return self.name
    def set_name(self, name: str) -> None: self.name = name
    # ... more getters/setters, no behavior

# Good: Rich domain object
class User:
    def __init__(self, name: str, email: str) -> None:
        self._name = name
        self._email = email
    
    def update_profile(self, name: str | None = None, email: str | None = None) -> None:
        """Encapsulates validation and update logic."""
        if name:
            self._validate_name(name)
            self._name = name
        if email:
            self._validate_email(email)
            self._email = email
```

### 2. Primitive Obsession
Using primitive types instead of domain objects:

```python
# Bad: String for phone number
user.phone = "+1-555-0123"

# Good: PhoneNumber value object
class PhoneNumber:
    def __init__(self, number: str) -> None:
        self._validate(number)
        self._number = number
    
    def format_international(self) -> str: ...
    def format_local(self) -> str: ...
```

### 3. Feature Envy
A method that seems more interested in another class:

```python
# Bad: OrderService constantly accessing Customer internals
class OrderService:
    def calculate_shipping(self, order: Order, customer: Customer) -> float:
        if customer.address.country == "USA":
            if customer.membership_level == "premium":
                return 0.0
        # ...

# Good: Customer knows its own shipping rate
class Customer:
    def get_shipping_rate(self, destination: Address) -> float: ...
```

---

## 6. Design Principles Summary

| Principle | Description | Benefit |
|-----------|-------------|---------|
| **Single Responsibility** | One reason to change | Maintainability |
| **Open/Closed** | Open for extension, closed for modification | Stability |
| **Tell, Don't Ask** | Tell objects what to do | Encapsulation |
| **Composition over Inheritance** | Has-a vs is-a | Flexibility |
| **Dependency Injection** | Pass dependencies in | Testability |

---

## Exercises

Complete the 6 design problems in `exercises/day06/`:

1. **Parking Lot System** - Design parking spots, vehicles, and ticketing
2. **ATM Machine** - Design accounts, cards, and transaction handling
3. **Order Management** - Design products, customers, and orders
4. **Task Board** - Design Kanban board with tasks, columns, and users
5. **Hotel Booking Model** - Design hotel with rooms, bookings, and guests
6. **Mini Library Design** - Full library system design practice

Each exercise applies class design principles to create cohesive, loosely-coupled systems.

---

## Summary

- **Single Responsibility**: Each class should have one clear purpose
- **High Cohesion**: Related responsibilities stay together
- **Low Coupling**: Classes depend on abstractions, not concrete implementations
- **Encapsulation**: Hide implementation details, expose stable interfaces
- **Design for Change**: Structure code so future changes are localized
- **Tell, Don't Ask**: Objects should have behavior, not just data
