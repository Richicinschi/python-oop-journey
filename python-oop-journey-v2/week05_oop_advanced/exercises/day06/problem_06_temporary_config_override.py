"""Problem 06: Temporary Config Override.

Topic: Context Managers, Configuration, Temporary Changes
Difficulty: Medium

Implement context managers for temporarily changing configuration values.

This is useful for:
- Testing with different configuration values
- Temporarily enabling debug modes
- A/B testing different settings
- Scoped configuration changes that automatically revert

Example:
    >>> config = Config({"debug": False, "timeout": 30})
    >>> print(config.debug)
    False
    
    >>> with config.override({"debug": True}):
    ...     print(config.debug)  # Temporary change
    ...     config.timeout = 60  # Temporary change
    True
    
    >>> print(config.debug)  # Restored
    False
    >>> print(config.timeout)  # Restored
    30
"""

from __future__ import annotations

from types import TracebackType
from typing import Any


class Config:
    """A configuration container with support for temporary overrides.
    
    Attributes can be accessed as dictionary items or as attributes.
    Supports temporary overrides via context manager.
    
    Example:
        >>> config = Config({"host": "localhost", "port": 8080})
        >>> config.host  # Attribute access
        'localhost'
        >>> config["port"]  # Dictionary access
        8080
        >>> with config.override({"port": 9090}):
        ...     config.port  # Temporarily 9090
    """
    
    def __init__(self, values: dict[str, Any] | None = None) -> None:
        """Initialize the configuration.
        
        Args:
            values: Initial configuration values.
        """
        raise NotImplementedError("Implement __init__")
    
    def __getattr__(self, name: str) -> Any:
        """Get configuration value by attribute access.
        
        Args:
            name: The configuration key.
        
        Returns:
            The configuration value.
        
        Raises:
            AttributeError: If the key doesn't exist.
        """
        raise NotImplementedError("Implement __getattr__")
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Set configuration value by attribute access.
        
        Args:
            name: The configuration key.
            value: The configuration value.
        """
        raise NotImplementedError("Implement __setattr__")
    
    def __getitem__(self, key: str) -> Any:
        """Get configuration value by dictionary access.
        
        Args:
            key: The configuration key.
        
        Returns:
            The configuration value.
        """
        raise NotImplementedError("Implement __getitem__")
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set configuration value by dictionary access.
        
        Args:
            key: The configuration key.
            value: The configuration value.
        """
        raise NotImplementedError("Implement __setitem__")
    
    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the configuration.
        
        Args:
            key: The configuration key.
        
        Returns:
            True if the key exists, False otherwise.
        """
        raise NotImplementedError("Implement __contains__")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value with optional default.
        
        Args:
            key: The configuration key.
            default: Default value if key doesn't exist.
        
        Returns:
            The configuration value or default.
        """
        raise NotImplementedError("Implement get")
    
    def update(self, values: dict[str, Any]) -> None:
        """Update multiple configuration values.
        
        Args:
            values: Dictionary of values to update.
        """
        raise NotImplementedError("Implement update")
    
    def override(self, values: dict[str, Any]) -> ConfigOverride:
        """Create a context manager for temporary configuration overrides.
        
        Args:
            values: Dictionary of temporary values.
        
        Returns:
            ConfigOverride context manager.
        """
        raise NotImplementedError("Implement override")
    
    def snapshot(self) -> dict[str, Any]:
        """Get a snapshot of the current configuration.
        
        Returns:
            Dictionary copy of current configuration.
        """
        raise NotImplementedError("Implement snapshot")


class ConfigOverride:
    """Context manager for temporary configuration overrides.
    
    This is returned by Config.override() and handles the save/restore
    logic for configuration values.
    
    Example:
        >>> config = Config({"debug": False, "level": "INFO"})
        >>> with ConfigOverride(config, {"debug": True, "level": "DEBUG"}):
        ...     # Inside context: values are overridden
        ...     pass
        >>> # Outside context: values restored
    """
    
    def __init__(self, config: Config, overrides: dict[str, Any]) -> None:
        """Initialize the override context manager.
        
        Args:
            config: The Config instance to modify.
            overrides: Dictionary of temporary values.
        """
        raise NotImplementedError("Implement __init__")
    
    def __enter__(self) -> ConfigOverride:
        """Enter the context and apply overrides.
        
        Returns:
            The ConfigOverride instance.
        """
        raise NotImplementedError("Implement __enter__")
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Exit the context and restore original values.
        
        Args:
            exc_type: Exception type if an error occurred.
            exc_val: Exception value if an error occurred.
            exc_tb: Exception traceback if an error occurred.
        
        Returns:
            None to propagate exceptions.
        """
        raise NotImplementedError("Implement __exit__")


# Hints for Temporary Config Override (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to save the original values, set new ones, then restore originals on
# exit - whether successful or not.
#
# Hint 2 - Structural plan:
# - __init__ takes config object and override dict
# - __enter__ saves original values, applies overrides, returns self
# - __exit__ restores all original values
#
# Hint 3 - Edge-case warning:
# Make sure to restore even if an exception occurs. Use try/finally logic in
# __exit__. What if a key didn't exist originally? You might need to delete it
# during restoration.


class NestedConfig:
    """Configuration with support for nested (dot-notation) keys.
    
    Allows accessing nested configuration like:
        config["database.host"] or config.database.host
    
    Example:
        >>> config = NestedConfig({
        ...     "database": {"host": "localhost", "port": 5432},
        ...     "api": {"timeout": 30}
        ... })
        >>> config["database.host"]
        'localhost'
        >>> with config.override({"database.port": 3306}):
        ...     config["database.port"]
        3306
    """
    
    def __init__(self, values: dict[str, Any] | None = None) -> None:
        """Initialize nested configuration.
        
        Args:
            values: Nested dictionary of configuration values.
        """
        raise NotImplementedError("Implement __init__")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value by key (supports dot notation).
        
        Args:
            key: The key, possibly with dots for nesting.
            default: Default value if key doesn't exist.
        
        Returns:
            The configuration value or default.
        """
        raise NotImplementedError("Implement get")
    
    def set(self, key: str, value: Any) -> None:
        """Set a value by key (supports dot notation).
        
        Args:
            key: The key, possibly with dots for nesting.
            value: The value to set.
        """
        raise NotImplementedError("Implement set")
    
    def override(self, values: dict[str, Any]) -> NestedConfigOverride:
        """Create a context manager for temporary overrides.
        
        Args:
            values: Dictionary of temporary values (supports dot notation).
        
        Returns:
            NestedConfigOverride context manager.
        """
        raise NotImplementedError("Implement override")


class NestedConfigOverride:
    """Context manager for temporary nested configuration overrides."""
    
    def __init__(self, config: NestedConfig, overrides: dict[str, Any]) -> None:
        """Initialize the override context manager.
        
        Args:
            config: The NestedConfig instance to modify.
            overrides: Dictionary of temporary values.
        """
        raise NotImplementedError("Implement __init__")
    
    def __enter__(self) -> NestedConfigOverride:
        """Enter the context and apply overrides."""
        raise NotImplementedError("Implement __enter__")
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Exit the context and restore original values."""
        raise NotImplementedError("Implement __exit__")
