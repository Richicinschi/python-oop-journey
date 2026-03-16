"""Problem 07: Config Package Loader

Topic: Multi-source config, package organization
Difficulty: Medium

Create a configuration loader that can load settings from multiple sources:
defaults, JSON files, and environment variables. Configs are merged with
precedence: defaults < file < env vars.

Requirements:
    - ConfigLoader class that loads and merges configuration
    - Support for default config dictionary
    - Support for loading from JSON file
    - Support for environment variable overrides (CONFIG_* prefix)
    - Dot notation access: config.get('database.host')
    - Type conversion helpers: get_int, get_float, get_bool
    - Validation that required keys are present

Example:
    loader = ConfigLoader()
    loader.set_defaults({
        "database": {"host": "localhost", "port": 5432},
        "debug": False
    })
    loader.load_from_file("config.json")  # Optional file
    loader.load_from_env()  # Loads CONFIG_DATABASE_HOST, etc.
    
    config = loader.get_config()
    print(config.get('database.host'))  # "localhost" or from file/env
    print(config.get_int('database.port'))  # 5432
    print(config.get_bool('debug'))  # False

Hints:
    * Hint 1: For dot notation (database.host), split the key by '.' and
      traverse the nested dict. Handle missing keys by returning default.
      Example: key.split('.') -> ['database', 'host'] -> config['database']['host']
    
    * Hint 2: Deep merge for nested dicts - recursively merge so that
      file values override defaults at any nesting level. Use:
      for key, value in override.items():
          if isinstance(value, dict) and key in base:
              recursively merge into base[key]
          else:
              base[key] = value
    
    * Hint 3: Environment variables use double underscore for nesting:
      CONFIG_DATABASE__HOST becomes database.host
      Strip prefix, replace __ with ., then set as override value

Debugging Tips:
    - "KeyError on dot access": You're not handling nested access properly.
      Traverse one level at a time with intermediate checks
    - "Env vars not overriding": Check that you're converting the value
      type correctly - env vars are always strings
    - "File loading fails silently": load_from_file should ignore missing
      files but raise on invalid JSON. Check FileNotFoundError vs JSONDecodeError
    - "Type conversion fails": String "true" != True. Implement proper
      string parsing for get_bool (check case-insensitive variants)
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional


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
        raise NotImplementedError("Implement __init__")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.
        
        Args:
            key: Dot-notation key (e.g., 'database.host')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        raise NotImplementedError("Implement get")
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get value as integer."""
        raise NotImplementedError("Implement get_int")
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get value as float."""
        raise NotImplementedError("Implement get_float")
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get value as boolean.
        
        String values 'true', 'yes', '1' (case-insensitive) are True.
        String values 'false', 'no', '0' (case-insensitive) are False.
        """
        raise NotImplementedError("Implement get_bool")
    
    def has(self, key: str) -> bool:
        """Check if key exists in configuration."""
        raise NotImplementedError("Implement has")
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as a dictionary."""
        raise NotImplementedError("Implement to_dict")


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
        raise NotImplementedError("Implement __init__")
    
    def set_defaults(self, defaults: Dict[str, Any]) -> ConfigLoader:
        """Set default configuration values.
        
        Args:
            defaults: Dictionary of default values
            
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement set_defaults")
    
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
        raise NotImplementedError("Implement load_from_file")
    
    def load_from_env(self, prefix: str = "CONFIG_") -> ConfigLoader:
        """Load configuration from environment variables.
        
        Variables like CONFIG_DATABASE__HOST become database.host.
        Double underscores indicate nesting.
        
        Args:
            prefix: Prefix for environment variables
            
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement load_from_env")
    
    def get_config(self) -> Config:
        """Get the merged configuration.
        
        Returns:
            Config object with all loaded values merged
        """
        raise NotImplementedError("Implement get_config")
    
    def validate_required(self, required_keys: List[str]) -> None:
        """Validate that required keys are present.
        
        Args:
            required_keys: List of required dot-notation keys
            
        Raises:
            ValueError: If any required key is missing
        """
        raise NotImplementedError("Implement validate_required")


def _merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries. Override takes precedence.
    
    Args:
        base: Base dictionary
        override: Dictionary with values to merge/override
        
    Returns:
        New dictionary with merged values
    """
    raise NotImplementedError("Implement _merge_dicts")
