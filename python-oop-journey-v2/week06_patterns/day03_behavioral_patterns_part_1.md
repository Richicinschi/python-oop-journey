# Day 3: Behavioral Patterns Part I

## Overview

Behavioral patterns focus on communication between objects, how they interact, and how responsibilities are distributed. Unlike creational or structural patterns that deal with object instantiation and composition, behavioral patterns address the flow of control and data through a system.

Today we cover five fundamental behavioral patterns: **Observer**, **Strategy**, **Command**, **State**, and **Mediator**. These patterns help you build flexible, decoupled systems where objects can communicate without tight coupling.

## Learning Objectives

By the end of today, you will be able to:

- Implement the **Observer** pattern for publish-subscribe scenarios
- Apply the **Strategy** pattern to encapsulate interchangeable algorithms
- Use the **Command** pattern to encapsulate requests as objects
- Implement the **State** pattern for object state management
- Apply the **Mediator** pattern to reduce direct object communication

## Key Concepts

### 1. Observer Pattern

The Observer pattern defines a one-to-many dependency between objects. When one object (the subject) changes state, all its dependents (observers) are notified automatically.

**When to use:**
- Event handling systems
- Model-View architectures
- Distributed event handling
- Stock tickers, news feeds, or any publish-subscribe scenario

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    """Abstract observer interface."""
    
    @abstractmethod
    def update(self, subject: Subject) -> None:
        """Receive update from subject."""
        pass

