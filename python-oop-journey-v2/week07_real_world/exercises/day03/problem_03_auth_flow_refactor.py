"""Problem 03: Authentication Flow Refactor

Topic: Refactoring Global State to Services
Difficulty: Medium-Hard

Refactor a function-based authentication system with global state into
a service-oriented OOP design with dependency injection.

BEFORE (Procedural with Global State):
    # Global dictionaries - problematic!
    _active_sessions = {}
    _user_database = {}
    
    register_user("alice", "password123")  # Modifies global state
    token = login("alice", "password123")  # Reads global state
    validate_token(token)

AFTER (OOP with DI):
    user_repo = InMemoryUserRepository()
    hasher = PasswordHasher()
    auth_service = AuthService(user_repo, hasher)
    
    auth_service.register("alice", "password123")
    session = auth_service.login("alice", "password123")
    auth_service.validate_token(session.token)

Your task:
1. Create User and Session as value objects
2. Create UserRepository protocol and InMemoryUserRepository
3. Create PasswordHasher for secure password handling
4. Create AuthService with dependency injection (no global state!)
5. Implement proper session expiration

HINTS AND DEBUGGING:

HINT 1 (Conceptual):
The key insight is replacing global state with instance state.
Instead of module-level dictionaries, each AuthService instance
has its own _sessions dict. This enables:
- Testing with isolated instances
- Multiple auth services with different configurations
- Clear ownership of data

HINT 2 (Structural):
Recommended class structure:
1. User (frozen dataclass): username, password_hash, created_at
2. Session (dataclass): token, username, created_at, expires_at
   - Add is_expired property comparing datetime.now() to expires_at
3. UserRepository (Protocol): get, save, exists methods
4. InMemoryUserRepository: implements protocol with dict storage
5. PasswordHasher: hash(password) -> "salt$hashed", verify(password, stored) -> bool
6. AuthService: accepts UserRepository and PasswordHasher in __init__
   - Owns _sessions: dict[str, Session]
   - Implements register, login, validate_token, logout

HINT 3 (Edge Cases):
- Register with existing username: raise ValueError
- Login with wrong password: raise ValueError
- validate_token should clean up expired sessions when found
- Session expiration: created_at + timedelta(hours=24)
- Use secrets.compare_digest() for password comparison (timing attack safe)

DEBUGGING - Common Refactoring Pitfalls:

1. Accidentally keeping global state:
   # WRONG - still global!
   class AuthService:
       _sessions = {}  # Class variable - shared across instances!
   
   # RIGHT - instance state
   class AuthService:
       def __init__(self, ...):
           self._sessions = {}  # Instance variable - per instance

2. Not using dependency injection:
   # WRONG - creates dependencies internally
   class AuthService:
       def __init__(self):
           self._repo = InMemoryUserRepository()  # Hard-coded!
   
   # RIGHT - dependencies injected
   class AuthService:
       def __init__(self, user_repo, hasher):
           self._repo = user_repo
           self._hasher = hasher

3. Protocol confusion:
   # Protocol defines an interface, not a base class
   # Use it for type hints, inherit from it optionally
   def func(repo: UserRepository):  # Accepts anything with get/save/exists
       ...

4. Session expiration logic errors:
   # Common mistake: comparing naive vs timezone-aware datetimes
   # Solution: Use datetime.now() consistently (all naive or all aware)
   # For expiration: session.expires_at < datetime.now()

5. Password hashing mistakes:
   # Never store plain passwords
   # Use secrets.token_hex() for salt (not random.random())
   # Use hashlib.sha256() with salt prepended to password
   # Format: f"{salt}${hashed}" for easy extraction during verify
"""

from __future__ import annotations

import hashlib
import secrets
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Protocol


# ============================================================================
# PROCEDURAL CODE (Before) - DO NOT MODIFY
# This shows the problematic global state approach
# ============================================================================

# Global state - shared across all code, hard to test
_active_sessions_proc: dict[str, dict] = {}
_user_database_proc: dict[str, dict] = {}


def _hash_password_proc(password: str) -> str:
    """Hash password with salt."""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${hashed}"


def _verify_password_proc(password: str, stored: str) -> bool:
    """Verify password against stored hash."""
    salt, hashed = stored.split("$")
    check = hashlib.sha256((password + salt).encode()).hexdigest()
    return secrets.compare_digest(hashed, check)


def register_user_proc(username: str, password: str) -> bool:
    """Register a new user (uses global _user_database_proc)."""
    if username in _user_database_proc:
        return False
    _user_database_proc[username] = {
        "username": username,
        "password_hash": _hash_password_proc(password),
        "created_at": datetime.now().isoformat(),
    }
    return True


def login_proc(username: str, password: str) -> str | None:
    """Login user, create session (uses global state)."""
    user = _user_database_proc.get(username)
    if not user or not _verify_password_proc(password, user["password_hash"]):
        return None
    token = secrets.token_urlsafe(32)
    _active_sessions_proc[token] = {
        "username": username,
        "created_at": datetime.now().isoformat(),
    }
    return token


def validate_token_proc(token: str) -> dict | None:
    """Validate session token (uses global _active_sessions_proc)."""
    return _active_sessions_proc.get(token)


