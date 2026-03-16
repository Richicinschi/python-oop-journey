# Day 3: Refactoring Procedural Code into OOP

## Learning Objectives

By the end of this day, you will be able to:

1. Identify "code smells" that suggest OOP would be beneficial
2. Extract classes from procedural code step by step
3. Convert data structures into encapsulated objects
4. Transform function groups into cohesive class hierarchies
5. Apply the refactoring process safely with tests
6. Recognize when NOT to refactor to OOP

---

## Key Concepts

### 1. When to Refactor to OOP

Procedural code isn't inherently bad, but certain patterns suggest OOP would improve the design:

| Code Smell | Description | OOP Solution |
|------------|-------------|--------------|
| **Data Clumps** | Same groups of variables passed together | Extract into a class |
| **Primitive Obsession** | Using primitives for domain concepts | Create value objects |
| **Switch Statements** | Complex conditionals on type codes | Polymorphism |
| **Feature Envy** | Functions that work mostly with another data structure | Move method to the class |
| **Shotgun Surgery** | Changing one thing requires many small changes | Cohesive classes |
| **Long Parameter Lists** | Functions with many parameters | Parameter object pattern |

### 2. The Refactoring Process

Safe refactoring follows a disciplined approach:

```
1. Ensure you have tests covering the code
2. Identify cohesive data and behavior
3. Create the new class structure
4. Migrate data and functions incrementally
5. Update callers gradually
6. Remove the old code
7. Verify all tests pass
```

### 3. Before and After: Invoice System

#### Before: Procedural Approach

```python
from __future__ import annotations

# Data as dictionaries
def create_invoice(customer_name: str, customer_email: str) -> dict:
    return {
        "customer_name": customer_name,
        "customer_email": customer_email,
        "items": [],
        "subtotal": 0.0,
        "tax": 0.0,
        "total": 0.0,
    }

def add_item(invoice: dict, name: str, quantity: int, unit_price: float) -> None:
    item = {
        "name": name,
        "quantity": quantity,
        "unit_price": unit_price,
        "line_total": quantity * unit_price,
    }
    invoice["items"].append(item)
    _recalculate(invoice)

def _recalculate(invoice: dict) -> None:
    invoice["subtotal"] = sum(item["line_total"] for item in invoice["items"])
    invoice["tax"] = invoice["subtotal"] * 0.10  # 10% tax
    invoice["total"] = invoice["subtotal"] + invoice["tax"]

def format_invoice(invoice: dict) -> str:
    lines = [f"Invoice for {invoice['customer_name']}"]
    lines.append("-" * 40)
    for item in invoice["items"]:
        lines.append(f"  {item['name']}: {item['quantity']} x ${item['unit_price']:.2f}")
    lines.append("-" * 40)
    lines.append(f"Subtotal: ${invoice['subtotal']:.2f}")
    lines.append(f"Tax (10%): ${invoice['tax']:.2f}")
    lines.append(f"Total: ${invoice['total']:.2f}")
    return "\n".join(lines)
```

**Problems:**
- Data structure is exposed - anyone can modify `invoice["items"]` directly
- Functions are decoupled from the data they operate on
- No validation or constraints enforced
- Easy to create inconsistent state

#### After: OOP Approach

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Self


@dataclass
class InvoiceItem:
    """Value object representing a line item."""
    
    name: str
    quantity: int
    unit_price: float
    
    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative")
    
    @property
    def line_total(self) -> float:
        return self.quantity * self.unit_price
    
    def __str__(self) -> str:
        return f"{self.name}: {self.quantity} x ${self.unit_price:.2f}"


@dataclass
class Customer:
    """Value object representing a customer."""
    
    name: str
    email: str
    
    def __post_init__(self) -> None:
        if "@" not in self.email:
            raise ValueError("Invalid email address")


