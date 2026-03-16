"""
Test Suite for Week 6 Game Framework Project

Tests cover:
- Event system (Observer pattern)
- Component system (ECS)
- Entity management
- Game systems
- State management
- Plugin system
"""

import pytest
from typing import Optional

# Import reference solution
from week06_patterns.project.reference_solution.events import (
    Event, EventBus, get_global_event_bus, reset_global_event_bus
)
from week06_patterns.project.reference_solution.components import (
    Component, PositionComponent, VelocityComponent, HealthComponent,
    RenderComponent, CollisionComponent
)
from week06_patterns.project.reference_solution.entity import Entity, EntityManager
from week06_patterns.project.reference_solution.systems import (
    System, PhysicsSystem, RenderSystem, HealthSystem, CollisionSystem, SystemManager
)
from week06_patterns.project.reference_solution.game import (
    Game, GameState, MenuState, PlayingState, PausedState, GameOverState, Plugin
)


# =============================================================================
# EVENT SYSTEM TESTS (Observer Pattern)
# =============================================================================

class TestEvent:
    """Test Event class."""
    
    def test_event_creation(self):
        """Test creating an event."""
        event = Event("test_event", {"key": "value"}, self)
        assert event.event_type == "test_event"
        assert event.data == {"key": "value"}
        assert event.sender is self
    
    def test_event_creation_minimal(self):
        """Test creating an event with minimal arguments."""
        event = Event("simple_event")
        assert event.event_type == "simple_event"
        assert event.data is None
        assert event.sender is None
    
    def test_event_repr(self):
        """Test event string representation."""
        event = Event("test", "data")
        repr_str = repr(event)
        assert "Event" in repr_str
        assert "test" in repr_str


class TestEventBus:
    """Test EventBus (Observer pattern implementation)."""
    
    def test_subscribe_and_publish(self):
        """Test subscribing and publishing events."""
        bus = EventBus()
        received = []
        
        def handler(event):
            received.append(event)
        
        bus.subscribe("test", handler)
        bus.publish("test", "data")
        
        assert len(received) == 1
        assert received[0].data == "data"
    
    def test_multiple_subscribers(self):
        """Test multiple subscribers for same event."""
        bus = EventBus()
        count = [0]
        
        def handler1(event):
            count[0] += 1
        
        def handler2(event):
            count[0] += 1
        
        bus.subscribe("test", handler1)
        bus.subscribe("test", handler2)
        bus.publish("test")
        
        assert count[0] == 2
    
    def test_unsubscribe(self):
        """Test unsubscribing from events."""
        bus = EventBus()
        received = []
        
        def handler(event):
            received.append(event)
        
        bus.subscribe("test", handler)
        assert bus.unsubscribe("test", handler) is True
        bus.publish("test")
        
        assert len(received) == 0
    
    def test_unsubscribe_not_found(self):
        """Test unsubscribing non-existent handler."""
        bus = EventBus()
        
        def handler(event):
            pass
        
        assert bus.unsubscribe("test", handler) is False
    
    def test_subscriber_count(self):
        """Test getting subscriber count."""
        bus = EventBus()
        
        def handler1(event): pass
        def handler2(event): pass
        
        assert bus.subscriber_count("test") == 0
        bus.subscribe("test", handler1)
        assert bus.subscriber_count("test") == 1
        bus.subscribe("test", handler2)
        assert bus.subscriber_count("test") == 2
    
    def test_clear(self):
        """Test clearing all subscribers."""
        bus = EventBus()
        
        def handler(event): pass
        
        bus.subscribe("test", handler)
        bus.clear()
        
        assert bus.subscriber_count("test") == 0
    
    def test_different_event_types_isolated(self):
        """Test that different event types are isolated."""
        bus = EventBus()
        received = []
        
        def handler(event):
            received.append(event.event_type)
        
        bus.subscribe("type1", handler)
        bus.publish("type2")
        bus.publish("type1")
        
        assert received == ["type1"]


class TestGlobalEventBus:
    """Test global event bus singleton."""
    
    def setup_method(self):
        """Reset global event bus before each test."""
        reset_global_event_bus()
    
    def teardown_method(self):
        """Reset global event bus after each test."""
        reset_global_event_bus()
    
    def test_singleton(self):
        """Test that global event bus is singleton."""
        bus1 = get_global_event_bus()
        bus2 = get_global_event_bus()
        assert bus1 is bus2
    
    def test_reset_creates_new_instance(self):
        """Test that reset creates new instance."""
        bus1 = get_global_event_bus()
        reset_global_event_bus()
        bus2 = get_global_event_bus()
        assert bus1 is not bus2


