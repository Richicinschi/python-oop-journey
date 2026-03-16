# Week 6 Project: Game Framework

A modular game framework demonstrating design patterns including Entity-Component-System (ECS), Observer pattern, State pattern, and plugin architecture.

## Goal

Build a working game framework that demonstrates how multiple design patterns work together to solve real architectural problems. By completing this project, you will:

- Implement a complete Entity-Component-System (ECS) architecture
- Use the Observer pattern for decoupled event-driven communication
- Apply the State pattern for clean game state management
- Create an extensible plugin system using Strategy pattern concepts
- Understand how patterns compose to build flexible, maintainable code

## Files That Matter Most

### Starter Files (Your Work Area)
```
starter/
├── entity.py       # Entity and EntityManager classes
├── components.py   # Component base class and specific components
├── systems.py      # System base class and game systems
├── events.py       # Event class and EventBus (Observer pattern)
└── game.py         # Game engine, GameState, and Plugin classes
```

### Key Files to Study
```
reference_solution/
├── entity.py       # Complete Entity and EntityManager implementation
├── components.py   # Complete component system with data classes
├── systems.py      # Physics, Render, Health, Collision systems
├── events.py       # EventBus implementing Observer pattern
└── game.py         # Complete Game engine with State pattern
```

### Tests
```
tests/
└── test_game_framework.py   # 114 tests covering all functionality
```

## Public Contract

The framework provides these public APIs:

### Entity-Component System
```python
# Create and manage entities
entity = Entity("player")                    # Create with ID
entity = Entity()                            # Auto-generate ID
entity.add_component(PositionComponent(x=0, y=0))
entity.get_component(PositionComponent)      # Returns component or None
entity.has_component(PositionComponent)      # Returns bool
entity.remove_component(PositionComponent)   # Returns bool
entity.activate() / entity.deactivate()      # Control entity lifecycle

# EntityManager for bulk operations
manager = EntityManager()
entity = manager.create_entity("id")
entities = manager.get_entities_with_component(PositionComponent)
entities = manager.get_entities_with_components(Position, Velocity)
```

### Event System (Observer Pattern)
```python
# Subscribe to events
bus = EventBus()
bus.subscribe("collision", callback_function)
bus.unsubscribe("collision", callback_function)

# Publish events
bus.publish("damage", {"amount": 10, "target": entity})

# Global event bus singleton
bus = get_global_event_bus()
reset_global_event_bus()  # For testing
```

### Game Systems
```python
# Systems process entities with specific components
physics = PhysicsSystem(priority=10)
render = RenderSystem(priority=100)
health = HealthSystem(priority=20)
collision = CollisionSystem(priority=30)

# Systems update automatically in priority order
system_manager.update(delta_time, entities)
```

### Game State Management
```python
# State pattern for game states
menu = MenuState()
playing = PlayingState()
paused = PausedState(previous_state=playing)
game_over = GameOverState(winner="Player 1")

# State transitions
game.change_state(menu)      # Replace current state
game.push_state(paused)      # Pause current, push new
game.pop_state()             # Return to previous state
```

### Plugin System
```python
# Create custom plugins
class MyPlugin(Plugin):
    def on_register(self, game):
        # Add systems, entities, or behaviors
        pass
    
    def on_unregister(self, game):
        # Cleanup
        pass

# Register with game
game.register_plugin(MyPlugin("my_plugin"))
```

## How to Approach the Starter

### Recommended Implementation Order

1. **Start with Components** (`components.py`)
   - Implement `Component` base class with entity reference
   - Implement `PositionComponent`, `VelocityComponent`, `HealthComponent`
   - Use `@dataclass` for clean component definitions
   - Add `__post_init__` to call `super().__init__()`

2. **Implement Events** (`events.py`)
   - Implement `Event` class with type, data, sender
   - Implement `EventBus` with subscribe/unsubscribe/publish
   - Use `defaultdict(list)` for subscriber storage
   - Implement global event bus singleton

3. **Build Entities** (`entity.py`)
   - Entity is just an ID + component dictionary
   - Implement component add/get/remove/has methods
   - Implement `EntityManager` with component indexing
   - The component index tracks which entities have which components

4. **Create Systems** (`systems.py`)
   - System base class with priority and enabled flag
   - `PhysicsSystem`: Update Position from Velocity
   - `RenderSystem`: Collect visible entities sorted by layer
   - `HealthSystem`: Track dead entities
   - `SystemManager`: Update systems in priority order

5. **Assemble the Game** (`game.py`)
   - Implement `GameState` base class with enter/update/exit
   - Implement concrete states: Menu, Playing, Paused, GameOver
   - Implement `Plugin` base class
   - Implement `Game` class tying everything together

### Key Implementation Details

**Entity-Component Relationship:**
- Components store data only (no behavior)
- Components have an `entity` back-reference
- Systems contain all behavior, process matching entities
- One component of each type per entity

**Event Bus Thread Safety:**
- Iterate over a copy of subscribers: `for callback in self._subscribers[event_type][:]`
- This prevents issues if callbacks modify subscriptions

**State Pattern:**
- Each state has `enter()`, `update(delta_time)`, `exit()`
- State stack allows pause/resume behavior
- Game delegates to current state's update method

**System Priority:**
- Lower priority numbers run first
- Physics (10) → Health (20) → Collision (30) → Render (100)
- Systems sorted automatically by `SystemManager`

## What Final Behavior Looks Like

