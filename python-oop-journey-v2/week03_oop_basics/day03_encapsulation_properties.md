# Day 3: Encapsulation and Properties

## Overview

Encapsulation is one of the fundamental principles of object-oriented programming. It involves bundling data (attributes) and the methods that operate on that data within a single unit (class), while controlling access to the internal state. Python's property system provides an elegant way to implement encapsulation without sacrificing the simplicity of attribute access.

## Learning Objectives

By the end of today, you will be able to:

- Understand the concept of encapsulation and why it matters in OOP
- Use name mangling and single underscore conventions for private/protected attributes
- Implement getters and setters using the `@property` decorator
- Create read-only, write-only, and computed properties
- Validate data within property setters to maintain object integrity
- Design classes with proper encapsulation boundaries

## Key Concepts

### 1. What is Encapsulation?

Encapsulation is the practice of hiding the internal implementation details of a class while exposing a clean public interface. Benefits include:

- **Data protection**: Prevents external code from corrupting internal state
- **Flexibility**: Internal implementation can change without affecting external code
- **Validation**: Ensures data integrity through controlled access
- **Abstraction**: Users interact with objects through well-defined interfaces

```python
class BankAccount:
    """Demonstrates encapsulation concepts."""
    
    def __init__(self, owner: str, balance: float) -> None:
        self.owner = owner          # Public attribute
        self._balance = balance     # Protected attribute (convention)
        self.__pin = "0000"         # Private attribute (name mangling)
```

### 2. Naming Conventions in Python

Python uses naming conventions rather than strict access control:

| Convention | Meaning | Access |
|------------|---------|--------|
| `name` | Public | Accessible everywhere |
| `_name` | Protected | Internal use, accessible but "hands off" |
| `__name` | Private | Name mangled to `_ClassName__name` |
| `__name__` | Dunder | Special Python methods |

```python
class Example:
    def __init__(self) -> None:
        self.public = "anyone can access"
        self._protected = "internal use only"
        self.__private = "name mangled"

obj = Example()
print(obj.public)        # ✓ Works
print(obj._protected)    # ✓ Works (but don't do it)
# print(obj.__private)   # ✗ AttributeError
print(obj._Example__private)  # ✓ Works (name mangling)
```

### 3. The @property Decorator

The `@property` decorator allows methods to be accessed like attributes:

```python
class Circle:
    def __init__(self, radius: float) -> None:
        self._radius = radius
    
    @property
    def radius(self) -> float:
        """Get the radius."""
        return self._radius
    
    @radius.setter
    def radius(self, value: float) -> None:
        """Set the radius with validation."""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @property
    def area(self) -> float:
        """Calculate area (read-only property)."""
        return 3.14159 * self._radius ** 2

# Usage
c = Circle(5)
print(c.radius)    # Access like an attribute (calls getter)
c.radius = 10      # Assignment calls setter
print(c.area)      # Computed property
# c.area = 100     # ✗ Error: read-only property
```

### 4. Property with Validation

Properties shine when you need to validate data:

```python
class Person:
    def __init__(self, name: str, age: int) -> None:
        self._name = name
        self._age = None
        self.age = age  # Uses setter for validation
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @property
    def age(self) -> int:
        return self._age
    
    @age.setter
    def age(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 0 or value > 150:
            raise ValueError("Age must be between 0 and 150")
        self._age = value
```

### 5. Read-Only Properties

Create read-only properties by omitting the setter:

```python
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self._width = width
        self._height = height
    
    @property
    def width(self) -> float:
        return self._width
    
    @property
    def height(self) -> float:
        return self._height
    
    @property
    def area(self) -> float:
        """Read-only computed property."""
        return self._width * self._height
    
    @property
    def perimeter(self) -> float:
        """Read-only computed property."""
        return 2 * (self._width + self._height)
```

### 6. Deleters and Deletion Protection

You can also control attribute deletion:

```python
class SecureValue:
    def __init__(self, value: str) -> None:
        self._value = value
    
    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, new_value: str) -> None:
        self._value = new_value
    
    @value.deleter
    def value(self) -> None:
        raise AttributeError("Cannot delete value - set to None instead")
```