# =============================================================================
# COMPONENT SYSTEM TESTS (ECS)
# =============================================================================

class TestPositionComponent:
    """Test PositionComponent."""
    
    def test_default_values(self):
        """Test default position values."""
        pos = PositionComponent()
        assert pos.x == 0.0
        assert pos.y == 0.0
        assert pos.z == 0.0
    
    def test_custom_values(self):
        """Test custom position values."""
        pos = PositionComponent(x=10, y=20, z=5)
        assert pos.x == 10
        assert pos.y == 20
        assert pos.z == 5
    
    def test_distance_to(self):
        """Test distance calculation."""
        pos1 = PositionComponent(x=0, y=0)
        pos2 = PositionComponent(x=3, y=4)
        assert pos1.distance_to(pos2) == 5.0
    
    def test_distance_to_same_position(self):
        """Test distance to same position is zero."""
        pos = PositionComponent(x=5, y=5)
        assert pos.distance_to(pos) == 0.0
    
    def test_to_dict(self):
        """Test serialization to dict."""
        pos = PositionComponent(x=1, y=2, z=3)
        data = pos.to_dict()
        assert data["type"] == "PositionComponent"
        assert data["x"] == 1
        assert data["y"] == 2
        assert data["z"] == 3


class TestVelocityComponent:
    """Test VelocityComponent."""
    
    def test_default_values(self):
        """Test default velocity values."""
        vel = VelocityComponent()
        assert vel.vx == 0.0
        assert vel.vy == 0.0
        assert vel.max_speed == 100.0
    
    def test_get_speed_zero(self):
        """Test speed when stationary."""
        vel = VelocityComponent(vx=0, vy=0)
        assert vel.get_speed() == 0.0
    
    def test_get_speed(self):
        """Test speed calculation."""
        vel = VelocityComponent(vx=3, vy=4)
        assert vel.get_speed() == 5.0
    
    def test_clamp_to_max(self):
        """Test velocity clamping."""
        vel = VelocityComponent(vx=100, vy=100, max_speed=50)
        vel.clamp_to_max()
        assert vel.get_speed() <= 50.0
    
    def test_clamp_to_max_no_change(self):
        """Test velocity not clamped when under max."""
        vel = VelocityComponent(vx=10, vy=10, max_speed=100)
        vel.clamp_to_max()
        assert vel.vx == 10
        assert vel.vy == 10


class TestHealthComponent:
    """Test HealthComponent."""
    
    def test_default_values(self):
        """Test default health values."""
        health = HealthComponent()
        assert health.current == 100.0
        assert health.max_health == 100.0
        assert health.is_invulnerable is False
    
    def test_take_damage(self):
        """Test taking damage."""
        health = HealthComponent(current=100, max_health=100)
        damage = health.take_damage(30)
        assert damage == 30
        assert health.current == 70
    
    def test_take_damage_invulnerable(self):
        """Test no damage when invulnerable."""
        health = HealthComponent(current=100, is_invulnerable=True)
        damage = health.take_damage(30)
        assert damage == 0
        assert health.current == 100
    
    def test_take_damage_negative(self):
        """Test negative damage does nothing."""
        health = HealthComponent(current=100)
        damage = health.take_damage(-10)
        assert damage == 0
        assert health.current == 100
    
    def test_take_damage_exceeds_current(self):
        """Test damage cannot exceed current health."""
        health = HealthComponent(current=50)
        damage = health.take_damage(100)
        assert damage == 50
        assert health.current == 0
    
    def test_heal(self):
        """Test healing."""
        health = HealthComponent(current=50, max_health=100)
        healed = health.heal(20)
        assert healed == 20
        assert health.current == 70
    
    def test_heal_exceeds_max(self):
        """Test healing cannot exceed max."""
        health = HealthComponent(current=90, max_health=100)
        healed = health.heal(20)
        assert healed == 10
        assert health.current == 100
    
    def test_heal_negative(self):
        """Test negative heal does nothing."""
        health = HealthComponent(current=50)
        healed = health.heal(-10)
        assert healed == 0
        assert health.current == 50
    
    def test_is_alive_true(self):
        """Test is_alive when health > 0."""
        health = HealthComponent(current=1)
        assert health.is_alive() is True
    
    def test_is_alive_false(self):
        """Test is_alive when health = 0."""
        health = HealthComponent(current=0)
        assert health.is_alive() is False
    
    def test_get_health_percentage(self):
        """Test health percentage calculation."""
        health = HealthComponent(current=50, max_health=100)
        assert health.get_health_percentage() == 50.0
    
    def test_get_health_percentage_zero_max(self):
        """Test health percentage with zero max."""
        health = HealthComponent(current=0, max_health=0)
        assert health.get_health_percentage() == 0.0


