# Day 1: Classes and Objects

## Learning Objectives

By the end of this day, you will be able to:

1. Define classes using the `class` keyword
2. Create objects (instances) from classes
3. Understand and use the `__init__` constructor method
4. Use `self` to access instance attributes and methods
5. Define and call instance methods
6. Understand the difference between classes and objects
7. Create meaningful representations with `__str__` and `__repr__`

---

## Key Concepts

### 1. What is a Class?

A class is a blueprint for creating objects. It defines:
- **Attributes**: Data that each object will hold
- **Methods**: Functions that operate on the object's data

```python
class Dog:
    """A simple Dog class."""
    
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
    
    def bark(self) -> str:
        return f"{self.name} says woof!"
```

### 2. Creating Objects (Instances)

Objects are created by calling the class like a function:

```python
# Create instances
my_dog = Dog("Buddy", 3)
your_dog = Dog("Max", 5)

# Access attributes
print(my_dog.name)  # "Buddy"
print(your_dog.age)  # 5

# Call methods
print(my_dog.bark())  # "Buddy says woof!"
```

### 3. The `__init__` Constructor

`__init__` is a special method called when an object is created:

```python
class Person:
    def __init__(self, name: str, age: int) -> None:
        # 'self' refers to the new object being created
        self.name = name  # Create an instance attribute
        self.age = age
```

**Key points about `__init__`:**
- It runs automatically when you create an instance
- It's used to initialize object attributes
- It can have default parameter values
- It never returns a value (always returns `None`)

### 4. Understanding `self`

`self` is the first parameter of instance methods and refers to the current object:

```python
class Counter:
    def __init__(self) -> None:
        self.count = 0  # Each Counter instance has its own count
    
    def increment(self) -> None:
        self.count += 1  # Modify this instance's count
    
    def get_count(self) -> int:
        return self.count  # Return this instance's count

# Each object maintains its own state
c1 = Counter()
c2 = Counter()
c1.increment()
print(c1.get_count())  # 1
print(c2.get_count())  # 0 (unchanged)
```

**Important:** You don't pass `self` when calling methods - Python does it automatically.

### 5. Instance Attributes

Attributes store data unique to each instance:

```python
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
        self.area = width * height  # Can compute and store

rect = Rectangle(5.0, 3.0)
print(rect.width)   # 5.0
print(rect.height)  # 3.0
print(rect.area)    # 15.0
```

Attributes can be modified after creation:

```python
rect.width = 10.0
rect.area = rect.width * rect.height  # Must recalculate manually
```

### 6. Instance Methods

Methods are functions that belong to objects:

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount: float) -> float:
        """Add money to the account."""
        if amount > 0:
            self.balance += amount
        return self.balance
    
    def withdraw(self, amount: float) -> float | None:
        """Remove money if sufficient funds exist."""
        if 0 < amount <= self.balance:
            self.balance -= amount
            return self.balance
        return None
    
    def get_balance(self) -> float:
        """Return current balance."""
        return self.balance
```

### 7. String Representation: `__str__` and `__repr__`

These special methods control how objects are displayed:

```python
class Book:
    def __init__(self, title: str, author: str) -> None:
        self.title = title
        self.author = author
    
    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"'{self.title}' by {self.author}"
    
    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        return f"Book(title='{self.title}', author='{self.author}')"

book = Book("1984", "George Orwell")
print(book)           # Uses __str__: '1984' by George Orwell
print(repr(book))     # Uses __repr__: Book(title='1984', author='George Orwell')
```

| Method | Purpose | Used By |
|--------|---------|---------|
| `__str__` | Human-readable | `print()`, `str()` |
| `__repr__` | Unambiguous, for debugging | `repr()`, interactive shell |

**Best practice:** `__repr__` should ideally be valid Python code that could recreate the object.

### 8. Type Hints in Classes

Always use type hints for clarity:

```python
from __future__ import annotations

class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def distance_to(self, other: Point) -> float:
        """Calculate distance to another Point."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
```

---

## Common Mistakes

### 1. Forgetting `self` in Method Definitions

```python
# Wrong
class Person:
    def greet():  # Missing 'self'
        return "Hello"

# Right
class Person:
    def greet(self) -> str:
        return "Hello"
```

### 2. Forgetting `self.` When Accessing Attributes

```python
class Person:
    def __init__(self, name: str) -> None:
        name = name  # Wrong! Creates local variable, not attribute
        self.name = name  # Right!
```

### 3. Passing `self` When Calling Methods

```python
person = Person("Alice")
person.greet(self)  # Wrong! Don't pass self
person.greet()       # Right! Python passes self automatically
```

### 4. Confusing Class and Instance

```python
class Dog:
    def __init__(self, name: str) -> None:
        self.name = name

Dog.bark()  # Wrong! Dog is the class, not an instance
my_dog = Dog("Buddy")
my_dog.bark()  # Right! my_dog is an instance
```

### 5. Mutable Default Arguments

```python
# Wrong - shared list across all instances!
class Student:
    def __init__(self, name: str, grades: list[int] = []) -> None:
        self.grades = grades

# Right - creates new list for each instance
class Student:
    def __init__(self, name: str, grades: list[int] | None = None) -> None:
        self.grades = grades if grades is not None else []
```

### 6. Forgetting `__init__` Return Type

```python
# Wrong - __init__ should not return anything
class Foo:
    def __init__(self):
        return 42  # Type error!

# Right
class Foo:
    def __init__(self) -> None:
        pass  # Returns None implicitly
```

---

## Connection to Exercises

Today's exercises reinforce these concepts through practical problems:

| Problem | Skills Practiced |
|---------|------------------|
| 01. Person | Basic class, `__init__`, attributes |
| 02. BankAccount | Methods, validation, state management |
| 03. Rectangle | Computed properties, geometry |
| 04. Student | Collections as attributes, aggregations |
| 05. Counter | Simple state manipulation |
| 06. Temperature | Unit conversion, validation |
| 07. Book | String representation, data modeling |
| 08. ShoppingCart | Collection management, operations |
| 09. Point2D | Mathematical operations, distance |
| 10. Timer | Time tracking, state persistence |

---

## Weekly Project Connection

The Week 3 project is a **Basic E-commerce System**. Day 1's concepts are essential because:

- **Classes** define Product, Customer, and Order entities
- **Objects** represent actual products, customers, and orders
- **Attributes** store entity data (price, name, quantity)
- **Methods** define entity behaviors (add_to_cart, calculate_total)
- **`__str__`** provides readable output for users

---

## Quick Reference

```python
from __future__ import annotations

class MyClass:
    def __init__(self, value: int) -> None:
        self.value = value
    
    def method(self) -> int:
        return self.value * 2
    
    def __str__(self) -> str:
        return f"MyClass({self.value})"
    
    def __repr__(self) -> str:
        return f"MyClass(value={self.value})"

# Create instance
obj = MyClass(42)

# Access attributes
print(obj.value)

# Call methods
result = obj.method()

# String representation
print(str(obj))
print(repr(obj))
```

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify your solutions
2. Review any problems you found challenging
3. Preview Day 2: **Method Types (instance, class, static)**
