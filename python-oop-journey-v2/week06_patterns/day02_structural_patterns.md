# Day 2: Structural Patterns

## Learning Objectives

By the end of this day, you will be able to:

1. Understand the Adapter pattern for interface compatibility
2. Implement the Decorator pattern for flexible behavior extension
3. Apply the Composite pattern for tree-like structures
4. Use the Facade pattern to simplify complex subsystems
5. Implement the Proxy pattern for access control and lazy loading
6. Choose the appropriate structural pattern for different scenarios

---

## Learning Objectives

By the end of this day, you will be able to:

1. Understand the Adapter pattern for interface compatibility
2. Implement the Decorator pattern for flexible behavior extension
3. Apply the Composite pattern for tree-like structures
4. Use the Facade pattern to simplify complex subsystems
5. Implement the Proxy pattern for access control and lazy loading
6. Choose the appropriate structural pattern for different scenarios

---

## Key Concepts

### 1. Adapter Pattern

The Adapter pattern allows incompatible interfaces to work together. It acts as a bridge between two incompatible interfaces.

**When to use:**
- When you want to use an existing class but its interface doesn't match what you need
- When creating a reusable class that works with unrelated classes
- When you need to adapt a legacy API to a new interface

```python
from abc import ABC, abstractmethod
from __future__ import annotations


class ModernPaymentProcessor(ABC):
    """Target interface expected by client code."""
    
    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> str:
        pass


class LegacyPaymentGateway:
    """Adaptee - existing class with incompatible interface."""
    
    def make_payment(self, amount_in_cents: int, currency_code: str) -> bool:
        # Legacy implementation
        return True


class PaymentAdapter(ModernPaymentProcessor):
    """Adapter that makes LegacyPaymentGateway compatible."""
    
    def __init__(self, legacy_gateway: LegacyPaymentGateway) -> None:
        self._gateway = legacy_gateway
    
    def process_payment(self, amount: float, currency: str) -> str:
        # Convert to legacy format
        amount_in_cents = int(amount * 100)
        success = self._gateway.make_payment(amount_in_cents, currency)
        return "Success" if success else "Failed"
```

### 2. Decorator Pattern

The Decorator pattern allows adding new functionality to objects without altering their structure. It wraps the original object and provides additional behavior.

**When to use:**
- When you need to add responsibilities dynamically
- When extension by subclassing is impractical
- When you want to add functionality that can be removed later

```python
from abc import ABC, abstractmethod
from __future__ import annotations


class TextComponent(ABC):
    """Component interface."""
    
    @abstractmethod
    def render(self) -> str:
        pass


class PlainText(TextComponent):
    """Concrete component."""
    
    def __init__(self, text: str) -> None:
        self._text = text
    
    def render(self) -> str:
        return self._text


class TextDecorator(TextComponent, ABC):
    """Base decorator class."""
    
    def __init__(self, wrapped: TextComponent) -> None:
        self._wrapped = wrapped


class BoldDecorator(TextDecorator):
    """Concrete decorator adding bold formatting."""
    
    def render(self) -> str:
        return f"<b>{self._wrapped.render()}</b>"


class ItalicDecorator(TextDecorator):
    """Concrete decorator adding italic formatting."""
    
    def render(self) -> str:
        return f"<i>{self._wrapped.render()}</i>"
```

### 3. Composite Pattern

The Composite pattern composes objects into tree structures to represent part-whole hierarchies. It lets clients treat individual objects and compositions uniformly.

**When to use:**
- When you need to represent part-whole hierarchies
- When clients should ignore differences between compositions and individual objects
- For tree-like structures (file systems, UI components, organization charts)

```python
from abc import ABC, abstractmethod
from __future__ import annotations


class FileSystemComponent(ABC):
    """Component interface for file system items."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def size(self) -> int:
        pass


class File(FileSystemComponent):
    """Leaf - represents a file."""
    
    def __init__(self, name: str, size: int) -> None:
        self._name = name
        self._size = size
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def size(self) -> int:
        return self._size


class Directory(FileSystemComponent):
    """Composite - can contain files and other directories."""
    
    def __init__(self, name: str) -> None:
        self._name = name
        self._children: list[FileSystemComponent] = []
    
    def add(self, component: FileSystemComponent) -> None:
        self._children.append(component)
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def size(self) -> int:
        return sum(child.size for child in self._children)
```

### 4. Facade Pattern

The Facade pattern provides a simplified interface to a complex subsystem. It hides the complexity of multiple classes behind a single, easier-to-use interface.

**When to use:**
- When you want to provide a simple interface to a complex subsystem
- When there are many dependencies between clients and implementation classes
- When you want to layer your subsystems

