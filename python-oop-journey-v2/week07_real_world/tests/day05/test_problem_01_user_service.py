"""Tests for Problem 01: User Service."""

from __future__ import annotations

import pytest

from week07_real_world.solutions.day05.problem_01_user_service import (
    AuthenticationResult,
    EmailService,
    PasswordHasher,
    RegistrationResult,
    User,
    UserRepository,
    UserService,
)


class MockUserRepository(UserRepository):
    """Mock implementation of UserRepository for testing."""
    
    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._email_index: dict[str, int] = {}
        self._next_id = 1
    
    def get_by_id(self, user_id: int) -> User | None:
        return self._users.get(user_id)
    
    def get_by_email(self, email: str) -> User | None:
        user_id = self._email_index.get(email)
        if user_id:
            return self._users.get(user_id)
        return None
    
    def exists(self, email: str) -> bool:
        return email in self._email_index
    
    def save(self, user: User) -> User:
        if user.id is None:
            user = User(
                id=self._next_id,
                email=user.email,
                password_hash=user.password_hash,
                is_active=user.is_active,
            )
            self._next_id += 1
        self._users[user.id] = user
        self._email_index[user.email] = user.id
        return user


class MockPasswordHasher(PasswordHasher):
    """Mock implementation of PasswordHasher for testing."""
    
    def hash(self, password: str) -> str:
        return f"hashed_{password}"
    
    def verify(self, password: str, hash_value: str) -> bool:
        return hash_value == f"hashed_{password}"


class MockEmailService(EmailService):
    """Mock implementation of EmailService for testing."""
    
    def __init__(self) -> None:
        self.sent_emails: list[str] = []
    
    def send_welcome_email(self, email: str) -> None:
        self.sent_emails.append(email)


@pytest.fixture
def user_service() -> UserService:
    """Create a UserService with mock dependencies."""
    return UserService(
        user_repo=MockUserRepository(),
        password_hasher=MockPasswordHasher(),
        email_service=MockEmailService(),
    )


@pytest.fixture
def user_service_with_email() -> tuple[UserService, MockEmailService]:
    """Create a UserService with accessible mock email service."""
    email_service = MockEmailService()
    service = UserService(
        user_repo=MockUserRepository(),
        password_hasher=MockPasswordHasher(),
        email_service=email_service,
    )
    return service, email_service


class TestUserService:
    """Tests for UserService class."""
    
    def test_register_creates_user(self, user_service: UserService) -> None:
        """Test that register creates a new user."""
        result = user_service.register("test@example.com", "password123")
        
        assert result.success
        assert result.user is not None
        assert result.user.id is not None
        assert result.user.email == "test@example.com"
        assert result.user.is_active
    
    def test_register_hashes_password(self, user_service: UserService) -> None:
        """Test that register hashes the password."""
        result = user_service.register("test@example.com", "password123")
        
        assert result.user is not None
        assert result.user.password_hash == "hashed_password123"
    
    def test_register_rejects_duplicate_email(
        self, user_service: UserService
    ) -> None:
        """Test that register rejects duplicate emails."""
        user_service.register("test@example.com", "password123")
        result = user_service.register("test@example.com", "password456")
        
        assert not result.success
        assert result.error_message == "Email already registered"
        assert result.user is None
    
    def test_register_rejects_short_password(
        self, user_service: UserService
    ) -> None:
        """Test that register rejects passwords shorter than 8 characters."""
        result = user_service.register("test@example.com", "short")
        
        assert not result.success
        assert "at least 8 characters" in result.error_message
    
    def test_register_sends_welcome_email(
        self, user_service_with_email: tuple[UserService, MockEmailService]
    ) -> None:
        """Test that register sends a welcome email."""
        service, email_service = user_service_with_email
        service.register("test@example.com", "password123")
        
        assert "test@example.com" in email_service.sent_emails
    
    def test_authenticate_success(self, user_service: UserService) -> None:
        """Test successful authentication."""
        user_service.register("test@example.com", "password123")
        result = user_service.authenticate("test@example.com", "password123")
        
        assert result.success
        assert result.user is not None
        assert result.user.email == "test@example.com"
    
    def test_authenticate_wrong_password(self, user_service: UserService) -> None:
        """Test authentication with wrong password."""
        user_service.register("test@example.com", "password123")
        result = user_service.authenticate("test@example.com", "wrongpassword")
        
        assert not result.success
        assert "Invalid credentials" in result.error_message
    
    def test_authenticate_nonexistent_user(
        self, user_service: UserService
    ) -> None:
        """Test authentication for non-existent user."""
        result = user_service.authenticate("nobody@example.com", "password123")
        
        assert not result.success
        assert "Invalid credentials" in result.error_message
    
    def test_authenticate_inactive_user(self, user_service: UserService) -> None:
        """Test authentication for deactivated user."""
        reg_result = user_service.register("test@example.com", "password123")
        assert reg_result.user is not None
        
        user_service.deactivate_user(reg_result.user.id)
        result = user_service.authenticate("test@example.com", "password123")
        
        assert not result.success
        assert "deactivated" in result.error_message
    
    def test_get_user_returns_active_user(
        self, user_service: UserService
    ) -> None:
        """Test get_user returns active user."""
        reg_result = user_service.register("test@example.com", "password123")
        assert reg_result.user is not None
        
        user = user_service.get_user(reg_result.user.id)
        
        assert user is not None
        assert user.email == "test@example.com"
    
    def test_get_user_returns_none_for_inactive(
        self, user_service: UserService
    ) -> None:
        """Test get_user returns None for inactive user."""
        reg_result = user_service.register("test@example.com", "password123")
        assert reg_result.user is not None
        
        user_service.deactivate_user(reg_result.user.id)
        user = user_service.get_user(reg_result.user.id)
        
        assert user is None
    
    def test_get_user_returns_none_for_nonexistent(
        self, user_service: UserService
    ) -> None:
        """Test get_user returns None for non-existent user."""
        user = user_service.get_user(999)
        
        assert user is None
    
    def test_deactivate_user_success(self, user_service: UserService) -> None:
        """Test successful user deactivation."""
        reg_result = user_service.register("test@example.com", "password123")
        assert reg_result.user is not None
        
        success = user_service.deactivate_user(reg_result.user.id)
        
        assert success
        
        # Verify user is inactive
        user = user_service._user_repo.get_by_id(reg_result.user.id)
        assert user is not None
        assert not user.is_active
    
    def test_deactivate_user_nonexistent(self, user_service: UserService) -> None:
        """Test deactivation of non-existent user."""
        success = user_service.deactivate_user(999)
        
        assert not success
