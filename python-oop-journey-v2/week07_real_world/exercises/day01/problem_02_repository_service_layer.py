"""Problem 02: Repository Pattern with Service Layer

Topic: API Design with Classes - Repository Pattern
Difficulty: Medium

Implement the Repository pattern to abstract data access,
plus a service layer that contains business logic.

HINTS AND DEBUGGING:

HINT 1 (Conceptual):
The Repository pattern abstracts data access so your application
doesn't care whether data comes from memory, a database, or an API.

Key insight: The Service Layer depends on Repository INTERFACE,
not a concrete implementation. This enables:
- Testing with in-memory repositories
- Swapping storage without changing business logic
- Clear separation between data access and business logic

HINT 2 (Structural):

Repository (Abstract Base Class):
- Generic[T, K] where T = entity type, K = key type
- Methods: get(id), add(entity), update(entity), delete(id), list_all()
- Returns None from get() if not found

InMemoryRepository (Concrete):
- Takes storage dict in __init__ (allows injection for testing)
- Stores entities in self._storage: dict[K, T]
- Generate ID for new entities (max existing + 1 or 1 if empty)

UserService (Business Logic):
- Accepts Repository[User, int] in __init__
- Implements business rules (unique email, name required, etc.)
- Methods: register_user, get_user, update_user, deactivate_user

HINT 3 (Edge Cases):
- Register with duplicate email: raise ValueError
- Get non-existent user: return None (don't raise)
- Update non-existent user: raise ValueError
- Delete non-existent user: return False
- Empty name/email: raise ValueError during registration

DEBUGGING - Common Repository Pattern Mistakes:

1. Not using Generic types:
   # Without generics, repository isn't reusable
   class Repository:  # Not generic
       def get(self, id: int) -> User: ...  # Only works for User!
   
   # With generics
   class Repository(ABC, Generic[T, K]):
       def get(self, id: K) -> T | None: ...  # Works for any type

2. Repository with business logic:
   # WRONG - repository should just store/retrieve
   class UserRepository:
       def add(self, user):
           if not self._is_valid_email(user.email):  # Business logic!
               raise ValueError
   
   # RIGHT - validation in service layer
   class UserService:
       def register(self, email, name):
           if not self._is_valid_email(email):
               raise ValueError
           self._repo.add(User(email, name))

3. Service creating its own repository:
   # WRONG - hard to test
   class UserService:
       def __init__(self):
           self._repo = InMemoryRepository()  # Can't inject mock!
   
   # RIGHT - dependency injection
   class UserService:
       def __init__(self, repo: Repository[User, int]):
           self._repo = repo

4. Not handling ID generation:
   # New entities have id=0, need to assign real ID on add
   def add(self, entity: T) -> T:
       if entity.id == 0:
           entity.id = self._next_id()
       self._storage[entity.id] = entity
       return entity
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar


@dataclass
class User:
    """Domain model representing a user.
    
    Attributes:
        id: Unique identifier (0 for new users)
        email: User's email address
        name: User's display name
        is_active: Whether the account is active
    """
    email: str
    name: str
    id: int = 0
    is_active: bool = True


# Generic types for repository
T = TypeVar('T')
K = TypeVar('K')


class Repository(ABC, Generic[T, K]):
    """Abstract base class for repositories.
    
    Provides the standard CRUD interface for any entity type.
    
    Type Parameters:
        T: The entity type this repository manages
        K: The type of the entity's primary key
    """
    
    @abstractmethod
    def get(self, id_: K) -> T | None:
        """Get an entity by its ID.
        
        Args:
            id_: The entity's primary key
            
        Returns:
            The entity if found, None otherwise
        """
        raise NotImplementedError("Implement Repository.get")
    
    @abstractmethod
    def get_all(self) -> list[T]:
        """Get all entities.
        
        Returns:
            List of all entities in the repository
        """
        raise NotImplementedError("Implement Repository.get_all")
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Add a new entity.
        
        Args:
            entity: The entity to add (ID may be 0 for new entities)
            
        Returns:
            The added entity with its assigned ID
        """
        raise NotImplementedError("Implement Repository.add")
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an existing entity.
        
        Args:
            entity: The entity with updated values
            
        Returns:
            The updated entity
            
        Raises:
            ValueError: If entity doesn't exist
        """
        raise NotImplementedError("Implement Repository.update")
    
    @abstractmethod
    def delete(self, id_: K) -> bool:
        """Delete an entity by ID.
        
        Args:
            id_: The entity's primary key
            
        Returns:
            True if deleted, False if not found
        """
        raise NotImplementedError("Implement Repository.delete")
    
    @abstractmethod
    def find_by(self, **kwargs: str | bool | int) -> list[T]:
        """Find entities matching criteria.
        
        Args:
            **kwargs: Attribute names and values to match
            
        Returns:
            List of matching entities
        """
        raise NotImplementedError("Implement Repository.find_by")


class InMemoryUserRepository(Repository[User, int]):
    """In-memory implementation of User repository.
    
    Stores users in memory. Useful for testing.
    """
    
    def __init__(self) -> None:
        """Initialize the repository with empty storage."""
        raise NotImplementedError("Implement InMemoryUserRepository.__init__")
    
    def get(self, id_: int) -> User | None:
        """Get user by ID."""
        raise NotImplementedError("Implement InMemoryUserRepository.get")
    
    def get_all(self) -> list[User]:
        """Get all users."""
        raise NotImplementedError("Implement InMemoryUserRepository.get_all")
    
    def add(self, entity: User) -> User:
        """Add new user, auto-assigning ID."""
        raise NotImplementedError("Implement InMemoryUserRepository.add")
    
    def update(self, entity: User) -> User:
        """Update existing user."""
        raise NotImplementedError("Implement InMemoryUserRepository.update")
    
    def delete(self, id_: int) -> bool:
        """Delete user by ID."""
        raise NotImplementedError("Implement InMemoryUserRepository.delete")
    
    def find_by(self, **kwargs: str | bool | int) -> list[User]:
        """Find users by attributes.
        
        Examples:
            repo.find_by(email="user@example.com")
            repo.find_by(is_active=True)
        """
        raise NotImplementedError("Implement InMemoryUserRepository.find_by")


class UserService:
    """Service layer containing user-related business logic.
    
    The service layer sits between the API/controllers and the
    repository, handling business rules and orchestration.
    """
    
    def __init__(self, repository: InMemoryUserRepository) -> None:
        """Initialize with a user repository.
        
        Args:
            repository: The repository for user data access
        """
        raise NotImplementedError("Implement UserService.__init__")
    
    def register_user(self, email: str, name: str) -> User:
        """Register a new user with validation.
        
        Business Rules:
        - Email must be unique
        - Email must contain '@'
        - Name must not be empty
        
        Args:
            email: User's email address
            name: User's display name
            
        Returns:
            The newly created user
            
        Raises:
            ValueError: If validation fails
        """
        raise NotImplementedError("Implement UserService.register_user")
    
    def activate_user(self, user_id: int) -> User:
        """Activate a user's account.
        
        Args:
            user_id: ID of the user to activate
            
        Returns:
            The activated user
            
        Raises:
            ValueError: If user not found
        """
        raise NotImplementedError("Implement UserService.activate_user")
    
    def deactivate_user(self, user_id: int) -> User:
        """Deactivate a user's account.
        
        Args:
            user_id: ID of the user to deactivate
            
        Returns:
            The deactivated user
            
        Raises:
            ValueError: If user not found
        """
        raise NotImplementedError("Implement UserService.deactivate_user")
    
    def get_active_users(self) -> list[User]:
        """Get all active users.
        
        Returns:
            List of users with is_active=True
        """
        raise NotImplementedError("Implement UserService.get_active_users")
    
    def search_users(self, query: str) -> list[User]:
        """Search users by name or email.
        
        Args:
            query: Search string (case-insensitive)
            
        Returns:
            List of users whose name or email contains the query
        """
        raise NotImplementedError("Implement UserService.search_users")
