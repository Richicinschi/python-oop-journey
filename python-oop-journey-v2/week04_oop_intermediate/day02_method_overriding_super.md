# Day 2: Method Overriding and `super()`

## Learning Objectives

By the end of this day, you will be able to:

1. Understand what method overriding is and when to use it
2. Use `super()` to call parent class methods
3. Extend parent class behavior in child classes
4. Properly initialize parent class attributes with `super().__init__()`
5. Know when to call `super()` and when to completely replace parent behavior
6. Understand the Method Resolution Order (MRO) basics

---

## Key Concepts

### 1. What is Method Overriding?

Method overriding occurs when a child class provides a specific implementation of a method that is already defined in its parent class.

```python
class Animal:
    def speak(self) -> str:
        return "Some sound"

class Dog(Animal):
    def speak(self) -> str:  # Overrides Animal.speak
        return "Woof!"

class Cat(Animal):
    def speak(self) -> str:  # Also overrides Animal.speak
        return "Meow!"
```

### 2. Using `super()` to Extend Parent Behavior

`super()` returns a proxy object that allows you to call methods on the parent class.

```python
class Vehicle:
    def __init__(self, brand: str) -> None:
        self.brand = brand
        self.wheels = 4
    
    def describe(self) -> str:
        return f"A {self.brand} vehicle with {self.wheels} wheels"

class ElectricCar(Vehicle):
    def __init__(self, brand: str, battery_capacity: float) -> None:
        super().__init__(brand)  # Call parent's __init__
        self.battery_capacity = battery_capacity  # Add new attribute
    
    def describe(self) -> str:
        # Extend parent's describe method
        base = super().describe()
        return f"{base} and a {self.battery_capacity}kWh battery"
```

### 3. The `super().__init__()` Pattern

Always call `super().__init__()` in child `__init__` methods to ensure parent initialization happens:

```python
class Base:
    def __init__(self, name: str) -> None:
        self.name = name
        self.created_at = datetime.now()

class Derived(Base):
    def __init__(self, name: str, extra: str) -> None:
        super().__init__(name)  # Initialize Base attributes
        self.extra = extra      # Initialize Derived-specific attributes
```

### 4. Complete Override vs. Extension

**Complete Override:** Replace parent behavior entirely
```python
class Parent:
    def calculate(self, x: int) -> int:
        return x * 2

class Child(Parent):
    def calculate(self, x: int) -> int:  # Completely different logic
        return x ** 2
```

**Extension with `super()`:** Add to parent behavior
```python
class Child(Parent):
    def calculate(self, x: int) -> int:
        parent_result = super().calculate(x)  # Get parent's result
        return parent_result + 10  # Extend it
```

### 5. Method Resolution Order (MRO)

Python uses the C3 linearization algorithm to determine method lookup order:

```python
class A:
    def method(self) -> str:
        return "A"

class B(A):
    def method(self) -> str:
        return f"B -> {super().method()}"

class C(A):
    def method(self) -> str:
        return f"C -> {super().method()}"

class D(B, C):
    def method(self) -> str:
        return f"D -> {super().method()}"

d = D()
print(d.method())  # D -> B -> C -> A
print(D.__mro__)   # Shows the method resolution order
```

### 6. Common Patterns with `super()`

**Template Method Pattern:**
```python
class DataProcessor:
    def process(self, data: str) -> str:
        cleaned = self.clean(data)
        validated = self.validate(cleaned)
        return self.transform(validated)
    
    def clean(self, data: str) -> str:
        return data.strip()
    
    def validate(self, data: str) -> str:
        if not data:
            raise ValueError("Empty data")
        return data
    
    def transform(self, data: str) -> str:
        return data.upper()

class JSONProcessor(DataProcessor):
    def clean(self, data: str) -> str:
        # Extend with super() or completely replace
        base = super().clean(data)
        return base.replace("'", '"')
    
    def transform(self, data: str) -> str:
        import json
        return json.dumps({"content": data})
```

