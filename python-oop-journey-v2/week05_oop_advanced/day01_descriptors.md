# Day 1: Descriptors

## Learning Objectives

By the end of this day, you will be able to:

1. Understand what descriptors are and how they work
2. Implement the descriptor protocol (`__get__`, `__set__`, `__delete__`)
3. Create validated and type-checked attributes using descriptors
4. Build lazy evaluation and caching mechanisms
5. Implement observable and logged attributes
6. Understand the difference between data and non-data descriptors
7. Know when to use descriptors vs. properties

---

## Key Concepts

### 1. What are Descriptors?

A descriptor is any object that implements at least one of the descriptor protocol methods: `__get__`, `__set__`, or `__delete__`. Descriptors provide a way to customize attribute access.

```python
from __future__ import annotations


class Validator:
    """A descriptor that validates values."""
    
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.name = ""
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Called when descriptor is assigned to a class attribute."""
        self.name = name
        self.storage_name = f"_{name}"
    
    def __get__(self, instance: object | None, owner: type) -> int | Validator:
        """Called when accessing the attribute."""
        if instance is None:
            return self
        return getattr(instance, self.storage_name, None)
    
    def __set__(self, instance: object, value: int) -> None:
        """Called when setting the attribute."""
        if not isinstance(value, int):
            raise TypeError(f"{self.name} must be an integer")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"{self.name} must be between {self.min_value} and {self.max_value}"
            )
        setattr(instance, self.storage_name, value)


class Person:
    """Uses descriptors for validation."""
    
    age = Validator(0, 150)  # Descriptor instance
    score = Validator(0, 100)  # Another descriptor instance
    
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age  # Triggers Validator.__set__


# Usage
person = Person("Alice", 30)
print(person.age)  # 30 (triggers Validator.__get__)
person.age = 31    # Triggers Validator.__set__
```

### 2. The Descriptor Protocol

| Method | Purpose | When Called |
|--------|---------|-------------|
| `__get__(self, instance, owner)` | Get attribute value | `obj.attr` or `Class.attr` |
| `__set__(self, instance, value)` | Set attribute value | `obj.attr = value` |
| `__delete__(self, instance)` | Delete attribute | `del obj.attr` |
| `__set_name__(self, owner, name)` | Capture attribute name | At class creation time |

### 3. Data vs Non-Data Descriptors

**Data descriptors** implement `__set__` (and optionally `__delete__`):
- Take precedence over instance `__dict__`
- Always intercept attribute access
- Examples: `property` with setter, custom validators

**Non-data descriptors** only implement `__get__`:
- Instance `__dict__` takes precedence
- Allow instance to override class attribute
- Examples: methods, `classmethod`, `staticmethod`

```python
from __future__ import annotations


# Non-data descriptor
class NonDataDescriptor:
    def __get__(self, instance: object | None, owner: type) -> str:
        return "from descriptor"


class DataDescriptor:
    """Data descriptor with __set__."""
    
    def __get__(self, instance: object | None, owner: type) -> str:
        return "from data descriptor"
    
    def __set__(self, instance: object, value: str) -> None:
        raise AttributeError("Cannot set this attribute")


class MyClass:
    non_data = NonDataDescriptor()
    data = DataDescriptor()


obj = MyClass()

# Non-data: instance dict can override
obj.non_data = "from instance"
print(obj.non_data)  # "from instance"
print(MyClass.non_data)  # "from descriptor"

# Data: descriptor always wins
obj.data = "from instance"  # Raises AttributeError!
```

### 4. Storage Strategies

Descriptors need to store values somewhere. Common strategies:

**Strategy 1: Instance dictionary with mangled name**
```python
def __set_name__(self, owner: type, name: str) -> None:
    self.storage_name = f"_{name}"

def __get__(self, instance: object | None, owner: type) -> Any:
    if instance is None:
        return self
    return getattr(instance, self.storage_name, None)

def __set__(self, instance: object, value: Any) -> None:
    setattr(instance, self.storage_name, value)
```

