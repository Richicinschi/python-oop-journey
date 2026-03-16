"""Problem 09: URL Builder

Topic: @staticmethod builder pattern
Difficulty: Medium

Create a URLBuilder class with static methods for building and manipulating URLs.

Example:
    >>> URLBuilder.build("api.example.com", "/users")
    'https://api.example.com/users'
    >>> 
    >>> URLBuilder.build("api.example.com", "/users", secure=False)
    'http://api.example.com/users'
    >>> 
    >>> URLBuilder.add_query_param("/users", "page", "1")
    '/users?page=1'
    >>> 
    >>> URLBuilder.add_query_param("/users?page=1", "limit", "10")
    '/users?page=1&limit=10'
    >>> 
    >>> URLBuilder.join_paths("/api/v1", "users", "123")
    '/api/v1/users/123'
    >>> 
    >>> URLBuilder.normalize("//api.example.com//users//")
    'api.example.com/users'

Requirements:
    - build(host: str, path: str, secure: bool = True) -> str: static method
      Returns "https://host/path" or "http://host/path"
    - add_query_param(url: str, key: str, value: str) -> str: static method
      Adds ?key=value or &key=value depending on existing query params
    - join_paths(*parts: str) -> str: static method
      Joins path parts with /, avoiding double slashes
    - normalize(url: str) -> str: static method
      Removes leading/trailing slashes and duplicate slashes

Hints:
    - Hint 1: Static methods don't need self or cls - they're utility functions
    - Hint 2: Use "?" in url to check if query params already exist
    - Hint 3: join_paths: strip / from each part, then join with / between them
"""

from __future__ import annotations


class URLBuilder:
    """Utility class for building and manipulating URLs."""
    
    @staticmethod
    def build(host: str, path: str, secure: bool = True) -> str:
        """Build a complete URL from host and path.
        
        Args:
            host: The host (e.g., "api.example.com")
            path: The path (e.g., "/users")
            secure: Whether to use HTTPS (default) or HTTP
            
        Returns:
            Complete URL
        """
        raise NotImplementedError("Implement build")
    
    @staticmethod
    def add_query_param(url: str, key: str, value: str) -> str:
        """Add a query parameter to a URL.
        
        Args:
            url: Base URL or path
            key: Query parameter key
            value: Query parameter value
            
        Returns:
            URL with added query parameter
        """
        raise NotImplementedError("Implement add_query_param")
    
    @staticmethod
    def join_paths(*parts: str) -> str:
        """Join path parts with slashes.
        
        Handles leading/trailing slashes to avoid double slashes.
        
        Args:
            *parts: Path parts to join
            
        Returns:
            Joined path
        """
        raise NotImplementedError("Implement join_paths")
    
    @staticmethod
    def normalize(url: str) -> str:
        """Normalize a URL by removing extra slashes.
        
        Removes leading/trailing slashes and duplicate internal slashes.
        
        Args:
            url: URL to normalize
            
        Returns:
            Normalized URL
        """
        raise NotImplementedError("Implement normalize")
