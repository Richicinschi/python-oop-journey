# Day 5: Polymorphism

## Learning Objectives

By the end of this day, you will:

1. Understand polymorphism as "many forms" - the ability to treat different objects uniformly through a common interface
2. Implement inheritance-based polymorphism using method overriding
3. Use duck typing for polymorphic behavior without inheritance
4. Apply polymorphism to write flexible, extensible code
5. Design functions that work with any object supporting a specific interface
6. Recognize when to use polymorphism vs. isinstance checks

---

## Core Concepts

### 1. What is Polymorphism?

**Polymorphism** (from Greek: "many forms") is the ability of different objects to respond to the same method call in different ways. It allows you to write code that works with objects of different classes through a common interface.

```python
from __future__ import annotations

class Dog:
    def speak(self) -> str:
        return "Woof!"

class Cat:
    def speak(self) -> str:
        return "Meow!"

class Duck:
    def speak(self) -> str:
        return "Quack!"

# Polymorphic function - works with any object that has a speak() method
def animal_conversation(animal) -> str:
    return animal.speak()

# All these work because each object implements speak()
dog = Dog()
cat = Cat()
duck = Duck()

print(animal_conversation(dog))   # "Woof!"
print(animal_conversation(cat))   # "Meow!"
print(animal_conversation(duck))  # "Quack!"
```

### 2. Inheritance-Based Polymorphism

When subclasses override parent class methods, you get polymorphic behavior through inheritance:

```python
from __future__ import annotations
from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class for shapes."""
    
    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate the perimeter of the shape."""
        pass

class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius
    
    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius

# Polymorphic function - works with any Shape subclass
def print_shape_info(shape: Shape) -> None:
    print(f"Area: {shape.area():.2f}")
    print(f"Perimeter: {shape.perimeter():.2f}")

# Both work because Rectangle and Circle inherit from Shape
rect = Rectangle(5, 3)
circle = Circle(4)

print_shape_info(rect)    # Works with Rectangle
print_shape_info(circle)  # Works with Circle
```

### 3. Duck Typing

Python's dynamic typing enables **duck typing**: "If it walks like a duck and quacks like a duck, it is a duck."

```python
from __future__ import annotations

# No inheritance relationship needed!
class TextFile:
    def read(self) -> str:
        return "Text file contents"
    
    def close(self) -> None:
        print("Closing text file")

class NetworkStream:
    def read(self) -> str:
        return "Network data"
    
    def close(self) -> None:
        print("Closing network connection")

class DatabaseConnection:
    def read(self) -> str:
        return "Database records"
    
    def close(self) -> None:
        print("Closing database connection")

# Polymorphic function using duck typing
def process_data_source(source) -> str:
    """Works with any object that has read() and close() methods."""
    data = source.read()
    source.close()
    return data

# All work because they implement the required interface
text = TextFile()
stream = NetworkStream()
db = DatabaseConnection()

process_data_source(text)   # Works!
process_data_source(stream) # Works!
process_data_source(db)     # Works!
```

### 4. Polymorphic Collections

Polymorphism shines when processing collections of mixed types:

```python
from __future__ import annotations
from typing import List

class PaymentMethod:
    """Base class for payment methods."""
    
    def process_payment(self, amount: float) -> dict:
        raise NotImplementedError

class CreditCard(PaymentMethod):
    def process_payment(self, amount: float) -> dict:
        return {"method": "credit_card", "amount": amount, "fee": amount * 0.025}

class PayPal(PaymentMethod):
    def process_payment(self, amount: float) -> dict:
        return {"method": "paypal", "amount": amount, "fee": amount * 0.029}

class BankTransfer(PaymentMethod):
    def process_payment(self, amount: float) -> dict:
        return {"method": "bank_transfer", "amount": amount, "fee": 0.0}

# Process payments polymorphically
def process_all_payments(payments: List[PaymentMethod], amount: float) -> List[dict]:
    """Process all payments - each uses its own implementation."""
    results = []
    for payment in payments:
        results.append(payment.process_payment(amount))
    return results

# Mixed collection works!
payment_methods: List[PaymentMethod] = [
    CreditCard(),
    PayPal(),
    BankTransfer(),
]

results = process_all_payments(payment_methods, 100.0)
```

### 5. Runtime Polymorphism with Type Checking

Sometimes you need polymorphic behavior with type-specific handling:

```python
from __future__ import annotations
from typing import Union

class Employee:
    """Base employee class."""
    
    def __init__(self, name: str, salary: float) -> None:
        self.name = name
        self.salary = salary
    
    def calculate_bonus(self) -> float:
        return self.salary * 0.05

class Manager(Employee):
    def calculate_bonus(self) -> float:
        return self.salary * 0.10

class Developer(Employee):
    def calculate_bonus(self) -> float:
        return self.salary * 0.08

class Intern(Employee):
    def calculate_bonus(self) -> float:
        return 500.0  # Fixed bonus

# Function that processes employees polymorphically
def calculate_payroll(employees: list[Employee]) -> dict[str, float]:
    """Calculate total compensation for all employees."""
    payroll = {}
    for emp in employees:
        bonus = emp.calculate_bonus()  # Polymorphic call!
        payroll[emp.name] = emp.salary + bonus
    return payroll
```

### 6. Polymorphic Functions with Protocols (Structural Subtyping)

Python 3.8+ supports Protocols for explicit duck typing:

