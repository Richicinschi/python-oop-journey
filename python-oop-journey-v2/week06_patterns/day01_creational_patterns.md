# Day 1: Creational Patterns

## Learning Objectives

By the end of this day, you will be able to:

1. Understand the purpose and benefits of creational design patterns
2. Implement the Factory Method pattern for flexible object creation
3. Use the Abstract Factory pattern to create families of related objects
4. Apply the Builder pattern for constructing complex objects step by step
5. Implement the Singleton pattern for single-instance classes
6. Use the Prototype pattern for object cloning

---

## Key Concepts

### 1. What Are Creational Patterns?

Creational patterns deal with object creation mechanisms, trying to create objects in a manner suitable to the situation. They provide flexibility and reuse by separating the creation logic from the usage logic.

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| Factory Method | Create objects without specifying exact class | When you don't know beforehand what types you'll need |
| Abstract Factory | Create families of related objects | When you need to ensure compatibility across products |
| Builder | Construct complex objects step by step | When an object has many optional parameters |
| Singleton | Ensure only one instance exists | When exactly one object is needed (config, logging) |
| Prototype | Clone existing objects | When creating new instances is costly |

### 2. Factory Method Pattern

Defines an interface for creating an object, but lets subclasses decide which class to instantiate.

```python
from __future__ import annotations
from abc import ABC, abstractmethod

class Notification(ABC):
    """Product interface."""
    
    @abstractmethod
    def send(self, message: str) -> str:
        pass

class EmailNotification(Notification):
    """Concrete product."""
    
    def send(self, message: str) -> str:
        return f"Email sent: {message}"

class SMSNotification(Notification):
    """Concrete product."""
    
    def send(self, message: str) -> str:
        return f"SMS sent: {message}"

class NotificationFactory(ABC):
    """Creator abstract class."""
    
    @abstractmethod
    def create_notification(self) -> Notification:
        pass
    
    def notify(self, message: str) -> str:
        notification = self.create_notification()
        return notification.send(message)

class EmailNotificationFactory(NotificationFactory):
    """Concrete creator."""
    
    def create_notification(self) -> Notification:
        return EmailNotification()

class SMSNotificationFactory(NotificationFactory):
    """Concrete creator."""
    
    def create_notification(self) -> Notification:
        return SMSNotification()

# Usage
factory = EmailNotificationFactory()
result = factory.notify("Hello!")  # "Email sent: Hello!"
```

### 3. Abstract Factory Pattern

Provides an interface for creating families of related or dependent objects without specifying their concrete classes.

```python
from __future__ import annotations
from abc import ABC, abstractmethod

# Abstract products
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class Checkbox(ABC):
    @abstractmethod
    def check(self) -> str:
        pass

# Concrete products - Windows family
class WindowsButton(Button):
    def render(self) -> str:
        return "Rendering Windows button"

class WindowsCheckbox(Checkbox):
    def check(self) -> str:
        return "Checking Windows checkbox"

# Concrete products - Mac family
class MacButton(Button):
    def render(self) -> str:
        return "Rendering Mac button"

class MacCheckbox(Checkbox):
    def check(self) -> str:
        return "Checking Mac checkbox"

# Abstract factory
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

# Concrete factories
class WindowsUIFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

class MacUIFactory(UIFactory):
    def create_button(self) -> Button:
        return MacButton()
    
    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()
```

### 4. Builder Pattern

Separates the construction of a complex object from its representation, allowing the same construction process to create different representations.

```python
from __future__ import annotations
from typing import Self

class Pizza:
    """Product class."""
    
    def __init__(self) -> None:
        self.size: str = ""
        self.cheese: bool = False
        self.pepperoni: bool = False
        self.mushrooms: bool = False
    
    def __str__(self) -> str:
        toppings = []
        if self.cheese:
            toppings.append("cheese")
        if self.pepperoni:
            toppings.append("pepperoni")
        if self.mushrooms:
            toppings.append("mushrooms")
        return f"{self.size} pizza with {', '.join(toppings) if toppings else 'no toppings'}"

class PizzaBuilder:
    """Builder class."""
    
    def __init__(self) -> None:
        self._pizza = Pizza()
    
    def set_size(self, size: str) -> Self:
        self._pizza.size = size
        return self
    
    def add_cheese(self) -> Self:
        self._pizza.cheese = True
        return self
    
    def add_pepperoni(self) -> Self:
        self._pizza.pepperoni = True
        return self
    
    def add_mushrooms(self) -> Self:
        self._pizza.mushrooms = True
        return self
    
    def build(self) -> Pizza:
        return self._pizza

# Usage with method chaining
pizza = (PizzaBuilder()
    .set_size("Large")
    .add_cheese()
    .add_pepperoni()
    .build())
```

### 5. Singleton Pattern

Ensures a class has only one instance and provides a global point of access to it.