**Strategy 2: External storage with WeakKeyDictionary**
```python
from weakref import WeakKeyDictionary

class Descriptor:
    def __init__(self) -> None:
        self.data: WeakKeyDictionary = WeakKeyDictionary()
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        return self.data.get(instance)
    
    def __set__(self, instance: object, value: Any) -> None:
        self.data[instance] = value
```

### 5. Lazy Evaluation with Descriptors

```python
from __future__ import annotations

import time
from typing import Callable, Any


class LazyProperty:
    """A property that is computed once and cached."""
    
    def __init__(self, func: Callable[[Any], Any]) -> None:
        self.func = func
        self.name = func.__name__
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        
        # Compute the value
        value = self.func(instance)
        
        # Cache in instance dict (bypasses descriptor on next access)
        setattr(instance, self.name, value)
        
        return value


class ExpensiveObject:
    """Demonstrates lazy evaluation."""
    
    def __init__(self, data: list[int]) -> None:
        self.data = data
    
    @LazyProperty
    def expensive_computation(self) -> int:
        """This is only computed once."""
        time.sleep(0.1)  # Simulate expensive operation
        return sum(x * x for x in self.data)


# Usage
obj = ExpensiveObject([1, 2, 3, 4, 5])
print(obj.expensive_computation)  # Takes ~0.1s, computes 55
print(obj.expensive_computation)  # Instant - from cache
```

### 6. Observable Attributes

```python
from __future__ import annotations

from typing import Callable, Any


class Observable:
    """Descriptor that notifies observers on change."""
    
    def __init__(self) -> None:
        self.callbacks: dict[int, list[Callable[[Any, Any], None]]] = {}
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage_name = f"_{name}"
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage_name, None)
    
    def __set__(self, instance: object, value: Any) -> None:
        old_value = getattr(instance, self.storage_name, None)
        setattr(instance, self.storage_name, value)
        
        # Notify observers
        callbacks = self.callbacks.get(id(instance), [])
        for callback in callbacks:
            callback(old_value, value)
    
    def add_callback(
        self, 
        instance: object, 
        callback: Callable[[Any, Any], None]
    ) -> None:
        """Add a callback to be called when value changes."""
        if id(instance) not in self.callbacks:
            self.callbacks[id(instance)] = []
        self.callbacks[id(instance)].append(callback)


class StockPrice:
    """Stock with observable price."""
    
    price = Observable()
    
    def __init__(self, symbol: str, price: float) -> None:
        self.symbol = symbol
        self.price = price
    
    def on_price_change(
        self, 
        callback: Callable[[float, float], None]
    ) -> None:
        """Register a callback for price changes."""
        type(self).price.add_callback(self, callback)


# Usage
stock = StockPrice("AAPL", 150.0)
stock.on_price_change(lambda old, new: print(f"Price: {old} -> {new}"))
stock.price = 155.0  # Prints: Price: 150.0 -> 155.0
```

### 7. Read-Only Attributes

```python
from __future__ import annotations


class ReadOnly:
    """A write-once, read-only descriptor."""
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage_name = f"_{name}_set"
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage_name[1:-4], None)
    
    def __set__(self, instance: object, value: Any) -> None:
        if hasattr(instance, self.storage_name):
            raise AttributeError(f"Cannot modify read-only attribute '{self.name}'")
        setattr(instance, self.storage_name, True)
        setattr(instance, f"_{self.name}", value)


class ImmutableConfig:
    """Configuration with immutable values."""
    
    api_key = ReadOnly()
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key  # Can be set once


# Usage
config = ImmutableConfig("secret123")
print(config.api_key)  # "secret123"
config.api_key = "new"  # Raises AttributeError!
```

---

## Common Mistakes

### 1. Forgetting `instance is None` Check

```python
# Wrong
class Descriptor:
    def __get__(self, instance: object | None, owner: type) -> Any:
        return instance._value  # Crashes on Class.attr access!

# Right
class Descriptor:
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self  # Return descriptor when accessed on class
        return instance._value
```

