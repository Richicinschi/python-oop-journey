"""Tests for Problem 02: Fixture-Driven User Factory."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day06.problem_02_fixture_driven_user_factory import (
    User,
)


# Fixtures for different types of users

@pytest.fixture
def standard_user() -> User:
    """Return a standard active user."""
    return User("alice", "alice@example.com", 25)


@pytest.fixture
def inactive_user() -> User:
    """Return an inactive user."""
    user = User("bob", "bob@example.com", 30)
    user.deactivate()
    return user


@pytest.fixture
def minor_user() -> User:
    """Return a user who is a minor (under 18)."""
    return User("charlie", "charlie@example.com", 16)


@pytest.fixture
def adult_user() -> User:
    """Return an adult user (18 or older)."""
    return User("diana", "diana@example.com", 18)


@pytest.fixture
def admin_user() -> User:
    """Return an admin-like user (adult, active)."""
    return User("eve", "eve@example.com", 35)


# Tests using fixtures

class TestUserInitialization:
    """Tests for user creation and initialization."""

    def test_user_has_correct_attributes(self, standard_user: User) -> None:
        """Test that user attributes are set correctly."""
        assert standard_user.username == "alice"
        assert standard_user.email == "alice@example.com"
        assert standard_user.age == 25

    def test_user_is_active_by_default(self, standard_user: User) -> None:
        """Test that new users are active by default."""
        assert standard_user.is_active is True

    def test_invalid_username_too_short(self) -> None:
        """Test that short usernames are rejected."""
        with pytest.raises(ValueError, match="3-20 characters"):
            User("ab", "test@example.com", 25)

    def test_invalid_username_too_long(self) -> None:
        """Test that long usernames are rejected."""
        with pytest.raises(ValueError, match="3-20 characters"):
            User("a" * 21, "test@example.com", 25)

    def test_invalid_username_non_alphanumeric(self) -> None:
        """Test that non-alphanumeric usernames are rejected."""
        with pytest.raises(ValueError, match="alphanumeric"):
            User("alice_bob", "test@example.com", 25)

    def test_invalid_email_format(self) -> None:
        """Test that invalid emails are rejected."""
        with pytest.raises(ValueError, match="Invalid email"):
            User("alice", "not-an-email", 25)

    def test_invalid_email_no_domain(self) -> None:
        """Test that emails without domains are rejected."""
        with pytest.raises(ValueError, match="Invalid email"):
            User("alice", "alice@", 25)

    def test_invalid_age_zero(self) -> None:
        """Test that age of zero is rejected."""
        with pytest.raises(ValueError, match="positive"):
            User("alice", "alice@example.com", 0)

    def test_invalid_age_negative(self) -> None:
        """Test that negative age is rejected."""
        with pytest.raises(ValueError, match="positive"):
            User("alice", "alice@example.com", -5)


class TestUserActivation:
    """Tests for user activation/deactivation."""

    def test_deactivate_changes_status(self, standard_user: User) -> None:
        """Test that deactivation sets is_active to False."""
        standard_user.deactivate()
        assert standard_user.is_active is False

    def test_activate_changes_status(self, inactive_user: User) -> None:
        """Test that activation sets is_active to True."""
        inactive_user.activate()
        assert inactive_user.is_active is True

    def test_deactivate_already_inactive(self, inactive_user: User) -> None:
        """Test deactivating an already inactive user."""
        inactive_user.deactivate()
        assert inactive_user.is_active is False


class TestUserAge:
    """Tests for age-related functionality."""

    def test_minor_is_not_adult(self, minor_user: User) -> None:
        """Test that a minor is not considered an adult."""
        assert minor_user.is_adult() is False

    def test_adult_is_adult(self, adult_user: User) -> None:
        """Test that an 18-year-old is considered an adult."""
        assert adult_user.is_adult() is True

    def test_older_adult_is_adult(self, standard_user: User) -> None:
        """Test that an older user is considered an adult."""
        assert standard_user.is_adult() is True


class TestUserEmailUpdate:
    """Tests for email update functionality."""

    def test_update_email_valid(self, standard_user: User) -> None:
        """Test updating email with valid address."""
        standard_user.update_email("newemail@example.com")
        assert standard_user.email == "newemail@example.com"

    def test_update_email_invalid_format(self, standard_user: User) -> None:
        """Test that invalid email format is rejected."""
        with pytest.raises(ValueError, match="Invalid email"):
            standard_user.update_email("not-an-email")

    def test_update_email_preserves_other_attributes(self, standard_user: User) -> None:
        """Test that email update doesn't change other attributes."""
        old_username = standard_user.username
        old_age = standard_user.age
        standard_user.update_email("new@example.com")
        assert standard_user.username == old_username
        assert standard_user.age == old_age