```python
from __future__ import annotations
from threading import Lock
from typing import Self

class Singleton:
    """Thread-safe Singleton implementation."""
    
    _instance: Singleton | None = None
    _lock: Lock = Lock()
    
    def __new__(cls) -> Self:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

# Alternative using class method
class AppConfig:
    """Singleton using class method approach."""
    
    _instance: AppConfig | None = None
    _initialized: bool = False
    
    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not AppConfig._initialized:
            self.settings: dict[str, str] = {}
            AppConfig._initialized = True
    
    def get(self, key: str, default: str = "") -> str:
        return self.settings.get(key, default)
    
    def set(self, key: str, value: str) -> None:
        self.settings[key] = value
```

### 6. Prototype Pattern

Creates new objects by copying an existing object (the prototype).

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Self

class Prototype(ABC):
    """Prototype interface."""
    
    @abstractmethod
    def clone(self) -> Self:
        pass

class Document(Prototype):
    """Concrete prototype."""
    
    def __init__(self, title: str, content: str, author: str) -> None:
        self.title = title
        self.content = content
        self.author = author
        self.metadata: dict[str, str] = {}
    
    def clone(self) -> Self:
        return deepcopy(self)
    
    def __str__(self) -> str:
        return f"{self.title} by {self.author}"

# Usage
original = Document("Template", "Content here", "Admin")
original.metadata["created"] = "2024-01-01"

copy = original.clone()
copy.title = "New Document"
# copy has its own copy of metadata
```

---

## Common Mistakes

### 1. Singleton Race Conditions

```python
# Wrong - not thread-safe
class BadSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:  # Race condition here!
            cls._instance = super().__new__(cls)
        return cls._instance

# Right - thread-safe with double-checked locking
class GoodSingleton:
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

### 2. Builder Without Return Self

```python
# Wrong - can't chain
class BadBuilder:
    def set_x(self, x):
        self.x = x  # Missing return self
    
    def set_y(self, y):
        self.y = y

# Right - supports chaining
class GoodBuilder:
    def set_x(self, x) -> Self:
        self.x = x
        return self
    
    def set_y(self, y) -> Self:
        self.y = y
        return self
```

### 3. Factory Confusion

```python
# Wrong - using Factory Method when Simple Factory suffices
def create_notification(type_: str) -> Notification:
    if type_ == "email":
        return EmailNotification()
    elif type_ == "sms":
        return SMSNotification()
    raise ValueError(f"Unknown type: {type_}")

# Right - Factory Method when extensibility is needed
class NotificationFactory(ABC):
    @abstractmethod
    def create(self) -> Notification:
        pass

# New notification types can be added without modifying existing code
```

---

## Connection to Exercises

Today's exercises implement the five creational patterns:

| Problem | Pattern | Skills Practiced |
|---------|---------|------------------|
| 01. Factory Method Notifications | Factory Method | Creator/Product hierarchy, polymorphic creation |
| 02. Abstract Factory UI | Abstract Factory | Product families, platform abstraction |
| 03. Builder Query Object | Builder | Step-by-step construction, method chaining |
| 04. Singleton Config Store | Singleton | Single instance, global access |
| 05. Prototype Document Clone | Prototype | Object cloning, deep copy |

---

## Connection to Game Framework Project

Day 1's creational patterns are used throughout the Game Framework project:

| Pattern | Project Application |
|---------|---------------------|
| **Factory Method** | Creating different entity types (player, enemy, obstacle) |
| **Abstract Factory** | Creating themed entity families (fantasy vs sci-fi game modes) |
| **Builder** | Constructing complex entities with multiple components step-by-step |
| **Singleton** | Global event bus and game state manager |
| **Prototype** | Cloning entity templates for efficient spawning |

### Concrete Example: Entity Creation

```python
# In the project, you'll use a factory to create entities:
from project.starter.entity import Entity
from project.starter.components import PositionComponent, HealthComponent

# Factory method pattern for creating enemy types
class EntityFactory:
    def create_player(self, x: float, y: float) -> Entity:
        entity = Entity("player")
        entity.add_component(PositionComponent(x=x, y=y))
        entity.add_component(HealthComponent(max_health=100))
        return entity
    
    def create_enemy(self, x: float, y: float, health: int) -> Entity:
        entity = Entity("enemy")
        entity.add_component(PositionComponent(x=x, y=y))
        entity.add_component(HealthComponent(max_health=health))
        return entity
```

Understanding creational patterns is essential before building the Game Framework, as you'll need to create many different entity types with varying component configurations.

---

## Quick Reference

```python
from __future__ import annotations

# Factory Method
class Creator(ABC):
    @abstractmethod
    def factory_method(self) -> Product:
        pass

# Abstract Factory
class AbstractFactory(ABC):
    @abstractmethod
    def create_product_a(self) -> ProductA: pass
    @abstractmethod
    def create_product_b(self) -> ProductB: pass

# Builder
class Builder:
    def step1(self) -> Self: ...; return self
    def step2(self) -> Self: ...; return self
    def build(self) -> Product: ...

# Singleton
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Prototype
class Prototype(ABC):
    @abstractmethod
    def clone(self) -> Self: pass
```

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify your implementations
2. Compare the patterns and their use cases
3. Preview Day 2: **Structural Patterns**
