# Day 2: Instance, Class, and Static Methods

## Learning Objectives

By the end of this day, you will be able to:

1. Understand the difference between instance, class, and static methods
2. Use `@classmethod` to create alternative constructors and factory methods
3. Use `@staticmethod` for utility functions that belong to a class
4. Understand when to use each method type
5. Implement the factory pattern using `@classmethod`
6. Create registry patterns with `@classmethod`
7. Build utility classes with mixed method types

---

## Key Concepts

### 1. Instance Methods

Instance methods are the most common type. They take `self` as the first parameter and can access/modify instance attributes.

```python
class Person:
    def __init__(self, name: str) -> None:
        self.name = name
    
    def greet(self) -> str:  # Instance method
        return f"Hello, I'm {self.name}"

person = Person("Alice")
print(person.greet())  # "Hello, I'm Alice"
```

---

### 2. Class Methods (`@classmethod`)

Class methods take `cls` as the first parameter and operate on the class itself, not instances. They're useful for:

- Alternative constructors
- Factory methods
- Accessing/modifying class attributes

```python
class Person:
    default_name = "Unknown"
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Person:
        """Alternative constructor from a dictionary."""
        return cls(name=data.get("name", cls.default_name))
    
    @classmethod
    def anonymous(cls) -> Person:
        """Factory method for anonymous person."""
        return cls(name=cls.default_name)

# Using alternative constructor
person1 = Person.from_dict({"name": "Bob"})
person2 = Person.anonymous()
```

---

### 3. Static Methods (`@staticmethod`)

Static methods don't take `self` or `cls`. They're utility functions that logically belong to the class but don't need class/instance data.

```python
class MathUtils:
    @staticmethod
    def add(a: int, b: int) -> int:
        return a + b
    
    @staticmethod
    def is_even(n: int) -> bool:
        return n % 2 == 0

# Usage without creating an instance
result = MathUtils.add(5, 3)  # 8
```

---

### 4. When to Use Each Type

| Method Type | Use When | Accesses |
|-------------|----------|----------|
| Instance | Working with instance data | `self` attributes |
| Class Method | Working with class data, alternative constructors | `cls` attributes |
| Static Method | Utility function, no instance/class data needed | Neither |

---

### 5. Common Patterns

#### Factory Pattern with `@classmethod`

```python
class Animal:
    def __init__(self, name: str) -> None:
        self.name = name
    
    @classmethod
    def create(cls, animal_type: str, name: str) -> Animal:
        if animal_type == "dog":
            return Dog(name)
        elif animal_type == "cat":
            return Cat(name)
        return cls(name)

class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} says Meow!"
```

#### Registry Pattern with `@classmethod`

```python
class Plugin:
    _registry: dict[str, type[Plugin]] = {}
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__] = cls
    
    @classmethod
    def get_plugin(cls, name: str) -> type[Plugin] | None:
        return cls._registry.get(name)
    
    @classmethod
    def list_plugins(cls) -> list[str]:
        return list(cls._registry.keys())
```

---

## Connection to Exercises

Today's exercises reinforce method types through practical implementations:

| Problem | Skills Practiced | Method Type Focus |
|---------|------------------|-------------------|
| 01. Inventory Item | Alternative constructor | `@classmethod` |
| 02. Date Helper | Utility functions | `@staticmethod` |
| 03. Temperature Converter | Unit conversions | `@staticmethod` |
| 04. User Factory | Factory pattern | `@classmethod` |
| 05. Student Registry | Registry pattern | `@classmethod` |
| 06. Bank Branch | Mixed method types | Instance + `@classmethod` + `@staticmethod` |
| 07. Math Toolkit | Pure utilities | `@staticmethod` |
| 08. Logger Config | Configuration management | `@classmethod` |
| 09. URL Builder | String utilities | `@staticmethod` |
| 10. Account Factory | Advanced factory | `@classmethod` with logic |

---

## Weekly Project Connection

The Week 3 **E-commerce System** uses different method types throughout:

| Class | Method Type | Example Use |
|-------|-------------|-------------|
| `Product` | `@classmethod` | `Product.from_dict(data)` - Create product from API response |
| `User` | `@staticmethod` | `User.validate_email(email)` - Email format validation |
| `Inventory` | `@classmethod` | Track class-level stock across all products |
| `ShoppingCart` | Instance method | `cart.add_item(product)` - Modify instance state |

**Key insight**: Use `@staticmethod` for pure functions (validation, calculations), `@classmethod` for alternative constructors and class-level configuration.

---

## Common Mistakes

### 1. Calling ClassMethod on Instance (Works but Confusing)

```python
# Technically works but misleading
person = Person("Alice")
person.from_dict({"name": "Bob"})  # Works, but looks wrong

# Better - call on class
person = Person.from_dict({"name": "Bob"})  # Clear intent
```

### 2. Forgetting @staticmethod Decorator

```python
# Wrong - expects 'self', crashes when called on class
class MathUtils:
    def add(a, b):  # Missing @staticmethod!
        return a + b

MathUtils.add(1, 2)  # TypeError: add() missing 1 required argument

# Right
class MathUtils:
    @staticmethod
    def add(a: int, b: int) -> int:
        return a + b
```

### 3. Using Instance Method When Static Would Do

```python
# Wrong - creates unnecessary instance
class Temperature:
    def c_to_f(self, c: float) -> float:  # Doesn't need 'self'
        return (c * 9/5) + 32

t = Temperature()
t.c_to_f(100)  # Must create instance just to convert

# Right - use @staticmethod
class Temperature:
    @staticmethod
    def c_to_f(c: float) -> float:
        return (c * 9/5) + 32

Temperature.c_to_f(100)  # Clean, no instance needed
```

### 4. Modifying Class State Accidentally

```python
# Risky - all instances share the same list
class User:
    roles = []  # Class attribute - shared!
    
    def add_role(self, role: str) -> None:
        self.roles.append(role)  # Modifies class attribute!

u1 = User()
u2 = User()
u1.add_role("admin")
print(u2.roles)  # ["admin"] - oops, u2 has it too!

# Right - use instance attribute
class User:
    def __init__(self) -> None:
        self.roles: list[str] = []  # Each user has own list
    
    def add_role(self, role: str) -> None:
        self.roles.append(role)
```

---

## Practice Problems

Complete all 10 problems in order:

1. **inventory_item** - Item with @classmethod alternative constructor
2. **date_helper** - Date utilities with @staticmethod
3. **temperature_converter** - @staticmethod conversion methods
4. **user_factory** - @classmethod factory methods
5. **student_registry** - @classmethod registry pattern
6. **bank_branch** - @classmethod and @staticmethod mix
7. **math_toolkit** - @staticmethod math utilities
8. **logger_config** - @classmethod config management
9. **url_builder** - @staticmethod builder pattern
10. **account_factory** - Factory pattern with @classmethod

---

## Key Takeaways

- **Instance methods** need instance data (`self`)
- **Class methods** work with class-level data and create alternative constructors (`cls`)
- **Static methods** are utility functions that don't need instance or class context
- Use `@classmethod` for factory patterns and alternative constructors
- Use `@staticmethod` for helper functions that logically belong to a class
- All three method types can coexist in the same class
