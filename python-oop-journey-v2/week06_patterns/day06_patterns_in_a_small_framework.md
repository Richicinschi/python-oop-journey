# Day 6: Patterns in a Mini Framework

## Learning Objectives

After completing this day, you will be able to:

1. Combine multiple design patterns in a cohesive architecture
2. Implement the Plugin pattern for extensible systems
3. Use the Event Bus pattern (Observer) for decoupled communication
4. Apply the Command pattern for routing and dispatching
5. Implement the Registry pattern for component management
6. Use the Memento pattern for state persistence
7. Know when and how patterns work together to solve complex problems

## Theory

### Why Combine Patterns?

Real systems rarely use just one pattern. Patterns work together to create architectures that are:
- **Extensible**: New features can be added without changing existing code
- **Decoupled**: Components communicate through well-defined interfaces
- **Testable**: Each component can be tested in isolation
- **Maintainable**: Clear boundaries make the code easier to understand

### The Plugin Pattern

The Plugin pattern allows extending functionality without modifying core code:

```python
from abc import ABC, abstractmethod
from typing import Protocol


class GamePlugin(Protocol):
    """Protocol for game plugins."""
    
    @property
    def name(self) -> str: ...
    
    def initialize(self) -> None: ...
    def update(self, delta_time: float) -> None: ...
    def shutdown(self) -> None: ...


class PluginManager:
    """Manages plugin lifecycle."""
    
    def __init__(self) -> None:
        self._plugins: dict[str, GamePlugin] = {}
    
    def register(self, plugin: GamePlugin) -> None:
        self._plugins[plugin.name] = plugin
        plugin.initialize()
    
    def update_all(self, delta_time: float) -> None:
        for plugin in self._plugins.values():
            plugin.update(delta_time)
```

### The Event Bus Pattern

The Event Bus (Observer pattern) enables decoupled communication:

```python
from typing import Callable, Any
from collections import defaultdict


class EventBus:
    """Central event distribution system."""
    
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[..., None]]] = defaultdict(list)
    
    def subscribe(self, event_type: str, handler: Callable[..., None]) -> None:
        self._subscribers[event_type].append(handler)
    
    def publish(self, event_type: str, **kwargs: Any) -> None:
        for handler in self._subscribers.get(event_type, []):
            handler(**kwargs)
```

### The Command Pattern with Dispatcher

Commands encapsulate requests as objects, enabling routing and queuing:

```python
from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass


@dataclass
class CommandContext:
    """Context passed to command execution."""
    args: list[str]
    environment: dict[str, Any]


class Command(ABC):
    """Abstract command."""
    
    @property
    @abstractmethod
    def name(self) -> str: ...
    
    @abstractmethod
    def execute(self, context: CommandContext) -> str: ...


class CommandDispatcher:
    """Routes commands to their handlers."""
    
    def __init__(self) -> None:
        self._commands: dict[str, Command] = {}
    
    def register(self, command: Command) -> None:
        self._commands[command.name] = command
    
    def dispatch(self, name: str, context: CommandContext) -> str:
        if command := self._commands.get(name):
            return command.execute(context)
        return f"Unknown command: {name}"
```

### The Component Registry Pattern

A registry manages components by type or interface:

```python
from typing import TypeVar, Generic, Type, Optional

T = TypeVar("T")


class ComponentRegistry(Generic[T]):
    """Registry for managing components of a specific type."""
    
    def __init__(self) -> None:
        self._components: dict[str, T] = {}
        self._types: dict[str, Type[T]] = {}
    
    def register_type(self, name: str, component_type: Type[T]) -> None:
        self._types[name] = component_type
    
    def create(self, name: str, **kwargs: Any) -> Optional[T]:
        if component_type := self._types.get(name):
            return component_type(**kwargs)
        return None
    
    def register_instance(self, name: str, instance: T) -> None:
        self._components[name] = instance
    
    def get(self, name: str) -> Optional[T]:
        return self._components.get(name)
```

### The Memento Pattern for State Persistence

Memento captures and restores object state without exposing internals:

```python
from dataclasses import dataclass, field
from typing import Any
import json


@dataclass
class GameStateMemento:
    """Immutable state snapshot."""
    player_position: tuple[float, float]
    player_health: int
    inventory: list[str] = field(default_factory=list)
    level: int = 1
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "player_position": self.player_position,
            "player_health": self.player_health,
            "inventory": self.inventory,
            "level": self.level,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GameStateMemento":
        return cls(**data)


class GameState:
    """Originator - creates and restores from mementos."""
    
    def __init__(self) -> None:
        self.player_position = (0.0, 0.0)
        self.player_health = 100
        self.inventory: list[str] = []
        self.level = 1
    
    def save(self) -> GameStateMemento:
        return GameStateMemento(
            player_position=self.player_position,
            player_health=self.player_health,
            inventory=self.inventory.copy(),
            level=self.level,
        )
    
    def restore(self, memento: GameStateMemento) -> None:
        self.player_position = memento.player_position
        self.player_health = memento.player_health
        self.inventory = memento.inventory.copy()
        self.level = memento.level


class SaveManager:
    """Caretaker - manages memento persistence."""
    
    def __init__(self) -> None:
        self._saves: dict[str, str] = {}
    
    def save(self, name: str, memento: GameStateMemento) -> None:
        self._saves[name] = json.dumps(memento.to_dict())
    
    def load(self, name: str) -> Optional[GameStateMemento]:
        if data := self._saves.get(name):
            return GameStateMemento.from_dict(json.loads(data))
        return None
```

