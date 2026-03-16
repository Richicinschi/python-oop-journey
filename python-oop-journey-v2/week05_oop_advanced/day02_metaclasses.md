# Day 2: Metaclasses

## Learning Objectives

After completing this day, you will understand:
- What metaclasses are and how they control class creation
- The relationship between `type` and metaclasses
- How to use `__new__` and `__init__` in metaclasses
- Common metaclass patterns: Singleton, Registry, Auto-property generation
- When to use metaclasses vs. class decorators
- How metaclasses interact with inheritance

## Theory

### Understanding Metaclasses

A **metaclass** is a class that creates and controls classes, just as classes create and control instances.

```python
# A class is an instance of type
class MyClass:
    pass

print(type(MyClass))  # <class 'type'>
```

By default, Python uses `type` as the metaclass for all classes. You can create custom metaclasses by subclassing `type`.

### The `type` Metaclass

`type` is the built-in metaclass. When Python sees:

```python
class MyClass(BaseClass, metaclass=MyMeta):
    x = 1
    def method(self):
        pass
```

Python effectively calls:

```python
MyClass = MyMeta('MyClass', (BaseClass,), {'x': 1, 'method': <function>})
```

### Creating a Custom Metaclass

```python
from typing import Any


class EchoMeta(type):
    """A simple metaclass that announces class creation."""
    
    def __new__(
        mcs: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:
        print(f"Creating class: {name}")
        return super().__new__(mcs, name, bases, namespace)


class MyClass(metaclass=EchoMeta):
    pass  # Prints: Creating class: MyClass
```

### Key Metaclass Methods

**`__new__(mcs, name, bases, namespace)`**
- Creates and returns the class object
- Receives: metaclass, class name, base classes, attribute dict
- Use for: Modifying the class before creation

**`__init__(cls, name, bases, namespace)`**
- Initializes the created class
- Receives: the class object (now created), name, bases, namespace
- Use for: Post-creation setup, registration

**`__call__(cls, *args, **kwargs)`**
- Called when the class is instantiated
- Controls instance creation
- Use for: Custom instance creation logic

### Common Metaclass Patterns

#### 1. Singleton Pattern

```python
class SingletonMeta(type):
    """Ensures only one instance of the class exists."""
    _instances: dict[type, Any] = {}
    
    def __call__(cls: type, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """Only one database connection exists."""
    
    def __init__(self) -> None:
        self.connection = "Connected"

db1 = Database()
db2 = Database()
assert db1 is db2  # Same instance
```

#### 2. Auto-Registration

```python
class PluginRegistry(type):
    """Automatically registers all subclasses."""
    _registry: dict[str, type] = {}
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != 'BasePlugin':  # Don't register base
            mcs._registry[name] = cls
        return cls


class BasePlugin(metaclass=PluginRegistry):
    pass


class EmailPlugin(BasePlugin):
    pass


class SmsPlugin(BasePlugin):
    pass

# PluginRegistry._registry == {'EmailPlugin': EmailPlugin, 'SmsPlugin': SmsPlugin}
```

#### 3. Attribute Transformation

```python
class UpperCaseMeta(type):
    """Converts all string attributes to uppercase."""
    
    def __new__(mcs, name, bases, namespace):
        upper_namespace = {
            key: value.upper() if isinstance(value, str) else value
            for key, value in namespace.items()
        }
        return super().__new__(mcs, name, bases, upper_namespace)


class Config(metaclass=UpperCaseMeta):
    app_name = "myapp"  # Becomes "MYAPP"
```

### Metaclasses vs. Class Decorators

| Metaclasses | Class Decorators |
|------------|------------------|
| Control class creation process | Transform an already-created class |
| Inherited by subclasses | Not inherited |
| More powerful/complex | Simpler, often sufficient |
| Use for: deep class control | Use for: simple transformations |

Prefer class decorators when possible. Use metaclasses when:
- You need to control class creation, not just transformation
- The behavior must be inherited by subclasses
- You're building a framework with strict conventions

### Metaclass Inheritance

```python
class MetaA(type):
    pass

class MetaB(type):
    pass

class A(metaclass=MetaA):
    pass

class B(metaclass=MetaB):
    pass

# This causes TypeError - metaclass conflict
# class C(A, B): pass

# Solution: create a common metaclass
class MetaCommon(MetaA, MetaB):
    pass

class C(A, B, metaclass=MetaCommon):
    pass
```

### Interaction with `__init_subclass__`

Python 3.6+ provides `__init_subclass__` as a cleaner alternative for some metaclass use cases:

```python
class Base:
    _registry: dict[str, type] = {}
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Base._registry[cls.__name__] = cls
```

Use `__init_subclass__` for simple registration. Use metaclasses when you need more control.

## Common Mistakes

1. **Metaclass conflicts in multiple inheritance**: When mixing classes with different metaclasses, you need a common metaclass.

2. **Modifying namespace incorrectly**: Remember that namespace contains ALL class attributes, including methods and special names.

3. **Forgetting that metaclasses affect subclasses**: A metaclass on a base class affects all derived classes.

4. **Overusing metaclasses**: Many problems that seem to need metaclasses are better solved with simpler tools.

## Summary

- Metaclasses are classes that create classes
- Use `__new__` to control class creation, `__init__` for post-creation setup
- Common patterns: Singleton, Registry, Validation, Attribute transformation
- Prefer simpler alternatives (decorators, `__init_subclass__`) when possible
- Metaclasses are powerful but can make code harder to understand

## Connection to Exercises

Today's exercises explore different metaclass patterns:

| Problem | Skills Practiced |
|---------|------------------|
| 01. Singleton Metaclass | `__call__` method, instance management |
| 02. Class Registry Metaclass | Auto-registration, `__new__` vs `__init__` |
| 03. Auto-Property Metaclass | Dynamic attribute generation, namespace modification |
| 04. Validation Metaclass | Class-level validation, `__new__` intercept |
| 05. Immutable Metaclass | Freezing class attributes after creation |
| 06. Tracked Class Metaclass | Tracking class creation, metadata collection |
| 07. Abstract Metaclass | Enforcing abstract methods at creation |
| 08. Plugin Registry Metaclass | Framework-style auto-registration |
| 09. Attribute Checker Metaclass | Validating required attributes |
| 10. Serializable Metaclass | Auto-generating serialization methods |

---

## Connection to Weekly Project

The Task Management System project uses metaclasses for:
- Auto-registering task types for the plugin system
- Validating task configurations at class creation time
- Enforcing required attributes on model classes
