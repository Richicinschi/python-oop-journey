"""Solution for Problem 05: User Password Rules.

Demonstrates password validation with property setter.
"""

from __future__ import annotations

import re


class User:
    """A user with password validation rules.
    
    This class demonstrates complex validation logic within a property
    setter, ensuring passwords meet security requirements.
    
    Attributes:
        username: The user's username (read-only after creation).
    
    Example:
        >>> user = User("alice", "Password123!")
        >>> user.check_password("Password123!")
        True
        >>> user.check_password("wrong")
        False
    """
    
    MIN_PASSWORD_LENGTH = 8
    
    def __init__(self, username: str, password: str) -> None:
        """Initialize a user with password validation.
        
        Args:
            username: The unique username.
            password: The initial password (must meet requirements).
        
        Raises:
            TypeError: If types are incorrect.
            ValueError: If username is empty or password doesn't meet requirements.
        """
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        if not username.strip():
            raise ValueError("Username cannot be empty")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        self._username = username.strip()
        
        # Store password hash instead of plain text
        self._password_hash: str = ""
        self.password = password  # Use property setter
    
    @property
    def username(self) -> str:
        """Get the username.
        
        Returns:
            The username.
        """
        return self._username
    
    @property
    def password(self) -> str:
        """Get password is not allowed.
        
        Raises:
            AttributeError: Password cannot be read, only set.
        """
        raise AttributeError("Password is write-only and cannot be read")
    
    @password.setter
    def password(self, value: str) -> None:
        """Set the password with validation.
        
        Password must be at least 8 characters and contain:
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        
        Args:
            value: The new password.
        
        Raises:
            TypeError: If value is not a string.
            ValueError: If password doesn't meet requirements.
        """
        if not isinstance(value, str):
            raise TypeError("Password must be a string")
        
        if len(value) < self.MIN_PASSWORD_LENGTH:
            raise ValueError(f"Password must be at least {self.MIN_PASSWORD_LENGTH} characters")
        
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', value):
            raise ValueError("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', value):
            raise ValueError("Password must contain at least one digit")
        
        # Store hashed version (simple hash for demonstration)
        self._password_hash = self._hash_password(value)
    
    def _hash_password(self, password: str) -> str:
        """Simple password hashing (for demonstration only).
        
        In production, use bcrypt, argon2, or similar.
        
        Args:
            password: The plain text password.
        
        Returns:
            A simple hash of the password.
        """
        # Simple hash - NOT for production use
        result = 0
        for i, char in enumerate(password):
            result += (ord(char) * (i + 1)) % 1000000007
        return str(result)
    
    def check_password(self, password: str) -> bool:
        """Verify if the provided password is correct.
        
        Args:
            password: The password to check.
        
        Returns:
            True if password matches, False otherwise.
        """
        return self._hash_password(password) == self._password_hash
    
    def change_password(self, old_password: str, new_password: str) -> bool:
        """Change password after verifying old password.
        
        Args:
            old_password: The current password.
            new_password: The new password to set.
        
        Returns:
            True if password was changed, False if old password is incorrect.
        
        Raises:
            ValueError: If new password doesn't meet requirements.
        """
        if not self.check_password(old_password):
            return False
        self.password = new_password
        return True
