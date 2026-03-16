"""Reference solution for Problem 02: Fixture-Driven User Factory."""

from __future__ import annotations

import re


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
        if not isinstance(username, str):
            raise ValueError("Username must be a string")
        if not (3 <= len(username) <= 20):
            raise ValueError("Username must be 3-20 characters")
        if not username.isalnum():
            raise ValueError("Username must be alphanumeric")

        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")

        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        if age <= 0:
            raise ValueError("Age must be positive")

        self.username = username
        self.email = email
        self.age = age
        self._is_active = True

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Check if email format is valid."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    @property
    def is_active(self) -> bool:
        """Return whether the user account is active."""
        return self._is_active

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self._is_active = False

    def activate(self) -> None:
        """Activate the user account."""
        self._is_active = True

    def is_adult(self) -> bool:
        """Return True if user is 18 or older."""
        return self.age >= 18

    def update_email(self, new_email: str) -> None:
        """Update the user's email address.

        Raises:
            ValueError: If email format is invalid.
        """
        if not self._is_valid_email(new_email):
            raise ValueError("Invalid email format")
        self.email = new_email
