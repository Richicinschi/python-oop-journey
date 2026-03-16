"""Reference solution for Problem 06: Temporary Config Override."""

from __future__ import annotations

from copy import deepcopy
from types import TracebackType
from typing import Any


class Config:
    """A configuration container with support for temporary overrides."""
    
    def __init__(self, values: dict[str, Any] | None = None) -> None:
        """Initialize the configuration.
        
        Args:
            values: Initial configuration values.
        """
        object.__setattr__(self, '_data', deepcopy(values) if values else {})
    
    def __getattr__(self, name: str) -> Any:
        """Get configuration value by attribute access.
        
        Args:
            name: The configuration key.
        
        Returns:
            The configuration value.
        
        Raises:
            AttributeError: If the key doesn't exist.
        """
        if name.startswith('_'):
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")
        
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Set configuration value by attribute access.
        
        Args:
            name: The configuration key.
            value: The configuration value.
        """
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            self._data[name] = value
    
    def __getitem__(self, key: str) -> Any:
        """Get configuration value by dictionary access."""
        return self._data[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set configuration value by dictionary access."""
        self._data[key] = value
    
    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the configuration."""
        return key in self._data
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value with optional default."""
        return self._data.get(key, default)
    
    def update(self, values: dict[str, Any]) -> None:
        """Update multiple configuration values."""
        self._data.update(values)
    
    def override(self, values: dict[str, Any]) -> ConfigOverride:
        """Create a context manager for temporary configuration overrides.
        
        Args:
            values: Dictionary of temporary values.
        
        Returns:
            ConfigOverride context manager.
        """
        return ConfigOverride(self, values)
    
    def snapshot(self) -> dict[str, Any]:
        """Get a snapshot of the current configuration."""
        return deepcopy(self._data)
    
    def __str__(self) -> str:
        """String representation."""
        return f"Config({self._data})"
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return f"Config({self._data!r})"


class ConfigOverride:
    """Context manager for temporary configuration overrides."""
    
    def __init__(self, config: Config, overrides: dict[str, Any]) -> None:
        """Initialize the override context manager.
        
        Args:
            config: The Config instance to modify.
            overrides: Dictionary of temporary values.
        """
        self._config = config
        self._overrides = overrides
        self._original: dict[str, Any] = {}
    
    def __enter__(self) -> ConfigOverride:
        """Enter the context and apply overrides."""
        # Save original values
        for key in self._overrides:
            if key in self._config._data:
                self._original[key] = deepcopy(self._config._data[key])
            else:
                self._original[key] = None  # Mark as new
        
        # Apply overrides
        for key, value in self._overrides.items():
            self._config._data[key] = deepcopy(value)
        
        return self
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Exit the context and restore original values."""
        # Restore original values
        for key, original_value in self._original.items():
            if original_value is None:
                # Key didn't exist before, remove it
                self._config._data.pop(key, None)
            else:
                # Restore original value
                self._config._data[key] = original_value
        
        return None  # Don't suppress exceptions


class NestedConfig:
    """Configuration with support for nested (dot-notation) keys."""
    
    def __init__(self, values: dict[str, Any] | None = None) -> None:
        """Initialize nested configuration."""
        self._data: dict[str, Any] = deepcopy(values) if values else {}
    
    def _get_nested(self, key: str) -> tuple[dict[str, Any], str]:
        """Get the nested dict and final key from a dot-notation key.
        
        Args:
            key: Dot-notation key like "database.host".
        
        Returns:
            Tuple of (parent dict, final key).
        """
        parts = key.split('.')
        current = self._data
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
            if not isinstance(current, dict):
                raise KeyError(f"Cannot navigate into non-dict at '{part}'")
        
        return current, parts[-1]
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value by key (supports dot notation)."""
        try:
            parent, final_key = self._get_nested(key)
            return deepcopy(parent[final_key])
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set a value by key (supports dot notation)."""
        parent, final_key = self._get_nested(key)
        parent[final_key] = value
    
    def __getitem__(self, key: str) -> Any:
        """Get value by key."""
        parent, final_key = self._get_nested(key)
        return parent[final_key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set value by key."""
        self.set(key, value)
    
    def override(self, values: dict[str, Any]) -> NestedConfigOverride:
        """Create a context manager for temporary overrides."""
        return NestedConfigOverride(self, values)
    
    def snapshot(self) -> dict[str, Any]:
        """Get a snapshot of the current configuration."""
        return deepcopy(self._data)


class NestedConfigOverride:
    """Context manager for temporary nested configuration overrides."""
    
    def __init__(self, config: NestedConfig, overrides: dict[str, Any]) -> None:
        """Initialize the override context manager."""
        self._config = config
        self._overrides = overrides
        self._original: dict[str, Any] = {}
    
    def __enter__(self) -> NestedConfigOverride:
        """Enter the context and apply overrides."""
        for key, value in self._overrides.items():
            # Save current value (if exists)
            try:
                self._original[key] = deepcopy(self._config[key])
            except KeyError:
                self._original[key] = None  # Mark as new
            
            # Apply override
            self._config.set(key, deepcopy(value))
        
        return self
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Exit the context and restore original values."""
        for key, original_value in self._original.items():
            if original_value is None:
                # Remove the key - it didn't exist before
                try:
                    parent, final_key = self._config._get_nested(key)
                    del parent[final_key]
                except (KeyError, TypeError):
                    pass
            else:
                # Restore original value
                self._config.set(key, original_value)
        
        return None
