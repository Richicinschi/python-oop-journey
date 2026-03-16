"""Problem 01: User Service

Topic: Service layer pattern, dependency injection
Difficulty: Medium

Implement a UserService class that encapsulates user management business logic.
The service should coordinate between repositories and external services while
keeping business rules testable and isolated.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class User:
    """Domain model for a user."""
    id: int | None
    email: str
    password_hash: str
    is_active: bool = True


class UserRepository(ABC):
    """Abstract repository for user persistence."""
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        """Retrieve user by ID."""
        raise NotImplementedError("Implement get_by_id")
    
    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """Retrieve user by email."""
        raise NotImplementedError("Implement get_by_email")
    
    @abstractmethod
    def exists(self, email: str) -> bool:
        """Check if email already registered."""
        raise NotImplementedError("Implement exists")
    
    @abstractmethod
    def save(self, user: User) -> User:
        """Save user and return with assigned ID."""
        raise NotImplementedError("Implement save")


class PasswordHasher(ABC):
    """Abstract password hashing service."""
    
    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash a plain-text password."""
        raise NotImplementedError("Implement hash")
    
    @abstractmethod
    def verify(self, password: str, hash_value: str) -> bool:
        """Verify password against hash."""
        raise NotImplementedError("Implement verify")


class EmailService(ABC):
    """Abstract email service."""
    
    @abstractmethod
    def send_welcome_email(self, email: str) -> None:
        """Send welcome email to new user."""
        raise NotImplementedError("Implement send_welcome_email")


@dataclass
class RegistrationResult:
    """Result of user registration attempt."""
    success: bool
    user: User | None = None
    error_message: str | None = None


@dataclass
class AuthenticationResult:
    """Result of authentication attempt."""
    success: bool
    user: User | None = None
    error_message: str | None = None


class UserService:
    """Service for user management operations.
    
    Responsibilities:
    - User registration with validation
    - User authentication
    - Profile retrieval
    
    Dependencies (injected via constructor):
    - user_repo: UserRepository for persistence
    - password_hasher: PasswordHasher for secure passwords
    - email_service: EmailService for notifications
    
    Example:
        >>> service = UserService(repo, hasher, email)
        >>> result = service.register("user@example.com", "password123")
        >>> if result.success:
        ...     print(f"Created user {result.user.id}")
    """
    
    def __init__(
        self,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
        email_service: EmailService,
    ) -> None:
        """Initialize with dependencies.
        
        Args:
            user_repo: Repository for user persistence
            password_hasher: Service for password hashing
            email_service: Service for sending emails
        """
        raise NotImplementedError("Implement __init__")
    
    def register(self, email: str, password: str) -> RegistrationResult:
        """Register a new user.
        
        Business rules:
        - Email must not already exist
        - Password must be at least 8 characters
        - Welcome email sent after successful registration
        
        Args:
            email: User's email address
            password: Plain-text password (will be hashed)
        
        Returns:
            RegistrationResult with success status and user or error
        """
        raise NotImplementedError("Implement register")
    
    def authenticate(self, email: str, password: str) -> AuthenticationResult:
        """Authenticate a user by credentials.
        
        Business rules:
        - User must exist
        - Password must match
        - User must be active
        
        Args:
            email: User's email address
            password: Plain-text password to verify
        
        Returns:
            AuthenticationResult with success status
        """
        raise NotImplementedError("Implement authenticate")
    
    def get_user(self, user_id: int) -> User | None:
        """Retrieve user by ID.
        
        Args:
            user_id: ID of user to retrieve
            
        Returns:
            User if found and active, None otherwise
        """
        raise NotImplementedError("Implement get_user")
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user account.
        
        Args:
            user_id: ID of user to deactivate
            
        Returns:
            True if user was found and deactivated
        """
        raise NotImplementedError("Implement deactivate_user")
