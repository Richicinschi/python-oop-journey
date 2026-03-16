# Week 3: OOP Basics 🎯

> **CRITICAL WEEK**: This is your **first week of Object-Oriented Programming**—the transition from procedural to object-oriented thinking. Everything you learn here enables every advanced OOP concept that follows.

**Week Goal**: Learn to model real-world entities using classes, methods, and encapsulation.

## 🚀 Start Here

New to OOP? Begin your journey:

1. **Read**: Start with [Day 1: Classes and Objects](day01_classes_objects.md) (15-20 min)
2. **Code**: Open your first exercise: `exercises/day01/problem_01_person.py`
3. **Test**: Run `pytest week03_oop_basics/tests/day01/test_problem_01_person.py -v`
4. **Project**: Review the [E-commerce System](project/README.md) to see where this week leads

> **Pro tip**: Don't skip Day 1 theory—understanding `self` and `__init__` unlocks everything else.

---

## Week Objective

By the end of this week, you will:
- Create classes and instantiate objects
- Understand instance, class, and static methods
- Apply encapsulation using private attributes and properties
- Implement magic methods for natural object behavior
- Use composition and aggregation to build complex systems
- Design classes with single responsibility

## Prerequisites

- Completion of Weeks 1-2: Python Fundamentals and Advanced Fundamentals
- Understanding of functions, modules, and file handling
- Familiarity with testing using pytest

## Daily Topics

| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | Classes and Objects | 10 | Easy-Medium |
| Day 2 | Method Types (Instance, Class, Static) | 10 | Medium |
| Day 3 | Encapsulation and Properties | 10 | Medium |
| Day 4 | Magic Methods (Dunder Methods) | 8 | Medium |
| Day 5 | Composition and Aggregation | 8 | Medium |
| Day 6 | Class Design Best Practices (Stretch) | 6 | Medium-Hard |*

*Day 6 is bonus content for learners who want extra practice with design principles.

## File Structure

```
week03_oop_basics/
├── README.md                    # This file
├── day01_classes_objects.md     # Day 1 theory
├── day02_method_types.md        # Day 2 theory
├── day03_encapsulation_properties.md    # Day 3 theory
├── day04_magic_methods.md       # Day 4 theory
├── day05_composition_aggregation.md     # Day 5 theory
├── day06_class_design.md        # Day 6 theory
├── exercises/                   # Your working area
│   ├── day01/                   # Day 1 exercises (10 files)
│   ├── day02/                   # Day 2 exercises (10 files)
│   ├── day03/                   # Day 3 exercises (10 files)
│   ├── day04/                   # Day 4 exercises (8 files)
│   ├── day05/                   # Day 5 exercises (8 files)
│   └── day06/                   # Day 6 exercises (6 files)
├── solutions/                   # Reference solutions
│   ├── day01/                   # Day 1 solutions
│   ├── day02/                   # Day 2 solutions
│   ├── day03/                   # Day 3 solutions
│   ├── day04/                   # Day 4 solutions
│   ├── day05/                   # Day 5 solutions
│   └── day06/                   # Day 6 solutions
├── tests/                       # Test suite
│   ├── day01/                   # Day 1 tests
│   ├── day02/                   # Day 2 tests
│   ├── day03/                   # Day 3 tests
│   ├── day04/                   # Day 4 tests
│   ├── day05/                   # Day 5 tests
│   └── day06/                   # Day 6 tests
└── project/                     # Weekly project
    ├── README.md                # Project documentation
    ├── starter/                 # Starter code
    ├── reference_solution/      # Complete solution
    └── tests/                   # Project tests
```

## How to Work Through This Week

### Daily Workflow

1. **Read the theory** document for the day (15-20 minutes)
2. **Attempt exercises** in order:
   - Problems 01-03: Warm-up/foundational
   - Problems 04-06: Core practice
   - Problems 07-08: Harder application
   - Problems 09-10: Stretch/bonus (if available)
3. **Check solutions** only when stuck
4. **Run tests** to verify your work

---

## ✅ How to Check Your Work

Follow this verification path to build confidence:

### Step 1: Manual Verification
Run the example usage in each exercise file:
```python
# In a Python shell or add to the bottom of your file:
if __name__ == "__main__":
    # Test your implementation
    obj = YourClass("test")
    print(obj)  # Does it look right?
```

### Step 2: Run the Tests
```bash
# Test a single problem
pytest week03_oop_basics/tests/day01/test_problem_01_person.py -v

# Test a full day
pytest week03_oop_basics/tests/day01/ -v

# Test all Week 3
pytest week03_oop_basics/tests/ -v
```

### Step 3: Compare with Reference Solution
Only after you've made a real attempt:
```bash
# Look at the reference solution
week03_oop_basics/solutions/day01/problem_01_person.py
```

### Step 4: Connect to the Project
After each day, think about how the concepts apply to the [E-commerce System](project/README.md):
- Day 1: How are Product, User, and Order classes structured?
- Day 2: Which methods should be `@staticmethod` vs `@classmethod`?
- Day 3: Where do properties protect data in the e-commerce system?

> **Anti-cheating rule**: Don't look at reference solutions until you've attempted the problem or are genuinely stuck for 15+ minutes.

## Weekly Project: Basic E-commerce System

Build a complete e-commerce system using OOP principles:
- **Product** class with validation and magic methods
- **User** class with shopping cart composition
- **ShoppingCart** with item management
- **Order** with status transitions
- **Inventory** for stock management

