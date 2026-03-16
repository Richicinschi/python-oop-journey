# Day 5: Pattern Tradeoffs and Anti-patterns

## Learning Objectives

After completing this day, you will understand:
- Common anti-patterns and how to recognize them
- The God Object anti-pattern and how to refactor it
- When Singleton becomes an anti-pattern and alternatives
- The cost of over-engineering and premature abstraction
- How to convert complex conditionals to the Strategy pattern
- When to favor composition over deep inheritance hierarchies
- How to simplify over-abstracted code

## Theory

### Common Anti-patterns

Anti-patterns are common solutions to recurring problems that appear beneficial but actually cause more problems than they solve.

#### 1. God Object (God Class)

A God Object is a class that knows too much or does too much. It has too many responsibilities and dependencies.

**The Problem:**
```python
class OrderManager:  # God Object - does WAY too much
    def __init__(self):
        self.inventory = {}
        self.customers = {}
        self.payments = []
        self.shipments = []
        self.reports = []
    
    def add_product(self, sku, name, price): ...
    def update_inventory(self, sku, quantity): ...
    def add_customer(self, customer_id, name, email): ...
    def process_payment(self, order_id, amount, method): ...
    def refund_payment(self, payment_id): ...
    def create_shipment(self, order_id, address): ...
    def track_shipment(self, shipment_id): ...
    def generate_sales_report(self, start_date, end_date): ...
    def generate_inventory_report(self): ...
    def send_notification(self, customer_id, message): ...
    def calculate_taxes(self, amount, region): ...
    def apply_discount(self, order_id, code): ...
```

**Why It's Bad:**
- Violates Single Responsibility Principle
- Hard to test (too many dependencies)
- Changes for any reason (high churn)
- Cannot be reused in parts
- Team conflicts (everyone edits the same file)

**The Solution - Split by Responsibility:**
```python
class InventoryService:
    """Manages products and stock levels."""
    def __init__(self) -> None:
        self._products: dict[str, Product] = {}
    
    def add_product(self, product: Product) -> None: ...
    def check_stock(self, sku: str) -> int: ...


class CustomerService:
    """Manages customer data."""
    def __init__(self) -> None:
        self._customers: dict[str, Customer] = {}
    
    def register_customer(self, customer: Customer) -> None: ...
    def get_customer(self, customer_id: str) -> Customer | None: ...


class PaymentProcessor:
    """Handles payment operations."""
    def process(self, amount: Decimal, method: PaymentMethod) -> PaymentResult: ...
    def refund(self, payment_id: str) -> RefundResult: ...


class OrderService:
    """Coordinates order workflow using composed services."""
    def __init__(
        self,
        inventory: InventoryService,
        customers: CustomerService,
        payments: PaymentProcessor,
    ) -> None:
        self._inventory = inventory
        self._customers = customers
        self._payments = payments
```

#### 2. Singleton Overuse

Singleton ensures only one instance exists, but often creates hidden dependencies and makes testing difficult.

**The Problem:**
```python
class DatabaseConnection:
    _instance: DatabaseConnection | None = None
    
    def __new__(cls) -> DatabaseConnection:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def query(self, sql: str) -> list[dict]: ...

# Hidden dependency - hard to test, hard to mock
class UserRepository:
    def get_user(self, user_id: str) -> User | None:
        db = DatabaseConnection()  # Hidden coupling!
        result = db.query(f"SELECT * FROM users WHERE id = {user_id}")
        return User.from_row(result[0]) if result else None
```

**Why It's Bad:**
- Hidden dependencies (tight coupling)
- Hard to unit test (cannot mock)
- Global state (action at a distance)
- Cannot have different configs for different contexts

**The Solution - Dependency Injection:**
```python
from typing import Protocol


class Database(Protocol):
    """Database interface - can be real or mock."""
    def query(self, sql: str, params: tuple = ()) -> list[dict]: ...


class PostgresDatabase:
    """Real database implementation."""
    def __init__(self, connection_string: str) -> None:
        self._conn = connect(connection_string)
    
    def query(self, sql: str, params: tuple = ()) -> list[dict]: ...


class UserRepository:
    """Repository with explicit dependency."""
    def __init__(self, db: Database) -> None:
        self._db = db  # Injected dependency - testable!
    
    def get_user(self, user_id: str) -> User | None:
        result = self._db.query(
            "SELECT * FROM users WHERE id = %s", (user_id,)
        )
        return User.from_row(result[0]) if result else None

# Testing is now easy:
class MockDatabase:
    """Test double for database."""
    def __init__(self, data: list[dict]) -> None:
        self._data = data
    
    def query(self, sql: str, params: tuple = ()) -> list[dict]:
        return [row for row in self._data if row["id"] == params[0]]

# Usage:
repo = UserRepository(MockDatabase([{"id": "1", "name": "Alice"}]))
user = repo.get_user("1")  # Returns test user, no real DB needed
```