class TestRenderComponent:
    """Test RenderComponent."""
    
    def test_default_values(self):
        """Test default render values."""
        render = RenderComponent()
        assert render.symbol == "?"
        assert render.color == "white"
        assert render.visible is True
        assert render.layer == 0
    
    def test_custom_values(self):
        """Test custom render values."""
        render = RenderComponent(symbol="@", color="red", visible=False, layer=5)
        assert render.symbol == "@"
        assert render.color == "red"
        assert render.visible is False
        assert render.layer == 5


class TestCollisionComponent:
    """Test CollisionComponent."""
    
    def test_default_values(self):
        """Test default collision values."""
        col = CollisionComponent()
        assert col.radius == 10.0
        assert col.solid is True
        assert col.layer == "default"
    
    def test_intersects_true(self):
        """Test intersection detection when colliding."""
        col1 = CollisionComponent(radius=5)
        col2 = CollisionComponent(radius=5)
        pos1 = PositionComponent(x=0, y=0)
        pos2 = PositionComponent(x=5, y=0)
        assert col1.intersects(col2, pos1, pos2) is True
    
    def test_intersects_false(self):
        """Test intersection detection when not colliding."""
        col1 = CollisionComponent(radius=5)
        col2 = CollisionComponent(radius=5)
        pos1 = PositionComponent(x=0, y=0)
        pos2 = PositionComponent(x=20, y=0)
        assert col1.intersects(col2, pos1, pos2) is False
    
    def test_intersects_touching(self):
        """Test intersection when exactly touching."""
        col1 = CollisionComponent(radius=5)
        col2 = CollisionComponent(radius=5)
        pos1 = PositionComponent(x=0, y=0)
        pos2 = PositionComponent(x=10, y=0)
        assert col1.intersects(col2, pos1, pos2) is False  # Distance == sum of radii


class TestComponentBase:
    """Test Component base class functionality."""
    
    def test_entity_reference(self):
        """Test entity reference on component."""
        pos = PositionComponent()
        assert pos.entity is None
        
        entity = object()  # Mock entity
        pos.entity = entity
        assert pos.entity is entity


# =============================================================================
# ENTITY MANAGEMENT TESTS
# =============================================================================

class TestEntity:
    """Test Entity class."""
    
    def test_entity_creation_with_id(self):
        """Test creating entity with specific ID."""
        entity = Entity("player1")
        assert entity.id == "player1"
        assert entity.active is True
    
    def test_entity_creation_auto_id(self):
        """Test creating entity with auto-generated ID."""
        entity1 = Entity()
        entity2 = Entity()
        assert entity1.id != entity2.id
        assert entity1.id.startswith("entity_")
    
    def test_add_component(self):
        """Test adding component to entity."""
        entity = Entity("test")
        pos = PositionComponent(x=10, y=20)
        result = entity.add_component(pos)
        
        assert result is entity  # Returns self for chaining
        assert entity.has_component(PositionComponent) is True
        assert entity.get_component(PositionComponent) is pos
    
    def test_add_duplicate_component_raises(self):
        """Test adding duplicate component raises error."""
        entity = Entity("test")
        entity.add_component(PositionComponent())
        
        with pytest.raises(ValueError):
            entity.add_component(PositionComponent())
    
    def test_get_component_not_found(self):
        """Test getting non-existent component returns None."""
        entity = Entity("test")
        assert entity.get_component(PositionComponent) is None
    
    def test_remove_component(self):
        """Test removing component."""
        entity = Entity("test")
        entity.add_component(PositionComponent())
        
        removed = entity.remove_component(PositionComponent)
        assert removed is True
        assert entity.has_component(PositionComponent) is False
    
    def test_remove_component_not_found(self):
        """Test removing non-existent component."""
        entity = Entity("test")
        removed = entity.remove_component(PositionComponent)
        assert removed is False
    
    def test_has_all_components(self):
        """Test checking multiple components."""
        entity = Entity("test")
        entity.add_component(PositionComponent())
        entity.add_component(VelocityComponent())
        
        assert entity.has_all_components(PositionComponent, VelocityComponent) is True
        assert entity.has_all_components(PositionComponent, HealthComponent) is False
    
    def test_get_components(self):
        """Test getting all components."""
        entity = Entity("test")
        pos = PositionComponent()
        vel = VelocityComponent()
        entity.add_component(pos)
        entity.add_component(vel)
        
        components = entity.get_components()
        assert len(components) == 2
        assert pos in components
        assert vel in components
    
    def test_clear_components(self):
        """Test clearing all components."""
        entity = Entity("test")
        entity.add_component(PositionComponent())
        entity.add_component(VelocityComponent())
        
        entity.clear_components()
        assert entity.get_components() == []
    
    def test_activate_deactivate(self):
        """Test activation/deactivation."""
        entity = Entity("test")
        assert entity.active is True
        
        entity.deactivate()
        assert entity.active is False
        
        entity.activate()
        assert entity.active is True
    
    def test_entity_repr(self):
        """Test entity string representation."""
        entity = Entity("test")
        entity.add_component(PositionComponent())
        repr_str = repr(entity)
        assert "Entity" in repr_str
        assert "test" in repr_str
        assert "PositionComponent" in repr_str


