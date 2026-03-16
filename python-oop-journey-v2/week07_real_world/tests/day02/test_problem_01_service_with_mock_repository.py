"""Tests for Problem 01: Service with Mock Repository."""

from __future__ import annotations

from typing import cast
from unittest.mock import Mock, create_autospec

import pytest

from week07_real_world.solutions.day02.problem_01_service_with_mock_repository import (
    DuplicateEmailError,
    User,
    UserNotFoundError,
    UserRepository,
    UserService,
)


class TestUserServiceGetUser:
    """Tests for get_user method."""
    
    def test_get_existing_user_returns_user(self) -> None:
        """Should return user when found by ID."""
        # Arrange
        mock_repo = create_autospec(UserRepository)
        expected_user = User(id=1, username="alice", email="alice@example.com")
        mock_repo.find_by_id.return_value = expected_user
        
        service = UserService(mock_repo)
        
        # Act
        result = service.get_user(1)
        
        # Assert
        assert result == expected_user
        mock_repo.find_by_id.assert_called_once_with(1)
    
    def test_get_nonexistent_user_raises_error(self) -> None:
        """Should raise UserNotFoundError when user doesn't exist."""
        # Arrange
        mock_repo = create_autospec(UserRepository)
        mock_repo.find_by_id.return_value = None
        
        service = UserService(mock_repo)
        
        # Act & Assert
        with pytest.raises(UserNotFoundError, match="User with ID 999 not found"):
            service.get_user(999)
        
        mock_repo.find_by_id.assert_called_once_with(999)


class TestUserServiceRegisterUser:
    """Tests for register_user method."""
    
    def test_register_new_user_saves_to_repository(self) -> None:
        """Should create and save a new user."""
        # Arrange
        mock_repo = create_autospec(UserRepository)
        mock_repo.find_by_email.return_value = None
        mock_repo.save.return_value = User(id=1, username="bob", email="bob@example.com")
        
        service = UserService(mock_repo)
        
        # Act
        result = service.register_user("bob", "bob@example.com")
        
        # Assert
        assert result.username == "bob"
        assert result.email == "bob@example.com"
        mock_repo.find_by_email.assert_called_once_with("bob@example.com")
        mock_repo.save.assert_called_once()
    
    def test_register_duplicate_email_raises_error(self) -> None:
        """Should raise DuplicateEmailError when email exists."""
        # Arrange
        existing_user = User(id=1, username="alice", email="taken@example.com")
        mock_repo = create_autospec(UserRepository)
        mock_repo.find_by_email.return_value = existing_user
        
        service = UserService(mock_repo)
        
        # Act & Assert
        with pytest.raises(DuplicateEmailError, match="taken@example.com"):
            service.register_user("newuser", "taken@example.com")
        
        mock_repo.save.assert_not_called()
    
    @pytest.mark.parametrize("username,email", [
        ("", "valid@example.com"),
        ("   ", "valid@example.com"),
        (None, "valid@example.com"),
    ])
    def test_register_empty_username_raises_error(self, username: str, email: str) -> None:
        """Should raise ValueError for empty username."""
        mock_repo = create_autospec(UserRepository)
        service = UserService(mock_repo)
        
        with pytest.raises(ValueError, match="Username cannot be empty"):
            service.register_user(cast(str, username), email)
    
    @pytest.mark.parametrize("email", [
        "",
        "   ",
        "not-an-email",
        "missing-at-sign",
    ])
    def test_register_invalid_email_raises_error(self, email: str) -> None:
        """Should raise ValueError for invalid email."""
        mock_repo = create_autospec(UserRepository)
        service = UserService(mock_repo)
        
        with pytest.raises(ValueError, match="Invalid email address"):
            service.register_user("validuser", email)
    
    def test_register_normalizes_email_case(self) -> None:
        """Should lowercase email addresses."""
        mock_repo = create_autospec(UserRepository)
        mock_repo.find_by_email.return_value = None
        mock_repo.save.return_value = User(id=1, username="user", email="user@example.com")
        
        service = UserService(mock_repo)
        service.register_user("user", "USER@EXAMPLE.COM")
        
        # Check that find was called with uppercase (we lowercase in service, then search)
        mock_repo.find_by_email.assert_called_once_with("user@example.com")


class TestUserServiceDeactivateUser:
    """Tests for deactivate_user method."""
    
    def test_deactivate_sets_is_active_false(self) -> None:
        """Should set is_active to False and save."""
        # Arrange
        user = User(id=1, username="alice", email="alice@example.com", is_active=True)
        mock_repo = create_autospec(UserRepository)
        mock_repo.find_by_id.return_value = user
        mock_repo.save.return_value = User(id=1, username="alice", email="alice@example.com", is_active=False)
        
        service = UserService(mock_repo)
        
        # Act
        result = service.deactivate_user(1)
        
        # Assert
        assert result.is_active is False
        mock_repo.save.assert_called_once()
    
    def test_deactivate_nonexistent_user_raises_error(self) -> None:
        """Should raise UserNotFoundError for unknown user."""
        mock_repo = create_autospec(UserRepository)
        mock_repo.find_by_id.return_value = None
        
        service = UserService(mock_repo)
        
        with pytest.raises(UserNotFoundError):
            service.deactivate_user(999)