#### 3. Complex Conditionals (If-Else Ladder)

Long chains of if-elif-else statements for behavior selection.

**The Problem:**
```python
class PaymentProcessor:
    def process(self, amount: float, method: str) -> str:
        if method == "credit_card":
            # 20 lines of credit card logic
            return f"Charged ${amount} to credit card"
        elif method == "paypal":
            # 20 lines of PayPal logic
            return f"Paid ${amount} via PayPal"
        elif method == "bitcoin":
            # 20 lines of crypto logic
            return f"Transferred ${amount} in BTC"
        elif method == "bank_transfer":
            # 20 lines of bank logic
            return f"Bank transfer of ${amount} initiated"
        else:
            raise ValueError(f"Unknown payment method: {method}")
```

**Why It's Bad:**
- Violates Open/Closed Principle (modify to add new method)
- Code duplication
- Hard to test each branch
- Grows unbounded

**The Solution - Strategy Pattern:**
```python
from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """Abstract payment strategy."""
    
    @abstractmethod
    def pay(self, amount: float) -> str: ...
    
    @abstractmethod
    def validate(self) -> bool: ...


class CreditCardStrategy(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str) -> None:
        self._card_number = card_number
        self._cvv = cvv
    
    def validate(self) -> bool:
        return len(self._card_number) == 16 and len(self._cvv) == 3
    
    def pay(self, amount: float) -> str:
        return f"Charged ${amount} to card ending in {self._card_number[-4:]}"


class PayPalStrategy(PaymentStrategy):
    def __init__(self, email: str) -> None:
        self._email = email
    
    def validate(self) -> bool:
        return "@" in self._email
    
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} via PayPal ({self._email})"


class PaymentProcessor:
    """Uses Strategy pattern for extensible payments."""
    
    def __init__(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy
    
    def process(self, amount: float) -> str:
        if not self._strategy.validate():
            raise ValueError("Payment validation failed")
        return self._strategy.pay(amount)

# Adding new payment methods requires NO changes to existing code:
class BitcoinStrategy(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f"Transferred ${amount} worth of BTC"
```

#### 4. Deep Inheritance Hierarchies

Excessive inheritance depth creates rigid, fragile code.

**The Problem:**
```python
class Widget: ...
class Control(Widget): ...
class TextControl(Control): ...
class InputField(TextControl): ...
class ValidatedInput(InputField): ...
class EmailInput(ValidatedInput): ...
class SecureEmailInput(EmailInput): ...  # 6 levels deep!
```

**Why It's Bad:**
- Fragile Base Class problem
- Hard to understand (must read entire hierarchy)
- Methods defined far from where they're used
- Cannot change behavior at runtime
- Testing requires understanding all parent classes

**The Solution - Composition:**
```python
from dataclasses import dataclass
from typing import Callable


@dataclass
class ValidationRule:
    """Composable validation rule."""
    validate: Callable[[str], bool]
    message: str


class InputField:
    """Simple input with composable behaviors."""
    
    def __init__(
        self,
        name: str,
        validators: list[ValidationRule] | None = None,
        mask_input: bool = False,
    ) -> None:
        self.name = name
        self._validators = validators or []
        self._mask_input = mask_input
        self._value = ""
    
    def set_value(self, value: str) -> list[str]:
        """Set value and return validation errors."""
        errors = [
            rule.message for rule in self._validators
            if not rule.validate(value)
        ]
        if not errors:
            self._value = value
        return errors

# Compose behavior instead of inheriting:
email_input = InputField(
    name="email",
    validators=[
        ValidationRule(lambda x: "@" in x, "Must contain @"),
        ValidationRule(lambda x: "." in x.split("@")[-1], "Must have domain"),
    ],
)

secure_email = InputField(
    name="secure_email",
    validators=[email_input._validators[0]],  # Reuse validators
    mask_input=True,  # Compose behavior
)
```

#### 5. Over-Engineering / Premature Abstraction

Creating abstractions before they are needed, adding complexity without value.

**The Problem:**
```python
# Over-abstracted simple task
class AbstractTaskExecutor:
    @abstractmethod
    def pre_execute(self): ...
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def post_execute(self): ...

class AbstractValidator:
    @abstractmethod
    def validate(self, context): ...

class TaskContext:
    def __init__(self):
        self.validators: list[AbstractValidator] = []
        self.preprocessors: list[Callable] = []
        self.postprocessors: list[Callable] = []

class ConcreteTask(AbstractTaskExecutor):
    def __init__(self):
        self.context = TaskContext()
    
    def pre_execute(self): 
        for p in self.context.preprocessors:
            p()
    
    def execute(self):
        for v in self.context.validators:
            v.validate(self.context)
        result = self._do_actual_work()  # 5 lines of real logic!
        return result
    
    def post_execute(self):
        for p in self.context.postprocessors:
            p()
    
    def _do_actual_work(self):
        return "Hello World"  # All this for THIS?
```

