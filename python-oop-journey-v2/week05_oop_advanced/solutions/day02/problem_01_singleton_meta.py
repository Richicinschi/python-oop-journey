"""Problem 01: Singleton Metaclass - Solution.

Implements the Singleton pattern via metaclass to ensure only one
instance of a class exists throughout the application.
"""

from __future__ import annotations

from typing import Any


class SingletonMeta(type):
    """Metaclass that ensures only one instance per class exists.
    
    The metaclass maintains a dictionary mapping classes to their
    single instances. When a class is instantiated:
    - If no instance exists, create and store one
    - If an instance exists, return the existing one
    """
    
    _instances: dict[type, Any] = {}
    
    def __call__(cls: type, *args: Any, **kwargs: Any) -> Any:
        """Control instance creation to enforce singleton pattern.
        
        Args:
            cls: The class being instantiated
            *args: Positional arguments for __init__
            **kwargs: Keyword arguments for __init__
            
        Returns:
            The singleton instance of the class
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """Example singleton class representing a database connection.
    
    Attributes:
        connection_string: The database connection string
        is_connected: Whether the connection is active
    """
    
    _initialized: bool = False
    
    def __init__(self, connection_string: str = "default") -> None:
        """Initialize the database connection.
        
        Note: For singletons, typically only the first initialization matters.
        
        Args:
            connection_string: The connection string for the database
        """
        # Only set values on first initialization
        if not self._initialized:
            self.connection_string = connection_string
            self.is_connected = False
            self._initialized = True
    
    def connect(self) -> str:
        """Establish the database connection.
        
        Returns:
            Status message indicating connection success
        """
        self.is_connected = True
        return f"Connected to {self.connection_string}"
    
    def query(self, sql: str) -> str:
        """Execute a query.
        
        Args:
            sql: The SQL query to execute
            
        Returns:
            Simulated query result
        """
        if not self.is_connected:
            return "Error: Not connected"
        return f"Query result for: {sql}"


class CacheManager(metaclass=SingletonMeta):
    """Example singleton class representing a cache manager.
    
    Attributes:
        max_size: Maximum number of items in cache
        _cache: Internal cache storage
    """
    
    _initialized: bool = False
    
    def __init__(self, max_size: int = 100) -> None:
        """Initialize the cache manager.
        
        Args:
            max_size: Maximum cache size
        """
        # Only set values on first initialization
        if not self._initialized:
            self.max_size = max_size
            self._cache: dict[str, str] = {}
            self._initialized = True
    
    def get(self, key: str) -> str | None:
        """Retrieve a value from the cache.
        
        Args:
            key: The cache key
            
        Returns:
            The cached value or None if not found
        """
        return self._cache.get(key)
    
    def set(self, key: str, value: str) -> bool:
        """Store a value in the cache.
        
        Args:
            key: The cache key
            value: The value to cache
            
        Returns:
            True if stored successfully
        """
        if len(self._cache) >= self.max_size and key not in self._cache:
            return False
        self._cache[key] = value
        return True
