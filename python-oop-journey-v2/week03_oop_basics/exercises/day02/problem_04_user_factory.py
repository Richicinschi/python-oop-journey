"""Problem 04: User Factory

Topic: @classmethod factory methods
Difficulty: Easy

Create a User class with classmethod factory methods for creating
users from different data sources.

Example:
    >>> user1 = User("alice", "alice@example.com")
    >>> user1.username
    'alice'
    >>> 
    >>> # Create from dictionary
    >>> user2 = User.from_dict({"username": "bob", "email": "bob@test.com"})
    >>> user2.username
    'bob'
    >>> 
    >>> # Create with default email
    >>> user3 = User.with_default_email("charlie")
    >>> user3.email
    'charlie@example.com'
    >>> 
    >>> # Create anonymous user
    >>> anon = User.anonymous()
    >>> anon.username
    'anonymous'

Requirements:
    - __init__ takes username (str) and email (str)
    - from_dict(cls, data: dict) -> User: classmethod
    - with_default_email(cls, username: str) -> User: classmethod
    - anonymous(cls) -> User: classmethod
    - Default email format: "{username}@example.com"
"""

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
        raise NotImplementedError("Implement __init__")
    
    @classmethod
    def from_dict(cls, data: dict[str, str]) -> User:
        """Create a User from a dictionary.
        
        Args:
            data: Dictionary with 'username' and 'email' keys
            
        Returns:
            New User instance
        """
        raise NotImplementedError("Implement from_dict")
    
    @classmethod
    def with_default_email(cls, username: str) -> User:
        """Create a User with default email format.
        
        Default email format: "{username}@example.com"
        
        Args:
            username: The username
            
        Returns:
            New User instance with auto-generated email
        """
        raise NotImplementedError("Implement with_default_email")
    
    @classmethod
    def anonymous(cls) -> User:
        """Create an anonymous user.
        
        Returns:
            New User with username 'anonymous' and email 'anon@example.com'
        """
        raise NotImplementedError("Implement anonymous")