class TestEntityManager:
    """Test EntityManager class."""
    
    def test_create_entity(self):
        """Test creating entity through manager."""
        manager = EntityManager()
        entity = manager.create_entity("player")
        
        assert entity.id == "player"
        assert manager.get_entity("player") is entity
    
    def test_add_entity_duplicate_id_raises(self):
        """Test adding entity with duplicate ID raises error."""
        manager = EntityManager()
        manager.create_entity("player")
        
        with pytest.raises(ValueError):
            manager.add_entity(Entity("player"))
    
    def test_get_entity_not_found(self):
        """Test getting non-existent entity."""
        manager = EntityManager()
        assert manager.get_entity("nonexistent") is None
    
    def test_remove_entity(self):
        """Test removing entity."""
        manager = EntityManager()
        manager.create_entity("player")
        
        removed = manager.remove_entity("player")
        assert removed is True
        assert manager.get_entity("player") is None
    
    def test_remove_entity_not_found(self):
        """Test removing non-existent entity."""
        manager = EntityManager()
        removed = manager.remove_entity("nonexistent")
        assert removed is False
    
    def test_get_all_entities(self):
        """Test getting all entities."""
        manager = EntityManager()
        e1 = manager.create_entity("e1")
        e2 = manager.create_entity("e2")
        
        all_entities = manager.get_all_entities()
        assert len(all_entities) == 2
        assert e1 in all_entities
        assert e2 in all_entities
    
    def test_get_active_entities(self):
        """Test getting only active entities."""
        manager = EntityManager()
        active = manager.create_entity("active")
        inactive = manager.create_entity("inactive")
        inactive.deactivate()
        
        active_entities = manager.get_active_entities()
        assert len(active_entities) == 1
        assert active in active_entities
        assert inactive not in active_entities
    
    def test_get_entities_with_component(self):
        """Test querying entities by component."""
        manager = EntityManager()
        e1 = manager.create_entity("e1")
        e2 = manager.create_entity("e2")
        e3 = manager.create_entity("e3")
        
        e1.add_component(PositionComponent())
        e2.add_component(PositionComponent())
        e3.add_component(VelocityComponent())
        
        with_pos = manager.get_entities_with_component(PositionComponent)
        assert len(with_pos) == 2
        assert e1 in with_pos
        assert e2 in with_pos
        assert e3 not in with_pos
    
    def test_get_entities_with_components(self):
        """Test querying entities by multiple components."""
        manager = EntityManager()
        e1 = manager.create_entity("e1")
        e2 = manager.create_entity("e2")
        
        e1.add_component(PositionComponent())
        e1.add_component(VelocityComponent())
        e2.add_component(PositionComponent())
        
        with_both = manager.get_entities_with_components(PositionComponent, VelocityComponent)
        assert len(with_both) == 1
        assert e1 in with_both
    
    def test_clear(self):
        """Test clearing all entities."""
        manager = EntityManager()
        manager.create_entity("e1")
        manager.create_entity("e2")
        
        manager.clear()
        assert manager.count() == 0
        assert manager.get_all_entities() == []
    
    def test_count(self):
        """Test entity count."""
        manager = EntityManager()
        assert manager.count() == 0
        
        manager.create_entity("e1")
        assert manager.count() == 1
        
        manager.create_entity("e2")
        assert manager.count() == 2


