"""
Entity Management - ECS Architecture

Entities are lightweight identifiers that group components together.
In ECS, entities have no behavior or data - they are just IDs with
component containers.
"""

from typing import Any, Dict, List, Optional, Type, TypeVar, Set
from collections import defaultdict

from week06_patterns.project.reference_solution.components import Component


T = TypeVar('T', bound=Component)


class Entity:
    """
    An entity is a unique identifier that groups components.
    
    Entities should be lightweight - they only store references
to their components and a unique ID.
    
    Example:
        >>> entity = Entity("player")
        >>> entity.add_component(PositionComponent(x=10, y=20))
        >>> pos = entity.get_component(PositionComponent)
    """
    
    _id_counter = 0
    
    def __init__(self, entity_id: Optional[str] = None):
        """
        Initialize an entity.
        
        Args:
            entity_id: Optional unique identifier. If None, auto-generate.
        """
        if entity_id is None:
            Entity._id_counter += 1
            entity_id = f"entity_{Entity._id_counter}"
        
        self._id: str = entity_id
        self._components: Dict[Type[Component], Component] = {}
        self._active: bool = True
        self._manager: Optional['EntityManager'] = None
    
    @property
    def id(self) -> str:
        """Get the entity's unique identifier."""
        return self._id
    
    @property
    def active(self) -> bool:
        """Get whether entity is active."""
        return self._active
    
    def activate(self) -> None:
        """Activate the entity."""
        self._active = True
    
    def deactivate(self) -> None:
        """Deactivate the entity."""
        self._active = False
    
    @property
    def manager(self) -> Optional['EntityManager']:
        """Get the entity manager this entity belongs to."""
        return self._manager
    
    @manager.setter
    def manager(self, value: Optional['EntityManager']) -> None:
        """Set the entity manager this entity belongs to."""
        self._manager = value
    
    def add_component(self, component: Component) -> 'Entity':
        """
        Add a component to this entity.
        
        Args:
            component: The component to add
            
        Returns:
            Entity: Self for method chaining
            
        Raises:
            ValueError: If component of this type already exists
        """
        component_type = type(component)
        if component_type in self._components:
            raise ValueError(f"Entity already has component of type {component_type.__name__}")
        
        self._components[component_type] = component
        component.entity = self
        component.on_attach()
        
        # Notify manager of component addition
        if self._manager is not None:
            self._manager.update_component_index(self, component_type, added=True)
        
        return self
    
    def get_component(self, component_type: Type[T]) -> Optional[T]:
        """
        Get a component by type.
        
        Args:
            component_type: The type of component to get
            
        Returns:
            The component instance, or None if not found
        """
        return self._components.get(component_type)
    
    def remove_component(self, component_type: Type[Component]) -> bool:
        """
        Remove a component by type.
        
        Args:
            component_type: The type of component to remove
            
        Returns:
            bool: True if component was found and removed
        """
        if component_type in self._components:
            component = self._components.pop(component_type)
            component.on_detach()
            component.entity = None
            
            # Notify manager of component removal
            if self._manager is not None:
                self._manager.update_component_index(self, component_type, added=False)
            
            return True
        return False
    
    def has_component(self, component_type: Type[Component]) -> bool:
        """
        Check if entity has a component of the given type.
        
        Args:
            component_type: The type to check for
            
        Returns:
            bool: True if component exists
        """
        return component_type in self._components
    
    def has_all_components(self, *component_types: Type[Component]) -> bool:
        """
        Check if entity has all specified component types.
        
        Args:
            *component_types: Variable number of component types
            
        Returns:
            bool: True if all components exist
        """
        return all(self.has_component(ct) for ct in component_types)
    
    def get_components(self) -> List[Component]:
        """
        Get all components attached to this entity.
        
        Returns:
            List of all components
        """
        return list(self._components.values())
    
    def clear_components(self) -> None:
        """Remove all components from this entity."""
        for component in self._components.values():
            component.on_detach()
            component.entity = None
        self._components.clear()
    
    def __repr__(self) -> str:
        """Return string representation."""
        component_names = [c.__class__.__name__ for c in self._components.values()]
        return f"Entity(id='{self._id}', active={self._active}, components={component_names})"