### 7. Property as a Function

For more control, use `property()` as a function:

```python
class Temperature:
    def __init__(self, celsius: float = 0) -> None:
        self._celsius = celsius
    
    def get_fahrenheit(self) -> float:
        return (self._celsius * 9/5) + 32
    
    def set_fahrenheit(self, value: float) -> None:
        self._celsius = (value - 32) * 5/9
    
    fahrenheit = property(get_fahrenheit, set_fahrenheit)
```

### 8. Best Practices

**Do:**
- Use properties when you need to add behavior to attribute access
- Validate in setters to maintain object integrity
- Use read-only properties for computed values
- Keep the interface simple - users shouldn't know it's a property

**Don't:**
- Add setters for attributes that shouldn't change
- Use properties for expensive computations (without caching)
- Create properties that do more than get/set (violates principle of least surprise)
- Expose internal data structures directly

```python
# GOOD: Clean property interface
class Employee:
    def __init__(self, name: str, salary: float) -> None:
        self._name = name
        self._salary = salary
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def salary(self) -> float:
        return self._salary
    
    @salary.setter
    def salary(self, value: float) -> None:
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = value

# BAD: Exposes internal structure, no validation
class BadEmployee:
    def __init__(self, name: str, salary: float) -> None:
        self.name = name      # Public, no validation
        self.salary = salary  # Public, no validation
```

## Common Mistakes

### 1. Calling the Property as a Method

```python
# WRONG
print(circle.radius())  # TypeError: 'float' object is not callable

# CORRECT
print(circle.radius)    # Access as attribute
```

### 2. Forgetting self in Property Methods

```python
# WRONG
@property
def area():           # Missing self!
    return self._radius ** 2 * pi

# CORRECT
@property
def area(self) -> float:
    return self._radius ** 2 * pi
```

### 3. Recursive Setter

```python
# WRONG - infinite recursion
@radius.setter
def radius(self, value: float) -> None:
    self.radius = value  # Calls setter again!

# CORRECT
@radius.setter
def radius(self, value: float) -> None:
    self._radius = value  # Use private backing field
```

### 4. Breaking the Interface

```python
# WRONG - changing public interface
class Account:
    def set_balance(self, value: float) -> None:
        self._balance = value

# CORRECT - use property to maintain clean interface
class Account:
    @property
    def balance(self) -> float:
        return self._balance
    
    @balance.setter
    def balance(self, value: float) -> None:
        self._balance = value
```

## Connection to Exercises

Today's exercises build encapsulation skills progressively:

| Exercise | Concepts Practiced |
|----------|-------------------|
| 01. Bank Account Private | Private attributes, getters, setters |
| 02. Person with Age Validation | Property with validation |
| 03. Temperature Property | @property for unit conversion |
| 04. Product Price Validation | Property with business rules |
| 05. User Password Rules | Password validation with setter |
| 06. Rectangle Dimensions | @property for computed values |
| 07. Email Address | Email validation with @property.setter |
| 08. Savings Account Limits | Multiple properties with validation |
| 09. Circle Radius Validation | @property with type checking |
| 10. Gradebook | Private grades with calculated GPA |

## Key Takeaways

1. **Encapsulation protects data** - Control access to internal state
2. **Properties provide clean interfaces** - Method behavior with attribute syntax
3. **Validate in setters** - Maintain object integrity
4. **Use Python's naming conventions** - `_protected` and `__private`
5. **Read-only for computed values** - No setter means immutable from outside
6. **Keep it simple** - Users shouldn't need to know about properties
7. **Fail fast** - Raise errors immediately on invalid data

## Further Reading

- [Python Properties Documentation](https://docs.python.org/3/library/functions.html#property)
- [Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html)
- [Python Encapsulation Patterns](https://peps.python.org/pep-0008/)

## Time Estimate

- Reading: 30-40 minutes
- Exercises: 2.5-3.5 hours
- Review: 20 minutes
