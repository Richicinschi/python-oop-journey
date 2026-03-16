"""
Game Systems - ECS Architecture

Systems contain all game logic and operate on entities with specific components.
Each system processes entities during the update cycle.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any

from week06_patterns.project.reference_solution.entity import Entity
from week06_patterns.project.reference_solution.components import (
    PositionComponent, VelocityComponent, HealthComponent, 
    RenderComponent, CollisionComponent
)


class System(ABC):
    """
    Abstract base class for all game systems.
    
    Systems implement game logic by processing entities
    that have specific component combinations.
    """
    
    def __init__(self, priority: int = 0):
        """
        Initialize the system.
        
        Args:
            priority: Execution order (lower = earlier). Default 0.
        """
        self._priority: int = priority
        self._enabled: bool = True
        self._game: Optional[Any] = None
    
    @property
    def priority(self) -> int:
        """Get system priority (lower = runs earlier)."""
        return self._priority
    
    @property
    def enabled(self) -> bool:
        """Get whether system is enabled."""
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set whether system is enabled."""
        self._enabled = value
    
    @property
    def game(self) -> Optional[Any]:
        """Get reference to the game instance."""
        return self._game
    
    @game.setter
    def game(self, value: Any) -> None:
        """Set reference to the game instance."""
        self._game = value
    
    @abstractmethod
    def update(self, delta_time: float, entities: List[Entity]) -> None:
        """
        Update the system for one frame.
        
        Args:
            delta_time: Time elapsed since last frame (seconds)
            entities: List of all entities to potentially process
        """
        pass
    
    def on_added(self) -> None:
        """
        Called when system is added to the game.
        Override for initialization.
        """
        pass
    
    def on_removed(self) -> None:
        """
        Called when system is removed from the game.
        Override for cleanup.
        """
        pass


class PhysicsSystem(System):
    """
    Updates positions based on velocity.
    Processes entities with PositionComponent and VelocityComponent.
    """
    
    def __init__(self, priority: int = 10):
        """Initialize physics system."""
        super().__init__(priority)
    
    def update(self, delta_time: float, entities: List[Entity]) -> None:
        """
        Update positions based on velocity.
        
        For each entity with Position and Velocity:
        1. Calculate new position: pos += vel * delta_time
        2. Clamp velocity to max_speed if VelocityComponent has one
        
        Args:
            delta_time: Time elapsed since last frame
            entities: All entities in the game
        """
        for entity in entities:
            if not entity.active:
                continue
                
            pos = entity.get_component(PositionComponent)
            vel = entity.get_component(VelocityComponent)
            
            if pos is None or vel is None:
                continue
            
            # Clamp velocity to max speed
            vel.clamp_to_max()
            
            # Update position
            pos.x += vel.vx * delta_time
            pos.y += vel.vy * delta_time


class RenderSystem(System):
    """
    Collects renderable entities and sorts by layer.
    Processes entities with PositionComponent and RenderComponent.
    """
    
    def __init__(self, priority: int = 100):
        """Initialize render system."""
        super().__init__(priority)
        self._visible_entities: List[Entity] = []
    
    def update(self, delta_time: float, entities: List[Entity]) -> None:
        """
        Collect and sort renderable entities.
        
        This should update the internal render list.
        Actual rendering would happen in a render() method.
        
        Args:
            delta_time: Time elapsed since last frame
            entities: All entities in the game
        """
        self._visible_entities = self.get_visible_entities(entities)
    
    def get_visible_entities(self, entities: List[Entity]) -> List[Entity]:
        """
        Get all visible entities sorted by render layer.
        
        Args:
            entities: All entities in the game
            
        Returns:
            List of entities with Position and visible Render components,
            sorted by layer (lowest first)
        """
        visible = []
        for entity in entities:
            if not entity.active:
                continue
                
            pos = entity.get_component(PositionComponent)
            render = entity.get_component(RenderComponent)
            
            if pos is not None and render is not None and render.visible:
                visible.append(entity)
        
        # Sort by layer (lower layer = rendered first/behind)
        visible.sort(key=lambda e: e.get_component(RenderComponent).layer)
        return visible


