# Day 4: Multiple Inheritance and MRO

## Learning Objectives

By the end of this day, you will be able to:

1. Understand how multiple inheritance works in Python
2. Use the Method Resolution Order (MRO) to predict method calls
3. Apply the `super()` function correctly in multiple inheritance hierarchies
4. Recognize and resolve the "diamond problem"
5. Design effective mixin classes
6. Use `__mro__` and `mro()` to inspect class hierarchies

---

## 1. Understanding Multiple Inheritance

Multiple inheritance allows a class to inherit from more than one parent class. This is powerful but requires understanding how Python resolves method calls.

### Basic Syntax

```python
from __future__ import annotations


class Flyable:
    """Mixin for flying capability."""
    
    def fly(self) -> str:
        return "Flying!"


class Swimmable:
    """Mixin for swimming capability."""
    
    def swim(self) -> str:
        return "Swimming!"


class Duck(Flyable, Swimmable):
    """A duck can both fly and swim."""
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    def describe(self) -> str:
        return f"{self.name} is a duck"


# Usage
duck = Duck("Donald")
print(duck.fly())   # From Flyable
print(duck.swim())  # From Swimmable
print(duck.describe())  # From Duck
```

---

## 2. Method Resolution Order (MRO)

The MRO defines the order in which Python looks for methods. Python uses the **C3 Linearization** algorithm.

### Viewing the MRO

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


class D(B, C):
    pass


# View MRO
print(D.__mro__)
# Output: (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

# Or use the mro() method
print(D.mro())
# Same output

# Or use help()
help(D)
```

### The MRO Rules

1. **Children precede parents**: A class is checked before its parents
2. **Left-to-right**: Parents are checked in the order listed in the class definition
3. **No duplicates**: Each class appears only once in the MRO

---

## 3. The Diamond Problem

The diamond problem occurs when a class inherits from two classes that share a common ancestor.

```
    A
   / \
  B   C
   \ /
    D
```

```python
from __future__ import annotations


class A:
    """Top of the diamond."""
    
    def __init__(self) -> None:
        print("A.__init__")
        self.value_a = "A"
    
    def method(self) -> str:
        return "A"


class B(A):
    """Left branch."""
    
    def __init__(self) -> None:
        print("B.__init__")
        super().__init__()  # Calls C.__init__, not A.__init__!
        self.value_b = "B"
    
    def method(self) -> str:
        return f"B -> {super().method()}"


class C(A):
    """Right branch."""
    
    def __init__(self) -> None:
        print("C.__init__")
        super().__init__()  # Calls A.__init__
        self.value_c = "C"
    
    def method(self) -> str:
        return f"C -> {super().method()}"


class D(B, C):
    """Bottom of the diamond."""
    
    def __init__(self) -> None:
        print("D.__init__")
        super().__init__()  # Follows MRO: B -> C -> A
        self.value_d = "D"
    
    def method(self) -> str:
        return f"D -> {super().method()}"


# Check MRO
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

# Method resolution follows MRO
d = D()
print(d.method())  # D -> B -> C -> A
```

**Output:**
```
D.__init__
B.__init__
C.__init__
A.__init__
D -> B -> C -> A
```

---

## 4. Using `super()` in Multiple Inheritance

`super()` doesn't just call the parent class—it follows the MRO.

### Cooperative Multiple Inheritance

```python
from __future__ import annotations


class Base:
    """Base class that starts the chain."""
    
    def __init__(self, value: int) -> None:
        self.value = value
        print(f"Base initialized with {value}")


class AddTen:
    """Mixin that adds 10 to the value."""
    
    def __init__(self, value: int) -> None:
        super().__init__(value + 10)
        print(f"AddTen: value is now {self.value}")


class MultiplyByTwo:
    """Mixin that multiplies the value by 2."""
    
    def __init__(self, value: int) -> None:
        super().__init__(value * 2)
        print(f"MultiplyByTwo: value is now {self.value}")


class Combined(MultiplyByTwo, AddTen, Base):
    """Inherits from all three.
    
    MRO: Combined -> MultiplyByTwo -> AddTen -> Base -> object
    """
    pass


