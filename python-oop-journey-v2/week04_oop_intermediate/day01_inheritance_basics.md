# Day 1: Inheritance Basics

## Learning Objectives

By the end of this day, you will be able to:

1. Understand what inheritance is and why it's useful
2. Create base (parent) classes and derived (child) classes
3. Use `super()` to call parent class methods
4. Override methods in child classes
5. Use `isinstance()` and `issubclass()` for type checking
6. Understand the Method Resolution Order (MRO)
7. Know when to use inheritance vs composition

---

## Key Concepts

### 1. What is Inheritance?

Inheritance allows a class to inherit attributes and methods from another class. It represents an "is-a" relationship.

```python
class Animal:  # Base class (parent)
    def __init__(self, name: str) -> None:
        self.name = name
    
    def speak(self) -> str:
        return f"{self.name} makes a sound"

class Dog(Animal):  # Derived class (child)
    def speak(self) -> str:  # Override parent method
        return f"{self.name} says woof!"

class Cat(Animal):  # Another derived class
    def speak(self) -> str:
        return f"{self.name} says meow!"

# Usage
dog = Dog("Buddy")
cat = Cat("Whiskers")
print(dog.speak())  # "Buddy says woof!"
print(cat.speak())  # "Whiskers says meow!"
```

### 2. Base Class and Derived Class

| Term | Description | Example |
|------|-------------|---------|
| Base Class | The class being inherited from | `Vehicle` |
| Derived Class | The class that inherits | `Car`, `Truck` |
| Parent Class | Same as base class | `Vehicle` |
| Child Class | Same as derived class | `Car`, `Truck` |
| Superclass | Same as base/parent class | `Vehicle` |
| Subclass | Same as derived/child class | `Car`, `Truck` |

### 3. Using `super()`

`super()` allows you to call methods from the parent class:

```python
class Vehicle:
    def __init__(self, brand: str, year: int) -> None:
        self.brand = brand
        self.year = year
        self.odometer = 0

class Car(Vehicle):
    def __init__(self, brand: str, year: int, doors: int) -> None:
        super().__init__(brand, year)  # Call parent's __init__
        self.doors = doors  # Add car-specific attribute
```

**Why use `super()`?**
- Avoids hardcoding the parent class name
- Properly handles multiple inheritance (MRO)
- Makes code more maintainable

### 4. Method Overriding

Child classes can override parent methods to provide specialized behavior:

```python
class Shape:
    def area(self) -> float:
        raise NotImplementedError("Subclasses must implement area()")
    
    def describe(self) -> str:
        return f"This is a shape"

class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
    
    def area(self) -> float:  # Override
        return self.width * self.height
    
    def describe(self) -> str:  # Override with extension
        base = super().describe()  # Call parent
        return f"{base} with width={self.width}, height={self.height}"
```

### 5. Inheriting and Extending

You can add new methods and attributes in child classes:

```python
class Employee:
    def __init__(self, name: str, salary: float) -> None:
        self.name = name
        self.salary = salary
    
    def get_details(self) -> str:
        return f"{self.name}: ${self.salary}"

class Manager(Employee):
    def __init__(self, name: str, salary: float, department: str) -> None:
        super().__init__(name, salary)
        self.department = department
        self.reports: list[Employee] = []  # New attribute
    
    def add_report(self, employee: Employee) -> None:
        self.reports.append(employee)
    
    def get_details(self) -> str:  # Override
        base = super().get_details()
        return f"{base}, Dept: {self.department}, Reports: {len(self.reports)}"
```

### 6. Type Checking: `isinstance()` and `issubclass()`

```python
class Animal:
    pass

class Dog(Animal):
    pass

class Cat(Animal):
    pass

# isinstance() - check if an object is an instance of a class
dog = Dog()
print(isinstance(dog, Dog))      # True
print(isinstance(dog, Animal))   # True (inheritance)
print(isinstance(dog, Cat))      # False

# issubclass() - check if a class is a subclass of another
print(issubclass(Dog, Animal))   # True
print(issubclass(Dog, Dog))      # True (a class is a subclass of itself)
print(issubclass(Animal, Dog))   # False
```

### 7. Method Resolution Order (MRO)

MRO defines the order in which Python looks for methods:

```python
class A:
    def method(self) -> str:
        return "A"

class B(A):
    def method(self) -> str:
        return "B"

class C(A):
    def method(self) -> str:
        return "C"

class D(B, C):  # Multiple inheritance
    pass

d = D()
print(d.method())  # "B" (follows MRO: D -> B -> C -> A)

# View MRO
print(D.__mro__)  # (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

### 8. Accessing Parent Methods Directly

Sometimes you need to call a specific parent method:

```python
class Parent:
    def greet(self) -> str:
        return "Hello from Parent"

class Child(Parent):
    def greet(self) -> str:
        parent_greeting = Parent.greet(self)  # Direct parent call
        return f"{parent_greeting} and Child"
```

**Note:** Prefer `super()` over direct parent calls in most cases.

---

## Common Mistakes

### 1. Forgetting to Call Parent `__init__`

```python
# Wrong
class Car(Vehicle):
    def __init__(self, brand: str, year: int, doors: int) -> None:
        self.doors = doors  # Missing super().__init__()!

