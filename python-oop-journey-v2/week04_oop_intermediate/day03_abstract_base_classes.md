# Day 3: Abstract Base Classes

## Overview

Abstract Base Classes (ABCs) provide a way to define interfaces in Python. They allow you to create classes that cannot be instantiated directly but serve as blueprints for subclasses. ABCs ensure that derived classes implement specific methods, making your code more robust and self-documenting.

## Learning Objectives

By the end of today, you will be able to:

- Understand what Abstract Base Classes are and why they matter
- Create ABCs using the `abc` module and `ABC` base class
- Define abstract methods using the `@abstractmethod` decorator
- Create abstract properties using `@abstractproperty` (or `@property` + `@abstractmethod`)
- Implement abstract methods in concrete subclasses
- Recognize when to use ABCs versus regular inheritance

## Key Concepts

### 1. What are Abstract Base Classes?

An Abstract Base Class is a class that:
- Cannot be instantiated directly
- Defines one or more abstract methods that must be implemented by subclasses
- Serves as a contract or interface specification
- Enforces a consistent API across related classes

```python
from abc import ABC, abstractmethod

class Animal(ABC):  # Inherit from ABC
    """Abstract base class for animals."""
    
    @abstractmethod
    def make_sound(self) -> str:
        """Return the sound this animal makes."""
        pass
    
    @abstractmethod
    def move(self) -> str:
        """Return how this animal moves."""
        pass

# This will raise TypeError:
# animal = Animal()  # ✗ Can't instantiate abstract class

class Dog(Animal):
    """A concrete dog implementation."""
    
    def make_sound(self) -> str:
        return "Woof!"
    
    def move(self) -> str:
        return "Running on four legs"

dog = Dog()  # ✓ Works - all abstract methods implemented
```

### 2. The `abc` Module

Python's `abc` module provides the infrastructure for defining ABCs:

```python
from abc import ABC, ABCMeta, abstractmethod, abstractproperty
```

| Component | Purpose |
|-----------|---------|
| `ABC` | Base class for defining ABCs (uses `ABCMeta`) |
| `ABCMeta` | Metaclass for creating ABCs manually |
| `@abstractmethod` | Decorator for abstract methods |
| `@abstractproperty` | Decorator for abstract properties (deprecated, use `@property` + `@abstractmethod`) |

### 3. Creating Abstract Methods

Abstract methods define an interface that subclasses must implement:

```python
from abc import ABC, abstractmethod
from typing import Protocol

class PaymentProcessor(ABC):
    """Abstract base for payment processors."""
    
    def __init__(self, merchant_id: str) -> None:
        self.merchant_id = merchant_id
        self._transaction_log: list[dict] = []
    
    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> dict:
        """Process a payment and return transaction details."""
        pass
    
    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """Refund a transaction by ID."""
        pass
    
    def log_transaction(self, details: dict) -> None:
        """Concrete method - subclasses inherit this."""
        self._transaction_log.append(details)
```

### 4. Abstract Properties

Create abstract properties using both decorators:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class for geometric shapes."""
    
    @property
    @abstractmethod
    def area(self) -> float:
        """Calculate and return the area of the shape."""
        pass
    
    @property
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate and return the perimeter of the shape."""
        pass

class Rectangle(Shape):
    """Concrete rectangle implementation."""
    
    def __init__(self, width: float, height: float) -> None:
        self._width = width
        self._height = height
    
    @property
    def area(self) -> float:
        return self._width * self._height
    
    @property
    def perimeter(self) -> float:
        return 2 * (self._width + self._height)
```

**Important:** The order of decorators matters! Use `@property` above `@abstractmethod`.

### 5. Abstract Class Methods and Static Methods

You can also make class methods and static methods abstract:

```python
from abc import ABC, abstractmethod

class Serializer(ABC):
    """Abstract base for serializers."""
    
    @classmethod
    @abstractmethod
    def from_json(cls, json_data: str) -> "Serializer":
        """Create instance from JSON string."""
        pass
    
    @staticmethod
    @abstractmethod
    def get_format_name() -> str:
        """Return the format name."""
        pass
```

### 6. Partial Implementation

Abstract classes can provide partial implementation:

```python
from abc import ABC, abstractmethod

class DataSource(ABC):
    """Abstract data source with partial implementation."""
    
    def __init__(self, source_name: str) -> None:
        self.source_name = source_name
        self._connected = False
    
    @abstractmethod
    def connect(self) -> None:
        """Establish connection to data source."""
        pass
    
    @abstractmethod
    def fetch_data(self) -> list[dict]:
        """Fetch data from source."""
        pass
    
    def close(self) -> None:
        """Close connection - concrete implementation."""
        self._connected = False
    
    def is_connected(self) -> bool:
        """Check connection status - concrete implementation."""
        return self._connected
