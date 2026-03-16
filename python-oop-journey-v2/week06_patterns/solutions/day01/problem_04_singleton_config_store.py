"""Reference solution for Problem 04: Singleton Config Store."""

from __future__ import annotations

from threading import Lock
from typing import Self, Any


class ConfigStore:
    """Singleton configuration store."""
    
    _instance: ConfigStore | None = None
    _lock: Lock = Lock()
    _initialized: bool = False
    
    def __new__(cls) -> Self:
        """Create or return the singleton instance (thread-safe)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize the configuration store (only once)."""
        if not ConfigStore._initialized:
            self._config: dict[str, Any] = {}
            ConfigStore._initialized = True
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)
    
    def has(self, key: str) -> bool:
        """Check if a key exists."""
        return key in self._config
    
    def delete(self, key: str) -> None:
        """Delete a configuration key."""
        self._config.pop(key, None)
    
    def clear(self) -> None:
        """Clear all configuration values."""
        self._config.clear()
    
    def keys(self) -> list[str]:
        """Get all configuration keys."""
        return list(self._config.keys())
    
    def load_from_dict(self, config: dict[str, Any]) -> None:
        """Load configuration from a dictionary."""
        self._config.update(config)
    
    def to_dict(self) -> dict[str, Any]:
        """Export configuration to a dictionary."""
        return self._config.copy()
    
    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (for testing purposes)."""
        cls._instance = None
        cls._initialized = False


class AppConfig:
    """Alternative singleton implementation using class method approach."""
    
    _instance: AppConfig | None = None
    _lock: Lock = Lock()
    
    def __init__(self) -> None:
        """Prevent direct instantiation."""
        if not hasattr(self, '_initialized'):
            self._database_url: str = ""
            self._debug_mode: bool = False
            self._initialized = True
    
    @classmethod
    def get_instance(cls) -> AppConfig:
        """Get the singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls.__new__(cls)
                    cls._instance.__init__()
        return cls._instance
    
    def set_database_url(self, url: str) -> None:
        """Set the database URL."""
        self._database_url = url
    
    def get_database_url(self) -> str:
        """Get the database URL."""
        return self._database_url
    
    def set_debug_mode(self, enabled: bool) -> None:
        """Set debug mode."""
        self._debug_mode = enabled
    
    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        return self._debug_mode
    
    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (for testing)."""
        cls._instance = None