**Why It's Bad:**
- Massive indirection for simple operations
- Hard to follow execution flow
- YAGNI (You Aren't Gonna Need It)
- Abstraction without purpose

**The Solution - Start Simple:**
```python
def execute_task() -> str:
    """Simple, direct, testable."""
    # Pre-processing (if needed)
    print("Starting task...")
    
    # Validation (if needed)
    if not has_permission():
        raise PermissionError("No access")
    
    # Actual work
    result = "Hello World"
    
    # Post-processing (if needed)
    log_completion()
    
    return result

# Abstract ONLY when you have multiple implementations:
class Task(ABC):
    """Abstract only when we NEED multiple task types."""
    @abstractmethod
    def run(self) -> str: ...

class EmailTask(Task):
    def run(self) -> str: ...

class ReportTask(Task):
    def run(self) -> str: ...
```

### Pattern Tradeoffs

| Pattern | When to Use | When NOT to Use | Cost |
|---------|-------------|-----------------|------|
| Singleton | Truly single resource (DB connection pool) | Testing, multiple configs needed | Hidden dependencies |
| Factory | Object creation is complex | Simple constructors work fine | Indirection |
| Strategy | Multiple interchangeable algorithms | Only one algorithm exists | More classes |
| Observer | Event-driven architectures | Simple synchronous code | Memory leaks if not careful |
| Decorator | Add responsibilities dynamically | Simple subclassing works | Wrapper complexity |
| Adapter | Interface mismatch | Control over both interfaces | Indirection |

### The Golden Rule

> "Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away." - Antoine de Saint-Exupéry

**Start simple. Abstract only when:**
1. You have actual duplication (not just similar code)
2. You have multiple implementations that need common interface
3. The abstraction makes the code EASIER to understand
4. Testing requires the abstraction

## Connection to Exercises

Today's exercises focus on recognizing and fixing anti-patterns:

| Exercise | Anti-Pattern Addressed | Solution Applied |
|----------|------------------------|------------------|
| 01. Refactor God Object | God Object / Class with too many responsibilities | Split into focused services with single responsibilities |
| 02. Remove Unnecessary Singleton | Singleton overuse / Hidden dependencies | Dependency injection with explicit interfaces |
| 03. Strategy vs Conditionals | Complex if-elif chains | Strategy pattern for interchangeable algorithms |
| 04. Inheritance to Composition | Deep inheritance hierarchies | Flatten to composition with behavior injection |
| 05. Over-Abstracted Service Cleanup | Premature abstraction / YAGNI | Simplify to direct, readable code |

---

## Connection to Game Framework Project

The tradeoffs and anti-patterns from Day 5 are especially relevant when building the Game Framework:

### Avoiding God Objects in ECS

The Game Framework uses ECS specifically to avoid God Objects:
- Instead of a `Player` class with 20 methods, you have a player `Entity`
- Data is in `Component`s (PositionComponent, HealthComponent, etc.)
- Behavior is in `System`s that process entities with specific components

```python
# Anti-pattern: God Object
class Player:  # Does WAY too much
    def move(self): ...
    def render(self): ...
    def attack(self): ...
    def take_damage(self): ...
    def save_progress(self): ...
    def load_inventory(self): ...

# Better: ECS separation
def move_system(entities):  # Only movement
    for e in entities_with(Position, Velocity):
        e.position += e.velocity

def render_system(entities):  # Only rendering
    for e in entities_with(Position, Sprite):
        draw(e.sprite, e.position)
```

### Singleton Tradeoffs in Games

The Game Framework's EventBus could be a Singleton, but the project shows alternatives:
- **Singleton approach**: Global event bus accessible everywhere
- **Dependency injection approach**: Event bus passed to systems that need it (more testable)

### When to Add Patterns to the Game Framework

As you build the project, ask these questions before adding a pattern:

1. **Do I have actual duplication?** (not just similar-looking code)
2. **Will this make the code easier or harder to understand?**
3. **Am I solving a problem I actually have, or one I might have someday?**
4. **Can I write a simple version first and refactor later?**

---

## Summary

- **God Objects**: Split by responsibility using composition
- **Singleton Overuse**: Replace with dependency injection
- **Complex Conditionals**: Use Strategy pattern for algorithm selection
- **Deep Inheritance**: Favor composition with small, focused classes
- **Over-Engineering**: Start simple, abstract only when necessary
- Patterns are tools, not goals - use them judiciously
