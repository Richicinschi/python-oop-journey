"""Exercise: User Password Rules.

Implement a User class with password validation.

TODO:
1. Implement @property getter that raises AttributeError (write-only)
2. Implement @password.setter with validation rules
3. Implement check_password method
4. Implement change_password method
"""

from __future__ import annotations

import re


class User:
    """A user with password validation rules.
    
    Attributes:
        username: The user's username (read-only after creation).
    """
    
    MIN_PASSWORD_LENGTH = 8
    
    def __init__(self, username: str, password: str) -> None:
        """Initialize a user with password validation."""
        if not isinstance(username, str) or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        self._username = username.strip()
        self._password_hash: str = ""
        self.password = password  # Use setter
    
    @property
    def username(self) -> str:
        """Get the username."""
        return self._username
    
    @property
    def password(self) -> str:
        """Get password is not allowed - raises AttributeError."""
        # TODO: Raise AttributeError with message "Password is write-only"
        raise NotImplementedError("Prevent reading password")
    
    @password.setter
    def password(self, value: str) -> None:
        """Set the password with validation.
        
        Rules:
        - At least MIN_PASSWORD_LENGTH characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        """
        # TODO: Validate minimum length
        # TODO: Validate at least one uppercase letter (use re.search)
        # TODO: Validate at least one lowercase letter
        # TODO: Validate at least one digit
        # TODO: Store a hash of the password (use _hash_password)
        raise NotImplementedError("Validate and store password")
    
    def _hash_password(self, password: str) -> str:
        """Simple password hashing (for demonstration)."""
        result = 0
        for i, char in enumerate(password):
            result += (ord(char) * (i + 1)) % 1000000007
        return str(result)
    
    def check_password(self, password: str) -> bool:
        """Verify if the provided password is correct."""
        # TODO: Hash the provided password and compare with stored hash
        raise NotImplementedError("Check password")
    
    def change_password(self, old_password: str, new_password: str) -> bool:
        """Change password after verifying old password."""
        # TODO: Check old_password is correct
        # TODO: If correct, set new_password and return True
        # TODO: If incorrect, return False
        raise NotImplementedError("Change password")
