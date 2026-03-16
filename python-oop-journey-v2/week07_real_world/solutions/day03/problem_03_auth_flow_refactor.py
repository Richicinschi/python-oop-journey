"""Reference solution for Problem 03: Authentication Flow Refactor."""

from __future__ import annotations

import hashlib
import secrets
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Protocol


# ============================================================================
# PROCEDURAL CODE (Before) - Kept for reference
# ============================================================================

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
    """Register a new user."""
    if username in _user_database_proc:
        return False
    _user_database_proc[username] = {
        "username": username,
        "password_hash": _hash_password_proc(password),
        "created_at": datetime.now().isoformat(),
    }
    return True


def login_proc(username: str, password: str) -> str | None:
    """Login user, create session."""
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
    """Validate session token."""
    return _active_sessions_proc.get(token)


def logout_proc(token: str) -> bool:
    """Logout user."""
    if token in _active_sessions_proc:
        del _active_sessions_proc[token]
        return True
    return False


def clear_global_state() -> None:
    """Clear global state for testing."""
    _active_sessions_proc.clear()
    _user_database_proc.clear()


# ============================================================================
# OOP IMPLEMENTATION (After)
# ============================================================================


@dataclass(frozen=True)
class User:
    """Immutable user value object."""
    
    username: str
    password_hash: str
    created_at: datetime


@dataclass
class Session:
    """Session entity with expiration."""
    
    token: str
    username: str
    created_at: datetime
    expires_at: datetime
    
    @property
    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        return not self.is_expired


class UserRepository(Protocol):
    """Protocol defining user storage interface."""
    
    def get(self, username: str) -> User | None:
        ...
    
    def save(self, user: User) -> None:
        ...
    
    def exists(self, username: str) -> bool:
        ...


class InMemoryUserRepository:
    """In-memory implementation of UserRepository."""
    
    def __init__(self, storage: dict[str, User] | None = None) -> None:
        self._storage = storage if storage is not None else {}
    
    def get(self, username: str) -> User | None:
        return self._storage.get(username)
    
    def save(self, user: User) -> None:
        self._storage[user.username] = user
    
    def exists(self, username: str) -> bool:
        return username in self._storage


class PasswordHasher:
    """Encapsulates password hashing strategy."""
    
    def hash(self, password: str) -> str:
        salt = secrets.token_hex(16)
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${hashed}"
    
    def verify(self, password: str, stored: str) -> bool:
        salt, hashed = stored.split("$")
        check = hashlib.sha256((password + salt).encode()).hexdigest()
        return secrets.compare_digest(hashed, check)


class AuthService:
    """Authentication service with dependency injection."""
    
    SESSION_DURATION_HOURS = 24
    
    def __init__(
        self,
        user_repo: UserRepository,
        hasher: PasswordHasher,
    ) -> None:
        self._user_repo = user_repo
        self._hasher = hasher
        self._sessions: dict[str, Session] = {}
    
    def register(self, username: str, password: str) -> User:
        """Register a new user."""
        if self._user_repo.exists(username):
            raise ValueError(f"User '{username}' already exists")
        
        password_hash = self._hasher.hash(password)
        user = User(
            username=username,
            password_hash=password_hash,
            created_at=datetime.now(),
        )
        self._user_repo.save(user)
        return user
    
    def login(self, username: str, password: str) -> Session:
        """Authenticate and create session."""
        user = self._user_repo.get(username)
        if not user:
            raise ValueError("Invalid credentials")
        
        if not self._hasher.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")
        
        now = datetime.now()
        session = Session(
            token=secrets.token_urlsafe(32),
            username=username,
            created_at=now,
            expires_at=now + timedelta(hours=self.SESSION_DURATION_HOURS),
        )
        self._sessions[session.token] = session
        return session
    
    def validate_token(self, token: str) -> Session | None:
        """Validate a session token."""
        session = self._sessions.get(token)
        if session and session.is_valid:
            return session
        # Clean up expired session
        if session and session.is_expired:
            del self._sessions[token]
        return None
    
    def logout(self, token: str) -> bool:
        """Invalidate a session."""
        if token in self._sessions:
            del self._sessions[token]
            return True
        return False
    
    def get_active_sessions_count(self) -> int:
        """Return number of active (non-expired) sessions."""
        return sum(1 for s in self._sessions.values() if s.is_valid)