class HealthSystem(System):
    """
    Manages health regeneration and death detection.
    Processes entities with HealthComponent.
    """
    
    def __init__(self, priority: int = 20):
        """Initialize health system."""
        super().__init__(priority)
        self._dead_entities: List[Entity] = []
    
    def update(self, delta_time: float, entities: List[Entity]) -> None:
        """
        Update health status and detect deaths.
        
        For each entity with HealthComponent:
        1. Track which entities die this frame
        2. Optionally: Apply regeneration if implemented
        
        Args:
            delta_time: Time elapsed since last frame
            entities: All entities in the game
        """
        self._dead_entities = []
        
        for entity in entities:
            if not entity.active:
                continue
                
            health = entity.get_component(HealthComponent)
            if health is None:
                continue
            
            if not health.is_alive():
                self._dead_entities.append(entity)
    
    def get_dead_entities(self, entities: List[Entity]) -> List[Entity]:
        """
        Get all entities that died this frame.
        
        Args:
            entities: All entities in the game
            
        Returns:
            List of entities with HealthComponent where is_alive() is False
        """
        dead = []
        for entity in entities:
            health = entity.get_component(HealthComponent)
            if health is not None and not health.is_alive():
                dead.append(entity)
        return dead


class CollisionSystem(System):
    """
    Detects collisions between entities.
    Processes entities with PositionComponent and CollisionComponent.
    """
    
    def __init__(self, priority: int = 30):
        """Initialize collision system."""
        super().__init__(priority)
        self._collisions: List[tuple] = []
    
    def update(self, delta_time: float, entities: List[Entity]) -> None:
        """
        Detect and handle collisions.
        
        For each pair of entities with collision components:
        1. Check if they intersect
        2. Track collision pairs
        
        Args:
            delta_time: Time elapsed since last frame
            entities: All entities in the game
        """
        self._collisions = self.find_collisions(entities)
    
    def find_collisions(self, entities: List[Entity]) -> List[tuple]:
        """
        Find all colliding entity pairs.
        
        Args:
            entities: All entities in the game
            
        Returns:
            List of tuples (entity1, entity2) that are colliding
        """
        collisions = []
        
        # Get entities with collision components
        collidable = []
        for entity in entities:
            if not entity.active:
                continue
            pos = entity.get_component(PositionComponent)
            col = entity.get_component(CollisionComponent)
            if pos is not None and col is not None:
                collidable.append((entity, pos, col))
        
        # Check each pair
        for i, (e1, pos1, col1) in enumerate(collidable):
            for e2, pos2, col2 in collidable[i + 1:]:
                if col1.intersects(col2, pos1, pos2):
                    collisions.append((e1, e2))
        
        return collisions


class SystemManager:
    """
    Manages all systems, ensuring they execute in priority order.
    """
    
    def __init__(self):
        """Initialize system manager."""
        self._systems: List[System] = []
    
    def add_system(self, system: System) -> 'SystemManager':
        """
        Add a system and sort by priority.
        
        Args:
            system: The system to add
            
        Returns:
            SystemManager: Self for method chaining
        """
        self._systems.append(system)
        self._systems.sort(key=lambda s: s.priority)
        system.on_added()
        return self
    
    def remove_system(self, system_type: type) -> bool:
        """
        Remove a system by type.
        
        Args:
            system_type: The type of system to remove
            
        Returns:
            bool: True if system was found and removed
        """
        for i, system in enumerate(self._systems):
            if isinstance(system, system_type):
                system.on_removed()
                self._systems.pop(i)
                return True
        return False
    
    def get_system(self, system_type: type) -> Optional[System]:
        """
        Get a system by type.
        
        Args:
            system_type: The type of system to get
            
        Returns:
            System instance or None
        """
        for system in self._systems:
            if isinstance(system, system_type):
                return system
        return None
    
    def update(self, delta_time: float, entities: List[Entity]) -> None:
        """
        Update all enabled systems in priority order.
        
        Args:
            delta_time: Time elapsed since last frame
            entities: All entities to process
        """
        for system in self._systems:
            if system.enabled:
                system.update(delta_time, entities)
    
    def clear(self) -> None:
        """Remove all systems."""
        for system in self._systems:
            system.on_removed()
        self._systems.clear()
    
    def count(self) -> int:
        """
        Get the number of systems.
        
        Returns:
            int: System count
        """
        return len(self._systems)