```python
from __future__ import annotations


class VideoDecoder:
    def decode(self, file: str) -> str:
        return f"Decoded {file}"


class AudioDecoder:
    def extract(self, file: str) -> str:
        return f"Audio from {file}"


class Renderer:
    def render(self, video: str, audio: str) -> str:
        return "Rendering..."


class MediaPlayerFacade:
    """Simplified interface for media playback."""
    
    def __init__(self) -> None:
        self._video = VideoDecoder()
        self._audio = AudioDecoder()
        self._renderer = Renderer()
    
    def play(self, file: str) -> str:
        video = self._video.decode(file)
        audio = self._audio.extract(file)
        return self._renderer.render(video, audio)
```

### 5. Proxy Pattern

The Proxy pattern provides a placeholder or surrogate for another object to control access to it.

**Types of proxies:**
- **Virtual Proxy:** Delays expensive object creation (lazy loading)
- **Protection Proxy:** Controls access based on permissions
- **Remote Proxy:** Represents objects in different address spaces
- **Caching Proxy:** Stores results of expensive operations

**When to use:**
- When creating an object is expensive and you want to defer it
- When you need access control
- When you need to add logging or caching transparently

```python
from abc import ABC, abstractmethod
from __future__ import annotations


class Image(ABC):
    """Subject interface."""
    
    @abstractmethod
    def display(self) -> str:
        pass


class RealImage(Image):
    """Real subject - expensive to create."""
    
    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._load_from_disk()
    
    def _load_from_disk(self) -> None:
        # Expensive operation
        pass
    
    def display(self) -> str:
        return f"Displaying {self._filename}"


class ImageProxy(Image):
    """Proxy - controls access to RealImage."""
    
    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._real_image: RealImage | None = None
    
    def display(self) -> str:
        # Lazy loading - only create when needed
        if self._real_image is None:
            self._real_image = RealImage(self._filename)
        return self._real_image.display()
```

---

## Pattern Comparison

| Pattern | Purpose | Analogy |
|---------|---------|---------|
| Adapter | Make incompatible interfaces work together | Power plug adapter |
| Decorator | Add behavior dynamically | Russian nesting dolls |
| Composite | Tree structures, part-whole hierarchies | File system |
| Facade | Simplify complex subsystems | TV remote control |
| Proxy | Control access to objects | Bank check (represents money) |

---

## Common Mistakes

1. **Adapter vs Decorator:**
   - Adapter changes interface to match expected one
   - Decorator keeps same interface but adds behavior

2. **Composite overuse:**
   - Don't use composite for flat collections
   - Use it when you need tree structures

3. **Facade bloat:**
   - Keep facade focused on common use cases
   - Don't expose every subsystem feature

4. **Proxy confusion:**
   - Decorator adds functionality
   - Proxy controls access

---

## Exercises

Complete the 5 problems for today:

1. **Problem 01:** Adapter Payment Gateway
2. **Problem 02:** Decorator Text Formatting
3. **Problem 03:** Composite File Tree
4. **Problem 04:** Facade Media System
5. **Problem 05:** Proxy Image Loader

---

## Connection to Game Framework Project

Day 2's structural patterns are fundamental to the Game Framework's architecture:

| Pattern | Project Application |
|---------|---------------------|
| **Adapter** | Unifying different input systems (keyboard, mouse, gamepad) into common interface |
| **Decorator** | Adding visual effects (glow, shield) to entities without modifying base components |
| **Composite** | Scene graph hierarchy - entities can have child entities for complex game objects |
| **Facade** | Simplified Game API that hides ECS complexity from game developers |
| **Proxy** | Lazy loading of game assets (sprites, sounds) only when needed |

### Concrete Example: Scene Graph with Composite

```python
# In the project, the scene uses Composite pattern:
from project.starter.entity import Entity

# Create a complex game object with hierarchy
player_ship = Entity("player_ship")
player_ship.add_component(PositionComponent(x=100, y=100))

# Child entities (weapons, shields) move with parent
left_wing = Entity("left_wing")
right_wing = Entity("right_wing")

# The composite structure allows treating single entities and 
# groups uniformly in the rendering system
render_system.render(scene_root)  # Renders entire tree
```

### Concrete Example: Input Adapter

```python
# The project uses Adapter to normalize different input types:
class KeyboardInput:
    def get_key_state(self, key_code: int) -> bool: ...

class GamepadInput:
    def get_button_state(self, button: str) -> float: ...

# Adapter makes both look the same to the game
class InputAdapter:
    def is_action_pressed(self, action: str) -> bool:
        # Adapts both keyboard and gamepad to common interface
        ...
```

Structural patterns help organize the relationships between game objects and subsystems, making the framework flexible and maintainable.

---

## Additional Resources

- "Design Patterns" by Gang of Four (GoF)
- Python's `functools.wraps` for decorator implementation
- Python's `abc` module for abstract base classes
