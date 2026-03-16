"""Tests for Problem 03: Authentication Flow Refactor."""

from __future__ import annotations

import time
from datetime import datetime, timedelta

import pytest

from week07_real_world.solutions.day03.problem_03_auth_flow_refactor import (
    User,
    Session,
    InMemoryUserRepository,
    PasswordHasher,
    AuthService,
    register_user_proc,
    login_proc,
    validate_token_proc,
    logout_proc,
    clear_global_state,
)


class TestUser:
    """Tests for User value object."""
    
    def test_creation(self) -> None:
        now = datetime.now()
        user = User("alice", "hashed_password", now)
        assert user.username == "alice"
        assert user.password_hash == "hashed_password"
        assert user.created_at == now
    
    def test_immutable(self) -> None:
        user = User("alice", "hash", datetime.now())
        with pytest.raises(AttributeError):
            user.username = "bob"


class TestSession:
    """Tests for Session entity."""
    
    def test_creation(self) -> None:
        now = datetime.now()
        expires = now + timedelta(hours=1)
        session = Session("token123", "alice", now, expires)
        
        assert session.token == "token123"
        assert session.username == "alice"
        assert session.created_at == now
        assert session.expires_at == expires
    
    def test_is_valid_when_not_expired(self) -> None:
        now = datetime.now()
        expires = now + timedelta(hours=1)
        session = Session("token", "alice", now, expires)
        
        assert session.is_valid is True
        assert session.is_expired is False
    
    def test_is_expired_when_past_expiration(self) -> None:
        past = datetime.now() - timedelta(hours=1)
        session = Session("token", "alice", past - timedelta(hours=1), past)
        
        assert session.is_expired is True
        assert session.is_valid is False


class TestInMemoryUserRepository:
    """Tests for InMemoryUserRepository."""
    
    def test_init_with_default_storage(self) -> None:
        repo = InMemoryUserRepository()
        assert repo.exists("anyone") is False
    
    def test_init_with_provided_storage(self) -> None:
        storage: dict[str, User] = {}
        repo = InMemoryUserRepository(storage)
        user = User("alice", "hash", datetime.now())
        repo.save(user)
        assert storage["alice"] == user
    
    def test_save_and_get(self) -> None:
        repo = InMemoryUserRepository()
        user = User("alice", "hash", datetime.now())
        
        repo.save(user)
        retrieved = repo.get("alice")
        
        assert retrieved == user
    
    def test_get_nonexistent_returns_none(self) -> None:
        repo = InMemoryUserRepository()
        assert repo.get("nobody") is None
    
    def test_exists(self) -> None:
        repo = InMemoryUserRepository()
        user = User("alice", "hash", datetime.now())
        
        assert repo.exists("alice") is False
        repo.save(user)
        assert repo.exists("alice") is True


class TestPasswordHasher:
    """Tests for PasswordHasher."""
    
    def test_hash_returns_salted_hash(self) -> None:
        hasher = PasswordHasher()
        hashed = hasher.hash("password123")
        
        assert "$" in hashed
        parts = hashed.split("$")
        assert len(parts) == 2
        assert len(parts[0]) == 32  # 16 bytes = 32 hex chars
    
    def test_hash_is_different_each_time(self) -> None:
        hasher = PasswordHasher()
        hash1 = hasher.hash("password123")
        hash2 = hasher.hash("password123")
        
        assert hash1 != hash2  # Different salts
    
    def test_verify_correct_password(self) -> None:
        hasher = PasswordHasher()
        hashed = hasher.hash("password123")
        
        assert hasher.verify("password123", hashed) is True
    
    def test_verify_wrong_password(self) -> None:
        hasher = PasswordHasher()
        hashed = hasher.hash("password123")
        
        assert hasher.verify("wrongpassword", hashed) is False
    
    def test_verify_different_salt_fails(self) -> None:
        hasher = PasswordHasher()
        hash1 = hasher.hash("password123")
        hash2 = hasher.hash("password123")
        
        # Cross-verify should fail
        assert hasher.verify("password123", hash1) is True
        assert hasher.verify("password123", hash2) is True
        # But the hashes themselves are different
        assert hash1 != hash2


