"""Problem 01: Service with Mock Repository

Topic: Mocking dependencies
Difficulty: Medium

Learn to isolate service classes from their dependencies using mocks.
This enables fast, deterministic unit tests without real database connections.
"""

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
    """Abstract repository interface for user operations.
    
    This interface defines the contract that concrete repositories must implement.
    Services depend on this abstraction, not concrete implementations.
    """
    
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find a user by their ID.
        
        Args:
            user_id: The unique identifier of the user
            
        Returns:
            The User if found, None otherwise
        """
        raise NotImplementedError("Implement find_by_id")
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by their email address.
        
        Args:
            email: The email address to search for
            
        Returns:
            The User if found, None otherwise
        """
        raise NotImplementedError("Implement find_by_email")
    
    @abstractmethod
    def save(self, user: User) -> User:
        """Save a user to the repository.
        
        Args:
            user: The user to save
            
        Returns:
            The saved user with any generated fields populated
        """
        raise NotImplementedError("Implement save")
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete a user by their ID.
        
        Args:
            user_id: The ID of the user to delete
            
        Returns:
            True if deleted, False if not found
        """
        raise NotImplementedError("Implement delete")


class UserNotFoundError(Exception):
    """Raised when a requested user cannot be found."""
    pass


class DuplicateEmailError(Exception):
    """Raised when attempting to create a user with an existing email."""
    pass


class UserService:
    """Service class for user-related business operations.
    
    This service orchestrates user operations while remaining agnostic
    to the underlying persistence mechanism through repository abstraction.
    
    TODO: Implement all methods following the docstring specifications.
    """
    
    def __init__(self, repository: UserRepository) -> None:
        """Initialize the service with a repository.
        
        Args:
            repository: The repository to use for persistence
        """
        raise NotImplementedError("Implement __init__")
    
    def get_user(self, user_id: int) -> User:
        """Retrieve a user by ID.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            The requested user
            
        Raises:
            UserNotFoundError: If the user doesn't exist
        """
        raise NotImplementedError("Implement get_user")
    
    def register_user(self, username: str, email: str) -> User:
        """Register a new user.
        
        Args:
            username: The desired username
            email: The user's email address
            
        Returns:
            The newly created user
            
        Raises:
            DuplicateEmailError: If the email is already registered
            ValueError: If username or email is empty/invalid
        """
        raise NotImplementedError("Implement register_user")
    
    def deactivate_user(self, user_id: int) -> User:
        """Deactivate a user account.
        
        Args:
            user_id: The ID of the user to deactivate
            
        Returns:
            The deactivated user
            
        Raises:
            UserNotFoundError: If the user doesn't exist
        """
        raise NotImplementedError("Implement deactivate_user")
    
    def update_email(self, user_id: int, new_email: str) -> User:
        """Update a user's email address.
        
        Args:
            user_id: The ID of the user to update
            new_email: The new email address
            
        Returns:
            The updated user
            
        Raises:
            UserNotFoundError: If the user doesn't exist
            DuplicateEmailError: If the new email is already registered
            ValueError: If the email is invalid
        """
        raise NotImplementedError("Implement update_email")
