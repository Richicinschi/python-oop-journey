"""Reference solution for Problem 07: Config Package Loader."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional


def _merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries. Override takes precedence.
    
    Args:
        base: Base dictionary
        override: Dictionary with values to merge/override
        
    Returns:
        New dictionary with merged values
    """
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def _set_nested_value(data: Dict[str, Any], key: str, value: Any) -> None:
    """Set a value using dot notation key.
    
    Args:
        data: Dictionary to modify
        key: Dot-notation key (e.g., 'database.host')
        value: Value to set
    """
    keys = key.split(".")
    current = data
    for k in keys[:-1]:
        if k not in current or not isinstance(current[k], dict):
            current[k] = {}
        current = current[k]
    current[keys[-1]] = value


def _get_nested_value(data: Dict[str, Any], key: str) -> Any:
    """Get a value using dot notation key.
    
    Args:
        data: Dictionary to read from
        key: Dot-notation key (e.g., 'database.host')
        
    Returns:
        The value, or None if key not found
    """
    keys = key.split(".")
    current = data
    for k in keys:
        if not isinstance(current, dict) or k not in current:
            return None
        current = current[k]
    return current


class Config:
    """Configuration object with dot-notation access.
    
    Provides methods to retrieve configuration values with type conversion
    and dot-notation key access (e.g., 'database.host').
    """
    
    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize with configuration data.
        
        Args:
            data: Dictionary containing configuration
        """
        self._data = dict(data)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.
        
        Args:
            key: Dot-notation key (e.g., 'database.host')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        value = _get_nested_value(self._data, key)
        return default if value is None else value
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get value as integer."""
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except (TypeError, ValueError):
            return default
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get value as float."""
        value = self.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except (TypeError, ValueError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get value as boolean.
        
        String values 'true', 'yes', '1' (case-insensitive) are True.
        String values 'false', 'no', '0' (case-insensitive) are False.
        """
        value = self.get(key)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "yes", "1", "on")
        return bool(value)
    
    def has(self, key: str) -> bool:
        """Check if key exists in configuration."""
        return _get_nested_value(self._data, key) is not None
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as a dictionary."""
        return dict(self._data)


class ConfigLoader:
    """Loads and merges configuration from multiple sources.
    
    Configuration precedence (higher overrides lower):
    1. Default values
    2. JSON file values
    3. Environment variables
    
    Environment variables should be prefixed with 'CONFIG_' and
    use double underscore for nesting: CONFIG_DATABASE__HOST
    """
    
    def __init__(self) -> None:
        """Initialize the config loader with empty defaults."""
        self._defaults: Dict[str, Any] = {}
        self._file_config: Dict[str, Any] = {}
        self._env_config: Dict[str, Any] = {}
    
    def set_defaults(self, defaults: Dict[str, Any]) -> ConfigLoader:
        """Set default configuration values.
        
        Args:
            defaults: Dictionary of default values
            
        Returns:
            Self for method chaining
        """
        self._defaults = dict(defaults)
        return self
    
    def load_from_file(self, filepath: str) -> ConfigLoader:
        """Load configuration from a JSON file.
        
        Missing files are silently ignored (for optional configs).
        
        Args:
            filepath: Path to JSON config file
            
        Returns:
            Self for method chaining
            
        Raises:
            json.JSONDecodeError: If file contains invalid JSON
        """
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                self._file_config = json.load(f)
        return self
    
    def load_from_env(self, prefix: str = "CONFIG_") -> ConfigLoader:
        """Load configuration from environment variables.
        
        Variables like CONFIG_DATABASE__HOST become database.host.
        Double underscores indicate nesting.
        
        Args:
            prefix: Prefix for environment variables
            
        Returns:
            Self for method chaining
        """
        self._env_config = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                # Remove prefix and convert to dot notation
                config_key = key[len(prefix):].replace("__", ".").lower()
                _set_nested_value(self._env_config, config_key, value)
        return self
    
    def get_config(self) -> Config:
        """Get the merged configuration.
        
        Returns:
            Config object with all loaded values merged
        """
        # Merge in order: defaults -> file -> env
        merged = _merge_dicts(self._defaults, self._file_config)
        merged = _merge_dicts(merged, self._env_config)
        return Config(merged)
    
    def validate_required(self, required_keys: List[str]) -> None:
        """Validate that required keys are present.
        
        Args:
            required_keys: List of required dot-notation keys
            
        Raises:
            ValueError: If any required key is missing
        """
        config = self.get_config()
        missing = [key for key in required_keys if not config.has(key)]
        if missing:
            raise ValueError(f"Missing required configuration keys: {missing}")
