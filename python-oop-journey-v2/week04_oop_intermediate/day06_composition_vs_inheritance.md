# Day 6: Composition vs Inheritance

## Learning Objectives

After completing this day, you will understand:
- The difference between "is-a" (inheritance) and "has-a" (composition) relationships
- When to prefer composition over inheritance
- How to implement the Strategy pattern using composition
- How to build plugin architectures with composition
- The Repository pattern for data access abstraction

## Theory

### Inheritance vs Composition

**Inheritance** represents an "is-a" relationship:
```python
class Animal:
    pass

class Dog(Animal):  # Dog IS-A Animal
    pass
```

**Composition** represents a "has-a" relationship:
```python
class Engine:
    pass

class Car:
    def __init__(self):
        self.engine = Engine()  # Car HAS-A Engine
```

### The "Favor Composition Over Inheritance" Principle

Inheritance creates tight coupling between parent and child:
- Changes to parent affect all children
- Deep hierarchies become hard to understand
- Multiple inheritance can lead to diamond problems
- You inherit everything, wanted or not

Composition is more flexible:
- Components can be swapped at runtime
- Behavior can be changed without modifying the class
- Classes remain focused and cohesive
- Testing is easier with mock components

### When to Use Inheritance

Use inheritance when:
- The relationship is truly "is-a" and will always be
- You want to share implementation details
- The Liskov Substitution Principle holds (child can substitute parent)
- You're creating a framework/extension point

### The Strategy Pattern

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable.

```python
from abc import ABC, abstractmethod
from typing import Protocol


class SortStrategy(Protocol):
    """Protocol for sorting strategies."""
    
    def sort(self, data: list[int]) -> list[int]: ...


class BubbleSort:
    def sort(self, data: list[int]) -> list[int]:
        result = data.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result


class QuickSort:
    def sort(self, data: list[int]) -> list[int]:
        if len(data) <= 1:
            return data.copy()
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)


class Sorter:
    """Uses composition to allow strategy swapping."""
    
    def __init__(self, strategy: SortStrategy) -> None:
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy
    
    def sort(self, data: list[int]) -> list[int]:
        return self._strategy.sort(data)
```

### Composition for Behaviors

Instead of inheritance hierarchies, compose behaviors:

```python
from abc import ABC, abstractmethod


class FlyBehavior(ABC):
    @abstractmethod
    def fly(self) -> str: ...


class FlyWithWings(FlyBehavior):
    def fly(self) -> str:
        return "Flying with wings!"


class CannotFly(FlyBehavior):
    def fly(self) -> str:
        return "Cannot fly."


class QuackBehavior(ABC):
    @abstractmethod
    def quack(self) -> str: ...


class Quack(QuackBehavior):
    def quack(self) -> str:
        return "Quack!"


class Squeak(QuackBehavior):
    def quack(self) -> str:
        return "Squeak!"


class Duck:
    """A duck that composes its behaviors."""
    
    def __init__(
        self,
        name: str,
        fly_behavior: FlyBehavior,
        quack_behavior: QuackBehavior
    ) -> None:
        self.name = name
        self._fly_behavior = fly_behavior
        self._quack_behavior = quack_behavior
    
    def fly(self) -> str:
        return self._fly_behavior.fly()
    
    def quack(self) -> str:
        return self._quack_behavior.quack()
    
    def set_fly_behavior(self, behavior: FlyBehavior) -> None:
        self._fly_behavior = behavior
```

### Plugin Architecture

Composition enables plugin systems:

```python
from abc import ABC, abstractmethod
from typing import TypeVar


T = TypeVar("T")


class Plugin(ABC):
    @abstractmethod
    def activate(self) -> str: ...
    
    @abstractmethod
    def deactivate(self) -> str: ...


class PluginManager:
    """Manages plugins through composition."""
    
    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}
    
    def register(self, name: str, plugin: Plugin) -> None:
        self._plugins[name] = plugin
    
    def activate_all(self) -> list[str]:
        return [p.activate() for p in self._plugins.values()]
```

### Repository Pattern

The Repository pattern abstracts data access:

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional


T = TypeVar("T")
K = TypeVar("K")


class Repository(ABC, Generic[T, K]):
    """Abstract repository for type T with key type K."""
    
    @abstractmethod
    def get(self, id: K) -> Optional[T]: ...
    
    @abstractmethod
    def save(self, item: T) -> None: ...
    
    @abstractmethod
    def delete(self, id: K) -> bool: ...
    
    @abstractmethod
    def get_all(self) -> list[T]: ...


class User:
    def __init__(self, user_id: int, name: str) -> None:
        self.user_id = user_id
        self.name = name


class InMemoryUserRepository(Repository[User, int]):
    """In-memory implementation of User repository."""
    
    def __init__(self) -> None:
        self._users: dict[int, User] = {}
    
    def get(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)
    
    def save(self, user: User) -> None:
        self._users[user.user_id] = user
    
    def delete(self, user_id: int) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False
    
    def get_all(self) -> list[User]:
        return list(self._users.values())
```

### Refactoring from Inheritance to Composition

**Before (Inheritance):**
```python
class Vehicle:
    def __init__(self, brand: str) -> None:
        self.brand = brand

class ElectricVehicle(Vehicle):
    def __init__(self, brand: str, battery_capacity: float) -> None:
        super().__init__(brand)
        self.battery_capacity = battery_capacity