# =============================================================================
# SYSTEM TESTS
# =============================================================================

class TestPhysicsSystem:
    """Test PhysicsSystem."""
    
    def test_updates_position_from_velocity(self):
        """Test that position updates based on velocity."""
        entity = Entity("test")
        pos = PositionComponent(x=0, y=0)
        vel = VelocityComponent(vx=10, vy=5)
        entity.add_component(pos)
        entity.add_component(vel)
        
        physics = PhysicsSystem()
        physics.update(delta_time=1.0, entities=[entity])
        
        assert pos.x == 10.0
        assert pos.y == 5.0
    
    def test_updates_position_with_delta_time(self):
        """Test position update with fractional delta time."""
        entity = Entity("test")
        pos = PositionComponent(x=0, y=0)
        vel = VelocityComponent(vx=10, vy=10)
        entity.add_component(pos)
        entity.add_component(vel)
        
        physics = PhysicsSystem()
        physics.update(delta_time=0.5, entities=[entity])
        
        assert pos.x == 5.0
        assert pos.y == 5.0
    
    def test_skips_entities_without_components(self):
        """Test that entities without required components are skipped."""
        entity = Entity("test")
        pos = PositionComponent(x=0, y=0)
        entity.add_component(pos)  # No velocity
        
        physics = PhysicsSystem()
        physics.update(delta_time=1.0, entities=[entity])
        
        assert pos.x == 0.0  # Unchanged
    
    def test_skips_inactive_entities(self):
        """Test that inactive entities are skipped."""
        entity = Entity("test")
        pos = PositionComponent(x=0, y=0)
        vel = VelocityComponent(vx=10, vy=10)
        entity.add_component(pos)
        entity.add_component(vel)
        entity.deactivate()
        
        physics = PhysicsSystem()
        physics.update(delta_time=1.0, entities=[entity])
        
        assert pos.x == 0.0  # Unchanged


class TestRenderSystem:
    """Test RenderSystem."""
    
    def test_get_visible_entities(self):
        """Test getting visible entities."""
        entity = Entity("test")
        entity.add_component(PositionComponent())
        entity.add_component(RenderComponent(visible=True))
        
        render = RenderSystem()
        visible = render.get_visible_entities([entity])
        
        assert len(visible) == 1
        assert entity in visible
    
    def test_invisible_entities_filtered(self):
        """Test that invisible entities are filtered out."""
        entity = Entity("test")
        entity.add_component(PositionComponent())
        entity.add_component(RenderComponent(visible=False))
        
        render = RenderSystem()
        visible = render.get_visible_entities([entity])
        
        assert len(visible) == 0
    
    def test_sorts_by_layer(self):
        """Test that entities are sorted by render layer."""
        e1 = Entity("e1")
        e1.add_component(PositionComponent())
        e1.add_component(RenderComponent(layer=2))
        
        e2 = Entity("e2")
        e2.add_component(PositionComponent())
        e2.add_component(RenderComponent(layer=1))
        
        render = RenderSystem()
        visible = render.get_visible_entities([e1, e2])
        
        assert visible[0] == e2  # Lower layer first
        assert visible[1] == e1


class TestHealthSystem:
    """Test HealthSystem."""
    
    def test_detects_dead_entities(self):
        """Test detection of dead entities."""
        entity = Entity("test")
        health = HealthComponent(current=0)
        entity.add_component(health)
        
        health_sys = HealthSystem()
        dead = health_sys.get_dead_entities([entity])
        
        assert len(dead) == 1
        assert entity in dead
    
    def test_alive_entities_not_dead(self):
        """Test that alive entities are not marked dead."""
        entity = Entity("test")
        health = HealthComponent(current=50)
        entity.add_component(health)
        
        health_sys = HealthSystem()
        dead = health_sys.get_dead_entities([entity])
        
        assert len(dead) == 0


class TestCollisionSystem:
    """Test CollisionSystem."""
    
    def test_find_collisions(self):
        """Test finding colliding entities."""
        e1 = Entity("e1")
        e1.add_component(PositionComponent(x=0, y=0))
        e1.add_component(CollisionComponent(radius=5))
        
        e2 = Entity("e2")
        e2.add_component(PositionComponent(x=3, y=0))
        e2.add_component(CollisionComponent(radius=5))
        
        e3 = Entity("e3")
        e3.add_component(PositionComponent(x=100, y=0))
        e3.add_component(CollisionComponent(radius=5))
        
        collision_sys = CollisionSystem()
        collisions = collision_sys.find_collisions([e1, e2, e3])
        
        assert len(collisions) == 1
        assert (e1, e2) in collisions or (e2, e1) in collisions


