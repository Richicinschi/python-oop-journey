"""Reference solution for Problem 01: User Service."""

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
    """
    
    def __init__(
        self,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
        email_service: EmailService,
    ) -> None:
        """Initialize with dependencies."""
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._email_service = email_service
    
    def register(self, email: str, password: str) -> RegistrationResult:
        """Register a new user.
        
        Business rules:
        - Email must not already exist
        - Password must be at least 8 characters
        - Welcome email sent after successful registration
        """
        # Validate email not exists
        if self._user_repo.exists(email):
            return RegistrationResult(
                success=False,
                error_message="Email already registered",
            )
        
        # Validate password length
        if len(password) < 8:
            return RegistrationResult(
                success=False,
                error_message="Password must be at least 8 characters",
            )
        
        # Hash password
        password_hash = self._password_hasher.hash(password)
        
        # Create and save user
        user = User(
            id=None,
            email=email,
            password_hash=password_hash,
            is_active=True,
        )
        saved_user = self._user_repo.save(user)
        
        # Send welcome email
        self._email_service.send_welcome_email(email)
        
        return RegistrationResult(success=True, user=saved_user)
    
    def authenticate(self, email: str, password: str) -> AuthenticationResult:
        """Authenticate a user by credentials.
        
        Business rules:
        - User must exist
        - Password must match
        - User must be active
        """
        # Get user by email
        user = self._user_repo.get_by_email(email)
        if user is None:
            return AuthenticationResult(
                success=False,
                error_message="Invalid credentials",
            )
        
        # Verify password
        if not self._password_hasher.verify(password, user.password_hash):
            return AuthenticationResult(
                success=False,
                error_message="Invalid credentials",
            )
        
        # Check user is active
        if not user.is_active:
            return AuthenticationResult(
                success=False,
                error_message="Account is deactivated",
            )
        
        return AuthenticationResult(success=True, user=user)
    
    def get_user(self, user_id: int) -> User | None:
        """Retrieve user by ID."""
        user = self._user_repo.get_by_id(user_id)
        if user is None or not user.is_active:
            return None
        return user
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user account."""
        user = self._user_repo.get_by_id(user_id)
        if user is None:
            return False
        
        user.is_active = False
        self._user_repo.save(user)
        return True