class GasVehicle(Vehicle):
    def __init__(self, brand: str, tank_capacity: float) -> None:
        super().__init__(brand)
        self.tank_capacity = tank_capacity
```

**After (Composition):**
```python
from abc import ABC, abstractmethod


class PowerSource(ABC):
    @abstractmethod
    def describe(self) -> str: ...


class Battery(PowerSource):
    def __init__(self, capacity: float) -> None:
        self.capacity = capacity
    
    def describe(self) -> str:
        return f"Battery: {self.capacity} kWh"


class GasTank(PowerSource):
    def __init__(self, capacity: float) -> None:
        self.capacity = capacity
    
    def describe(self) -> str:
        return f"Gas Tank: {self.capacity} gallons"


class Vehicle:
    def __init__(self, brand: str, power_source: PowerSource) -> None:
        self.brand = brand
        self.power_source = power_source
```

---

## Common Mistakes

### 1. Using Inheritance for Code Sharing Only

```python
# WRONG - No true "is-a" relationship
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height

class Square(Rectangle):  # Problematic!
    def __init__(self, side: float) -> None:
        super().__init__(side, side)
    
    def set_width(self, width: float) -> None:
        self.width = width
        # Oops! height is now out of sync

# RIGHT - Use composition
class Square:
    def __init__(self, side: float) -> None:
        self._side = side
    
    @property
    def width(self) -> float:
        return self._side
    
    @property
    def height(self) -> float:
        return self._side
    
    def area(self) -> float:
        return self._side ** 2
```

### 2. Deep Inheritance Hierarchies

```python
# WRONG - Hard to understand, brittle
class Animal:
    pass

class Mammal(Animal):
    pass

class Primate(Mammal):
    pass

class GreatApe(Primate):
    pass

class Chimpanzee(GreatApe):
    pass

# RIGHT - Flatten with composition
class Animal:
    def __init__(self, species: str, traits: list[Trait]) -> None:
        self.species = species
        self.traits = traits

class Trait:
    pass

class MammalTrait(Trait):
    pass

class PrimateTrait(Trait):
    pass
```

### 3. Mixing Is-A and Has-A Confusion

```python
# WRONG - A car is not an engine
class Engine:
    def start(self) -> str:
        return "Engine started"

class Car(Engine):  # Wrong! Car is not an Engine
    pass

# RIGHT - Car has an Engine
class Car:
    def __init__(self) -> None:
        self.engine = Engine()
    
    def start(self) -> str:
        return self.engine.start()
```

### 4. Premature Abstraction

```python
# WRONG - Over-engineering simple cases
from abc import ABC, abstractmethod

class Greeter(ABC):
    @abstractmethod
    def greet(self, name: str) -> str: ...

class FormalGreeter(Greeter):
    def greet(self, name: str) -> str:
        return f"Good day, {name}."

class CasualGreeter(Greeter):
    def greet(self, name: str) -> str:
        return f"Hey {name}!"

# RIGHT - Start simple, add complexity when needed
def formal_greet(name: str) -> str:
    return f"Good day, {name}."

def casual_greet(name: str) -> str:
    return f"Hey {name}!"
```

---

## Connection to Exercises

Today's exercises practice choosing and implementing the right relationship:

| Exercise | Focus Area | Key Decision |
|----------|-----------|--------------|
| 01. weapon_system | Weapon behaviors with composition | Strategy pattern |
| 02. document_processor | Processor composition | Plugin architecture |
| 03. character_builder | Character attributes via composition | Flexible character creation |
| 04. database_connection | Repository pattern | Data access abstraction |
| 05. notification_service | Notification channels via composition | Multiple notification types |
| 06. vehicle_assembly | Vehicle parts composition | Building complex objects |
| 07. plugin_system | Plugin manager architecture | Runtime extensibility |

---

## Connection to Weekly Project

The Animal Shelter Management System demonstrates when to use each approach:

### Inheritance (Is-A)
- **Animal hierarchy**: Dog IS-A Animal, Cat IS-A Animal - proper inheritance
- **Staff roles**: Veterinarian IS-A StaffMember - role specialization

### Composition (Has-A)
- **Enclosure**: Shelter HAS-A Enclosures, Enclosure HAS-A Animals
- **Medical records**: Animal HAS-A MedicalRecord (not IS-A MedicalRecord)
- **Adoption system**: Shelter HAS-A AdoptionManager
- **Staff assignments**: Enclosure HAS-A assigned Caretaker

### The Key Lesson
The project uses inheritance for the natural type hierarchies (animals, staff) and composition for the management relationships (shelter contains things, enclosures contain animals).

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify: `pytest week04_oop_intermediate/tests/day06/ -v`
2. Review any problems you found challenging
3. Start the **Animal Shelter Management System** project to apply all Week 4 concepts
4. Review Week 4: Which concepts were most challenging? Revisit those exercises.

---

## Summary

- **Composition** provides "has-a" relationships and greater flexibility
- **Inheritance** provides "is-a" relationships but creates tight coupling
- **Strategy Pattern** lets you vary algorithms by composing different strategies
- **Plugin Architecture** uses composition for extensible systems
- **Repository Pattern** abstracts data access through composition
- "Favor composition over inheritance" is a guideline, not a rule—use the right tool