class TestSystemManager:
    """Test SystemManager."""
    
    def test_add_system(self):
        """Test adding system."""
        manager = SystemManager()
        physics = PhysicsSystem()
        
        result = manager.add_system(physics)
        assert result is manager
        assert manager.count() == 1
    
    def test_systems_sorted_by_priority(self):
        """Test that systems are sorted by priority."""
        manager = SystemManager()
        
        high_priority = PhysicsSystem(priority=1)
        low_priority = RenderSystem(priority=100)
        mid_priority = HealthSystem(priority=50)
        
        manager.add_system(low_priority)
        manager.add_system(high_priority)
        manager.add_system(mid_priority)
        
        systems = [manager.get_system(PhysicsSystem), 
                   manager.get_system(HealthSystem),
                   manager.get_system(RenderSystem)]
        priorities = [s.priority for s in systems]
        assert priorities == [1, 50, 100]
    
    def test_get_system_not_found(self):
        """Test getting non-existent system."""
        manager = SystemManager()
        assert manager.get_system(PhysicsSystem) is None
    
    def test_remove_system(self):
        """Test removing system."""
        manager = SystemManager()
        manager.add_system(PhysicsSystem())
        
        removed = manager.remove_system(PhysicsSystem)
        assert removed is True
        assert manager.count() == 0
    
    def test_remove_system_not_found(self):
        """Test removing non-existent system."""
        manager = SystemManager()
        removed = manager.remove_system(PhysicsSystem)
        assert removed is False
    
    def test_update_calls_all_enabled_systems(self):
        """Test that update calls all enabled systems."""
        manager = SystemManager()
        
        # Use physics system and verify it updates entity position
        entity = Entity("test")
        entity.add_component(PositionComponent())
        entity.add_component(VelocityComponent(vx=10, vy=0))
        
        manager.add_system(PhysicsSystem())
        manager.update(delta_time=1.0, entities=[entity])
        
        pos = entity.get_component(PositionComponent)
        assert pos.x == 10.0


# =============================================================================
# GAME STATE TESTS (State Pattern)
# =============================================================================

class TestGameState:
    """Test GameState base class."""
    
    def test_state_name(self):
        """Test state name property."""
        state = MenuState()
        assert state.name == "MENU"
    
    def test_state_game_reference(self):
        """Test game reference on state."""
        state = MenuState()
        assert state.game is None
        
        game = Game()
        state.game = game
        assert state.game is game


class TestMenuState:
    """Test MenuState."""
    
    def test_menu_state_name(self):
        """Test menu state name."""
        state = MenuState()
        assert state.name == "MENU"
    
    def test_menu_state_lifecycle(self):
        """Test menu state lifecycle methods."""
        state = MenuState()
        state.enter()
        state.update(0.016)
        state.exit()


class TestPlayingState:
    """Test PlayingState."""
    
    def test_playing_state_name(self):
        """Test playing state name."""
        state = PlayingState()
        assert state.name == "PLAYING"


class TestPausedState:
    """Test PausedState."""
    
    def test_paused_state_name(self):
        """Test paused state name."""
        previous = PlayingState()
        state = PausedState(previous)
        assert state.name == "PAUSED"
    
    def test_paused_state_previous(self):
        """Test paused state stores previous state."""
        previous = PlayingState()
        state = PausedState(previous)
        assert state.previous_state is previous


class TestGameOverState:
    """Test GameOverState."""
    
    def test_game_over_state_name(self):
        """Test game over state name."""
        state = GameOverState()
        assert state.name == "GAME_OVER"
    
    def test_game_over_state_winner(self):
        """Test game over state with winner."""
        state = GameOverState(winner="Player 1")
        assert state.winner == "Player 1"
    
    def test_game_over_state_no_winner(self):
        """Test game over state without winner."""
        state = GameOverState()
        assert state.winner is None


# =============================================================================
# PLUGIN SYSTEM TESTS
# =============================================================================

