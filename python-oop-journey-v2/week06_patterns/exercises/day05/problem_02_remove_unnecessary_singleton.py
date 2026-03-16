"""Problem 02: Remove Unnecessary Singleton

Topic: Pattern Tradeoffs and Anti-patterns
Difficulty: Medium

Replace a Singleton pattern with Dependency Injection to improve
testability and reduce hidden coupling.

The `AppConfig` class is implemented as a Singleton, which creates
hidden dependencies and makes testing difficult. Your task is to:

1. Remove the Singleton pattern from AppConfig
2. Use Dependency Injection to pass configuration where needed
3. Make the code testable with mock configurations

Classes to implement:
- AppConfig (regular class, NOT singleton)
- DatabaseConnection (accepts config via injection)
- ApiClient (accepts config via injection)
- ServiceLocator (optional pattern for managing dependencies)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


# BEFORE: The Singleton (do not modify - for reference)
class SingletonAppConfig:
    """This is the Singleton we're replacing.
    
    Problems:
    - Hidden global state
    - Cannot have different configs for testing
    - Hard to mock
    - Action at a distance
    """
    
    _instance: SingletonAppConfig | None = None
    _initialized: bool = False
    
    def __new__(cls) -> SingletonAppConfig:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not SingletonAppConfig._initialized:
            self._config: dict[str, Any] = {
                "database_url": "postgresql://localhost/mydb",
                "api_key": "secret_key_123",
                "timeout": 30,
                "debug": False,
            }
            SingletonAppConfig._initialized = True
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self._config[key] = value


# This class uses the singleton - tightly coupled!
class SingletonDatabaseConnection:
    """Uses the singleton - hard to test!"""
    
    def __init__(self) -> None:
        config = SingletonAppConfig()
        self._url = config.get("database_url")
        self._connected = False
    
    def connect(self) -> str:
        self._connected = True
        return f"Connected to {self._url}"
    
    def query(self, sql: str) -> list[dict]:
        if not self._connected:
            raise RuntimeError("Not connected")
        return [{"result": f"Query: {sql}"}]


# AFTER: Your refactored classes (implement these)

class AppConfig:
    """Regular configuration class (NOT a singleton).
    
    This is a simple configuration container that can be instantiated
    multiple times with different settings. This enables:
    - Testing with mock configs
    - Different configs for different environments
    - Clear dependencies (explicit, not hidden)
    """
    
    def __init__(self, config_dict: dict[str, Any] | None = None) -> None:
        """Initialize with configuration values.
        
        Args:
            config_dict: Configuration dictionary. If None, use defaults.
        """
        raise NotImplementedError("Implement __init__")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        raise NotImplementedError("Implement get")
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        raise NotImplementedError("Implement set")
    
    def get_database_url(self) -> str:
        """Get database URL."""
        raise NotImplementedError("Implement get_database_url")
    
    def get_api_key(self) -> str:
        """Get API key."""
        raise NotImplementedError("Implement get_api_key")
    
    def get_timeout(self) -> int:
        """Get timeout value."""
        raise NotImplementedError("Implement get_timeout")
    
    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        raise NotImplementedError("Implement is_debug")


class DatabaseConnection:
    """Database connection that receives config via dependency injection.
    
    This class is now:
    - Testable (pass mock config)
    - Not coupled to global state
    - Clear about its dependencies
    """
    
    def __init__(self, config: AppConfig) -> None:
        """Initialize with injected config.
        
        Args:
            config: Configuration object (injected dependency)
        """
        raise NotImplementedError("Implement __init__")
    
    def connect(self) -> str:
        """Connect to database."""
        raise NotImplementedError("Implement connect")
    
    def disconnect(self) -> str:
        """Disconnect from database."""
        raise NotImplementedError("Implement disconnect")
    
    def is_connected(self) -> bool:
        """Check if connected."""
        raise NotImplementedError("Implement is_connected")
    
    def query(self, sql: str) -> list[dict[str, Any]]:
        """Execute a query."""
        raise NotImplementedError("Implement query")


class ApiClient:
    """API client that receives config via dependency injection."""
    
    def __init__(self, config: AppConfig) -> None:
        """Initialize with injected config.
        
        Args:
            config: Configuration object (injected dependency)
        """
        raise NotImplementedError("Implement __init__")
    
    def make_request(self, endpoint: str) -> dict[str, Any]:
        """Make API request.
        
        In real implementation, this would use the API key from config.
        For this exercise, return a dict with endpoint and api_key.
        """
        raise NotImplementedError("Implement make_request")
    
    def get_timeout(self) -> int:
        """Get configured timeout."""
        raise NotImplementedError("Implement get_timeout")


class ConfigurableService:
    """A service class that uses both DatabaseConnection and ApiClient.
    
    Demonstrates how dependency injection chains together:
    AppConfig -> DatabaseConnection
    AppConfig -> ApiClient
    (DatabaseConnection, ApiClient) -> ConfigurableService
    """
    
    def __init__(self, db: DatabaseConnection, api: ApiClient) -> None:
        """Initialize with injected dependencies.
        
        Args:
            db: Database connection (injected)
            api: API client (injected)
        """
        raise NotImplementedError("Implement __init__")
    
    def fetch_and_store(self, endpoint: str, table: str) -> dict[str, Any]:
        """Fetch data from API and store in database.
        
        Args:
            endpoint: API endpoint to fetch from
            table: Database table to store in
        
        Returns:
            Dict with operation results
        """
        raise NotImplementedError("Implement fetch_and_store")
    
    def get_db_connection_string(self) -> str:
        """Get the database connection string being used."""
        raise NotImplementedError("Implement get_db_connection_string")
    
    def get_api_key(self) -> str:
        """Get the API key being used."""
        raise NotImplementedError("Implement get_api_key")


# Optional: Simple dependency injection container
class ServiceLocator:
    """Simple service locator for managing dependencies.
    
    While not required, this can help wire up dependencies in larger apps.
    Note: Service Locator is itself sometimes considered an anti-pattern,
    but used carefully it can be better than Singleton.
    """
    
    def __init__(self) -> None:
        raise NotImplementedError("Implement __init__")
    
    def register_config(self, config: AppConfig) -> None:
        """Register configuration."""
        raise NotImplementedError("Implement register_config")
    
    def get_config(self) -> AppConfig:
        """Get registered configuration."""
        raise NotImplementedError("Implement get_config")
    
    def create_database_connection(self) -> DatabaseConnection:
        """Create database connection using registered config."""
        raise NotImplementedError("Implement create_database_connection")
    
    def create_api_client(self) -> ApiClient:
        """Create API client using registered config."""
        raise NotImplementedError("Implement create_api_client")
