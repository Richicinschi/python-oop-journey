"""Problem 04: Singleton Config Store

Topic: Singleton Pattern
Difficulty: Medium

Implement the Singleton pattern for a configuration store that ensures
only one instance exists and provides global access to it.
"""

from __future__ import annotations

from threading import Lock
from typing import Self, Any


class ConfigStore:
    """Singleton configuration store.
    
    This class ensures that only one instance of the configuration
    store exists throughout the application lifecycle.
    
    The implementation must be thread-safe.
    """
    
    _instance: ConfigStore | None = None
    _lock: Lock = Lock()
    _initialized: bool = False
    
    def __new__(cls) -> Self:
        """Create or return the singleton instance.
        
        This method must be thread-safe using double-checked locking.
        
        Returns:
            The singleton ConfigStore instance
        """
        raise NotImplementedError("Implement ConfigStore.__new__")
    
    def __init__(self) -> None:
        """Initialize the configuration store.
        
        This should only execute once, even if __init__ is called
        multiple times due to __new__ returning the same instance.
        """
        raise NotImplementedError("Implement ConfigStore.__init__")
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        raise NotImplementedError("Implement ConfigStore.set")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            The configuration value or default
        """
        raise NotImplementedError("Implement ConfigStore.get")
    
    def has(self, key: str) -> bool:
        """Check if a key exists.
        
        Args:
            key: Configuration key
            
        Returns:
            True if key exists, False otherwise
        """
        raise NotImplementedError("Implement ConfigStore.has")
    
    def delete(self, key: str) -> None:
        """Delete a configuration key.
        
        Args:
            key: Configuration key to delete
        """
        raise NotImplementedError("Implement ConfigStore.delete")
    
    def clear(self) -> None:
        """Clear all configuration values."""
        raise NotImplementedError("Implement ConfigStore.clear")
    
    def keys(self) -> list[str]:
        """Get all configuration keys.
        
        Returns:
            List of all keys in the store
        """
        raise NotImplementedError("Implement ConfigStore.keys")
    
    def load_from_dict(self, config: dict[str, Any]) -> None:
        """Load configuration from a dictionary.
        
        Args:
            config: Dictionary of configuration values
        """
        raise NotImplementedError("Implement ConfigStore.load_from_dict")
    
    def to_dict(self) -> dict[str, Any]:
        """Export configuration to a dictionary.
        
        Returns:
            Dictionary copy of all configuration values
        """
        raise NotImplementedError("Implement ConfigStore.to_dict")
    
    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (for testing purposes).
        
        This method clears the instance and allows creating a new one.
        """
        raise NotImplementedError("Implement ConfigStore.reset_instance")


class AppConfig:
    """Alternative singleton implementation using class method approach.
    
    This class provides a simpler singleton pattern that uses
    a class-level instance storage.
    """
    
    _instance: AppConfig | None = None
    _lock: Lock = Lock()
    
    def __init__(self) -> None:
        """Prevent direct instantiation.
        
        Raises:
            RuntimeError: If trying to instantiate directly
        """
        raise NotImplementedError("Implement AppConfig.__init__")
    
    @classmethod
    def get_instance(cls) -> AppConfig:
        """Get the singleton instance.
        
        Returns:
            The singleton AppConfig instance
        """
        raise NotImplementedError("Implement AppConfig.get_instance")
    
    def set_database_url(self, url: str) -> None:
        """Set the database URL."""
        raise NotImplementedError("Implement AppConfig.set_database_url")
    
    def get_database_url(self) -> str:
        """Get the database URL."""
        raise NotImplementedError("Implement AppConfig.get_database_url")
    
    def set_debug_mode(self, enabled: bool) -> None:
        """Set debug mode."""
        raise NotImplementedError("Implement AppConfig.set_debug_mode")
    
    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        raise NotImplementedError("Implement AppConfig.is_debug_mode")
    
    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (for testing)."""
        raise NotImplementedError("Implement AppConfig.reset_instance")