class Invoice:
    """Invoice entity with encapsulated state and behavior."""
    
    TAX_RATE = 0.10
    
    def __init__(self, customer: Customer) -> None:
        self._customer = customer
        self._items: list[InvoiceItem] = []
        self._subtotal: float = 0.0
        self._tax: float = 0.0
        self._total: float = 0.0
    
    @property
    def customer(self) -> Customer:
        return self._customer
    
    @property
    def items(self) -> tuple[InvoiceItem, ...]:
        """Return immutable view of items."""
        return tuple(self._items)
    
    @property
    def subtotal(self) -> float:
        return self._subtotal
    
    @property
    def tax(self) -> float:
        return self._tax
    
    @property
    def total(self) -> float:
        return self._total
    
    def add_item(self, name: str, quantity: int, unit_price: float) -> Self:
        """Add an item and return self for chaining."""
        item = InvoiceItem(name, quantity, unit_price)
        self._items.append(item)
        self._recalculate()
        return self
    
    def remove_item(self, index: int) -> Self:
        """Remove an item by index."""
        if 0 <= index < len(self._items):
            self._items.pop(index)
            self._recalculate()
        return self
    
    def _recalculate(self) -> None:
        """Recalculate totals - private method."""
        self._subtotal = sum(item.line_total for item in self._items)
        self._tax = self._subtotal * self.TAX_RATE
        self._total = self._subtotal + self._tax
    
    def format(self) -> str:
        """Format invoice as string."""
        lines = [f"Invoice for {self._customer.name}", "-" * 40]
        for item in self._items:
            lines.append(f"  {item}")
        lines.extend([
            "-" * 40,
            f"Subtotal: ${self._subtotal:.2f}",
            f"Tax ({self.TAX_RATE:.0%}): ${self._tax:.2f}",
            f"Total: ${self._total:.2f}",
        ])
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return self.format()


# Usage
invoice = Invoice(Customer("Alice Smith", "alice@example.com"))
invoice.add_item("Widget", 2, 29.99).add_item("Gadget", 1, 49.99)
print(invoice)
```

**Benefits:**
- Encapsulation prevents invalid states
- Validation in constructors
- Business logic lives with the data
- Immutable views prevent external modification
- Chainable methods for fluent interface

### 4. Before and After: CSV Report Generation

#### Before: Script-Style Code

```python
from __future__ import annotations

import csv
from pathlib import Path


def read_sales_data(filepath: str) -> list[dict]:
    """Read sales data from CSV."""
    with open(filepath, newline="") as f:
        return list(csv.DictReader(f))


def calculate_total_sales(records: list[dict]) -> float:
    """Sum all sales amounts."""
    return sum(float(r["amount"]) for r in records)


def calculate_sales_by_region(records: list[dict]) -> dict[str, float]:
    """Aggregate sales by region."""
    totals: dict[str, float] = {}
    for record in records:
        region = record["region"]
        amount = float(record["amount"])
        totals[region] = totals.get(region, 0.0) + amount
    return totals


def generate_report(data_file: str, output_file: str) -> None:
    """Generate a sales report."""
    records = read_sales_data(data_file)
    total = calculate_total_sales(records)
    by_region = calculate_sales_by_region(records)
    
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total Sales", f"${total:.2f}"])
        writer.writerow([])
        writer.writerow(["Region", "Sales"])
        for region, amount in sorted(by_region.items()):
            writer.writerow([region, f"${amount:.2f}"])
```

#### After: Class-Based Design

```python
from __future__ import annotations

import csv
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class SalesRecord:
    """Immutable sales record."""
    
    id: str
    region: str
    amount: float
    date: str
    
    @classmethod
    def from_dict(cls, data: dict[str, str]) -> SalesRecord:
        return cls(
            id=data["id"],
            region=data["region"],
            amount=float(data["amount"]),
            date=data["date"],
        )


