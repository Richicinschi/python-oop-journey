"""
Component System - ECS Architecture

Components are pure data containers used in the Entity-Component-System pattern.
Each component type represents a specific aspect of an entity.
"""

from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import math


class Component(ABC):
    """
    Abstract base class for all components.
    
    Components should contain only data, no behavior.
    All behavior is implemented in Systems.
    """
    
    def __init__(self):
        """Initialize component with optional entity reference."""
        self._entity: Optional[Any] = None
    
    @property
    def entity(self) -> Optional[Any]:
        """Get the entity this component is attached to."""
        return self._entity
    
    @entity.setter
    def entity(self, value: Any) -> None:
        """Set the entity this component is attached to."""
        self._entity = value
    
    def on_attach(self) -> None:
        """
        Called when component is attached to an entity.
        Override in subclasses for initialization logic.
        """
        pass
    
    def on_detach(self) -> None:
        """
        Called when component is detached from an entity.
        Override in subclasses for cleanup logic.
        """
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize component to dictionary.
        
        Returns:
            Dict containing component data
        """
        return {"type": self.__class__.__name__}


@dataclass
class PositionComponent(Component):
    """
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
        """Call parent __init__ after dataclass init."""
        super().__init__()
    
    def distance_to(self, other: 'PositionComponent') -> float:
        """
        Calculate Euclidean distance to another position.
        
        Args:
            other: Another PositionComponent
            
        Returns:
            float: Distance between positions
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "type": "PositionComponent",
            "x": self.x,
            "y": self.y,
            "z": self.z
        }


@dataclass
class VelocityComponent(Component):
    """
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
        """Call parent __init__ after dataclass init."""
        super().__init__()
    
    def get_speed(self) -> float:
        """
        Calculate current speed magnitude.
        
        Returns:
            float: Speed (magnitude of velocity vector)
        """
        return math.sqrt(self.vx * self.vx + self.vy * self.vy)
    
    def clamp_to_max(self) -> None:
        """Clamp velocity to max_speed if exceeded."""
        speed = self.get_speed()
        if speed > self.max_speed and speed > 0:
            scale = self.max_speed / speed
            self.vx *= scale
            self.vy *= scale
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "type": "VelocityComponent",
            "vx": self.vx,
            "vy": self.vy,
            "max_speed": self.max_speed
        }


@dataclass
class HealthComponent(Component):
    """
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
        """Call parent __init__ and ensure current <= max."""
        super().__init__()
        if self.current > self.max_health:
            self.current = self.max_health
    
    def take_damage(self, amount: float) -> float:
        """
        Apply damage to health.
        
        Args:
            amount: Amount of damage to apply
            
        Returns:
            float: Actual damage taken (0 if invulnerable)
        """
        if self.is_invulnerable or amount <= 0:
            return 0.0
        
        actual_damage = min(amount, self.current)
        self.current -= actual_damage
        return actual_damage
    
    def heal(self, amount: float) -> float:
        """
        Heal the entity.
        
        Args:
            amount: Amount to heal
            
        Returns:
            float: Actual amount healed
        """
        if amount <= 0:
            return 0.0
        
        old_health = self.current
        self.current = min(self.current + amount, self.max_health)
        return self.current - old_health
    
    def is_alive(self) -> bool:
        """
        Check if entity is alive.
        
        Returns:
            bool: True if current > 0
        """
        return self.current > 0
    
    def get_health_percentage(self) -> float:
        """
        Get health as percentage of max.
        
        Returns:
            float: Percentage (0.0 to 100.0)
        """
        if self.max_health <= 0:
            return 0.0
        return (self.current / self.max_health) * 100.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "type": "HealthComponent",
            "current": self.current,
            "max_health": self.max_health,
            "is_invulnerable": self.is_invulnerable
        }


@dataclass
class RenderComponent(Component):
    """
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
        """Call parent __init__ after dataclass init."""
        super().__init__()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "type": "RenderComponent",
            "symbol": self.symbol,
            "color": self.color,
            "visible": self.visible,
            "layer": self.layer
        }


@dataclass
class CollisionComponent(Component):
    """
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
        """Call parent __init__ after dataclass init."""
        super().__init__()
    
    def intersects(self, other: 'CollisionComponent', 
                   self_pos: PositionComponent, 
                   other_pos: PositionComponent) -> bool:
        """
        Check if this collision shape intersects with another.
        
        Args:
            other: Other collision component
            self_pos: This entity's position
            other_pos: Other entity's position
            
        Returns:
            bool: True if shapes intersect
        """
        distance = self_pos.distance_to(other_pos)
        return distance < (self.radius + other.radius)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "type": "CollisionComponent",
            "radius": self.radius,
            "solid": self.solid,
            "layer": self.layer
        }