**Cooperative Multiple Inheritance:**
```python
class Logged:
    def __init__(self) -> None:
        self.log: list[str] = []
        super().__init__()  # Important for MRO
    
    def log_action(self, action: str) -> None:
        self.log.append(action)

class Timestamped:
    def __init__(self) -> None:
        from datetime import datetime
        self.created_at = datetime.now()
        super().__init__()  # Important for MRO

class LoggedTimestampedObject(Logged, Timestamped):
    def __init__(self) -> None:
        super().__init__()  # Properly initializes both parents
```

---

## Common Mistakes

### 1. Forgetting to Call `super().__init__()`

```python
class Parent:
    def __init__(self, value: int) -> None:
        self.value = value

class Child(Parent):
    def __init__(self, value: int, extra: str) -> None:
        # WRONG: Parent's __init__ never called!
        self.extra = extra

# Correct:
class Child(Parent):
    def __init__(self, value: int, extra: str) -> None:
        super().__init__(value)  # Initialize parent first
        self.extra = extra
```

### 2. Wrong Argument Order in `super()`

```python
# Old Python 2 style (still works but not needed in Python 3)
super(Child, self).__init__()

# Python 3 style (preferred)
super().__init__()
```

### 3. Not Using Parent's Return Value

```python
class Parent:
    def compute(self, x: int) -> int:
        return x * 2

class Child(Parent):
    def compute(self, x: int) -> int:
        super().compute(x)  # WRONG: Result is lost!
        return x + 10

# Correct:
class Child(Parent):
    def compute(self, x: int) -> int:
        parent_result = super().compute(x)
        return parent_result + 10
```

### 4. Infinite Recursion with `super()`

```python
class A:
    def method(self) -> str:
        return "A"

class B(A):
    def method(self) -> str:
        # WRONG if C also does this - infinite loop!
        return f"B -> {super().method()}"

class C(A):
    def method(self) -> str:
        # This would cause issues if improperly used
        return f"C -> {super().method()}"
```

---

## Best Practices

1. **Always call `super().__init__()`** in child classes unless you have a specific reason not to
2. **Accept and forward `*args` and `**kwargs`** for flexible initialization:
   ```python
   def __init__(self, extra: str, *args: Any, **kwargs: Any) -> None:
       super().__init__(*args, **kwargs)
   ```
3. **Document when you're overriding** with a docstring comment
4. **Use `super()` to extend, direct replacement to change** behavior completely
5. **Check `__mro__`** when debugging multiple inheritance issues

---

## Connection to Today's Exercises

Today's exercises build a progression of `super()` usage:

| Exercise | `super()` Pattern | Project Connection |
|----------|-------------------|-------------------|
| 01. Notification Services | Override `send()`, share logging via `super()` | Staff notification system |
| 02. Payment Methods | `super().__init__()` for common attributes | Payment processing in adoptions |
| 03. Shipping Options | Base + extension pattern | Cost calculations |
| 04. Media Player Hierarchy | Extend behavior, call parent methods | Media handling patterns |
| 05. Report Generators | Template method pattern | Shelter reports |
| 06. Game Character Actions | Common + specific via `super()` | Character/staff actions |

Each exercise demonstrates a different pattern of method overriding and `super()` usage that you'll encounter in real-world code.

---

## Connection to Weekly Project

The Week 4 project (Animal Shelter Management System) uses method overriding extensively:

- **Animals**: Different types override `make_sound()`, `calculate_care_cost()`, and `get_care_instructions()`
- **Staff roles**: Override `perform_duties()` with base + specific patterns
- **Initialization**: All classes use `super().__init__()` to ensure proper parent setup
- **Template method**: The adoption workflow uses `super()` for common validation logic

Mastering `super()` today prepares you for clean, maintainable inheritance in the project.

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify: `pytest week04_oop_intermediate/tests/day02/ -v`
2. Review any problems you found challenging
3. Preview Day 3: **Abstract Base Classes** - Define interfaces that must be implemented
