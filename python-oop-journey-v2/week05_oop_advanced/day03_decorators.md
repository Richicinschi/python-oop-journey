# Day 3: Function and Class Decorators

## Learning Objectives

By the end of this day, you will be able to:

1. Understand what decorators are and how they work
2. Create function decorators with `@wraps` for metadata preservation
3. Create parameterized decorators (decorator factories)
4. Implement class decorators that modify class behavior
5. Use built-in decorators like `@staticmethod`, `@classmethod`, `@property`
6. Understand decorator stacking and order of execution
7. Apply decorators for cross-cutting concerns (logging, timing, caching, etc.)

---

## Key Concepts

### 1. What is a Decorator?

A decorator is a function that takes another function or class as input and extends or modifies its behavior without explicitly changing its source code.

```python
from __future__ import annotations
from functools import wraps
from typing import Callable

def my_decorator(func: Callable) -> Callable:
    """A simple decorator that wraps a function."""
    @wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@my_decorator
def say_hello():
    """Greet the world."""
    print("Hello!")

# Usage
say_hello()
# Output:
# Before function call
# Hello!
# After function call
```

### 2. Why Use `@wraps`?

The `@wraps` decorator preserves the original function's metadata:

```python
from functools import wraps
from typing import Callable

def bad_decorator(func: Callable) -> Callable:
    """Without wraps - loses metadata."""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def good_decorator(func: Callable) -> Callable:
    """With wraps - preserves metadata."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def func1():
    """My function."""
    pass

@good_decorator
def func2():
    """My function."""
    pass

print(func1.__name__)   # "wrapper" - wrong!
print(func1.__doc__)    # None - wrong!
print(func2.__name__)   # "func2" - correct!
print(func2.__doc__)    # "My function." - correct!
```

### 3. Decorators with Arguments (Decorator Factories)

To create a decorator that accepts arguments, you need an additional level of nesting:

```python
from functools import wraps
from typing import Callable

def repeat(times: int) -> Callable:
    """Decorator factory that repeats a function n times."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result  # Return last result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name: str) -> None:
    print(f"Hello, {name}!")

greet("Alice")
# Output:
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

### 4. Class Decorators

Class decorators modify class behavior just like function decorators modify functions:

```python
from typing import Type, Callable

def add_method(method_name: str, method: Callable) -> Callable:
    """Add a method to a class."""
    def decorator(cls: Type) -> Type:
        setattr(cls, method_name, method)
        return cls
    return decorator

def singleton(cls: Type) -> Type:
    """Ensure only one instance of the class exists."""
    instances: dict = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Database:
    """A singleton database class."""
    def __init__(self) -> None:
        self.connection = "Connected"

db1 = Database()
db2 = Database()
print(db1 is db2)  # True - same instance
```

### 5. Method Decorators in Classes

```python
from functools import wraps
from typing import Callable

def log_calls(func: Callable) -> Callable:
    """Log all method calls."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(self, *args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

class Calculator:
    """A calculator with logged methods."""
    
    @log_calls
    def add(self, a: int, b: int) -> int:
        return a + b
    
    @log_calls
    def multiply(self, a: int, b: int) -> int:
        return a * b
```

### 6. Stacking Decorators

Decorators can be stacked, and they apply from bottom to top:

```python
from functools import wraps
from typing import Callable
import time

def timer(func: Callable) -> Callable:
    """Time function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

def log_entry(func: Callable) -> Callable:
    """Log function entry."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Entering {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@timer
@log_entry
def slow_function():
    time.sleep(0.1)
    return "Done"

# Execution order:
# 1. log_entry wrapper (prints "Entering slow_function")
# 2. timer wrapper (times the log_entry call)
# Equivalent to: timer(log_entry(slow_function))
```

### 7. Common Decorator Patterns

#### Timing Decorator
```python
from functools import wraps
from time import perf_counter
from typing import Callable

def timer(func: Callable) -> Callable:
    """Time function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper
```

#### Caching/Memoization Decorator
```python
from functools import wraps
from typing import Callable, Any