class SalesData:
    """Encapsulates sales data with query methods."""
    
    def __init__(self, records: list[SalesRecord]) -> None:
        self._records = records
    
    @classmethod
    def from_csv(cls, filepath: str) -> SalesData:
        with open(filepath, newline="") as f:
            rows = list(csv.DictReader(f))
        return cls([SalesRecord.from_dict(r) for r in rows])
    
    @property
    def total_sales(self) -> float:
        return sum(r.amount for r in self._records)
    
    def sales_by_region(self) -> dict[str, float]:
        totals: dict[str, float] = {}
        for record in self._records:
            totals[record.region] = totals.get(record.region, 0.0) + record.amount
        return totals
    
    def sales_by_date_range(self, start: str, end: str) -> SalesData:
        """Filter records by date range, returns new SalesData."""
        filtered = [r for r in self._records if start <= r.date <= end]
        return SalesData(filtered)


class ReportFormatter(ABC):
    """Abstract base for report formatters."""
    
    @abstractmethod
    def format(self, data: SalesData) -> str:
        pass


class CSVReportFormatter(ReportFormatter):
    """Format reports as CSV."""
    
    def format(self, data: SalesData) -> str:
        lines = []
        lines.append("Metric,Value")
        lines.append(f"Total Sales,${data.total_sales:.2f}")
        lines.append("")
        lines.append("Region,Sales")
        for region, amount in sorted(data.sales_by_region().items()):
            lines.append(f"{region},${amount:.2f}")
        return "\n".join(lines)


class ReportGenerator:
    """High-level report generation orchestrator."""
    
    def __init__(self, formatter: ReportFormatter) -> None:
        self._formatter = formatter
    
    def generate(self, data: SalesData) -> str:
        return self._formatter.format(data)
    
    def generate_to_file(self, data: SalesData, filepath: str) -> None:
        Path(filepath).write_text(self.generate(data))


# Usage
sales = SalesData.from_csv("sales.csv")
report = ReportGenerator(CSVReportFormatter())
report.generate_to_file(sales, "report.csv")
```

### 5. Before and After: Authentication Flow

#### Before: Function-Based Auth

```python
from __future__ import annotations

import hashlib
import secrets
from typing import Callable

# Global state (problematic!)
_active_sessions: dict[str, dict] = {}
_user_database: dict[str, dict] = {}


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${hashed}"


def verify_password(password: str, stored: str) -> bool:
    salt, hashed = stored.split("$")
    check = hashlib.sha256((password + salt).encode()).hexdigest()
    return secrets.compare_digest(hashed, check)


def register_user(username: str, password: str) -> bool:
    if username in _user_database:
        return False
    _user_database[username] = {
        "password": hash_password(password),
        "created_at": "2024-01-01",
    }
    return True


def login(username: str, password: str) -> str | None:
    user = _user_database.get(username)
    if not user or not verify_password(password, user["password"]):
        return None
    token = secrets.token_urlsafe(32)
    _active_sessions[token] = {
        "username": username,
        "created_at": "2024-01-01",
    }
    return token


def validate_token(token: str) -> dict | None:
    return _active_sessions.get(token)


def logout(token: str) -> bool:
    if token in _active_sessions:
        del _active_sessions[token]
        return True
    return False
```

**Problems:**
- Global state makes testing difficult
- No encapsulation of user data
- Cannot have multiple auth services
- Hard to swap implementations

#### After: Service Class Design

```python
from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Protocol


@dataclass(frozen=True)
class User:
    """Immutable user value object."""
    
    username: str
    password_hash: str
    created_at: datetime


@dataclass
class Session:
    """Session entity with expiration."""
    
    token: str
    username: str
    created_at: datetime
    expires_at: datetime
    
    @property
    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        return not self.is_expired


class UserRepository(Protocol):
    """Repository interface for user storage."""
    
    def get(self, username: str) -> User | None:
        ...
    
    def save(self, user: User) -> None:
        ...
    
    def exists(self, username: str) -> bool:
        ...


class InMemoryUserRepository:
    """In-memory implementation of UserRepository."""
    
    def __init__(self) -> None:
        self._users: dict[str, User] = {}
    
    def get(self, username: str) -> User | None:
        return self._users.get(username)
    
    def save(self, user: User) -> None:
        self._users[user.username] = user
    
    def exists(self, username: str) -> bool:
        return username in self._users