```python
from __future__ import annotations
from typing import Protocol

class Drawable(Protocol):
    """Protocol for drawable objects."""
    
    def draw(self) -> str:
        """Return a string representation of the object."""
        ...

class Circle:
    def draw(self) -> str:
        return "Drawing a circle"

class Square:
    def draw(self) -> str:
        return "Drawing a square"

class Triangle:
    def draw(self) -> str:
        return "Drawing a triangle"

# Function accepts any object matching the Drawable protocol
def render_scene(objects: list[Drawable]) -> list[str]:
    return [obj.draw() for obj in objects]

# All work because they implement draw()
shapes = [Circle(), Square(), Triangle()]
render_scene(shapes)
```

---

## Common Patterns

### Strategy Pattern with Polymorphism

```python
from __future__ import annotations
from typing import Callable

class ShoppingCart:
    """Shopping cart with polymorphic discount strategies."""
    
    def __init__(self, discount_strategy: Callable[[float], float] | None = None) -> None:
        self.items: list[float] = []
        self.discount_strategy = discount_strategy or (lambda total: total)
    
    def add_item(self, price: float) -> None:
        self.items.append(price)
    
    def calculate_total(self) -> float:
        subtotal = sum(self.items)
        return self.discount_strategy(subtotal)

# Different discount strategies (polymorphic functions)
def no_discount(total: float) -> float:
    return total

def ten_percent_off(total: float) -> float:
    return total * 0.90

def bulk_discount(total: float) -> float:
    return total * 0.85 if total > 100 else total

# Usage
cart1 = ShoppingCart(ten_percent_off)
cart2 = ShoppingCart(bulk_discount)
```

---

## Common Mistakes

### 1. Breaking Polymorphism with Type Checking

```python
from __future__ import annotations

# WRONG - defeats polymorphism
def process_payment_wrong(payment) -> dict:
    if isinstance(payment, CreditCard):
        return payment.process_credit_card()
    elif isinstance(payment, PayPal):
        return payment.process_paypal()
    # ... more checks needed for each new type

# RIGHT - use polymorphism
def process_payment_right(payment: PaymentMethod) -> dict:
    return payment.process_payment()  # Polymorphic!
```

### 2. Inconsistent Interfaces

```python
from __future__ import annotations

# WRONG - inconsistent method signatures
class BadDog:
    def speak(self, volume: int) -> str:  # Different signature!
        return "Woof!" * volume

class BadCat:
    def speak(self) -> str:  # No volume parameter
        return "Meow!"

# RIGHT - consistent interface
class GoodDog:
    def speak(self, volume: int = 1) -> str:
        return "Woof!" * volume

class GoodCat:
    def speak(self, volume: int = 1) -> str:
        return "Meow!" * volume
```

### 3. Missing Abstract Methods

```python
from __future__ import annotations
from abc import ABC, abstractmethod

# WRONG - forgot @abstractmethod, allows incomplete implementations
class Shape(ABC):
    def area(self) -> float:  # Missing @abstractmethod!
        raise NotImplementedError

# RIGHT - enforce implementation
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        """Calculate area - must be implemented by subclasses."""
        pass
```

---

## Best Practices

1. **Prefer composition over inheritance** - Use polymorphism through interfaces, not just class hierarchies
2. **Keep interfaces minimal** - Don't force classes to implement methods they don't need
3. **Use type hints** - Make interfaces explicit with Protocols or ABCs
4. **Test with mocks** - Polymorphic code is easy to test with mock implementations
5. **Document expected interfaces** - Clear docstrings help others implement your interfaces

---

## Connection to Exercises

Today's exercises focus on practical polymorphism:

| Problem | Focus Area | Project Connection |
|---------|-----------|-------------------|
| 01. payment_runtime_dispatch | PaymentProcessor subclasses processed uniformly | Payment processing polymorphism |
| 02. report_renderer_dispatch | Different report formats rendered polymorphically | Shelter report generation |
| 03. media_handler_dispatch | Audio, Video, Image handlers with common interface | Different data handlers |
| 04. transport_simulator | Car, Bike, Bus in simulation with shared methods | Movement behaviors |
| 05. shape_area_dispatch | Calculate total area of mixed shapes | Batch operations |
| 06. employee_bonus_dispatch | Different employee types with bonus calculation | Staff salary calculations |
| 07. notification_system | Multiple notification channels | Shelter notification system |

---

## Connection to Weekly Project

Polymorphism is essential for the Animal Shelter Management System:

- **Animal Processing**: Process Dog, Cat, Bird, Rabbit uniformly through the Animal interface
- **Staff Operations**: All staff roles (Veterinarian, Caretaker, AdoptionCoordinator) work through StaffMember interface
- **Adoption Workflow**: Different adoption statuses are handled polymorphically
- **Report Generation**: Different report types (animal inventory, adoption stats, medical records) use common interfaces
- **Extensibility**: New animal types or staff roles can be added without changing existing code

The concepts practiced today enable the flexible, extensible architecture needed for the shelter system.

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify: `pytest week04_journey_v2/tests/day05/ -v`
2. Review any problems you found challenging
3. Preview Day 6: **Composition vs Inheritance** - Choosing the right relationship

---

## Summary

- **Polymorphism** means "many forms" - different objects responding to the same interface
- **Inheritance-based polymorphism** uses method overriding in class hierarchies
- **Duck typing** enables polymorphism without inheritance (if it quacks like a duck...)
- **Protocols** provide explicit structural subtyping in Python 3.8+
- Polymorphic code is **flexible** - add new types without changing existing code
- Polymorphic code is **testable** - easy to mock or stub implementations