### 2. Name Collision in Storage

```python
# Wrong - all instances share the same value!
class BadDescriptor:
    def __init__(self) -> None:
        self.value = None
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        return self.value
    
    def __set__(self, instance: object, value: Any) -> None:
        self.value = value  # All instances share this!

# Right - store per-instance
class GoodDescriptor:
    def __set_name__(self, owner: type, name: str) -> None:
        self.storage_name = f"_{name}"
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage_name, None)
    
    def __set__(self, instance: object, value: Any) -> None:
        setattr(instance, self.storage_name, value)
```

### 3. Infinite Recursion in `__get__`

```python
# Wrong - accessing self.name triggers __get__ again!
class BadDescriptor:
    def __get__(self, instance: object | None, owner: type) -> Any:
        return getattr(instance, self.name)  # Recursion!

# Right - use storage_name with underscore
class GoodDescriptor:
    def __set_name__(self, owner: type, name: str) -> None:
        self.storage_name = f"_{name}"
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        return getattr(instance, self.storage_name, None)
```

### 4. Not Implementing `__set_name__`

```python
# Works but fragile
class Descriptor:
    def __init__(self, name: str) -> None:
        self.name = name

class MyClass:
    attr = Descriptor("attr")  # Have to repeat name!

# Better - automatic name capture
class BetterDescriptor:
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

class BetterClass:
    attr = BetterDescriptor()  # Name captured automatically
```

---

## Connection to Exercises

Today's exercises explore different descriptor patterns:

| Problem | Skills Practiced |
|---------|------------------|
| 01. Validated Attribute | Basic descriptor protocol, validation |
| 02. Typed Attribute | Type checking with descriptors |
| 03. Cached Property | Lazy evaluation, caching |
| 04. Range Validator | Numeric validation, custom exceptions |
| 05. Lazy Property | Non-data descriptor pattern |
| 06. Observable Attribute | Observer pattern with descriptors |
| 07. Logged Attribute | Logging hooks in descriptors |
| 08. Read-Only Attribute | Write-once semantics |
| 09. Attribute History | Tracking all value changes |
| 10. Weak Reference Descriptor | Memory-efficient per-instance storage |

---

## Quick Reference

```python
from __future__ import annotations

from typing import Any


class DescriptorTemplate:
    """Template for a data descriptor."""
    
    def __init__(self, default: Any = None) -> None:
        self.default = default
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Capture the attribute name."""
        self.name = name
        self.storage_name = f"_{name}"
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        """Get the attribute value."""
        if instance is None:
            return self  # Class access returns descriptor
        return getattr(instance, self.storage_name, self.default)
    
    def __set__(self, instance: object, value: Any) -> None:
        """Set the attribute value."""
        # Add validation or transformation here
        setattr(instance, self.storage_name, value)
    
    def __delete__(self, instance: object) -> None:
        """Delete the attribute."""
        if hasattr(instance, self.storage_name):
            delattr(instance, self.storage_name)


class NonDataDescriptor:
    """Template for a non-data descriptor."""
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        # Compute and return value
        return None


# Usage
class MyClass:
    attr = DescriptorTemplate(default=0)


obj = MyClass()
obj.attr = 42  # __set__ called
print(obj.attr)  # __get__ called, returns 42
```

---

## Weekly Project Connection

The Week 5 project (Task Management System) uses descriptors for:

- **Validated attributes** - Title length validation, priority enums, status constraints
- **Type checking** - Ensuring assignee is a User object, tags are strings
- **Observable fields** - Notifying when task status changes for audit logging
- **Read-only attributes** - Created timestamp that cannot be modified after creation
- **Lazy evaluation** - Expensive computed properties like task statistics

Descriptors ensure data integrity at the attribute level, making the domain models robust.

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify your solutions
2. Review the descriptor protocol in the Python documentation
3. Preview Day 2: **Metaclasses**