class PasswordHasher:
    """Encapsulates password hashing strategy."""
    
    def hash(self, password: str) -> str:
        salt = secrets.token_hex(16)
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${hashed}"
    
    def verify(self, password: str, stored: str) -> bool:
        salt, hashed = stored.split("$")
        check = hashlib.sha256((password + salt).encode()).hexdigest()
        return secrets.compare_digest(hashed, check)


class AuthService:
    """Authentication service with dependency injection."""
    
    SESSION_DURATION_HOURS = 24
    
    def __init__(
        self,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._user_repo = user_repo
        self._hasher = password_hasher
        self._sessions: dict[str, Session] = {}
    
    def register(self, username: str, password: str) -> User:
        """Register a new user."""
        if self._user_repo.exists(username):
            raise ValueError(f"User '{username}' already exists")
        
        password_hash = self._hasher.hash(password)
        user = User(
            username=username,
            password_hash=password_hash,
            created_at=datetime.now(),
        )
        self._user_repo.save(user)
        return user
    
    def login(self, username: str, password: str) -> Session:
        """Authenticate and create session."""
        user = self._user_repo.get(username)
        if not user:
            raise ValueError("Invalid credentials")
        
        if not self._hasher.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")
        
        now = datetime.now()
        session = Session(
            token=secrets.token_urlsafe(32),
            username=username,
            created_at=now,
            expires_at=now + timedelta(hours=self.SESSION_DURATION_HOURS),
        )
        self._sessions[session.token] = session
        return session
    
    def validate_token(self, token: str) -> Session | None:
        """Validate a session token."""
        session = self._sessions.get(token)
        if session and session.is_valid:
            return session
        # Clean up expired session
        if session and session.is_expired:
            del self._sessions[token]
        return None
    
    def logout(self, token: str) -> bool:
        """Invalidate a session."""
        if token in self._sessions:
            del self._sessions[token]
            return True
        return False
```

### 6. Common Refactoring Patterns

#### Extract Class

When multiple functions operate on the same data:

```python
# Before: Functions operating on employee data
def calculate_employee_tax(employee: dict) -> float:
    return employee["salary"] * 0.25

def give_employee_raise(employee: dict, amount: float) -> None:
    employee["salary"] += amount

def format_employee(employee: dict) -> str:
    return f"{employee['name']}: ${employee['salary']}"

# After: Encapsulated Employee class
class Employee:
    TAX_RATE = 0.25
    
    def __init__(self, name: str, salary: float) -> None:
        self._name = name
        self._salary = salary
    
    @property
    def tax(self) -> float:
        return self._salary * self.TAX_RATE
    
    def give_raise(self, amount: float) -> None:
        self._salary += amount
    
    def __str__(self) -> str:
        return f"{self._name}: ${self._salary}"
```

#### Replace Conditional with Polymorphism

```python
# Before: Switch on type
def calculate_shipping(order: dict) -> float:
    if order["type"] == "standard":
        return 5.00
    elif order["type"] == "express":
        return 15.00
    elif order["type"] == "free":
        return 0.00

# After: Polymorphic classes
from abc import ABC, abstractmethod

class Order(ABC):
    @abstractmethod
    def calculate_shipping(self) -> float:
        pass

class StandardOrder(Order):
    def calculate_shipping(self) -> float:
        return 5.00

class ExpressOrder(Order):
    def calculate_shipping(self) -> float:
        return 15.00

class FreeShippingOrder(Order):
    def calculate_shipping(self) -> float:
        return 0.00
```

#### Introduce Parameter Object

```python
# Before: Long parameter list
def create_appointment(
    patient_first: str,
    patient_last: str,
    patient_email: str,
    doctor_name: str,
    date: str,
    time: str,
    duration: int,
) -> dict:
    ...

# After: Parameter objects
@dataclass
class Patient:
    first_name: str
    last_name: str
    email: str

@dataclass
class Doctor:
    name: str

@dataclass
class TimeSlot:
    date: str
    time: str
    duration_minutes: int

class Appointment:
    def __init__(self, patient: Patient, doctor: Doctor, slot: TimeSlot) -> None:
        self.patient = patient
        self.doctor = doctor
        self.slot = slot
```

---

## Common Mistakes

### 1. Refactoring Without Tests

```python
# Dangerous: No tests to catch regressions
def refactor_this():
    # Changing complex logic without safety net
    ...

# Safe: Add tests first, then refactor
def test_existing_behavior():
    assert legacy_function(input) == expected_output

def refactored_function():
    # Now refactor with confidence
    ...
```

### 2. Big Bang Refactoring

```python
# Wrong: Rewrite everything at once
# - High risk
# - Hard to debug
# - Easy to introduce bugs

# Right: Incremental refactoring
# 1. Extract one class at a time
# 2. Run tests after each change
# 3. Commit working code frequently
```

### 3. Over-Engineering

```python
# Wrong: Unnecessary abstraction for simple cases
class AbstractSingletonFactoryBean:
    ...

# Right: Keep it simple until complexity is needed
def process_data(data: list) -> list:
    return [transform(item) for item in data]
```

### 4. Preserving Procedural API

```python
# Wrong: Creating a class but keeping global functions
def old_function():
    return NewClass().method()  # Just a wrapper

# Right: Migrate callers to use the new class directly
# Gradually update imports and calls
```

---

## When NOT to Refactor

Sometimes procedural code is the right choice:

| Keep Procedural | Reason |
|-----------------|--------|
| Scripts & one-offs | No maintenance, no complexity |
| Pure data transformation | Functions like `map`, `filter` are clearer |
| Mathematical operations | Algorithms are naturally procedural |
| Simple utilities | `os.path.join()` is fine as a function |
| Performance-critical code | OOP overhead might matter |

---

## Connection to Exercises

Today's exercises practice refactoring real-world scenarios:

| Problem | Starting Point | OOP Design |
|---------|----------------|------------|
| 01. Invoice Refactor | Dict-based invoice functions | Invoice/Item/Customer classes |
| 02. CSV Report Refactor | Script-style report generation | Data class + Formatter + Generator |
| 03. Auth Flow Refactor | Global state functions | Service + Repository + Value objects |
| 04. Shopping Cart Refactor | Dict-based cart | Cart + LineItem + Product classes |
| 05. Log Parser Refactor | Parsing functions | LogEntry + Analyzer + Report classes |

## Connection to Weekly Project

The Personal Finance Tracker project demonstrates refactoring principles:

- **Data Clumps → Classes**: Account info, transaction records, and budget data become proper objects
- **Feature Envy → Encapsulation**: Financial calculations live in the classes they operate on
- **Global State → Services**: Transaction processing moves from global functions to service classes
- **Validation**: Input validation happens at object construction, not scattered through code
- **Repository Pattern**: Data access is abstracted, allowing test doubles

When building the project, you'll refactor raw dictionary data into well-structured domain objects with proper encapsulation.

---

## Quick Reference

```python
from __future__ import annotations

# Refactoring Checklist
# 1. Write tests for existing behavior
# 2. Identify data clumps
# 3. Extract classes for related data
# 4. Move functions to appropriate classes
# 5. Replace conditionals with polymorphism
# 6. Introduce dependency injection
# 7. Remove global state
# 8. Run tests, commit, repeat

# Value Object Pattern
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

# Entity Pattern
class Order:
    def __init__(self, id: str) -> None:
        self._id = id
        self._items: list[OrderItem] = []
    
    @property
    def id(self) -> str:
        return self._id

# Service Pattern
class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self._repo = repository
    
    def create_order(self, customer: Customer) -> Order:
        ...

# Repository Pattern
class OrderRepository(Protocol):
    def get(self, id: str) -> Order | None: ...
    def save(self, order: Order) -> None: ...
```

---

## Next Steps

After completing today's exercises:
1. Compare procedural and OOP approaches in your own code
2. Practice identifying when each style is appropriate
3. Preview Day 4: **Data Processing with Objects**
