"""Problem 02: Fixture-Driven User Factory

Topic: Using pytest fixtures for test data
Difficulty: Easy

Create a User class and write tests using pytest fixtures to generate test users.

Your task:
    1. Complete the User class implementation
    2. Create fixtures that generate different types of test users
    3. Write tests that use these fixtures

Example:
    >>> user = User("alice", "alice@example.com", 25)
    >>> user.username
    'alice'
    >>> user.is_active
    True
    >>> user.deactivate()
    >>> user.is_active
    False
"""

from __future__ import annotations


class User:
    """A user account with basic attributes."""

    def __init__(self, username: str, email: str, age: int) -> None:
        """Initialize a user.

        Args:
            username: Unique username (3-20 characters)
            email: Valid email address
            age: Age in years (must be positive)

        Raises:
            ValueError: If any parameter is invalid.
        """
        # TODO: Implement validation and initialization
        raise NotImplementedError("Implement __init__ with validation")

    def deactivate(self) -> None:
        """Deactivate the user account."""
        # TODO: Implement deactivation
        raise NotImplementedError("Implement deactivate")

    def activate(self) -> None:
        """Activate the user account."""
        # TODO: Implement activation
        raise NotImplementedError("Implement activate")

    def is_adult(self) -> bool:
        """Return True if user is 18 or older."""
        # TODO: Implement age check
        raise NotImplementedError("Implement is_adult")

    def update_email(self, new_email: str) -> None:
        """Update the user's email address.

        Raises:
            ValueError: If email format is invalid.
        """
        # TODO: Implement email update with validation
        raise NotImplementedError("Implement update_email")


# TODO: Tests should use fixtures like:
# - @pytest.fixture for a standard user
# - @pytest.fixture for an inactive user
# - @pytest.fixture for a minor user
# - @pytest.fixture for an admin user
