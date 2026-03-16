"""Problem 05: Configuration Object

Topic: API Design with Classes - Hierarchical Configuration
Difficulty: Medium

Implement a hierarchical configuration system with validation,
type conversion, and nested section support.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ConfigError(Exception):
    """Exception raised for configuration errors."""
    pass


class ConfigSection:
    """A section within the configuration hierarchy.
    
    Provides typed access to configuration values and
    supports nested sections.
    """
    
    def __init__(self, name: str, data: dict[str, Any]) -> None:
        """Initialize a configuration section.
        
        Args:
            name: Section name (for error messages)
            data: Dictionary containing configuration values
        """
        raise NotImplementedError("Implement ConfigSection.__init__")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        raise NotImplementedError("Implement ConfigSection.get")
    
    def require(self, key: str) -> Any:
        """Get a required configuration value.
        
        Args:
            key: Configuration key
            
        Returns:
            Configuration value
            
        Raises:
            ConfigError: If key is not found
        """
        raise NotImplementedError("Implement ConfigSection.require")
    
    def get_str(self, key: str, default: str = "") -> str:
        """Get a string configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            String value
        """
        raise NotImplementedError("Implement ConfigSection.get_str")
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get an integer configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Integer value
            
        Raises:
            ConfigError: If value cannot be converted to int
        """
        raise NotImplementedError("Implement ConfigSection.get_int")
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get a boolean configuration value.
        
        Supports: True, "true", "yes", "1", "on" (case-insensitive)
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Boolean value
        """
        raise NotImplementedError("Implement ConfigSection.get_bool")
    
    def get_list(self, key: str, default: list[str] | None = None) -> list[str]:
        """Get a list configuration value.
        
        Supports comma-separated strings or actual lists.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            List of strings
        """
        raise NotImplementedError("Implement ConfigSection.get_list")
    
    def get_section(self, name: str) -> ConfigSection:
        """Get a nested configuration section.
        
        Args:
            name: Section name
            
        Returns:
            ConfigSection for the nested section
            
        Raises:
            ConfigError: If section not found or not a dict
        """
        raise NotImplementedError("Implement ConfigSection.get_section")
    
    def has_key(self, key: str) -> bool:
        """Check if a key exists.
        
        Args:
            key: Configuration key
            
        Returns:
            True if key exists
        """
        raise NotImplementedError("Implement ConfigSection.has_key")
    
    def has_section(self, name: str) -> bool:
        """Check if a nested section exists.
        
        Args:
            name: Section name
            
        Returns:
            True if section exists and is a dict
        """
        raise NotImplementedError("Implement ConfigSection.has_section")
    
    def keys(self) -> list[str]:
        """Get all keys in this section.
        
        Returns:
            List of key names
        """
        raise NotImplementedError("Implement ConfigSection.keys")


class Configuration:
    """Root configuration object.
    
    Provides a hierarchical configuration interface with
    validation and type conversion.
    """
    
    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize with configuration data.
        
        Args:
            data: Dictionary containing configuration
            
        Raises:
            ConfigError: If data is not a dict
        """
        raise NotImplementedError("Implement Configuration.__init__")
    
    def get_section(self, name: str) -> ConfigSection:
        """Get a top-level configuration section.
        
        Args:
            name: Section name
            
        Returns:
            ConfigSection for the section
            
        Raises:
            ConfigError: If section not found or not a dict
        """
        raise NotImplementedError("Implement Configuration.get_section")
    
    def has_section(self, name: str) -> bool:
        """Check if a section exists.
        
        Args:
            name: Section name
            
        Returns:
            True if section exists
        """
        raise NotImplementedError("Implement Configuration.has_section")
    
    def sections(self) -> list[str]:
        """Get names of all top-level sections.
        
        Returns:
            List of section names (keys that map to dicts)
        """
        raise NotImplementedError("Implement Configuration.sections")
    
    def keys(self) -> list[str]:
        """Get all top-level keys.
        
        Returns:
            List of all top-level keys
        """
        raise NotImplementedError("Implement Configuration.keys")
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Configuration:
        """Create Configuration from dictionary.
        
        Args:
            data: Configuration dictionary
            
        Returns:
            New Configuration instance
        """
        raise NotImplementedError("Implement Configuration.from_dict")


class ValidatedConfiguration(Configuration):
    """Configuration with schema validation.
    
    Validates that required sections and keys exist.
    """
    
    REQUIRED_SECTIONS: list[str] = []
    REQUIRED_KEYS: dict[str, list[str]] = {}
    
    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize and validate configuration.
        
        Args:
            data: Configuration dictionary
            
        Raises:
            ConfigError: If validation fails
        """
        raise NotImplementedError("Implement ValidatedConfiguration.__init__")
    
    def _validate(self) -> None:
        """Validate configuration against schema.
        
        Raises:
            ConfigError: If required sections or keys missing
        """
        raise NotImplementedError("Implement ValidatedConfiguration._validate")


class DatabaseConfiguration(ValidatedConfiguration):
    """Configuration specifically for database settings.
    
    Requires 'database' section with 'host' and 'port' keys.
    """
    
    REQUIRED_SECTIONS = ["database"]
    REQUIRED_KEYS = {"database": ["host", "port"]}
    
    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize database configuration.
        
        Args:
            data: Configuration dictionary
            
        Raises:
            ConfigError: If database section or required keys missing
        """
        raise NotImplementedError("Implement DatabaseConfiguration.__init__")
    
    def get_connection_string(self) -> str:
        """Build a database connection string.
        
        Uses database.host, database.port, database.name (optional),
        database.user (optional), database.password (optional).
        
        Returns:
            Connection string in format:
            "host:port/name" or "user:password@host:port/name"
        """
        raise NotImplementedError("Implement DatabaseConfiguration.get_connection_string")