class TestPlugin:
    """Test Plugin base class."""
    
    def test_plugin_name(self):
        """Test plugin name property."""
        class TestPluginImpl(Plugin):
            def on_register(self, game): pass
            def on_unregister(self, game): pass
        
        plugin = TestPluginImpl("test_plugin")
        assert plugin.name == "test_plugin"
    
    def test_plugin_enabled_default(self):
        """Test plugin is enabled by default."""
        class TestPluginImpl(Plugin):
            def on_register(self, game): pass
            def on_unregister(self, game): pass
        
        plugin = TestPluginImpl("test")
        assert plugin.enabled is True
    
    def test_plugin_disable(self):
        """Test disabling plugin."""
        class TestPluginImpl(Plugin):
            def on_register(self, game): pass
            def on_unregister(self, game): pass
        
        plugin = TestPluginImpl("test")
        plugin.enabled = False
        assert plugin.enabled is False


class TestConcretePlugin:
    """Test concrete plugin implementation."""
    
    def test_plugin_registration(self):
        """Test plugin registration callback."""
        registered_games = []
        
        class TestPluginImpl(Plugin):
            def on_register(self, game):
                registered_games.append(game)
            def on_unregister(self, game): pass
        
        game = Game()
        plugin = TestPluginImpl("test")
        game.register_plugin(plugin)
        
        assert len(registered_games) == 1
        assert registered_games[0] is game


# =============================================================================
# GAME ENGINE TESTS
# =============================================================================