See [project/README.md](project/README.md) for full requirements.

## Key Concepts by Day

### Day 1: Classes and Objects
- Class definition with `class` keyword
- `__init__` constructor method
- Instance attributes and `self`
- Creating objects (instantiation)
- Instance methods for behavior
- Object state management

### Day 2: Method Types
- Instance methods (require `self`)
- Class methods with `@classmethod` and `cls`
- Static methods with `@staticmethod`
- Factory methods for alternative constructors
- Use cases for each method type
- Class state with class attributes

### Day 3: Encapsulation and Properties
- Private attributes with single underscore `_`
- Name mangling with double underscore `__`
- Property decorators `@property`, `@<name>.setter`
- Validation in setters
- Read-only properties (no setter)
- Data encapsulation principles

### Day 4: Magic Methods
- String representation: `__str__` and `__repr__`
- Comparison methods: `__eq__`, `__lt__`, `__gt__`, etc.
- Numeric operations: `__add__`, `__sub__`, `__mul__`, etc.
- Container methods: `__len__`, `__getitem__`, `__iter__`
- Context managers: `__enter__`, `__exit__`
- Making objects Pythonic

### Day 5: Composition and Aggregation
- Composition: "has-a" relationship (strong ownership)
- Aggregation: "has-a" relationship (weak reference)
- Building complex objects from simple parts
- Avoiding deep inheritance hierarchies
- Delegation pattern
- Lifecycle management

### Day 6: Class Design
- Single Responsibility Principle
- Separation of concerns
- Designing for testability
- Interface design
- Documentation and docstrings
- Refactoring procedural code to OOP

## Tips for Success

1. **Think in objects** - Model real-world entities as classes
2. **Encapsulate aggressively** - Keep internal state private
3. **Use properties** - They provide flexibility without breaking the interface
4. **Leverage magic methods** - Make your objects feel like built-in types
5. **Prefer composition over inheritance** - It's more flexible and testable
6. **Write tests early** - OOP benefits greatly from test-driven development

## Common Pitfalls

- **Mutable default arguments** - Use `None` as default for mutable types
- **Forgetting `self`** - Instance methods need `self` as first parameter
- **Public attributes** - Use private attributes with properties instead
- **Tight coupling** - Classes shouldn't know too much about each other
- **Getter/setter bloat** - Not every attribute needs a property
- **Magic method overload** - Don't implement dunder methods you don't need

## Common OOP Debugging Issues

### 1. Forgetting `self` in Method Definitions
**Problem:**
```python
def get_balance():  # Missing self!
    return self.balance  # AttributeError
```

**Fix:**
```python
def get_balance(self):  # Include self
    return self._balance
```

### 2. Modifying Class Instead of Instance Attributes
**Problem:**
```python
class BankAccount:
    balance = 0  # Class attribute - shared by ALL instances!
    
    def __init__(self):
        pass  # Not setting instance attribute
```

**Fix:**
```python
class BankAccount:
    def __init__(self):
        self._balance = 0  # Instance attribute - unique to each object
```

### 3. `__init__` Not Returning None
**Problem:**
```python
def __init__(self, value):
    return value  # TypeError: __init__() should return None
```

**Fix:**
```python
def __init__(self, value):
    self._value = value  # Never return from __init__
```

### 4. Property Getter/Setter Confusion
**Problem:**
```python
@property
def balance(self):
    return self.balance  # Recursion! Calls itself

@balance.setter
def balance(self, value):
    self.balance = value  # Recursion! Calls itself
```

**Fix:**
```python
@property
def balance(self):
    return self._balance  # Use private backing field

@balance.setter
def balance(self, value):
    self._balance = value  # Use private backing field
```

### 5. Class Method vs Instance Method Confusion
**Problem:**
```python
class MyClass:
    def method(cls):  # Missing @classmethod
        return cls.value
    
    @classmethod
    def other_method(self):  # Wrong parameter name
        return self.value
```

**Fix:**
```python
class MyClass:
    def method(self):  # Instance method
        return self._value
    
    @classmethod
    def other_method(cls):  # Class method uses cls
        return cls._class_value
```

### 6. AttributeError Because Attribute Not Initialized
**Problem:**
```python
def __init__(self, name):
    name = name  # Creates local variable, not attribute!

def greet(self):
    return f"Hello {self.name}"  # AttributeError: name not set
```

**Fix:**
```python
def __init__(self, name):
    self._name = name  # Use self. to create attribute

def greet(self):
    return f"Hello {self._name}"  # Now works!
```

### 7. Magic Method Signature Mismatch
**Problem:**
```python
def __eq__(self, other):  # Should accept any object
    return self.value == other.value  # Fails if other is not same type
```

**Fix:**
```python
def __eq__(self, other: object) -> bool:
    if not isinstance(other, MyClass):
        return NotImplemented
    return self._value == other._value
```

## Next Week

Week 4 introduces OOP Intermediate concepts:
- Inheritance and method overriding
- Multiple inheritance and MRO
- Abstract base classes
- Polymorphism
- Interfaces and protocols
- SOLID principles deep dive

---

**Total Exercises**: 58 problems (10 + 10 + 10 + 8 + 8 + 6 + 2 project files)  
**Estimated Time**: 6-18 hours depending on pace (add 2-3 hours for Day 6)