### Pattern Integration: A Mini Framework

Here's how patterns work together in a mini game framework:

```python
class MiniGameFramework:
    """Combines patterns into a cohesive architecture."""
    
    def __init__(self) -> None:
        # Observer pattern for events
        self.event_bus = EventBus()
        
        # Plugin pattern for extensibility
        self.plugin_manager = PluginManager()
        
        # Command pattern for actions
        self.command_dispatcher = CommandDispatcher()
        
        # Registry pattern for components
        self.component_registry = ComponentRegistry()
        
        # Memento pattern for save/load
        self.save_manager = SaveManager()
        self.game_state = GameState()
    
    def register_plugin(self, plugin: GamePlugin) -> None:
        """Add extensible behavior."""
        self.plugin_manager.register(plugin)
        # Notify via event bus
        self.event_bus.publish("plugin_loaded", plugin_name=plugin.name)
    
    def execute_command(self, command_name: str, args: list[str]) -> str:
        """Route commands through dispatcher."""
        context = CommandContext(args=args, environment={"framework": self})
        result = self.command_dispatcher.dispatch(command_name, context)
        self.event_bus.publish("command_executed", command=command_name, result=result)
        return result
    
    def save_game(self, slot: str) -> None:
        """Save state via memento."""
        memento = self.game_state.save()
        self.save_manager.save(slot, memento)
        self.event_bus.publish("game_saved", slot=slot)
    
    def load_game(self, slot: str) -> bool:
        """Load state via memento."""
        if memento := self.save_manager.load(slot):
            self.game_state.restore(memento)
            self.event_bus.publish("game_loaded", slot=slot)
            return True
        return False
```

### Pattern Relationships

| Pattern | Role | Interacts With |
|---------|------|----------------|
| Plugin | Extensibility | EventBus (notifies on load) |
| Event Bus | Communication | All patterns publish/subscribe |
| Command | Action routing | EventBus (notifies on execute) |
| Registry | Component lookup | Plugin (registers types) |
| Memento | State persistence | SaveManager (caretaker) |

### When to Use Multiple Patterns

**Use multiple patterns when:**
- You need both extensibility (Plugin) and communication (Event Bus)
- Commands need to be routed (Command + Dispatcher)
- State needs to be saved without exposing internals (Memento + Caretaker)
- Components need discovery (Registry)

**Avoid over-engineering:**
- A simple script doesn't need a full framework
- One pattern might be sufficient for small problems
- Patterns add complexity—justify each one

## Connection to Exercises

Today's exercises integrate multiple patterns into working systems:

| Exercise | Patterns Used | Integration Focus |
|----------|---------------|-------------------|
| 01. Plugin-Driven Game Loop | Plugin + Registry | Dynamic behavior loading |
| 02. Event Bus | Observer + Mediator | Decoupled communication hub |
| 03. Command Dispatcher | Command + Strategy | Routing commands to handlers |
| 04. Component Registry | Registry + Factory | Type-based component creation |
| 05. Save/Load State | Memento + Serializer | State persistence system |

---

## Connection to Game Framework Project

Day 6 directly prepares you for the Game Framework project. The patterns you'll implement today ARE the patterns used in the project:

### Pattern Mapping: Day 6 → Game Framework

| Day 6 Pattern | Game Framework Usage |
|---------------|---------------------|
| **Plugin Pattern** | Plugin system for adding custom behaviors |
| **Event Bus** | Core event system for game communication |
| **Command Dispatcher** | Input handling and action system |
| **Component Registry** | Entity component creation and management |
| **Memento + SaveManager** | Save/load game state |

### The Game Framework IS a Pattern Integration

The project starter gives you a skeleton that combines all these patterns:

```python
# From project/starter/game.py - the core integrates all patterns
class Game:
    def __init__(self):
        self.event_bus = EventBus()           # Observer pattern
        self.component_registry = ComponentRegistry()  # Registry pattern
        self.save_manager = SaveManager()     # Memento pattern
        self.state_machine = GameStateMachine()  # State pattern
        
    def register_system(self, system):
        # Systems use the event bus (Observer)
        self.event_bus.subscribe("update", system.update)
```

### Recommended Approach

1. **Complete today's exercises first** - they teach you the individual pattern combinations
2. **Study the project starter** - see how patterns connect in a larger system
3. **Implement incrementally**:
   - First: Get EventBus working (communication backbone)
   - Second: Add Entity/Component system (data model)
   - Third: Add Systems (behavior)
   - Fourth: Add State management (game flow)
   - Finally: Add Save/Load (persistence)

---

## Summary

- **Plugin Pattern**: Extend functionality without modifying core code
- **Event Bus**: Decoupled publish-subscribe communication
- **Command + Dispatcher**: Encapsulate and route operations
- **Registry**: Manage component types and instances
- **Memento + Caretaker**: Save and restore state without exposing internals
- **Pattern Integration**: Real systems combine patterns for cohesive architectures
- **Tradeoffs**: Each pattern adds complexity—use only when benefits justify costs
