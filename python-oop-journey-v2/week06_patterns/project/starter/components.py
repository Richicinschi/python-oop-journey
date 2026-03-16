"""
Component System - ECS Architecture

Components are pure data containers used in the Entity-Component-System pattern.
Each component type represents a specific aspect of an entity.

TODO: Complete the following:
1. Implement Component base class
2. Implement specific component types (Position, Velocity, Health, etc.)
3. Ensure components are data-only (no behavior)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


class Component(ABC):
    """
    Abstract base class for all components.
    
    TODO: Implement this class
    
    Components should contain only data, no behavior.
    All behavior is implemented in Systems.
    """
    
    def __init__(self):
        """TODO: Initialize component with optional entity reference."""
        # TODO: Initialize _entity reference to None
        raise NotImplementedError("Component.__init__ not implemented")
    
    @property
    def entity(self) -> Optional[Any]:
        """TODO: Get the entity this component is attached to."""
        raise NotImplementedError("Component.entity not implemented")
    
    @entity.setter
    def entity(self, value: Any) -> None:
        """TODO: Set the entity this component is attached to."""
        raise NotImplementedError("Component.entity setter not implemented")
    
    def on_attach(self) -> None:
        """
        TODO: Called when component is attached to an entity.
        Override in subclasses for initialization logic.
        """
        pass
    
    def on_detach(self) -> None:
        """
        TODO: Called when component is detached from an entity.
        Override in subclasses for cleanup logic.
        """
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """
        TODO: Serialize component to dictionary.
        
        Returns:
            Dict containing component data
        """
        raise NotImplementedError("Component.to_dict not implemented")


@dataclass
class PositionComponent(Component):
    """
    TODO: Implement PositionComponent
    
    Represents an entity's position in 2D space.
    
    Attributes:
        x (float): X coordinate
        y (float): Y coordinate
        z (float): Z coordinate (for layering)
    """
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def __post_init__(self):
        """TODO: Call parent __init__ after dataclass init."""
        # TODO: Call super().__init__()
        raise NotImplementedError("PositionComponent.__post_init__ not implemented")
    
    def distance_to(self, other: 'PositionComponent') -> float:
        """
        TODO: Calculate Euclidean distance to another position.
        
        Args:
            other: Another PositionComponent
            
        Returns:
            float: Distance between positions
        """
        raise NotImplementedError("PositionComponent.distance_to not implemented")
    
    def to_dict(self) -> Dict[str, Any]:
        """TODO: Serialize to dictionary."""
        raise NotImplementedError("PositionComponent.to_dict not implemented")


@dataclass
class VelocityComponent(Component):
    """
    TODO: Implement VelocityComponent
    
    Represents an entity's velocity in 2D space.
    
    Attributes:
        vx (float): Velocity in X direction
        vy (float): Velocity in Y direction
        max_speed (float): Maximum speed cap
    """
    vx: float = 0.0
    vy: float = 0.0
    max_speed: float = 100.0
    
    def __post_init__(self):
        """TODO: Call parent __init__ after dataclass init."""
        raise NotImplementedError("VelocityComponent.__post_init__ not implemented")
    
    def get_speed(self) -> float:
        """
        TODO: Calculate current speed magnitude.
        
        Returns:
            float: Speed (magnitude of velocity vector)
        """
        raise NotImplementedError("VelocityComponent.get_speed not implemented")
    
    def clamp_to_max(self) -> None:
        """TODO: Clamp velocity to max_speed if exceeded."""
        raise NotImplementedError("VelocityComponent.clamp_to_max not implemented")
    
    def to_dict(self) -> Dict[str, Any]:
        """TODO: Serialize to dictionary."""
        raise NotImplementedError("VelocityComponent.to_dict not implemented")


@dataclass
class HealthComponent(Component):
    """
    TODO: Implement HealthComponent
    
    Represents an entity's health/life points.
    
    Attributes:
        current (float): Current health
        max_health (float): Maximum health
        is_invulnerable (bool): Whether entity can take damage
    """
    current: float = 100.0
    max_health: float = 100.0
    is_invulnerable: bool = False
    
    def __post_init__(self):
        """TODO: Call parent __init__ and ensure current <= max."""
        raise NotImplementedError("HealthComponent.__post_init__ not implemented")
    
    def take_damage(self, amount: float) -> float:
        """
        TODO: Apply damage to health.
        
        Args:
            amount: Amount of damage to apply
            
        Returns:
            float: Actual damage taken (0 if invulnerable)
        """
        raise NotImplementedError("HealthComponent.take_damage not implemented")
    
    def heal(self, amount: float) -> float:
        """
        TODO: Heal the entity.
        
        Args:
            amount: Amount to heal
            
        Returns:
            float: Actual amount healed
        """
        raise NotImplementedError("HealthComponent.heal not implemented")
    
    def is_alive(self) -> bool:
        """
        TODO: Check if entity is alive.
        
        Returns:
            bool: True if current > 0
        """
        raise NotImplementedError("HealthComponent.is_alive not implemented")
    
    def get_health_percentage(self) -> float:
        """
        TODO: Get health as percentage of max.
        
        Returns:
            float: Percentage (0.0 to 100.0)
        """
        raise NotImplementedError("HealthComponent.get_health_percentage not implemented")
    
    def to_dict(self) -> Dict[str, Any]:
        """TODO: Serialize to dictionary."""
        raise NotImplementedError("HealthComponent.to_dict not implemented")


@dataclass
class RenderComponent(Component):
    """
    TODO: Implement RenderComponent
    
    Represents visual properties of an entity.
    
    Attributes:
        symbol (str): Character or string representation
        color (str): Color name or hex code
        visible (bool): Whether entity is visible
        layer (int): Render layer (higher = in front)
    """
    symbol: str = "?"
    color: str = "white"
    visible: bool = True
    layer: int = 0
    
    def __post_init__(self):
        """TODO: Call parent __init__ after dataclass init."""
        raise NotImplementedError("RenderComponent.__post_init__ not implemented")
    
    def to_dict(self) -> Dict[str, Any]:
        """TODO: Serialize to dictionary."""
        raise NotImplementedError("RenderComponent.to_dict not implemented")


@dataclass
class CollisionComponent(Component):
    """
    TODO: Implement CollisionComponent
    
    Represents collision properties of an entity.
    
    Attributes:
        radius (float): Collision circle radius
        solid (bool): Whether entity blocks movement
        layer (str): Collision layer (e.g., "player", "enemy", "wall")
    """
    radius: float = 10.0
    solid: bool = True
    layer: str = "default"
    
    def __post_init__(self):
        """TODO: Call parent __init__ after dataclass init."""
        raise NotImplementedError("CollisionComponent.__post_init__ not implemented")
    
    def intersects(self, other: 'CollisionComponent', 
                   self_pos: PositionComponent, 
                   other_pos: PositionComponent) -> bool:
        """
        TODO: Check if this collision shape intersects with another.
        
        Args:
            other: Other collision component
            self_pos: This entity's position
            other_pos: Other entity's position
            
        Returns:
            bool: True if shapes intersect
        """
        raise NotImplementedError("CollisionComponent.intersects not implemented")
    
    def to_dict(self) -> Dict[str, Any]:
        """TODO: Serialize to dictionary."""
        raise NotImplementedError("CollisionComponent.to_dict not implemented")