def memoize(func: Callable) -> Callable:
    """Cache function results."""
    cache: dict = {}
    
    @wraps(func)
    def wrapper(*args) -> Any:
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper
```

#### Retry Decorator
```python
from functools import wraps
from time import sleep
from typing import Callable, Type, Tuple

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """Retry a function on failure."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    sleep(delay)
            return None
        return wrapper
    return decorator
```

### 8. Property Decorators

The `@property` decorator turns methods into attributes:

```python
from __future__ import annotations

class Circle:
    """A circle with property decorators."""
    
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
        """Calculate area (read-only)."""
        import math
        return math.pi * self._radius ** 2
    
    @radius.deleter
    def radius(self) -> None:
        """Delete the radius."""
        del self._radius

# Usage
c = Circle(5.0)
print(c.radius)   # 5.0 (calls getter)
c.radius = 10.0   # calls setter
print(c.area)     # ~314.15 (computed property)
```

### 9. Built-in Class Decorators

```python
class MyClass:
    """Demonstrating built-in decorators."""
    
    _instance_count = 0
    
    def __init__(self) -> None:
        MyClass._instance_count += 1
    
    @staticmethod
    def utility_function(x: int) -> int:
        """A static method - no self or cls needed."""
        return x * 2
    
    @classmethod
    def get_instance_count(cls) -> int:
        """A class method - receives class as first argument."""
        return cls._instance_count
    
    @classmethod
    def create_default(cls) -> MyClass:
        """Factory method using classmethod."""
        return cls()
```

---

## Common Mistakes

### 1. Forgetting `@wraps`

```python
# Wrong - loses function metadata
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Right - preserves metadata
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 2. Incorrect Decorator Factory

```python
# Wrong - calling decorator instead of passing arguments
@retry  # Missing parentheses!
def func(): pass

# Right - using decorator factory correctly
@retry(max_attempts=3)
def func(): pass
```

### 3. Not Returning the Result

```python
# Wrong - doesn't return result
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)  # Missing return!
    return wrapper

# Right - returns result
def good_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 4. Incorrect Stacking Order

```python
# Order matters!
@timer
@log_calls
def func():
    pass

# timer wraps log_calls, so timer sees the logging overhead
# If you want to time just the function, reverse the order
```

### 5. Modifying Mutable Default Arguments in Decorators

```python
# Wrong - shared cache between decorated functions
def cache(func, _cache={}):  # Dangerous default!
    def wrapper(*args):
        if args not in _cache:
            _cache[args] = func(*args)
        return _cache[args]
    return wrapper

# Right - each decorator gets its own cache
def cache(func):
    _cache = {}  # Fresh cache per decorator
    @wraps(func)
    def wrapper(*args):
        if args not in _cache:
            _cache[args] = func(*args)
        return _cache[args]
    return wrapper
```

---

## Connection to Exercises

Today's exercises cover essential decorator patterns:

| Problem | Skills Practiced |
|---------|------------------|
| 01. Timer Decorator | Basic decorator with `@wraps` |
| 02. Cache Decorator | Memoization, stateful decorators |
| 03. Retry Decorator | Parameterized decorators, exception handling |
| 04. Validate Types Decorator | Runtime type checking |
| 05. Logged Class Decorator | Class decorators, method wrapping |
| 06. Singleton Decorator | Class modification, instance management |
| 07. Immutable Decorator | Preventing attribute modification |
| 08. Deprecated Decorator | Warnings, metadata preservation |
| 09. Counted Decorator | Call counting, state tracking |
| 10. Rate Limit Decorator | Time-based limiting |
| 11. Debug Decorator | Argument/return value inspection |
| 12. Once Decorator | One-time execution pattern |
| 13. Requires Decorator | Permission checking, parameterized decorators |

---

## Weekly Project Connection

The Week 5 project involves a **Task Management System**. Day 3's concepts are essential because:

- **Timing decorators** profile slow operations
- **Caching decorators** improve performance
- **Logging decorators** track method calls for audit trails
- **Retry decorators** handle transient failures
- **Validation decorators** enforce business rules
- **Permission decorators** control access to sensitive operations

---

## Quick Reference

```python
from __future__ import annotations
from functools import wraps
from typing import Callable, Type, Any

# Simple function decorator
def my_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Before
        result = func(*args, **kwargs)
        # After
        return result
    return wrapper

# Decorator with arguments
def my_decorator_with_args(arg1: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Use arg1 here
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Class decorator
def my_class_decorator(cls: Type) -> Type:
    # Modify class
    setattr(cls, 'new_method', lambda self: "new")
    return cls

# Usage
@my_decorator
def func(): pass

@my_decorator_with_args(42)
def func_with_args(): pass

@my_class_decorator
class MyClass: pass
```

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify your solutions
2. Review any problems you found challenging
3. Preview Day 4: **Dataclasses and Slots**
