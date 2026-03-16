"""Reference solution for Problem 02: Repository Pattern with Service Layer."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar


@dataclass
class User:
    """Domain model representing a user."""
    
    email: str
    name: str
    id: int = 0
    is_active: bool = True


T = TypeVar('T')
K = TypeVar('K')


class Repository(ABC, Generic[T, K]):
    """Abstract base class for repositories."""
    
    @abstractmethod
    def get(self, id_: K) -> T | None:
        """Get an entity by its ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> list[T]:
        """Get all entities."""
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Add a new entity."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an existing entity."""
        pass
    
    @abstractmethod
    def delete(self, id_: K) -> bool:
        """Delete an entity by ID."""
        pass
    
    @abstractmethod
    def find_by(self, **kwargs: str | bool | int) -> list[T]:
        """Find entities matching criteria."""
        pass


class InMemoryUserRepository(Repository[User, int]):
    """In-memory implementation of User repository."""
    
    def __init__(self) -> None:
        """Initialize the repository with empty storage."""
        self._users: dict[int, User] = {}
        self._next_id = 1
    
    def get(self, id_: int) -> User | None:
        """Get user by ID."""
        return self._users.get(id_)
    
    def get_all(self) -> list[User]:
        """Get all users."""
        return list(self._users.values())
    
    def add(self, entity: User) -> User:
        """Add new user, auto-assigning ID."""
        entity.id = self._next_id
        self._next_id += 1
        self._users[entity.id] = entity
        return entity
    
    def update(self, entity: User) -> User:
        """Update existing user."""
        if entity.id not in self._users:
            raise ValueError(f"User with id={entity.id} does not exist")
        self._users[entity.id] = entity
        return entity
    
    def delete(self, id_: int) -> bool:
        """Delete user by ID."""
        if id_ in self._users:
            del self._users[id_]
            return True
        return False
    
    def find_by(self, **kwargs: str | bool | int) -> list[User]:
        """Find users by attributes."""
        results = []
        for user in self._users.values():
            match = True
            for key, value in kwargs.items():
                if not hasattr(user, key) or getattr(user, key) != value:
                    match = False
                    break
            if match:
                results.append(user)
        return results


class UserService:
    """Service layer containing user-related business logic."""
    
    def __init__(self, repository: InMemoryUserRepository) -> None:
        """Initialize with a user repository."""
        self._repository = repository
    
    def register_user(self, email: str, name: str) -> User:
        """Register a new user with validation."""
        # Validate email format
        if "@" not in email:
            raise ValueError("Invalid email format: must contain '@'")
        
        # Validate name
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        
        # Check email uniqueness
        existing = self._repository.find_by(email=email)
        if existing:
            raise ValueError(f"Email already registered: {email}")
        
        # Create and save user
        user = User(email=email, name=name.strip())
        return self._repository.add(user)
    
    def activate_user(self, user_id: int) -> User:
        """Activate a user's account."""
        user = self._repository.get(user_id)
        if user is None:
            raise ValueError(f"User with id={user_id} not found")
        user.is_active = True
        return self._repository.update(user)
    
    def deactivate_user(self, user_id: int) -> User:
        """Deactivate a user's account."""
        user = self._repository.get(user_id)
        if user is None:
            raise ValueError(f"User with id={user_id} not found")
        user.is_active = False
        return self._repository.update(user)
    
    def get_active_users(self) -> list[User]:
        """Get all active users."""
        return self._repository.find_by(is_active=True)
    
    def search_users(self, query: str) -> list[User]:
        """Search users by name or email."""
        query_lower = query.lower()
        results = []
        for user in self._repository.get_all():
            if query_lower in user.name.lower() or query_lower in user.email.lower():
                results.append(user)
        return results