class TestGame:
    """Test Game engine class."""
    
    def test_game_creation(self):
        """Test game initialization."""
        game = Game()
        assert game.is_running is False
        assert game.current_state is None
        assert game.entity_manager is not None
        assert game.system_manager is not None
        assert game.event_bus is not None
    
    def test_create_entity(self):
        """Test creating entity through game."""
        game = Game()
        entity = game.create_entity("player")
        
        assert entity.id == "player"
        assert game.get_entity("player") is entity
    
    def test_add_entity(self):
        """Test adding entity to game."""
        game = Game()
        entity = Entity("test")
        
        result = game.add_entity(entity)
        assert result is game
        assert game.get_entity("test") is entity
    
    def test_remove_entity(self):
        """Test removing entity from game."""
        game = Game()
        game.create_entity("test")
        
        removed = game.remove_entity("test")
        assert removed is True
        assert game.get_entity("test") is None
    
    def test_add_system(self):
        """Test adding system to game."""
        game = Game()
        physics = PhysicsSystem()
        
        result = game.add_system(physics)
        assert result is game
        assert game.get_system(PhysicsSystem) is physics
    
    def test_change_state(self):
        """Test changing game state."""
        game = Game()
        state = MenuState()
        
        result = game.change_state(state)
        assert result is game
        assert game.current_state is state
        assert state.game is game
    
    def test_push_state(self):
        """Test pushing state onto stack."""
        game = Game()
        menu = MenuState()
        playing = PlayingState()
        
        game.change_state(menu)
        game.push_state(playing)
        
        assert game.current_state is playing
    
    def test_pop_state(self):
        """Test popping state from stack."""
        game = Game()
        menu = MenuState()
        playing = PlayingState()
        
        game.change_state(menu)
        game.push_state(playing)
        popped = game.pop_state()
        
        assert popped is playing
        assert game.current_state is menu
    
    def test_pop_empty_stack(self):
        """Test popping from empty state stack."""
        game = Game()
        popped = game.pop_state()
        assert popped is None
    
    def test_register_plugin(self):
        """Test registering plugin."""
        game = Game()
        
        class TestPluginImpl(Plugin):
            def on_register(self, game): pass
            def on_unregister(self, game): pass
        
        plugin = TestPluginImpl("test")
        result = game.register_plugin(plugin)
        
        assert result is game
        assert game.get_plugin("test") is plugin
    
    def test_unregister_plugin(self):
        """Test unregistering plugin."""
        game = Game()
        
        class TestPluginImpl(Plugin):
            def on_register(self, game): pass
            def on_unregister(self, game): pass
        
        plugin = TestPluginImpl("test")
        game.register_plugin(plugin)
        
        removed = game.unregister_plugin("test")
        assert removed is True
        assert game.get_plugin("test") is None
    
    def test_start_stop(self):
        """Test starting and stopping game."""
        game = Game()
        assert game.is_running is False
        
        game.start()
        assert game.is_running is True
        
        game.stop()
        assert game.is_running is False
    
    def test_update_increments_frame(self):
        """Test that update increments frame count."""
        game = Game()
        game.change_state(PlayingState())
        
        game.update(0.016)
        game.update(0.016)
        
        assert game._frame_count == 2
    
    def test_update_with_systems(self):
        """Test that update calls systems in playing state."""
        game = Game()
        game.change_state(PlayingState())
        
        entity = game.create_entity("test")
        entity.add_component(PositionComponent())
        entity.add_component(VelocityComponent(vx=10, vy=0))
        
        game.add_system(PhysicsSystem())
        game.update(delta_time=1.0)
        
        pos = entity.get_component(PositionComponent)
        assert pos.x == 10.0
    
    def test_update_skips_systems_in_menu(self):
        """Test that systems don't run in menu state."""
        game = Game()
        game.change_state(MenuState())
        
        entity = game.create_entity("test")
        entity.add_component(PositionComponent())
        entity.add_component(VelocityComponent(vx=10, vy=0))
        
        game.add_system(PhysicsSystem())
        game.update(delta_time=1.0)
        
        pos = entity.get_component(PositionComponent)
        assert pos.x == 0.0  # Unchanged
    
    def test_run_with_frame_limit(self):
        """Test running game with frame limit."""
        game = Game()
        game.change_state(PlayingState())
        
        game.run(max_frames=5)
        
        assert game._frame_count == 5
        assert game.is_running is False


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """Integration tests for the full framework."""
    
    def test_full_game_loop(self):
        """Test a complete game loop scenario."""
        game = Game()
        
        # Create player with all necessary components
        player = game.create_entity("player")
        player.add_component(PositionComponent(x=0, y=0))
        player.add_component(VelocityComponent(vx=10, vy=5))
        player.add_component(HealthComponent(max_health=100))
        player.add_component(RenderComponent(symbol="@", layer=1))
        
        # Add systems
        game.add_system(PhysicsSystem(priority=10))
        game.add_system(HealthSystem(priority=20))
        game.add_system(RenderSystem(priority=100))
        
        # Start and run for a few frames
        game.change_state(PlayingState())
        game.run(max_frames=10)
        
        # Verify player moved (delta_time = 1/60 per frame)
        pos = player.get_component(PositionComponent)
        expected_x = 10 * (1.0/60.0) * 10  # vx * delta * frames
        expected_y = 5 * (1.0/60.0) * 10   # vy * delta * frames
        assert abs(pos.x - expected_x) < 0.001
        assert abs(pos.y - expected_y) < 0.001
    
    def test_entity_collision_scenario(self):
        """Test collision detection scenario."""
        game = Game()
        
        # Create two colliding entities
        e1 = game.create_entity("e1")
        e1.add_component(PositionComponent(x=0, y=0))
        e1.add_component(CollisionComponent(radius=5))
        
        e2 = game.create_entity("e2")
        e2.add_component(PositionComponent(x=5, y=0))
        e2.add_component(CollisionComponent(radius=5))
        
        # Add collision system
        collision_sys = CollisionSystem()
        game.add_system(collision_sys)
        game.change_state(PlayingState())
        
        # Run one frame
        game.update(0.016)
        
        # Check collisions were detected
        collisions = collision_sys.find_collisions(game.entity_manager.get_all_entities())
        assert len(collisions) == 1
    
    def test_state_stack_scenario(self):
        """Test state stack behavior."""
        game = Game()
        
        # Start at menu
        menu = MenuState()
        game.change_state(menu)
        assert game.current_state.name == "MENU"
        
        # Push playing state
        playing = PlayingState()
        game.push_state(playing)
        assert game.current_state.name == "PLAYING"
        
        # Push pause state
        paused = PausedState(playing)
        game.push_state(paused)
        assert game.current_state.name == "PAUSED"
        
        # Pop back to playing
        game.pop_state()
        assert game.current_state.name == "PLAYING"
        
        # Pop back to menu
        game.pop_state()
        assert game.current_state.name == "MENU"
    
    def test_event_driven_damage(self):
        """Test event-driven damage system."""
        reset_global_event_bus()
        
        game = Game()
        
        # Create entity with health
        enemy = game.create_entity("enemy")
        health = HealthComponent(current=100)
        enemy.add_component(health)
        
        # Track damage events
        damages_received = []
        
        def on_damage(event):
            damages_received.append(event.data)
        
        game.event_bus.subscribe("damage", on_damage)
        
        # Apply damage through event
        actual_damage = health.take_damage(25)
        game.event_bus.publish("damage", {"entity": "enemy", "amount": actual_damage})
        
        assert len(damages_received) == 1
        assert damages_received[0]["amount"] == 25
        assert health.current == 75
        
        reset_global_event_bus()


# Count total tests
# Event tests: 12
# Component tests: 24
# Entity tests: 14
# System tests: 13
# State tests: 8
# Plugin tests: 4
# Game tests: 18
# Integration tests: 4
# Total: 97 tests