def logout_proc(token: str) -> bool:
    """Logout user (modifies global state)."""
    if token in _active_sessions_proc:
        del _active_sessions_proc[token]
        return True
    return False


def clear_global_state() -> None:
    """Clear global state for testing."""
    _active_sessions_proc.clear()
    _user_database_proc.clear()


# ============================================================================
# YOUR IMPLEMENTATION (After) - TODO: Implement these classes
# ============================================================================


@dataclass(frozen=True)
class User:
    """Immutable user value object.
    
    Attributes:
        username: Unique username
        password_hash: Hashed password with salt
        created_at: Account creation timestamp
    
    TODO: Define the dataclass with frozen=True and appropriate fields
    """
    pass  # TODO: Implement


@dataclass
class Session:
    """Session entity with expiration.
    
    Attributes:
        token: Unique session token
        username: Associated username
        created_at: Session creation time
        expires_at: Session expiration time
    
    TODO:
    1. Define dataclass fields
    2. Implement is_expired property
    3. Implement is_valid property (not expired)
    """
    
    @property
    def is_expired(self) -> bool:
        """TODO: Return True if current time > expires_at."""
        raise NotImplementedError("Implement is_expired")
    
    @property
    def is_valid(self) -> bool:
        """TODO: Return True if session has not expired."""
        raise NotImplementedError("Implement is_valid")


class UserRepository(Protocol):
    """Protocol defining user storage interface.
    
    This is the Repository pattern - abstracts storage mechanism.
    
    TODO: Define these methods:
    - get(username: str) -> User | None
    - save(user: User) -> None
    - exists(username: str) -> bool
    """
    pass  # TODO: Define protocol methods


class InMemoryUserRepository:
    """In-memory implementation of UserRepository.
    
    Replaces the global _user_database with an instance-based storage.
    
    TODO:
    1. Accept storage dict in __init__ (for dependency injection/testing)
    2. Implement get, save, exists methods
    """
    
    def __init__(self, storage: dict[str, User] | None = None) -> None:
        """TODO: Initialize with optional storage dict."""
        raise NotImplementedError("Implement __init__")
    
    def get(self, username: str) -> User | None:
        """TODO: Return User by username or None."""
        raise NotImplementedError("Implement get")
    
    def save(self, user: User) -> None:
        """TODO: Store user by username."""
        raise NotImplementedError("Implement save")
    
    def exists(self, username: str) -> bool:
        """TODO: Check if username exists."""
        raise NotImplementedError("Implement exists")


class PasswordHasher:
    """Encapsulates password hashing strategy.
    
    This makes the hashing algorithm swappable and testable.
    
    TODO:
    1. Implement hash(password: str) -> str with salt
    2. Implement verify(password: str, stored: str) -> bool
    
    Format: "salt$hashed" where hashed = SHA256(password + salt)
    """
    
    def hash(self, password: str) -> str:
        """TODO: Hash password with random salt.
        
        Returns: "salt$hashed" format string
        """
        raise NotImplementedError("Implement hash")
    
    def verify(self, password: str, stored: str) -> bool:
        """TODO: Verify password against stored hash.
        
        Split stored by '$', hash password with same salt,
        compare using secrets.compare_digest
        """
        raise NotImplementedError("Implement verify")


class AuthService:
    """Authentication service with dependency injection.
    
    NO GLOBAL STATE! All state is instance-based.
    
    Dependencies:
    - user_repo: UserRepository for user storage
    - hasher: PasswordHasher for password operations
    
    Owns:
    - _sessions: dict mapping token to Session
    
    TODO:
    1. Accept dependencies in __init__
    2. Implement register(username, password) -> User
    3. Implement login(username, password) -> Session
    4. Implement validate_token(token) -> Session | None
    5. Implement logout(token) -> bool
    """
    
    SESSION_DURATION_HOURS = 24
    
    def __init__(
        self,
        user_repo: UserRepository,
        hasher: PasswordHasher,
    ) -> None:
        """TODO: Initialize with dependencies, create empty sessions dict."""
        raise NotImplementedError("Implement __init__")
    
    def register(self, username: str, password: str) -> User:
        """TODO: Register new user.
        
        Raises:
            ValueError: If username already exists
        
        Returns:
            Created User
        """
        raise NotImplementedError("Implement register")
    
    def login(self, username: str, password: str) -> Session:
        """TODO: Authenticate and create session.
        
        Raises:
            ValueError: If credentials are invalid
        
        Returns:
            New Session with 24-hour expiration
        """
        raise NotImplementedError("Implement login")
    
    def validate_token(self, token: str) -> Session | None:
        """TODO: Validate a session token.
        
        Returns:
            Session if valid and not expired
            None if invalid or expired (clean up expired sessions)
        """
        raise NotImplementedError("Implement validate_token")
    
    def logout(self, token: str) -> bool:
        """TODO: Invalidate a session.
        
        Returns:
            True if session was found and removed
            False if session not found
        """
        raise NotImplementedError("Implement logout")
    
    def get_active_sessions_count(self) -> int:
        """TODO: Return number of active (non-expired) sessions.
        
        This is useful for testing and monitoring.
        """
        raise NotImplementedError("Implement get_active_sessions_count")
