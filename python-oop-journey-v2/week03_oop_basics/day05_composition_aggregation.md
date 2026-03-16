# Week 3, Day 5: Composition and Aggregation

## Learning Objectives

- Understand the difference between composition and aggregation
- Learn to design classes using "has-a" relationships
- Implement composition where the lifetime of parts is managed by the whole
- Implement aggregation where parts can exist independently of the whole
- Apply these concepts to model real-world relationships

---

## 1. Understanding Object Relationships

### Inheritance vs. Composition

Inheritance represents an "is-a" relationship, while composition and aggregation represent "has-a" relationships.

**Inheritance (is-a):**
```python
class Animal:
    pass

class Dog(Animal):  # Dog IS-A Animal
    pass
```

**Composition/Aggregation (has-a):**
```python
class Engine:
    pass

class Car:  # Car HAS-A Engine
    def __init__(self) -> None:
        self.engine = Engine()  # Composition
```

### When to Use Composition Over Inheritance

- When you need to share behavior without forcing a class hierarchy
- When an object's parts can change during its lifetime
- When you want to avoid the fragile base class problem
- When modeling complex objects made of simpler parts

---

## 2. Composition: Strong "Has-A" Relationship

In **composition**, the lifetime of the contained object is managed by the container. If the container is destroyed, the parts are destroyed too.

### Key Characteristics:
- **Strong ownership**: The whole owns the parts
- **Lifetime dependency**: Parts cannot exist without the whole
- **Creation/Destruction**: Parts are typically created with the whole

### Example:
```python
from __future__ import annotations


class Room:
    """A room in a house."""
    
    def __init__(self, name: str, area: float) -> None:
        self.name = name
        self.area = area


class House:
    """A house composed of rooms."""
    
    def __init__(self, address: str) -> None:
        self.address = address
        self.rooms: list[Room] = []
    
    def add_room(self, name: str, area: float) -> Room:
        room = Room(name, area)
        self.rooms.append(room)
        return room
    
    def get_total_area(self) -> float:
        return sum(room.area for room in self.rooms)
    
    def destroy(self) -> None:
        """When house is destroyed, rooms are destroyed too."""
        self.rooms.clear()
```

---

## 3. Aggregation: Weak "Has-A" Relationship

In **aggregation**, the contained objects can exist independently of the container. If the container is destroyed, the parts can still exist.

### Key Characteristics:
- **Weak ownership**: The whole references the parts
- **Independent lifetime**: Parts can exist without the whole
- **External creation**: Parts are typically created outside and passed in

### Example:
```python
from __future__ import annotations


class Student:
    """A student who can belong to multiple departments."""
    
    def __init__(self, name: str, student_id: str) -> None:
        self.name = name
        self.student_id = student_id


class Department:
    """A department that aggregates students."""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.students: list[Student] = []
    
    def add_student(self, student: Student) -> None:
        """Add an existing student to the department."""
        self.students.append(student)
    
    def remove_student(self, student: Student) -> None:
        """Remove a student from the department."""
        self.students.remove(student)
    
    def close_department(self) -> None:
        """When department closes, students still exist."""
        self.students.clear()  # Students continue to exist elsewhere
```

---

## 4. UML Notation

### Composition (Filled Diamond)
```
┌──────────┐     ◆─────────────────┐
│  House   │─────│      Room       │
└──────────┘     └─────────────────┘
```

### Aggregation (Empty Diamond)
```
┌──────────────┐   ◇─────────────────┐
│  Department  │─────│    Student    │
└──────────────┘     └─────────────────┘
```

---

## 5. Practical Examples

### Composition Example: Document and Pages
```python
from __future__ import annotations


class Page:
    """A page in a document."""
    
    def __init__(self, number: int, content: str = "") -> None:
        self.number = number
        self.content = content


class Document:
    """A document composed of pages."""
    
    def __init__(self, title: str) -> None:
        self.title = title
        self.pages: list[Page] = []
    
    def add_page(self, content: str = "") -> Page:
        page = Page(len(self.pages) + 1, content)
        self.pages.append(page)
        return page
    
    def delete_document(self) -> None:
        """Document owns its pages - they are destroyed together."""
        self.pages.clear()
```

