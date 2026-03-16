"""Tests for Problem 04: User Factory."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day02.problem_04_user_factory import User


class TestUserInit:
    """Test suite for User initialization."""
    
    def test_basic_init(self) -> None:
        """Test basic user creation."""
        user = User("alice", "alice@example.com")
        assert user.username == "alice"
        assert user.email == "alice@example.com"
    
    def test_different_values(self) -> None:
        """Test with different values."""
        user = User("bob123", "bob@test.org")
        assert user.username == "bob123"
        assert user.email == "bob@test.org"


class TestFromDict:
    """Test suite for from_dict class method."""
    
    def test_from_dict_basic(self) -> None:
        """Test creating user from dictionary."""
        data = {"username": "bob", "email": "bob@test.com"}
        user = User.from_dict(data)
        assert user.username == "bob"
        assert user.email == "bob@test.com"
    
    def test_from_dict_returns_user(self) -> None:
        """Test that from_dict returns a User instance."""
        data = {"username": "test", "email": "test@test.com"}
        user = User.from_dict(data)
        assert isinstance(user, User)


class TestWithDefaultEmail:
    """Test suite for with_default_email class method."""
    
    def test_default_email_format(self) -> None:
        """Test default email format."""
        user = User.with_default_email("charlie")
        assert user.username == "charlie"
        assert user.email == "charlie@example.com"
    
    def test_default_email_uses_class_attribute(self) -> None:
        """Test that default email uses class default_domain attribute."""
        user = User.with_default_email("test")
        assert user.email.endswith(User.default_domain)


class TestAnonymous:
    """Test suite for anonymous class method."""
    
    def test_anonymous_username(self) -> None:
        """Test anonymous user has correct username."""
        anon = User.anonymous()
        assert anon.username == "anonymous"
    
    def test_anonymous_email(self) -> None:
        """Test anonymous user has correct email."""
        anon = User.anonymous()
        assert anon.email == "anon@example.com"
    
    def test_anonymous_returns_user(self) -> None:
        """Test that anonymous returns a User instance."""
        anon = User.anonymous()
        assert isinstance(anon, User)


class TestFactoryMethodsCreateIndependentInstances:
    """Test that factory methods create independent instances."""
    
    def test_instances_are_independent(self) -> None:
        """Test that factory methods create separate objects."""
        user1 = User.with_default_email("user1")
        user2 = User.with_default_email("user2")
        
        assert user1.username != user2.username
        assert user1.email != user2.email
