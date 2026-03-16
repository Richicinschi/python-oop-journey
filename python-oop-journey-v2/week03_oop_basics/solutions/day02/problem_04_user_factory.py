"""Solution for Problem 04: User Factory."""

from __future__ import annotations


class User:
    """Represents a user with username and email."""
    
    default_domain = "example.com"
    
    def __init__(self, username: str, email: str) -> None:
        """Initialize a user.
        
        Args:
            username: The username
            email: The email address
        """
        self.username = username
        self.email = email
    
    @classmethod
    def from_dict(cls, data: dict[str, str]) -> User:
        """Create a User from a dictionary.
        
        Args:
            data: Dictionary with 'username' and 'email' keys
            
        Returns:
            New User instance
        """
        return cls(username=data["username"], email=data["email"])
    
    @classmethod
    def with_default_email(cls, username: str) -> User:
        """Create a User with default email format.
        
        Default email format: "{username}@example.com"
        
        Args:
            username: The username
            
        Returns:
            New User instance with auto-generated email
        """
        email = f"{username}@{cls.default_domain}"
        return cls(username=username, email=email)
    
    @classmethod
    def anonymous(cls) -> User:
        """Create an anonymous user.
        
        Returns:
            New User with username 'anonymous' and email 'anon@example.com'
        """
        return cls(username="anonymous", email=f"anon@{cls.default_domain}")