# Right
class Car(Vehicle):
    def __init__(self, brand: str, year: int, doors: int) -> None:
        super().__init__(brand, year)
        self.doors = doors
```

### 2. Incorrect `super()` Usage

```python
# Wrong - super() is a function, needs parentheses
class Child(Parent):
    def __init__(self) -> None:
        super.__init__()  # Missing () after super

# Right
class Child(Parent):
    def __init__(self) -> None:
        super().__init__()
```

### 3. Forgetting `self` When Calling Parent Directly

```python
# Wrong
class Child(Parent):
    def method(self) -> str:
        return Parent.greet()  # Missing self

# Right
class Child(Parent):
    def method(self) -> str:
        return Parent.greet(self)  # Need self
        # Or better: return super().greet()
```

### 4. Confusing `isinstance()` and `issubclass()`

```python
# Wrong - isinstance takes an instance first
dog = Dog()
print(isinstance(Dog, dog))  # Wrong order!

# Right
print(isinstance(dog, Dog))  # instance, class
print(issubclass(Dog, Animal))  # class, class
```

### 5. Overriding Without Calling super() When Needed

```python
# Problematic - might miss important parent setup
class LoggingList(list):
    def __init__(self) -> None:
        self.log: list[str] = []
        # Forgot super().__init__() - list not properly initialized!

# Better
class LoggingList(list):
    def __init__(self, iterable: list | None = None) -> None:
        super().__init__(iterable or [])
        self.log: list[str] = []
```

### 6. Using Inheritance for Code Sharing Only

```python
# Wrong - "is-a" relationship violated
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

class Square(Rectangle):  # Problematic! A square can't change width independently
    def __init__(self, side: float) -> None:
        super().__init__(side, side)

# Better - use composition or rethink design
class Square:
    def __init__(self, side: float) -> None:
        self._side = side
    
    @property
    def width(self) -> float:
        return self._side
    
    @property
    def height(self) -> float:
        return self._side
```

---

## Connection to Exercises

Today's exercises reinforce inheritance concepts through practical hierarchies:

| Problem | Skills Practiced |
|---------|------------------|
| 01. Vehicle Hierarchy | Basic inheritance, overriding |
| 02. Employee Hierarchy | `super()`, extending behavior |
| 03. Animal Kingdom | Multiple subclasses, polymorphism |
| 04. Bank Account Types | Method overriding, type-specific logic |
| 05. Shape Hierarchy | Abstract methods, area calculations |
| 06. Book and EBook | Media inheritance, format differences |
| 07. Student and Graduate | Academic hierarchy, thesis handling |
| 08. Smart Devices | IoT inheritance, device-specific features |

---

## Weekly Project Connection

The Week 4 project is the **Animal Shelter Management System**. Day 1's concepts are essential because:

- **Animal base class** defines common attributes (name, age, health_status) that all animals share
- **Derived classes** (Dog, Cat, Bird, Rabbit) implement type-specific behaviors
- **Method overriding** allows custom `make_sound()` and `get_care_instructions()` for each animal type
- **`isinstance()`** helps validate animal types in the adoption system
- **Inheritance** creates a clean hierarchy where all animals can be processed uniformly

---

## Quick Reference

```python
from __future__ import annotations

# Base class
class Vehicle:
    def __init__(self, brand: str) -> None:
        self.brand = brand
    
    def describe(self) -> str:
        return f"A vehicle by {self.brand}"

# Derived class
class Car(Vehicle):
    def __init__(self, brand: str, doors: int) -> None:
        super().__init__(brand)  # Call parent init
        self.doors = doors
    
    def describe(self) -> str:  # Override
        base = super().describe()
        return f"{base} with {self.doors} doors"

# Type checking
car = Car("Toyota", 4)
isinstance(car, Car)      # True
isinstance(car, Vehicle)  # True
issubclass(Car, Vehicle)  # True
```

---

## Connection to Exercises (Detailed)

| Exercise | Concept Focus | Project Connection |
|----------|---------------|-------------------|
| 01. Vehicle Hierarchy | Basic inheritance, method overriding | Like Animal → Dog/Cat/Bird |
| 02. Employee Hierarchy | `super()`, extending behavior | Staff roles will use this pattern |
| 03. Animal Kingdom | Multiple subclasses, polymorphism | Core pattern for animal types |
| 04. Bank Account Types | Method overriding with type logic | Different account types like different animals |
| 05. Shape Hierarchy | Abstract concepts, area calculations | Leads into Day 3 ABCs |
| 06. Book and EBook | Media inheritance, format differences | Shows when inheritance fits |
| 07. Student and Graduate | Academic hierarchy | Hierarchical data modeling |
| 08. Smart Devices | IoT inheritance, device features | Complex inheritance patterns |

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify your solutions: `pytest week04_oop_intermediate/tests/day01/ -v`
2. Review any problems you found challenging
3. Preview Day 2: **Method Overriding and super()** - Essential for proper inheritance initialization