# Usage
c = Combined(5)
# 1. Combined calls MultiplyByTwo.__init__(5)
# 2. MultiplyByTwo calls super().__init__(5 * 2 = 10)
# 3. AddTen calls super().__init__(10 + 10 = 20)
# 4. Base sets self.value = 20
# Final value: 20
```

### Key Points About `super()`

1. `super()` returns a proxy object that delegates method calls
2. It follows the MRO, not just the direct parent
3. For cooperative inheritance, all classes must use `super()`
4. The last class in MRO calls `object`'s method

---

## 5. Designing Mixins

Mixins are small, focused classes that provide specific functionality.

### Good Mixin Design

```python
from __future__ import annotations
from datetime import datetime
from typing import Any


class LoggerMixin:
    """Mixin that adds logging capability."""
    
    def log(self, message: str) -> None:
        """Log a message with the class name."""
        print(f"[{self.__class__.__name__}] {message}")


class TimestampMixin:
    """Mixin that adds timestamp tracking."""
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._created_at = datetime.now()
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    def age_seconds(self) -> float:
        """Return age in seconds."""
        return (datetime.now() - self._created_at).total_seconds()


class DataObject(LoggerMixin, TimestampMixin):
    """A data object with logging and timestamp capabilities."""
    
    def __init__(self, name: str, value: int) -> None:
        super().__init__()
        self.name = name
        self.value = value
        self.log(f"Created with name={name}, value={value}")


# Usage
obj = DataObject("test", 42)
print(f"Created at: {obj.created_at}")
print(f"Age: {obj.age_seconds():.2f} seconds")
obj.log("Processing complete")
```

### Mixin Best Practices

1. **Single Responsibility**: Each mixin does one thing
2. **No `__init__` required**: Design mixins to work without one
3. **Use `*args, **kwargs`**: Pass unknown arguments up the chain
4. **Don't create instances**: Mixins are meant to be inherited
5. **Document dependencies**: Note if a mixin requires specific methods

---

## 6. Common Patterns with Multiple Inheritance

### Pattern 1: Capability Mixins

```python
from __future__ import annotations


class JSONSerializable:
    """Mixin that adds JSON serialization."""
    
    def to_json(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }


class Validatable:
    """Mixin that adds validation."""
    
    def validate(self) -> list[str]:
        """Return list of validation errors."""
        errors: list[str] = []
        for name in dir(self):
            if name.startswith('_validate_'):
                error = getattr(self, name)()
                if error:
                    errors.append(error)
        return errors
    
    def is_valid(self) -> bool:
        return len(self.validate()) == 0
```

### Pattern 2: Abstract Base Classes + Mixins

```python
from __future__ import annotations
from abc import ABC, abstractmethod


class Drawable(ABC):
    """Abstract base for drawable objects."""
    
    @abstractmethod
    def draw(self) -> str:
        """Return a string representation."""
        pass
    
    @abstractmethod
    def get_bounds(self) -> tuple[int, int, int, int]:
        """Return bounding box as (x, y, width, height)."""
        pass


class Clickable(ABC):
    """Abstract base for clickable objects."""
    
    @abstractmethod
    def on_click(self) -> str:
        """Handle click event."""
        pass
    
    def is_hit(self, x: int, y: int) -> bool:
        """Check if point hits this object."""
        bx, by, bw, bh = self.get_bounds()
        return bx <= x <= bx + bw and by <= y <= by + bh


class Button(Drawable, Clickable):
    """A button is both drawable and clickable."""
    
    def __init__(self, x: int, y: int, width: int, height: int, label: str) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
    
    def draw(self) -> str:
        return f"[ {self.label} ]"
    
    def get_bounds(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.width, self.height)
    
    def on_click(self) -> str:
        return f"Button '{self.label}' clicked!"
```

### Pattern 3: Audit Trail with Multiple Inheritance

```python
from __future__ import annotations
from datetime import datetime
from typing import Any


class Auditable:
    """Mixin that tracks who made changes."""
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._audit_log: list[dict[str, Any]] = []
    
    def audit(self, action: str, user: str) -> None:
        """Record an audit entry."""
        self._audit_log.append({
            'timestamp': datetime.now(),
            'action': action,
            'user': user
        })
    
    def get_audit_trail(self) -> list[dict[str, Any]]:
        return self._audit_log.copy()


class Versioned:
    """Mixin that tracks versions."""
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._version = 1
        self._version_history: list[dict[str, Any]] = []
    
    @property
    def version(self) -> int:
        return self._version
    
    def bump_version(self, changes: str) -> None:
        """Increment version and record changes."""
        self._version_history.append({
            'version': self._version,
            'changes': changes,
            'timestamp': datetime.now()
        })
        self._version += 1


