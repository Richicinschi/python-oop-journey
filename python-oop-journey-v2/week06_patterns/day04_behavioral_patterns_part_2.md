# Day 4: Behavioral Patterns Part II

## Learning Objectives

By the end of this day, you will be able to:

1. Implement the **Template Method** pattern to define algorithm skeletons
2. Create custom **Iterator** objects for controlled traversal
3. Use the **Visitor** pattern for operations across object structures
4. Apply **Chain of Responsibility** for handling requests flexibly
5. Implement **Memento** for state capture and restoration
6. Understand when each pattern solves real design problems

---

## Key Concepts

### 1. Template Method Pattern

Defines the skeleton of an algorithm in a base class, letting subclasses override specific steps without changing the algorithm's structure.

```python
from __future__ import annotations
from abc import ABC, abstractmethod

class DataMiner(ABC):
    """Template method pattern for data mining algorithms."""
    
    def mine(self, path: str) -> dict:
        """Template method defining the algorithm skeleton."""
        file = self._open_file(path)
        raw_data = self._extract_data(file)
        data = self._parse_data(raw_data)
        analysis = self._analyze(data)
        self._close_file(file)
        return analysis
    
    def _open_file(self, path: str) -> object:
        """Common step - can be overridden but usually not."""
        return open(path, 'r')
    
    @abstractmethod
    def _extract_data(self, file: object) -> str:
        """Abstract step - must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def _parse_data(self, raw_data: str) -> list:
        """Abstract step - must be implemented by subclasses."""
        pass
    
    def _analyze(self, data: list) -> dict:
        """Hook with default implementation - can be overridden."""
        return {"count": len(data), "items": data}
    
    def _close_file(self, file: object) -> None:
        """Common step - can be overridden but usually not."""
        file.close()

class PDFDataMiner(DataMiner):
    """Concrete implementation for PDF files."""
    
    def _extract_data(self, file: object) -> str:
        # PDF-specific extraction
        return "pdf content"
    
    def _parse_data(self, raw_data: str) -> list:
        # PDF-specific parsing
        return raw_data.split()
```

**Key Characteristics:**
- Template method (`mine()`) defines the algorithm steps
- Abstract methods (`_extract_data`, `_parse_data`) must be implemented
- Concrete methods (`_open_file`, `_close_file`) provide common behavior
- Hook methods (`_analyze`) provide default behavior that can be overridden

---

### 2. Iterator Pattern

Provides a way to access elements of an aggregate object sequentially without exposing its underlying representation.

```python
from __future__ import annotations

class BookCollection:
    """Aggregate that can be iterated."""
    
    def __init__(self) -> None:
        self._books: list[str] = []
    
    def add(self, book: str) -> None:
        self._books.append(book)
    
    def __iter__(self) -> BookIterator:
        return BookIterator(self._books)

class BookIterator:
    """Custom iterator for book collection."""
    
    def __init__(self, books: list[str]) -> None:
        self._books = books
        self._index = 0
    
    def __iter__(self) -> BookIterator:
        return self
    
    def __next__(self) -> str:
        if self._index >= len(self._books):
            raise StopIteration
        book = self._books[self._index]
        self._index += 1
        return book
```

**Key Characteristics:**
- Separates traversal logic from collection logic
- Multiple iterators can traverse the same collection independently
- Iterator maintains its own traversal state

---

### 3. Visitor Pattern

Lets you define new operations without changing the classes of the elements on which they operate.

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import override

class ShapeVisitor(ABC):
    """Visitor interface defining operations for each element type."""
    
    @abstractmethod
    def visit_circle(self, circle: Circle) -> str:
        pass
    
    @abstractmethod
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        pass

class Shape(ABC):
    """Element interface - accepts visitors."""
    
    @abstractmethod
    def accept(self, visitor: ShapeVisitor) -> str:
        pass

class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius
    
    @override
    def accept(self, visitor: ShapeVisitor) -> str:
        return visitor.visit_circle(self)

class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
    
    @override
    def accept(self, visitor: ShapeVisitor) -> str:
        return visitor.visit_rectangle(self)