class Subject(ABC):
    """Abstract subject interface."""
    
    def __init__(self) -> None:
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """Add an observer."""
        self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Remove an observer."""
        self._observers.remove(observer)
    
    def notify(self) -> None:
        """Notify all observers."""
        for observer in self._observers:
            observer.update(self)

class ConcreteSubject(Subject):
    """Subject with state that observers watch."""
    
    def __init__(self) -> None:
        super().__init__()
        self._state: int = 0
    
    @property
    def state(self) -> int:
        return self._state
    
    @state.setter
    def state(self, value: int) -> None:
        self._state = value
        self.notify()  # Notify observers on change
```

**Key insight:** The subject doesn't know what observers do with the notification—it only knows they have an `update()` method. This loose coupling is the pattern's strength.

### 2. Strategy Pattern

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

**When to use:**
- Multiple ways to perform an operation
- Need to switch algorithms at runtime
- Avoiding massive conditional statements
- Isolating algorithm implementation details

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

class SortStrategy(ABC):
    """Abstract strategy interface."""
    
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        """Sort the data and return result."""
        pass

class BubbleSortStrategy(SortStrategy):
    """Concrete strategy: Bubble Sort."""
    
    def sort(self, data: List[int]) -> List[int]:
        result = data.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result

class QuickSortStrategy(SortStrategy):
    """Concrete strategy: Quick Sort."""
    
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data.copy()
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class Sorter:
    """Context class that uses a strategy."""
    
    def __init__(self, strategy: SortStrategy) -> None:
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy) -> None:
        """Change strategy at runtime."""
        self._strategy = strategy
    
    def sort(self, data: List[int]) -> List[int]:
        """Delegate to the current strategy."""
        return self._strategy.sort(data)

# Usage
sorter = Sorter(QuickSortStrategy())
result = sorter.sort([3, 1, 4, 1, 5])
sorter.set_strategy(BubbleSortStrategy())  # Switch strategy
```

**Key insight:** The context (Sorter) delegates to the strategy. The client can change algorithms without modifying the context's code.

### 3. Command Pattern

The Command pattern encapsulates a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.

**When to use:**
- Undo/redo functionality
- Queueing operations
- Logging changes
- Macro recording
- Decoupling sender from receiver

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

class Command(ABC):
    """Abstract command interface."""
    
    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        pass
    
    @abstractmethod
    def undo(self) -> None:
        """Undo the command."""
        pass

class Light:
    """Receiver class."""
    
    def __init__(self) -> None:
        self._on = False
    
    def on(self) -> None:
        self._on = True
    
    def off(self) -> None:
        self._on = False

class LightOnCommand(Command):
    """Concrete command to turn light on."""
    
    def __init__(self, light: Light) -> None:
        self._light = light
    
    def execute(self) -> None:
        self._light.on()
    
    def undo(self) -> None:
        self._light.off()

class RemoteControl:
    """Invoker class."""
    
    def __init__(self) -> None:
        self._commands: List[Command] = []
    
    def execute(self, command: Command) -> None:
        command.execute()
        self._commands.append(command)
    
    def undo_last(self) -> None:
        if self._commands:
            self._commands.pop().undo()
```

**Key insight:** Commands decouple the object that invokes the operation from the object that performs it. This enables features like undo/redo and macro recording.

### 4. State Pattern

The State pattern allows an object to alter its behavior when its internal state changes. The object will appear to change its class.

**When to use:**
- An object's behavior depends on its state
- Complex conditional statements based on state
- State-specific behavior that should be independent
- State transitions need to be explicit and controlled

```python
from __future__ import annotations
from abc import ABC, abstractmethod

class State(ABC):
    """Abstract state interface."""
    
    def __init__(self, context: TrafficLight) -> None:
        self._context = context
    
    @abstractmethod
    def handle(self) -> str:
        """Handle the current state and transition to next."""
        pass

class RedState(State):
    """Red light state."""
    
    def handle(self) -> str:
        self._context.state = GreenState(self._context)
        return "Red -> Green"

class GreenState(State):
    """Green light state."""
    
    def handle(self) -> str:
        self._context.state = YellowState(self._context)
        return "Green -> Yellow"

class YellowState(State):
    """Yellow light state."""
    
    def handle(self) -> str:
        self._context.state = RedState(self._context)
        return "Yellow -> Red"

class TrafficLight:
    """Context class with state."""
    
    def __init__(self) -> None:
        self._state: State = RedState(self)
    
    @property
    def state(self) -> State:
        return self._state
    
    @state.setter
    def state(self, state: State) -> None:
        self._state = state
    
    def change(self) -> str:
        """Trigger state transition."""
        return self._state.handle()
```

**Key insight:** Each state is a class with its own behavior. The context delegates state-specific behavior to the current state object. This eliminates long conditional chains.

### 5. Mediator Pattern

The Mediator pattern defines an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly.

**When to use:**
- Many objects communicate in complex ways
- Reusing an object is difficult due to many references
- Custom behavior distributed between several classes should be customizable without subclassing

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict

class Mediator(ABC):
    """Abstract mediator interface."""
    
    @abstractmethod
    def send(self, message: str, sender: Component) -> None:
        """Send message to appropriate recipients."""
        pass

class Component(ABC):
    """Abstract component that communicates through mediator."""
    
    def __init__(self, mediator: Mediator) -> None:
        self._mediator = mediator
    
    def send(self, message: str) -> None:
        """Send message through mediator."""
        self._mediator.send(message, self)
    
    @abstractmethod
    def receive(self, message: str) -> None:
        """Receive a message."""
        pass

class ChatRoom(Mediator):
    """Concrete mediator: Chat room."""
    
    def __init__(self) -> None:
        self._participants: Dict[str, User] = {}
    
    def register(self, user: User) -> None:
        """Register a user."""
        self._participants[user.name] = user
    
    def send(self, message: str, sender: Component) -> None:
        """Broadcast message to all except sender."""
        for name, user in self._participants.items():
            if user != sender:
                user.receive(f"[{sender.name}]: {message}")

class User(Component):
    """Concrete component: Chat user."""
    
    def __init__(self, name: str, mediator: Mediator) -> None:
        super().__init__(mediator)
        self.name = name
        self.messages: List[str] = []
    
    def receive(self, message: str) -> None:
        """Receive message."""
        self.messages.append(message)
```

**Key insight:** Objects don't communicate directly—they go through the mediator. This centralizes complex communication logic and reduces coupling.

## Pattern Comparison

| Pattern | Purpose | Decouples |
|---------|---------|-----------|
| Observer | One-to-many notification | Subject from observers |
| Strategy | Interchangeable algorithms | Context from algorithms |
| Command | Encapsulate requests | Invoker from receiver |
| State | State-dependent behavior | Context from state logic |
| Mediator | Centralized communication | Colleagues from each other |

## Common Mistakes

### 1. Observer: Memory Leaks

```python
# PROBLEM: Strong references prevent garbage collection
class Subject:
    def __init__(self):
        self._observers: List[Observer] = []  # Strong refs

# SOLUTION: Use weak references for observers that might outlive the subject
import weakref
class Subject:
    def __init__(self):
        self._observers: weakref.WeakSet[Observer] = weakref.WeakSet()
```

### 2. Strategy: Context Knows Too Much

```python
# PROBLEM: Context inspects strategy type
if isinstance(self._strategy, QuickSortStrategy):
    pass  # Do something special

# SOLUTION: Let strategies handle their own differences
# Strategy interface should be complete enough
```

### 3. Command: Not Implementing Undo

```python
# PROBLEM: Undo not properly implemented
class DeleteCommand(Command):
    def execute(self) -> None:
        self._document.delete(self._position)
    
    def undo(self) -> None:
        pass  # Empty! Can't restore!

# SOLUTION: Save state needed for undo
class DeleteCommand(Command):
    def __init__(self, document: Document, position: int):
        self._document = document
        self._position = position
        self._deleted_text: str = ""
    
    def execute(self) -> None:
        self._deleted_text = self._document.get_text(self._position)
        self._document.delete(self._position)
    
    def undo(self) -> None:
        self._document.insert(self._position, self._deleted_text)
```

### 4. State: Context Reaches Into State

```python
# PROBLEM: Context accessing state internals
if isinstance(self._state, DraftState) and self._state._edited:
    pass  # Logic that should be in state

# SOLUTION: Let state handle its own behavior
self._state.handle_save()  # State decides what to do
```

### 5. Mediator: God Object

```python
# PROBLEM: Mediator grows too complex
class Mediator:
    def method1(self): ...
    def method2(self): ...
    # 50 more methods...

# SOLUTION: Consider if multiple mediators would help
# Or if some coordination belongs elsewhere
```

## Best Practices

1. **Observer**: Consider event objects instead of multiple update parameters
2. **Strategy**: Keep strategy interface minimal but complete
3. **Command**: Implement CommandHistory for undo/redo; consider immutability
4. **State**: Make state transitions explicit; document the state machine
5. **Mediator**: Keep mediator focused; don't let it become a god object

## Connection to Exercises

| Exercise | Pattern | Key Learning |
|----------|---------|--------------|
| 01. Stock Ticker | Observer | Subject/observer lifecycle, dynamic attachment |
| 02. Sort Engine | Strategy | Runtime algorithm switching |
| 03. Text Editor | Command | Undo/redo, command history |
| 04. Order Lifecycle | State | State transitions, state-specific behavior |
| 05. Chat Room | Mediator | Colleague decoupling, message routing |

## Connection to Weekly Project

These patterns are essential for the Game Framework project:
- **Observer**: Event system for game events
- **Command**: Input handling and action recording
- **State**: Game state management (menu, playing, paused)

## Key Takeaways

1. **Behavioral patterns manage communication** - They control how objects interact
2. **Decoupling is the goal** - Objects shouldn't know too much about each other
3. **Composition over inheritance** - These patterns favor object composition
4. **Explicit is better than implicit** - State machines and command histories make behavior clear
5. **Trade-offs exist** - More flexibility often means more complexity

## Further Reading

- "Design Patterns" by Gamma, Helm, Johnson, Vlissides (Gang of Four)
- "Head First Design Patterns" by Freeman & Robson
- Python's `abc` module documentation
- Python's `weakref` module for Observer memory management

## Time Estimate

- Reading: 45-60 minutes
- Exercises: 3-4 hours
- Review: 30 minutes