### Working Example
```python
from week06_patterns.project.starter.game import Game, PlayingState
from week06_patterns.project.starter.entity import Entity
from week06_patterns.project.starter.components import (
    PositionComponent, VelocityComponent, HealthComponent, RenderComponent
)
from week06_patterns.project.starter.systems import (
    PhysicsSystem, RenderSystem, HealthSystem
)

# Create game
game = Game()

# Create player entity
player = game.create_entity("player")
player.add_component(PositionComponent(x=0, y=0))
player.add_component(VelocityComponent(vx=10, vy=5))
player.add_component(HealthComponent(max_health=100))
player.add_component(RenderComponent(symbol="@", layer=1))

# Add systems
game.add_system(PhysicsSystem(priority=10))
game.add_system(HealthSystem(priority=20))
game.add_system(RenderSystem(priority=100))

# Start playing
game.change_state(PlayingState())
game.run(max_frames=60)  # Runs for 60 frames

# Verify: Player position should have changed
pos = player.get_component(PositionComponent)
print(f"Player moved to: ({pos.x:.2f}, {pos.y:.2f})")
```

### Expected Behaviors

**Entity Management:**
- Entities can be created with custom or auto-generated IDs
- Components attach to entities with type-safe access
- EntityManager efficiently queries entities by component type

**Event System:**
- Subscribers receive events when published
- Multiple subscribers can listen to same event type
- Events carry typed data and sender reference

**Physics System:**
- Entities with Position + Velocity move each frame
- Position updates: `pos += vel * delta_time`
- Velocity clamped to max_speed

**State Management:**
- Game starts in no state
- `change_state()` exits old, enters new
- `push_state()` pauses current, enters new
- `pop_state()` exits current, resumes previous
- Systems only update in PlayingState

**Plugin System:**
- Plugins register/unregister cleanly
- Plugins can add systems, entities, or event handlers
- Disabled plugins are ignored

### Running the Tests

```bash
# Run all project tests
pytest week06_patterns/project/tests/ -v

# Run specific test category
pytest week06_patterns/project/tests/test_game_framework.py::TestEventBus -v
pytest week06_patterns/project/tests/test_game_framework.py::TestEntity -v
pytest week06_patterns/project/tests/test_game_framework.py::TestIntegration -v
```

All 114 tests should pass when implementation is complete.

## Connection to Daily Lessons

### Day 1: Creational Patterns
| Pattern | Project Usage |
|---------|--------------|
| **Factory Method** | `EntityManager.create_entity()` - Creates entities with optional custom IDs |
| **Singleton** | `get_global_event_bus()` - Single event bus instance across the game |

### Day 2: Structural Patterns
| Pattern | Project Usage |
|---------|--------------|
| **Component** | ECS architecture - Entities compose behavior through components |
| **Composite** | `EntityManager` treats individual entities and groups uniformly via queries |

### Day 3: Behavioral Patterns Part 1
| Pattern | Project Usage |
|---------|--------------|
| **Observer** | `EventBus` - Decoupled publish/subscribe for game events |
| **Strategy** | `System` classes - Interchangeable algorithms for game logic |
| **Command** | `GameState` transitions - Encapsulated state change requests |

### Day 4: Behavioral Patterns Part 2
| Pattern | Project Usage |
|---------|--------------|
| **State** | `GameState` hierarchy - Menu, Playing, Paused, GameOver states |
| **Template Method** | `System.update()` - Algorithm skeleton with customizable steps |
| **Iterator** | Component queries - Sequential access without exposing internals |

### Day 5: Pattern Tradeoffs
The project demonstrates when patterns add value:
- **State pattern** cleanly separates game mode behavior
- **Observer pattern** decouples systems without God objects
- **ECS pattern** avoids deep inheritance hierarchies

The project also shows restraint:
- No over-engineering with unnecessary abstractions
- Components are simple data classes (no complex hierarchy)
- Plugin system is minimal but extensible

### Day 6: Patterns in Standard Library
The project uses Pythonic pattern implementations:
- `@dataclass` for clean component definitions
- `defaultdict` for efficient subscriber storage
- Abstract base classes with `@abstractmethod`
- Module-level singleton (global event bus)

## Challenge Extensions

After completing the core framework, try these:

1. **Add WeaponComponent** - Damage, range, cooldown
2. **Add CombatSystem** - Process attacks between entities
3. **Add AIPlugin** - Entities that follow the player
4. **Add Serialization** - Save/load entity state to JSON using Component.to_dict()
5. **Add InputCommand** - Command pattern for player actions with undo

## Common Pitfalls

- **Components with behavior** - Keep components data-only, put logic in Systems
- **Missing super().__init__()** - Dataclass components need `__post_init__` to call parent init
- **State lifecycle** - Remember to call enter() and exit() on state changes
- **System priority** - Lower numbers run first, default is 0
- **Entity activation** - Inactive entities are skipped by systems
- **Event subscription cleanup** - Unsubscribe to prevent memory leaks in real games

## Verification Checklist

Before considering the project complete:

- [ ] All 114 tests pass
- [ ] Can create entities and add components
- [ ] EntityManager queries work correctly
- [ ] EventBus publishes to subscribers
- [ ] PhysicsSystem moves entities
- [ ] State transitions work (change, push, pop)
- [ ] Systems run in priority order
- [ ] Plugin registration/unregistration works

## License

MIT License - See root repository LICENSE