class AreaVisitor(ShapeVisitor):
    """Concrete visitor - calculates area."""
    
    def visit_circle(self, circle: Circle) -> str:
        area = 3.14159 * circle.radius ** 2
        return f"Circle area: {area:.2f}"
    
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        area = rectangle.width * rectangle.height
        return f"Rectangle area: {area:.2f}"

class DrawVisitor(ShapeVisitor):
    """Another concrete visitor - draws shapes."""
    
    def visit_circle(self, circle: Circle) -> str:
        return f"Drawing circle with radius {circle.radius}"
    
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        return f"Drawing rectangle {rectangle.width}x{rectangle.height}"
```

**Key Characteristics:**
- Double dispatch: `element.accept(visitor)` calls `visitor.visit_element(element)`
- New operations can be added without modifying element classes
- Elements must expose their concrete type to visitors

---

### 4. Chain of Responsibility Pattern

Lets you pass requests along a chain of handlers. Each handler decides either to process the request or pass it to the next handler.

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import override

class Handler(ABC):
    """Abstract handler in the chain."""
    
    def __init__(self) -> None:
        self._next: Handler | None = None
    
    def set_next(self, handler: Handler) -> Handler:
        """Set the next handler in the chain."""
        self._next = handler
        return handler  # Allow chaining: h1.set_next(h2).set_next(h3)
    
    def handle(self, request: str) -> str | None:
        """Handle request or pass to next handler."""
        result = self._process(request)
        if result is not None:
            return result
        if self._next:
            return self._next.handle(request)
        return None
    
    @abstractmethod
    def _process(self, request: str) -> str | None:
        """Process the request. Return None to pass to next handler."""
        pass

class SupportAgent(Handler):
    """Concrete handler - handles simple requests."""
    
    @override
    def _process(self, request: str) -> str | None:
        if request in ["password_reset", "login_help"]:
            return f"SupportAgent handled: {request}"
        return None

class TechnicalSupport(Handler):
    """Concrete handler - handles technical issues."""
    
    @override
    def _process(self, request: str) -> str | None:
        if request in ["bug_report", "performance_issue"]:
            return f"TechnicalSupport handled: {request}"
        return None

class Manager(Handler):
    """Concrete handler - handles escalations."""
    
    @override
    def _process(self, request: str) -> str | None:
        if request in ["refund", "complaint"]:
            return f"Manager handled: {request}"
        return None

# Usage
chain = SupportAgent()
chain.set_next(TechnicalSupport()).set_next(Manager())

result = chain.handle("bug_report")  # "TechnicalSupport handled: bug_report"
result = chain.handle("refund")      # "Manager handled: refund"
```

**Key Characteristics:**
- Decouples sender from receivers
- Chain can be changed dynamically
- Request may reach end of chain unhandled

---

### 5. Memento Pattern

Lets you save and restore the previous state of an object without revealing its implementation details.

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import override

@dataclass(frozen=True)
class TextMemento:
    """Memento - immutable snapshot of editor state."""
    content: str
    cursor_position: int
    timestamp: str

class TextEditor:
    """Originator - creates and restores from mementos."""
    
    def __init__(self) -> None:
        self._content = ""
        self._cursor_position = 0
    
    def type_text(self, text: str) -> None:
        """Modify state."""
        self._content = self._content[:self._cursor_position] + text
        self._cursor_position += len(text)
    
    def save(self) -> TextMemento:
        """Create memento of current state."""
        from datetime import datetime
        return TextMemento(
            content=self._content,
            cursor_position=self._cursor_position,
            timestamp=datetime.now().isoformat()
        )
    
    def restore(self, memento: TextMemento) -> None:
        """Restore state from memento."""
        self._content = memento.content
        self._cursor_position = memento.cursor_position
    
    def get_content(self) -> str:
        return self._content

class History:
    """Caretaker - manages mementos without accessing their contents."""
    
    def __init__(self) -> None:
        self._mementos: list[TextMemento] = []
    
    def push(self, memento: TextMemento) -> None:
        self._mementos.append(memento)
    
    def pop(self) -> TextMemento | None:
        if self._mementos:
            return self._mementos.pop()
        return None
    
    def can_undo(self) -> bool:
        return len(self._mementos) > 0
