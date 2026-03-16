"""Problem 02: Remove Unnecessary Singleton - Solution.

Replaces Singleton with Dependency Injection for better testability.
"""

from __future__ import annotations

from typing import Any


class AppConfig:
    """Regular configuration class (NOT a singleton)."""
    
    def __init__(self, config_dict: dict[str, Any] | None = None) -> None:
        self._config = config_dict or {
            "database_url": "postgresql://localhost/mydb",
            "api_key": "secret_key_123",
            "timeout": 30,
            "debug": False,
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value
    
    def get_database_url(self) -> str:
        """Get database URL."""
        return str(self._config.get("database_url", ""))
    
    def get_api_key(self) -> str:
        """Get API key."""
        return str(self._config.get("api_key", ""))
    
    def get_timeout(self) -> int:
        """Get timeout value."""
        return int(self._config.get("timeout", 30))
    
    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return bool(self._config.get("debug", False))


class DatabaseConnection:
    """Database connection that receives config via dependency injection."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._url = config.get_database_url()
        self._connected = False
    
    def connect(self) -> str:
        """Connect to database."""
        self._connected = True
        return f"Connected to {self._url}"
    
    def disconnect(self) -> str:
        """Disconnect from database."""
        self._connected = False
        return "Disconnected"
    
    def is_connected(self) -> bool:
        """Check if connected."""
        return self._connected
    
    def query(self, sql: str) -> list[dict[str, Any]]:
        """Execute a query."""
        if not self._connected:
            raise RuntimeError("Not connected")
        return [{"query": sql, "result": "mock_data"}]


class ApiClient:
    """API client that receives config via dependency injection."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._api_key = config.get_api_key()
        self._timeout = config.get_timeout()
    
    def make_request(self, endpoint: str) -> dict[str, Any]:
        """Make API request."""
        return {
            "endpoint": endpoint,
            "api_key": self._api_key,
            "timeout": self._timeout,
        }
    
    def get_timeout(self) -> int:
        """Get configured timeout."""
        return self._timeout


class ConfigurableService:
    """A service class that uses both DatabaseConnection and ApiClient."""
    
    def __init__(self, db: DatabaseConnection, api: ApiClient) -> None:
        self._db = db
        self._api = api
    
    def fetch_and_store(self, endpoint: str, table: str) -> dict[str, Any]:
        """Fetch data from API and store in database."""
        api_response = self._api.make_request(endpoint)
        db_result = self._db.query(f"INSERT INTO {table} VALUES (?)")
        return {
            "api_response": api_response,
            "db_result": db_result,
            "status": "success",
        }
    
    def get_db_connection_string(self) -> str:
        """Get the database connection string being used."""
        return self._db._url
    
    def get_api_key(self) -> str:
        """Get the API key being used."""
        return self._api._api_key


class ServiceLocator:
    """Simple service locator for managing dependencies."""
    
    def __init__(self) -> None:
        self._config: AppConfig | None = None
    
    def register_config(self, config: AppConfig) -> None:
        """Register configuration."""
        self._config = config
    
    def get_config(self) -> AppConfig:
        """Get registered configuration."""
        if self._config is None:
            raise RuntimeError("Config not registered")
        return self._config
    
    def create_database_connection(self) -> DatabaseConnection:
        """Create database connection using registered config."""
        return DatabaseConnection(self.get_config())
    
    def create_api_client(self) -> ApiClient:
        """Create API client using registered config."""
        return ApiClient(self.get_config())