### Aggregation Example: University and Professors
```python
from __future__ import annotations


class Professor:
    """A professor who can teach at multiple universities."""
    
    def __init__(self, name: str, specialty: str) -> None:
        self.name = name
        self.specialty = specialty


class University:
    """A university that aggregates professors."""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.professors: list[Professor] = []
    
    def hire_professor(self, professor: Professor) -> None:
        self.professors.append(professor)
    
    def fire_professor(self, professor: Professor) -> None:
        self.professors.remove(professor)
    
    def close_university(self) -> None:
        """Professors continue to exist after university closes."""
        self.professors.clear()
```

---

## 6. Best Practices

### When to Use Composition:
1. When the part cannot exist without the whole
2. When the whole is responsible for creating and destroying parts
3. When parts should not be shared between wholes
4. When you want tight encapsulation

### When to Use Aggregation:
1. When the part can exist independently of the whole
2. When parts are created outside and passed in
3. When parts can be shared between multiple wholes
4. When you need more flexibility in object lifetimes

### Guidelines:
- **Favor composition over inheritance** - it's more flexible
- Use **type hints** for all attributes and method signatures
- **Document ownership** clearly in docstrings
- Consider **immutability** for composed objects when appropriate
- Use **dependency injection** for aggregation relationships

---

## 7. Common Patterns

### The Component Pattern
```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Component(ABC):
    """Base class for all components."""
    
    @abstractmethod
    def operation(self) -> str:
        pass


class Leaf(Component):
    """A leaf component with no children."""
    
    def operation(self) -> str:
        return "Leaf"


class Composite(Component):
    """A composite component that contains other components."""
    
    def __init__(self) -> None:
        self.children: List[Component] = []
    
    def add(self, component: Component) -> None:
        self.children.append(component)
    
    def operation(self) -> str:
        results = [child.operation() for child in self.children]
        return f"Composite({', '.join(results)})"
```

---

## Weekly Project Connection

The Week 3 **E-commerce System** is built entirely on composition:

| Relationship | Type | Description |
|--------------|------|-------------|
| User → ShoppingCart | **Composition** | A User *has* a cart; cart dies with user |
| ShoppingCart → CartItem | **Composition** | Cart owns items; items deleted with cart |
| CartItem → Product | **Aggregation** | Item *references* product; product lives independently |
| User → Order | **Aggregation** | User *has* orders; orders persist if user deleted |
| Order → OrderItem | **Composition** | Order captures snapshot; items owned by order |

**Why composition for the cart?** The shopping cart has no meaning outside the context of a user. If the user is deleted, their cart should disappear too.

**Why aggregation for products?** Products exist independently of carts—multiple users can reference the same product, and products exist in the inventory even when no cart references them.

---

## Exercises

Complete the 8 problems in `exercises/day05/`:

1. **Car Composition** - Car with Engine, Transmission, Wheels
2. **Computer Components** - Computer with CPU, RAM, Storage
3. **Library Collection** - Library with Books, Patrons
4. **Team Roster** - Team with Players, Coach
5. **Restaurant Menu** - Restaurant with MenuItems, Orders
6. **School Classroom** - School with Classrooms, Teachers, Students
7. **Zoo Enclosure** - Zoo with Enclosures, Animals
8. **Company Department** - Company with Departments, Employees

Each exercise demonstrates different aspects of composition and aggregation relationships.

---

## Summary

- **Composition**: Strong ownership, parts die with the whole (filled diamond in UML)
- **Aggregation**: Weak ownership, parts outlive the whole (empty diamond in UML)
- Both represent "has-a" relationships and are preferred over deep inheritance hierarchies
- Choose based on lifetime requirements and ownership semantics
- Use type hints and clear documentation to indicate relationships