```

**Key Characteristics:**
- **Originator** (`TextEditor`): Creates and uses mementos
- **Memento** (`TextMemento`): Stores state, immutable, opaque to caretaker
- **Caretaker** (`History`): Manages mementos without accessing contents

---

## Pattern Comparison

| Pattern | Problem Solved | Key Benefit |
|---------|---------------|-------------|
| Template Method | Common algorithm, varying steps | Code reuse, algorithm structure protected |
| Iterator | Sequential access without exposing structure | Multiple traversals, clean separation |
| Visitor | New operations on existing classes | Add operations without modifying elements |
| Chain of Responsibility | Dynamic request handling | Decoupling, flexible processing chains |
| Memento | State capture and undo | Encapsulation preserved, state history |

---

## Common Mistakes

### 1. Template Method: Making Template Method Overridable

```python
# Wrong - template method should be final
class DataMiner:
    def mine(self):  # Missing protection
        pass

# Right - use naming or documentation to indicate finality
class DataMiner:
    def mine(self) -> dict:
        """Template method - DO NOT OVERRIDE."""
        # ...
```

### 2. Iterator: Not Supporting Multiple Iterations

```python
# Wrong - iterator can't be reused
iterator = BookIterator(books)
list(iterator)  # First iteration works
list(iterator)  # Second iteration empty!

# Right - create fresh iterator each time
class BookCollection:
    def __iter__(self) -> BookIterator:
        return BookIterator(self._books.copy())  # Fresh iterator
```

### 3. Visitor: Breaking Encapsulation

```python
# Wrong - visitor accesses private data
class BadVisitor(ShapeVisitor):
    def visit_circle(self, circle: Circle) -> str:
        return str(circle._private_data)  # Don't do this!

# Right - use public interface or accept limited access
class GoodVisitor(ShapeVisitor):
    def visit_circle(self, circle: Circle) -> str:
        return f"Radius: {circle.radius}"  # Public attribute
```

### 4. Chain of Responsibility: Infinite Loops

```python
# Wrong - circular chain
handler1.set_next(handler2)
handler2.set_next(handler1)  # Circular!

# Right - linear chain, check for cycles
```

### 5. Memento: Mutable Mementos

```python
# Wrong - memento can be modified
@dataclass
class BadMemento:
    state: list  # Mutable reference!

# Right - immutable or defensive copy
@dataclass(frozen=True)
class GoodMemento:
    state: tuple  # Immutable
```

---

## Connection to Exercises

| Problem | Pattern Practiced |
|---------|-------------------|
| 01. Template Report Pipeline | Template Method |
| 02. Iterator Menu System | Iterator |
| 03. Visitor Shape Export | Visitor |
| 04. Chain of Responsibility Support Tickets | Chain of Responsibility |
| 05. Memento Text History | Memento |

---

## Weekly Project Connection

The Week 6 project involves a **Game Framework**. Today's patterns are essential because:

- **Template Method**: Game loop phases, entity update sequences
- **Iterator**: Game world traversal, entity collections
- **Visitor**: Save/load systems, entity serialization
- **Chain of Responsibility**: Input handling, event propagation
- **Memento**: Save game states, undo/redo functionality

---

## Quick Reference

```python
# Template Method
class Algorithm(ABC):
    def template(self):      # Template method
        self.step1()
        self.step2()         # Abstract
        self.step3()         # Hook with default
    
    @abstractmethod
    def step2(self): pass

# Iterator
class Iterator:
    def __iter__(self): return self
    def __next__(self):  # Return item or raise StopIteration
        pass

# Visitor
class Visitor(ABC):
    def visit_a(self, a): pass
    def visit_b(self, b): pass

class Element(ABC):
    def accept(self, visitor): pass  # Calls visitor.visit_x(self)

# Chain of Responsibility
class Handler:
    def set_next(self, handler): pass
    def handle(self, request):    # Pass to next if not handled
        pass

# Memento
@dataclass(frozen=True)
class Memento:
    state: Any

class Originator:
    def save(self) -> Memento: pass
    def restore(self, m: Memento): pass
```

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify your solutions
2. Consider when each pattern is appropriate
3. Review the tradeoffs - patterns add complexity
4. Preview Day 5: **Pattern Tradeoffs and Anti-Patterns**