class Model(Auditable, Versioned):
    """Base model with audit and versioning."""
    
    def __init__(self, id: int, data: dict[str, Any]) -> None:
        super().__init__()
        self.id = id
        self._data = data.copy()
    
    def update(self, changes: dict[str, Any], user: str) -> None:
        """Update data and record audit/version."""
        self._data.update(changes)
        self.audit(f"Updated: {list(changes.keys())}", user)
        self.bump_version(str(changes))
    
    def get_data(self) -> dict[str, Any]:
        return self._data.copy()
```

---

## 7. Troubleshooting Multiple Inheritance

### Common Issue: Missing `super()` Call

```python
# Wrong - breaks the chain
class BadMixin:
    def __init__(self) -> None:
        # Missing super().__init__()!
        self.bad = True


# Right - maintains the chain
class GoodMixin:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.good = True
```

### Common Issue: Incompatible Signatures

```python
# Wrong - incompatible __init__ signatures
class A:
    def __init__(self, x: int) -> None:
        self.x = x


class B:
    def __init__(self, y: str) -> None:
        self.y = y


# This will fail!
class C(A, B):
    def __init__(self, x: int, y: str) -> None:
        A.__init__(self, x)  # Direct call - breaks cooperative inheritance
        B.__init__(self, y)


# Better - use keyword arguments and **kwargs
class BetterA:
    def __init__(self, x: int = 0, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.x = x


class BetterB:
    def __init__(self, y: str = "", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.y = y


class BetterC(BetterA, BetterB):
    def __init__(self, x: int = 0, y: str = "", **kwargs: Any) -> None:
        super().__init__(x=x, y=y, **kwargs)
```

---

## 8. Best Practices Summary

| Practice | Why It Matters |
|----------|----------------|
| Always use `super()` | Ensures cooperative inheritance works |
| Accept `*args, **kwargs` | Allows flexible parameter passing up the chain |
| Check MRO with `__mro__` | Understand method resolution order |
| Design mixins to be independent | Mixins should work with any class |
| Avoid deep hierarchies | Prefer composition for complex relationships |
| Document mixin requirements | Note any expected methods or attributes |
| Test with various MROs | Verify behavior in different inheritance orders |

---

## Connection to Exercises

Today's exercises explore multiple inheritance patterns:

| Exercise | Concepts Practiced | Project Connection |
|----------|-------------------|-------------------|
| 01. Logging and Timestamp Mixins | Combine LoggerMixin and TimestampMixin | Audit trails in shelter |
| 02. Flying and Swimming Animals | Flyable, Swimmable mixins with Duck and Penguin | Capability mixins pattern |
| 03. Audit Enabled Models | Auditable, Versioned with Model base class | Record tracking |
| 04. Cached Validated Objects | Cacheable, Validatable with DataObject | Validation mixins |
| 05. Admin Power User | Diamond inheritance: User → Admin, PowerUser → SuperAdmin | MRO understanding |
| 06. Renderable Clickable Widgets | Drawable, Clickable with Button, Icon | Multiple interface implementation |

---

## Connection to Weekly Project

The Animal Shelter Management System uses multiple inheritance for cross-cutting concerns:

- **LoggerMixin**: Adds logging capability to Animals, Staff, and Adoptions
- **TimestampMixin**: Tracks creation and modification times for all records
- **Validatable**: Ensures data integrity across different entity types
- **MedicalRecord**: Combines with Animal for medical tracking via mixins

Understanding MRO is critical when Animals inherit from both the base Animal class and various capability mixins.

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify: `pytest week04_oop_intermediate/tests/day04/ -v`
2. Review any problems you found challenging, especially MRO-related ones
3. Use `print(Class.__mro__)` to explore method resolution order
4. Preview Day 5: **Polymorphism and Duck Typing** - Treating different objects uniformly

---

## Summary

- **Multiple inheritance** allows a class to inherit from multiple parents
- **MRO** determines the order of method lookup using C3 linearization
- **`super()`** follows the MRO, not just the direct parent
- **The diamond problem** is solved by the MRO ensuring each class is visited once
- **Mixins** are small, focused classes that add specific functionality
- **Cooperative inheritance** requires all classes to use `super()` properly
- Use `__mro__` or `mro()` to inspect and understand method resolution
