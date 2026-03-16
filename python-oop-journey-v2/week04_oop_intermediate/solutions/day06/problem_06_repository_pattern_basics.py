"""Problem 06: Repository Pattern Basics.

Implement the Repository pattern for data access abstraction.
This pattern separates business logic from data access logic.

Classes to implement:
- Entity (ABC): Base class for domain entities
- User: A user entity
- Repository (Generic ABC): Abstract repository interface
- InMemoryRepository: In-memory implementation
- UserRepository: Specialized repository for Users

Example:
    >>> repo = UserRepository()
    >>> user = User(1, "alice", "alice@example.com")
    >>> repo.save(user)
    >>> repo.get(1).name
    'alice'
    >>> repo.find_by_email("alice@example.com").name
    'alice'
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, Optional


class Entity(ABC):
    """Base class for domain entities.
    
    All entities must have a unique identifier.
    
    Attributes:
        id: Unique entity identifier.
    """
    
    def __init__(self, entity_id: int) -> None:
        """Initialize an entity.
        
        Args:
            entity_id: Unique identifier.
        """
        self._id = entity_id
    
    @abstractmethod
    def get_display_name(self) -> str:
        """Get display name for the entity.
        
        Returns:
            Human-readable identifier.
        """
        ...
    
    @property
    def id(self) -> int:
        """Get entity ID.
        
        Returns:
            The entity's unique identifier.
        """
        return self._id
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on ID.
        
        Args:
            other: Object to compare.
        
        Returns:
            True if same ID and type.
        """
        if not isinstance(other, Entity):
            return NotImplemented
        return self._id == other._id and type(self) == type(other)
    
    def __hash__(self) -> int:
        """Hash based on ID.
        
        Returns:
            Hash of the ID.
        """
        return hash((self._id, type(self)))


class User(Entity):
    """A user entity.
    
    Attributes:
        id: Unique user ID.
        name: User's name.
        email: User's email address.
    """
    
    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Initialize a user.
        
        Args:
            user_id: Unique identifier.
            name: User's name.
            email: User's email address.
        """
        super().__init__(user_id)
        self._name = name
        self._email = email
    
    @property
    def name(self) -> str:
        """Get user name.
        
        Returns:
            The user's name.
        """
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set user name.
        
        Args:
            value: New name.
        """
        self._name = value
    
    @property
    def email(self) -> str:
        """Get user email.
        
        Returns:
            The user's email.
        """
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        """Set user email.
        
        Args:
            value: New email.
        """
        self._email = value
    
    def __repr__(self) -> str:
        """String representation.
        
        Returns:
            Detailed string representation.
        """
        return f"User(id={self._id}, name='{self._name}', email='{self._email}')"
    
    def __str__(self) -> str:
        """Human-readable string.
        
        Returns:
            User name.
        """
        return self._name
    
    def get_display_name(self) -> str:
        """Get display name for the entity.
        
        Returns:
            User's display name (name + email).
        """
        return f"{self._name} ({self._email})"


T = TypeVar("T", bound=Entity)
K = TypeVar("K")


class Repository(ABC, Generic[T, K]):
    """Abstract repository for entities.
    
    This is the core of the Repository pattern - it abstracts
    away data access details from business logic.
    
    Type Parameters:
        T: The entity type (must inherit from Entity).
        K: The key type (typically int or str).
    """
    
    @abstractmethod
    def get(self, id: K) -> Optional[T]:
        """Get an entity by ID.
        
        Args:
            id: Entity identifier.
        
        Returns:
            The entity or None if not found.
        """
        ...
    
    @abstractmethod
    def save(self, entity: T) -> None:
        """Save an entity.
        
        Args:
            entity: Entity to save.
        """
        ...
    
    @abstractmethod
    def delete(self, id: K) -> bool:
        """Delete an entity.
        
        Args:
            id: Entity identifier.
        
        Returns:
            True if deleted, False if not found.
        """
        ...
    
    @abstractmethod
    def get_all(self) -> list[T]:
        """Get all entities.
        
        Returns:
            List of all entities.
        """
        ...
    
    @abstractmethod
    def exists(self, id: K) -> bool:
        """Check if an entity exists.
        
        Args:
            id: Entity identifier.
        
        Returns:
            True if the entity exists.
        """
        ...
    
    @abstractmethod
    def count(self) -> int:
        """Get the count of entities.
        
        Returns:
            Number of entities.
        """
        ...


class InMemoryRepository(Repository[T, int], Generic[T]):
    """In-memory implementation of the Repository pattern.
    
    This implementation stores entities in a dictionary.
    Useful for testing and development.
    
    Attributes:
        _storage: Dictionary storing entities by ID.
    """
    
    def __init__(self) -> None:
        """Initialize the repository."""
        self._storage: dict[int, T] = {}
    
    def get(self, id: int) -> Optional[T]:
        """Get entity by ID.
        
        Args:
            id: Entity identifier.
        
        Returns:
            The entity or None.
        """
        return self._storage.get(id)
    
    def save(self, entity: T) -> None:
        """Save an entity.
        
        Args:
            entity: Entity to save.
        """
        self._storage[entity.id] = entity
    
    def delete(self, id: int) -> bool:
        """Delete an entity.
        
        Args:
            id: Entity identifier.
        
        Returns:
            True if deleted, False if not found.
        """
        if id in self._storage:
            del self._storage[id]
            return True
        return False
    
    def get_all(self) -> list[T]:
        """Get all entities.
        
        Returns:
            List of all entities.
        """
        return list(self._storage.values())
    
    def exists(self, id: int) -> bool:
        """Check if entity exists.
        
        Args:
            id: Entity identifier.
        
        Returns:
            True if exists.
        """
        return id in self._storage
    
    def count(self) -> int:
        """Get entity count.
        
        Returns:
            Number of entities.
        """
        return len(self._storage)
    
    def clear(self) -> None:
        """Clear all entities (useful for testing)."""
        self._storage.clear()


class UserRepository(InMemoryRepository[User]):
    """Specialized repository for User entities.
    
    Adds user-specific query methods while inheriting
    basic CRUD operations from InMemoryRepository.
    """
    
    def find_by_name(self, name: str) -> list[User]:
        """Find users by name.
        
        Args:
            name: Name to search for.
        
        Returns:
            List of matching users.
        """
        return [u for u in self.get_all() if u.name == name]
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email.
        
        Args:
            email: Email to search for.
        
        Returns:
            Matching user or None.
        """
        for user in self.get_all():
            if user.email == email:
                return user
        return None
    
    def search(self, query: str) -> list[User]:
        """Search users by name or email.
        
        Args:
            query: Search string.
        
        Returns:
            List of matching users.
        """
        query = query.lower()
        return [
            u for u in self.get_all()
            if query in u.name.lower() or query in u.email.lower()
        ]