```

### 7. When to Use ABCs

**Use ABCs when:**
- Defining a common interface for a family of related classes
- You want to enforce that certain methods are implemented
- Creating plugin architectures or frameworks
- Multiple implementations share a conceptual "is-a" relationship

**Don't use ABCs when:**
- Simple duck typing is sufficient
- You only need one implementation
- Composition would be cleaner than inheritance
- The interface is too granular or changes frequently

### 8. ABCs vs Protocols

Python 3.8+ introduced `Protocol` for structural subtyping:

```python
from abc import ABC, abstractmethod
from typing import Protocol

# ABC approach - nominal subtyping
class Drawable(ABC):
    @abstractmethod
    def draw(self) -> None:
        pass

# Protocol approach - structural subtyping
class DrawableProtocol(Protocol):
    def draw(self) -> None:
        pass

# With ABC, class must explicitly inherit
class Circle(Drawable):
    def draw(self) -> None:
        print("Drawing circle")

# With Protocol, any class with draw() method works
class Square:
    def draw(self) -> None:
        print("Drawing square")

def render(item: DrawableProtocol) -> None:
    item.draw()
```

## Common Mistakes

### 1. Forgetting to Inherit from ABC

```python
from abc import abstractmethod

class BadBase:  # WRONG - doesn't inherit from ABC
    @abstractmethod
    def method(self) -> None:
        pass

# This won't raise an error!
instance = BadBase()  # Creates instance without implementing method
```

### 2. Wrong Decorator Order

```python
from abc import ABC, abstractmethod

class WrongOrder(ABC):
    @abstractmethod  # WRONG order
    @property
    def value(self) -> int:
        pass

class RightOrder(ABC):
    @property
    @abstractmethod  # CORRECT - abstractmethod goes inside
    def value(self) -> int:
        pass
```

### 3. Calling super() on Abstract Methods

```python
from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def process(self) -> str:
        """Process something."""
        pass

class Derived(Base):
    def process(self) -> str:
        result = super().process()  # ✗ Don't call abstract method!
        return f"processed: {result}"
```

### 4. Instantiating Abstract Classes

```python
from abc import ABC, abstractmethod

class Plugin(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

# This raises TypeError:
plugin = Plugin()  # ✗ Can't instantiate abstract class
```

## Best Practices

1. **Use descriptive docstrings** - Document what each abstract method should do
2. **Provide type hints** - Make the interface clear
3. **Include concrete methods** - Share common logic in the base class
4. **Keep ABCs focused** - One responsibility per ABC
5. **Document preconditions** - Specify what inputs abstract methods expect
6. **Consider Protocol** - For structural typing, use Protocol instead

## Connection to Exercises

Today's exercises build ABC skills progressively:

| Exercise | Concepts Practiced | Project Connection |
|----------|-------------------|-------------------|
| 01. Payment Processor ABC | Basic ABC with process/refund methods | Payment processing interface |
| 02. Shape ABC | Abstract properties (area, perimeter) | Measurement patterns |
| 03. Employee Role ABC | Abstract calculate_pay with different implementations | Staff role abstraction |
| 04. Transport Interface | Abstract move/location methods | Animal movement tracking |
| 05. Storage Backend ABC | CRUD operations as abstract methods | Data persistence layer |
| 06. Parser Framework | Abstract parse/validate with partial implementation | Data import/export |

---

## Connection to Weekly Project

The Animal Shelter Management System relies heavily on Abstract Base Classes:

- **Animal (ABC)**: Defines the interface all animals must implement (`make_sound()`, `get_care_instructions()`)
- **StaffMember (ABC)**: Enforces that all staff roles implement `perform_duties()`
- **MedicalRecord (ABC)**: Standardizes medical record handling across all animal types
- **Adoptable (ABC)**: Interface for animals that can be adopted

ABCs ensure that new animal types or staff roles cannot be created without implementing all required functionality.

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify: `pytest week04_oop_intermediate/tests/day03/ -v`
2. Review any problems you found challenging
3. Preview Day 4: **Multiple Inheritance and MRO** - Combining multiple parent classes

## Key Takeaways

1. **ABCs define interfaces** - They specify what methods must exist without saying how
2. **Cannot instantiate ABCs** - The class must be subclassed and methods implemented
3. **@abstractmethod is required** - Just inheriting from ABC isn't enough
4. **Order matters for properties** - @property goes outside @abstractmethod
5. **Mix concrete and abstract** - ABCs can include implemented methods too
6. **Enforce contracts** - ABCs catch missing implementations at instantiation time

## Further Reading

- [Python ABC Documentation](https://docs.python.org/3/library/abc.html)
- [PEP 3119 - Introducing Abstract Base Classes](https://peps.python.org/pep-3119/)
- [Python Data Model - Abstract Base Classes](https://docs.python.org/3/reference/datamodel.html#abstract-base-classes)

## Time Estimate

- Reading: 30-40 minutes
- Exercises: 2-3 hours
- Review: 20 minutes
