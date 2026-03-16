"""Tests for Problem 05: User Password Rules."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day03.problem_05_user_password_rules import (
    User,
)


class TestUser:
    """Test suite for User class."""
    
    def test_initialization(self) -> None:
        """Test user initialization."""
        user = User("alice", "Password123!")
        assert user.username == "alice"
    
    def test_initialization_strips_username(self) -> None:
        """Test that username is stripped."""
        user = User("  alice  ", "Password123!")
        assert user.username == "alice"
    
    def test_initialization_invalid_username_type(self) -> None:
        """Test initialization with non-string username raises TypeError."""
        with pytest.raises(TypeError, match="string"):
            User(123, "Password123!")  # type: ignore
    
    def test_initialization_short_username(self) -> None:
        """Test initialization with short username raises ValueError."""
        with pytest.raises(ValueError, match="at least 3"):
            User("ab", "Password123!")
    
    def test_initialization_weak_password_no_uppercase(self) -> None:
        """Test initialization with password without uppercase raises."""
        with pytest.raises(ValueError, match="uppercase"):
            User("alice", "password123!")
    
    def test_initialization_weak_password_no_lowercase(self) -> None:
        """Test initialization with password without lowercase raises."""
        with pytest.raises(ValueError, match="lowercase"):
            User("alice", "PASSWORD123!")
    
    def test_initialization_weak_password_no_digit(self) -> None:
        """Test initialization with password without digit raises."""
        with pytest.raises(ValueError, match="digit"):
            User("alice", "Password!!!")
    
    def test_initialization_weak_password_too_short(self) -> None:
        """Test initialization with short password raises."""
        with pytest.raises(ValueError, match="at least 8"):
            User("alice", "Pass1!")
    
    def test_password_read_raises(self) -> None:
        """Test that reading password raises AttributeError."""
        user = User("alice", "Password123!")
        with pytest.raises(AttributeError, match="write-only"):
            _ = user.password
    
    def test_password_setter_valid(self) -> None:
        """Test password setter with valid password."""
        user = User("alice", "Password123!")
        user.password = "NewPass456!"
        assert user.check_password("NewPass456!") is True
    
    def test_password_setter_invalid(self) -> None:
        """Test password setter rejects invalid password."""
        user = User("alice", "Password123!")
        with pytest.raises(ValueError):
            user.password = "short"
        # Original password should still work
        assert user.check_password("Password123!") is True
    
    def test_check_password_correct(self) -> None:
        """Test check_password with correct password."""
        user = User("alice", "Password123!")
        assert user.check_password("Password123!") is True
    
    def test_check_password_incorrect(self) -> None:
        """Test check_password with incorrect password."""
        user = User("alice", "Password123!")
        assert user.check_password("WrongPassword") is False
    
    def test_check_password_case_sensitive(self) -> None:
        """Test that check_password is case sensitive."""
        user = User("alice", "Password123!")
        assert user.check_password("password123!") is False
    
    def test_change_password_success(self) -> None:
        """Test change_password with correct old password."""
        user = User("alice", "Password123!")
        result = user.change_password("Password123!", "NewPass456!")
        assert result is True
        assert user.check_password("NewPass456!") is True
        assert user.check_password("Password123!") is False
    
    def test_change_password_failure(self) -> None:
        """Test change_password with incorrect old password."""
        user = User("alice", "Password123!")
        result = user.change_password("WrongPassword", "NewPass456!")
        assert result is False
        # Original password should still work
        assert user.check_password("Password123!") is True
    
    def test_username_read_only(self) -> None:
        """Test that username is read-only."""
        user = User("alice", "Password123!")
        with pytest.raises(AttributeError):
            user.username = "bob"  # type: ignore
