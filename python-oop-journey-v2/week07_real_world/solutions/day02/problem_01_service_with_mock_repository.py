"""Reference solution for Problem 01: Service with Mock Repository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Domain entity representing a user."""
    
    id: int
    username: str
    email: str
    is_active: bool = True


class UserRepository(ABC):
    """Abstract repository interface for user operations."""
    
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find a user by their ID."""
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by their email address."""
        pass
    
    @abstractmethod
    def save(self, user: User) -> User:
        """Save a user to the repository."""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete a user by their ID."""
        pass


class UserNotFoundError(Exception):
    """Raised when a requested user cannot be found."""
    pass


class DuplicateEmailError(Exception):
    """Raised when attempting to create a user with an existing email."""
    pass


class UserService:
    """Service class for user-related business operations."""
    
    def __init__(self, repository: UserRepository) -> None:
        """Initialize the service with a repository."""
        self._repository = repository
    
    def get_user(self, user_id: int) -> User:
        """Retrieve a user by ID."""
        user = self._repository.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        return user
    
    def register_user(self, username: str, email: str) -> User:
        """Register a new user."""
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        if not email or "@" not in email:
            raise ValueError("Invalid email address")
        
        normalized_email = email.strip().lower()
        existing = self._repository.find_by_email(normalized_email)
        if existing is not None:
            raise DuplicateEmailError(f"Email {normalized_email} is already registered")
        
        user = User(id=0, username=username.strip(), email=normalized_email)
        return self._repository.save(user)
    
    def deactivate_user(self, user_id: int) -> User:
        """Deactivate a user account."""
        user = self.get_user(user_id)
        user.is_active = False
        return self._repository.save(user)
    
    def update_email(self, user_id: int, new_email: str) -> User:
        """Update a user's email address."""
        if not new_email or "@" not in new_email:
            raise ValueError("Invalid email address")
        
        user = self.get_user(user_id)
        
        existing = self._repository.find_by_email(new_email.strip().lower())
        if existing is not None and existing.id != user_id:
            raise DuplicateEmailError(f"Email {new_email} is already registered")
        
        user.email = new_email.strip().lower()
        return self._repository.save(user)