class TestUserServiceUpdateEmail:
    """Tests for update_email method."""
    
    def test_update_email_success(self) -> None:
        """Should update email when valid and not duplicate."""
        # Arrange
        user = User(id=1, username="alice", email="old@example.com")
        mock_repo = create_autospec(UserRepository)
        mock_repo.find_by_id.return_value = user
        mock_repo.find_by_email.return_value = None
        mock_repo.save.return_value = User(id=1, username="alice", email="new@example.com")
        
        service = UserService(mock_repo)
        
        # Act
        result = service.update_email(1, "new@example.com")
        
        # Assert
        assert result.email == "new@example.com"
    
    def test_update_email_to_own_current_email_succeeds(self) -> None:
        """Should allow keeping same email."""
        user = User(id=1, username="alice", email="same@example.com")
        mock_repo = create_autospec(UserRepository)
        mock_repo.find_by_id.return_value = user
        mock_repo.find_by_email.return_value = user  # User found is the same user
        mock_repo.save.return_value = user
        
        service = UserService(mock_repo)
        result = service.update_email(1, "same@example.com")
        
        assert result.email == "same@example.com"
    
    def test_update_email_to_other_users_email_raises_error(self) -> None:
        """Should raise DuplicateEmailError when email belongs to another user."""
        current_user = User(id=1, username="alice", email="alice@example.com")
        other_user = User(id=2, username="bob", email="bob@example.com")
        
        mock_repo = create_autospec(UserRepository)
        mock_repo.find_by_id.return_value = current_user
        mock_repo.find_by_email.return_value = other_user
        
        service = UserService(mock_repo)
        
        with pytest.raises(DuplicateEmailError):
            service.update_email(1, "bob@example.com")
    
    def test_update_email_invalid_format_raises_error(self) -> None:
        """Should raise ValueError for invalid email format."""
        mock_repo = create_autospec(UserRepository)
        mock_repo.find_by_id.return_value = User(id=1, username="alice", email="alice@example.com")
        
        service = UserService(mock_repo)
        
        with pytest.raises(ValueError, match="Invalid email address"):
            service.update_email(1, "not-an-email")


class TestUserServiceWithMockBehavior:
    """Tests demonstrating advanced mock behaviors."""
    
    def test_repository_interactions_are_isolated(self) -> None:
        """Service should not care about actual repository implementation."""
        # Arrange - create a mock that tracks all interactions
        mock_repo = Mock(spec=UserRepository)
        mock_repo.find_by_id.side_effect = [
            User(id=1, username="user1", email="u1@example.com"),
            User(id=2, username="user2", email="u2@example.com"),
            None,
        ]
        
        service = UserService(mock_repo)
        
        # Act
        user1 = service.get_user(1)
        user2 = service.get_user(2)
        
        # Assert
        assert user1.username == "user1"
        assert user2.username == "user2"
        assert mock_repo.find_by_id.call_count == 2
        mock_repo.find_by_id.assert_any_call(1)
        mock_repo.find_by_id.assert_any_call(2)
    
    def test_service_handles_repository_exceptions(self) -> None:
        """Service should propagate repository errors appropriately."""
        mock_repo = create_autospec(UserRepository)
        mock_repo.find_by_id.side_effect = ConnectionError("Database unavailable")
        
        service = UserService(mock_repo)
        
        # Act & Assert - ConnectionError should propagate
        with pytest.raises(ConnectionError, match="Database unavailable"):
            service.get_user(1)


class TestUserServiceIntegrationPatterns:
    """Tests showing integration testing patterns."""
    
    def test_full_registration_flow(self) -> None:
        """Test complete registration with all mock setup."""
        mock_repo = create_autospec(UserRepository)
        mock_repo.find_by_email.return_value = None
        # First save returns new user, second save returns deactivated user
        mock_repo.save.side_effect = [
            User(id=42, username="newuser", email="new@example.com", is_active=True),
            User(id=42, username="newuser", email="new@example.com", is_active=False),
        ]
        mock_repo.find_by_id.return_value = User(
            id=42, username="newuser", email="new@example.com", is_active=True
        )
        
        service = UserService(mock_repo)
        
        # Full flow
        user = service.register_user("newuser", "new@example.com")
        deactivated = service.deactivate_user(user.id)
        
        assert user.is_active is True
        assert deactivated.is_active is False
        assert mock_repo.save.call_count == 2