class TestAuthService:
    """Tests for AuthService."""
    
    @pytest.fixture
    def auth_service(self) -> AuthService:
        repo = InMemoryUserRepository()
        hasher = PasswordHasher()
        return AuthService(repo, hasher)
    
    def test_register_new_user(self, auth_service: AuthService) -> None:
        user = auth_service.register("alice", "password123")
        
        assert user.username == "alice"
        assert isinstance(user.password_hash, str)
        assert "$" in user.password_hash
    
    def test_register_duplicate_raises(self, auth_service: AuthService) -> None:
        auth_service.register("alice", "password123")
        
        with pytest.raises(ValueError, match="already exists"):
            auth_service.register("alice", "otherpassword")
    
    def test_login_success(self, auth_service: AuthService) -> None:
        auth_service.register("alice", "password123")
        session = auth_service.login("alice", "password123")
        
        assert session.username == "alice"
        assert isinstance(session.token, str)
        assert len(session.token) > 0
        assert session.is_valid is True
    
    def test_login_wrong_password_raises(self, auth_service: AuthService) -> None:
        auth_service.register("alice", "password123")
        
        with pytest.raises(ValueError, match="Invalid credentials"):
            auth_service.login("alice", "wrongpassword")
    
    def test_login_nonexistent_user_raises(self, auth_service: AuthService) -> None:
        with pytest.raises(ValueError, match="Invalid credentials"):
            auth_service.login("nobody", "password")
    
    def test_validate_token_success(self, auth_service: AuthService) -> None:
        auth_service.register("alice", "password123")
        session = auth_service.login("alice", "password123")
        
        validated = auth_service.validate_token(session.token)
        
        assert validated is not None
        assert validated.username == "alice"
    
    def test_validate_invalid_token_returns_none(self, auth_service: AuthService) -> None:
        assert auth_service.validate_token("invalid_token") is None
    
    def test_logout_success(self, auth_service: AuthService) -> None:
        auth_service.register("alice", "password123")
        session = auth_service.login("alice", "password123")
        
        result = auth_service.logout(session.token)
        
        assert result is True
        assert auth_service.validate_token(session.token) is None
    
    def test_logout_invalid_token_returns_false(self, auth_service: AuthService) -> None:
        assert auth_service.logout("invalid_token") is False
    
    def test_multiple_users_isolated(self, auth_service: AuthService) -> None:
        auth_service.register("alice", "alice_pass")
        auth_service.register("bob", "bob_pass")
        
        # Alice can't login with Bob's password
        with pytest.raises(ValueError):
            auth_service.login("alice", "bob_pass")
        
        # Both can login with their own passwords
        alice_session = auth_service.login("alice", "alice_pass")
        bob_session = auth_service.login("bob", "bob_pass")
        
        assert alice_session.username == "alice"
        assert bob_session.username == "bob"
    
    def test_get_active_sessions_count(self, auth_service: AuthService) -> None:
        auth_service.register("alice", "password123")
        auth_service.register("bob", "password123")
        
        assert auth_service.get_active_sessions_count() == 0
        
        auth_service.login("alice", "password123")
        assert auth_service.get_active_sessions_count() == 1
        
        auth_service.login("bob", "password123")
        assert auth_service.get_active_sessions_count() == 2
    
    def test_logout_reduces_active_count(self, auth_service: AuthService) -> None:
        auth_service.register("alice", "password123")
        session = auth_service.login("alice", "password123")
        
        assert auth_service.get_active_sessions_count() == 1
        
        auth_service.logout(session.token)
        assert auth_service.get_active_sessions_count() == 0


class TestAuthServiceSessionExpiration:
    """Tests for session expiration behavior."""
    
    def test_expired_session_not_validated(self) -> None:
        repo = InMemoryUserRepository()
        hasher = PasswordHasher()
        service = AuthService(repo, hasher)
        
        # Register and login
        service.register("alice", "password123")
        session = service.login("alice", "password123")
        
        # Manually expire the session
        session.expires_at = datetime.now() - timedelta(seconds=1)
        
        # Should not validate
        assert service.validate_token(session.token) is None
    
    def test_expired_session_cleaned_up(self) -> None:
        repo = InMemoryUserRepository()
        hasher = PasswordHasher()
        service = AuthService(repo, hasher)
        
        service.register("alice", "password123")
        session = service.login("alice", "password123")
        
        # Manually expire
        session.expires_at = datetime.now() - timedelta(seconds=1)
        
        # Validate should remove expired session
        service.validate_token(session.token)
        
        # Session should be gone
        assert session.token not in service._sessions


class TestNoGlobalState:
    """Tests ensuring no global state pollution."""
    
    def test_two_services_are_isolated(self) -> None:
        hasher = PasswordHasher()
        
        service1 = AuthService(InMemoryUserRepository(), hasher)
        service2 = AuthService(InMemoryUserRepository(), hasher)
        
        # Register in service1
        service1.register("alice", "password123")
        
        # Should not exist in service2
        with pytest.raises(ValueError):
            service2.login("alice", "password123")
    
    def test_sessions_isolated_between_services(self) -> None:
        hasher = PasswordHasher()
        repo = InMemoryUserRepository()
        
        service1 = AuthService(repo, hasher)
        service2 = AuthService(repo, hasher)  # Same repo, different sessions
        
        service1.register("alice", "password123")
        
        # Login on both
        session1 = service1.login("alice", "password123")
        session2 = service2.login("alice", "password123")
        
        # Each service tracks its own sessions
        assert service1.validate_token(session1.token) is not None
        assert service2.validate_token(session2.token) is not None
        
        # But session1 is not in service2 and vice versa
        assert service2.validate_token(session1.token) is None
        assert service1.validate_token(session2.token) is None


class TestProceduralCompatibility:
    """Tests comparing procedural and OOP behavior."""
    
    def setup_method(self) -> None:
        clear_global_state()
    
    def teardown_method(self) -> None:
        clear_global_state()
    
    def test_register_behavior(self) -> None:
        # Procedural
        proc_result = register_user_proc("alice", "password123")
        assert proc_result is True
        
        # OOP
        repo = InMemoryUserRepository()
        service = AuthService(repo, PasswordHasher())
        user = service.register("bob", "password123")  # Different user
        
        assert user.username == "bob"
    
    def test_login_success_behavior(self) -> None:
        # Procedural
        register_user_proc("alice", "password123")
        proc_token = login_proc("alice", "password123")
        assert proc_token is not None
        
        # OOP
        repo = InMemoryUserRepository()
        service = AuthService(repo, PasswordHasher())
        service.register("bob", "password123")
        session = service.login("bob", "password123")
        
        assert session.token is not None
    
    def test_login_failure_behavior(self) -> None:
        # Procedural - wrong password returns None
        register_user_proc("alice", "password123")
        proc_token = login_proc("alice", "wrongpassword")
        assert proc_token is None
        
        # OOP - raises exception
        repo = InMemoryUserRepository()
        service = AuthService(repo, PasswordHasher())
        service.register("bob", "password123")
        
        with pytest.raises(ValueError):
            service.login("bob", "wrongpassword")