class EntityManager:
    """
    Manages all entities in the game, providing efficient
    querying and lifecycle management.
    
    Example:
        >>> manager = EntityManager()
        >>> player = manager.create_entity("player")
        >>> entities_with_pos = manager.get_entities_with_component(PositionComponent)
    """
    
    def __init__(self):
        """Initialize the entity manager."""
        self._entities: Dict[str, Entity] = {}
        self._component_index: Dict[Type[Component], Set[str]] = defaultdict(set)
    
    def create_entity(self, entity_id: Optional[str] = None) -> Entity:
        """
        Create and register a new entity.
        
        Args:
            entity_id: Optional unique identifier
            
        Returns:
            Entity: The newly created entity
        """
        entity = Entity(entity_id)
        self.add_entity(entity)
        return entity
    
    def _set_entity_manager(self, entity: Entity) -> None:
        """Internal method to set the manager reference on an entity."""
        entity._manager = self
    
    def add_entity(self, entity: Entity) -> 'EntityManager':
        """
        Add an existing entity to management.
        
        Args:
            entity: The entity to manage
            
        Returns:
            EntityManager: Self for method chaining
            
        Raises:
            ValueError: If entity ID already exists
        """
        if entity.id in self._entities:
            raise ValueError(f"Entity with id '{entity.id}' already exists")
        
        self._entities[entity.id] = entity
        entity._manager = self
        
        # Index existing components
        for component_type in entity._components.keys():
            self._component_index[component_type].add(entity.id)
        
        return self
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """
        Get an entity by ID.
        
        Args:
            entity_id: The entity's unique identifier
            
        Returns:
            Entity or None if not found
        """
        return self._entities.get(entity_id)
    
    def remove_entity(self, entity_id: str) -> bool:
        """
        Remove and destroy an entity.
        
        Args:
            entity_id: The entity's unique identifier
            
        Returns:
            bool: True if entity was found and removed
        """
        entity = self._entities.get(entity_id)
        if entity is None:
            return False
        
        # Remove from component index
        for component_type in list(entity._components.keys()):
            self._component_index[component_type].discard(entity_id)
        
        # Clear components and remove entity
        entity.clear_components()
        del self._entities[entity_id]
        return True
    
    def get_all_entities(self) -> List[Entity]:
        """
        Get all managed entities.
        
        Returns:
            List of all entities
        """
        return list(self._entities.values())
    
    def get_active_entities(self) -> List[Entity]:
        """
        Get all active entities.
        
        Returns:
            List of active entities only
        """
        return [e for e in self._entities.values() if e.active]
    
    def get_entities_with_component(self, component_type: Type[Component]) -> List[Entity]:
        """
        Get all entities that have a specific component.
        
        Args:
            component_type: The component type to filter by
            
        Returns:
            List of entities with the component
        """
        entity_ids = self._component_index.get(component_type, set())
        return [self._entities[eid] for eid in entity_ids if eid in self._entities]
    
    def get_entities_with_components(self, *component_types: Type[Component]) -> List[Entity]:
        """
        Get all entities that have ALL specified components.
        
        Args:
            *component_types: Variable number of component types
            
        Returns:
            List of entities with all specified components
        """
        if not component_types:
            return []
        
        # Start with entities that have the first component
        result_ids = self._component_index.get(component_types[0], set()).copy()
        
        # Intersect with entities having each additional component
        for component_type in component_types[1:]:
            result_ids &= self._component_index.get(component_type, set())
        
        return [self._entities[eid] for eid in result_ids if eid in self._entities]
    
    def update_component_index(self, entity: Entity, component_type: Type[Component], 
                               added: bool = True) -> None:
        """
        Update the component index when components are added/removed.
        
        This is called internally when entity components change.
        
        Args:
            entity: The entity being modified
            component_type: The component type being added/removed
            added: True if added, False if removed
        """
        if added:
            self._component_index[component_type].add(entity.id)
        else:
            self._component_index[component_type].discard(entity.id)
    
    def clear(self) -> None:
        """Remove all entities."""
        for entity in self._entities.values():
            entity.clear_components()
        self._entities.clear()
        self._component_index.clear()
    
    def count(self) -> int:
        """
        Get the total number of entities.
        
        Returns:
            int: Entity count
        """
        return len(self._entities)
