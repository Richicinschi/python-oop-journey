"""Problem 06: Repository Pattern Basics

Topic: Composition vs Inheritance
Difficulty: Medium

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

Hints:
    Hint 1: Entity is an abstract base class with an abstract method
    get_display_name(). The User class extends Entity and must implement
    this method. The __eq__ and __hash__ methods should be based on id.
    
    Hint 2: Repository uses generics (Repository[T, K]). InMemoryRepository
    stores entities in a dictionary: dict[int, T]. The save() method uses
    entity.id as the key. Check type hints carefully - get() returns Optional[T].
    
    Hint 3: UserRepository extends InMemoryRepository[User] and adds
    user-specific methods. find_by_name() should use list comprehension
    filtering by name. find_by_email() should return the first match or None.
    search() should check if query appears in name OR email (case-insensitive).
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
        # TODO: Set self._id = entity_id
        raise NotImplementedError("Initialize with entity_id")
    
    @abstractmethod
    def get_display_name(self) -> str:
        """Get display name for the entity.
        
        Returns:
            Human-readable identifier.
        """
        # TODO: Abstract method - subclasses must implement
        raise NotImplementedError("Subclasses must implement get_display_name")
    
    @property
    def id(self) -> int:
        """Get entity ID.
        
        Returns:
            The entity's unique identifier.
        """
        # TODO: Return self._id
        raise NotImplementedError("Return entity id")
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on ID.
        
        Args:
            other: Object to compare.
        
        Returns:
            True if same ID and type.
        """
        # TODO: Check if other is Entity and has same id and type
        raise NotImplementedError("Implement equality check")
    
    def __hash__(self) -> int:
        """Hash based on ID.
        
        Returns:
            Hash of the ID.
        """
        # TODO: Return hash of (id, type)
        raise NotImplementedError("Implement hash")


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
        # TODO: Call super().__init__(user_id), then set _name and _email
        raise NotImplementedError("Initialize user")
    
    @property
    def name(self) -> str:
        """Get user name.
        
        Returns:
            The user's name.
        """
        # TODO: Return self._name
        raise NotImplementedError("Return name")
    
    @name.setter
    def name(self, value: str) -> None:
        """Set user name.
        
        Args:
            value: New name.
        """
        # TODO: Set self._name = value
        raise NotImplementedError("Set name")
    
    @property
    def email(self) -> str:
        """Get user email.
        
        Returns:
            The user's email.
        """
        # TODO: Return self._email
        raise NotImplementedError("Return email")
    
    @email.setter
    def email(self, value: str) -> None:
        """Set user email.
        
        Args:
            value: New email.
        """
        # TODO: Set self._email = value
        raise NotImplementedError("Set email")
    
    def __repr__(self) -> str:
        """String representation.
        
        Returns:
            Detailed string representation.
        """
        # TODO: Return f"User(id={self._id}, name='{self._name}', email='{self._email}')"
        raise NotImplementedError("Return repr")
    
    def __str__(self) -> str:
        """Human-readable string.
        
        Returns:
            User name.
        """
        # TODO: Return self._name
        raise NotImplementedError("Return str")
    
    def get_display_name(self) -> str:
        """Get display name for the entity.
        
        Returns:
            User's display name (name + email).
        """
        # TODO: Return f"{self._name} ({self._email})"
        raise NotImplementedError("Return display name")


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
        # TODO: Abstract method
        raise NotImplementedError("get must be implemented")
    
    @abstractmethod
    def save(self, entity: T) -> None:
        """Save an entity.
        
        Args:
            entity: Entity to save.
        """
        # TODO: Abstract method
        raise NotImplementedError("save must be implemented")
    
    @abstractmethod
    def delete(self, id: K) -> bool:
        """Delete an entity.
        
        Args:
            id: Entity identifier.
        
        Returns:
            True if deleted, False if not found.
        """
        # TODO: Abstract method
        raise NotImplementedError("delete must be implemented")
    
    @abstractmethod
    def get_all(self) -> list[T]:
        """Get all entities.
        
        Returns:
            List of all entities.
        """
        # TODO: Abstract method
        raise NotImplementedError("get_all must be implemented")
    
    @abstractmethod
    def exists(self, id: K) -> bool:
        """Check if an entity exists.
        
        Args:
            id: Entity identifier.
        
        Returns:
            True if the entity exists.
        """
        # TODO: Abstract method
        raise NotImplementedError("exists must be implemented")
    
    @abstractmethod
    def count(self) -> int:
        """Get the count of entities.
        
        Returns:
            Number of entities.
        """
        # TODO: Abstract method
        raise NotImplementedError("count must be implemented")


class InMemoryRepository(Repository[T, int], Generic[T]):
    """In-memory implementation of the Repository pattern.
    
    This implementation stores entities in a dictionary.
    Useful for testing and development.
    
    Attributes:
        _storage: Dictionary storing entities by ID.
    """
    
    def __init__(self) -> None:
        """Initialize the repository."""
        # TODO: Initialize self._storage as empty dict: dict[int, T]
        raise NotImplementedError("Initialize storage")
    
    def get(self, id: int) -> Optional[T]:
        """Get entity by ID.
        
        Args:
            id: Entity identifier.
        
        Returns:
            The entity or None.
        """
        # TODO: Return self._storage.get(id)
        raise NotImplementedError("Implement get")
    
    def save(self, entity: T) -> None:
        """Save an entity.
        
        Args:
            entity: Entity to save.
        """
        # TODO: Store entity in _storage using entity.id as key
        raise NotImplementedError("Implement save")
    
    def delete(self, id: int) -> bool:
        """Delete an entity.
        
        Args:
            id: Entity identifier.
        
        Returns:
            True if deleted, False if not found.
        """
        # TODO: Check if id in _storage, delete if present, return True/False
        raise NotImplementedError("Implement delete")
    
    def get_all(self) -> list[T]:
        """Get all entities.
        
        Returns:
            List of all entities.
        """
        # TODO: Return list(self._storage.values())
        raise NotImplementedError("Implement get_all")
    
    def exists(self, id: int) -> bool:
        """Check if entity exists.
        
        Args:
            id: Entity identifier.
        
        Returns:
            True if exists.
        """
        # TODO: Return id in self._storage
        raise NotImplementedError("Implement exists")
    
    def count(self) -> int:
        """Get entity count.
        
        Returns:
            Number of entities.
        """
        # TODO: Return len(self._storage)
        raise NotImplementedError("Implement count")
    
    def clear(self) -> None:
        """Clear all entities (useful for testing)."""
        # TODO: Clear self._storage
        raise NotImplementedError("Implement clear")


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
        # TODO: Return list of users where user.name == name
        raise NotImplementedError("Implement find_by_name")
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email.
        
        Args:
            email: Email to search for.
        
        Returns:
            Matching user or None.
        """
        # TODO: Loop through users, return first where user.email == email
        raise NotImplementedError("Implement find_by_email")
    
    def search(self, query: str) -> list[User]:
        """Search users by name or email.
        
        Args:
            query: Search string.
        
        Returns:
            List of matching users.
        """
        # TODO: Case-insensitive search in both name and email
        raise NotImplementedError("Implement search")
