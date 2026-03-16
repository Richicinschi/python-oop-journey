"""Reference solution for Problem 05: Configuration Object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ConfigError(Exception):
    """Exception raised for configuration errors."""
    pass


class ConfigSection:
    """A section within the configuration hierarchy."""
    
    def __init__(self, name: str, data: dict[str, Any]) -> None:
        """Initialize a configuration section."""
        self._name = name
        self._data = data
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._data.get(key, default)
    
    def require(self, key: str) -> Any:
        """Get a required configuration value."""
        if key not in self._data:
            raise ConfigError(f"Required key '{key}' missing in section '{self._name}'")
        return self._data[key]
    
    def get_str(self, key: str, default: str = "") -> str:
        """Get a string configuration value."""
        value = self._data.get(key, default)
        return str(value) if value is not None else default
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get an integer configuration value."""
        value = self._data.get(key, default)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError) as e:
            raise ConfigError(f"Cannot convert '{key}' to int: {value}") from e
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get a boolean configuration value."""
        value = self._data.get(key, default)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "yes", "1", "on")
        return bool(value)
    
    def get_list(self, key: str, default: list[str] | None = None) -> list[str]:
        """Get a list configuration value."""
        if default is None:
            default = []
        value = self._data.get(key, default)
        if value is None:
            return default
        if isinstance(value, list):
            return [str(item) for item in value]
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return [str(value)]
    
    def get_section(self, name: str) -> ConfigSection:
        """Get a nested configuration section."""
        if name not in self._data:
            raise ConfigError(f"Section '{name}' not found in '{self._name}'")
        if not isinstance(self._data[name], dict):
            raise ConfigError(f"'{name}' in '{self._name}' is not a section")
        return ConfigSection(name, self._data[name])
    
    def has_key(self, key: str) -> bool:
        """Check if a key exists."""
        return key in self._data
    
    def has_section(self, name: str) -> bool:
        """Check if a nested section exists."""
        return name in self._data and isinstance(self._data[name], dict)
    
    def keys(self) -> list[str]:
        """Get all keys in this section."""
        return [k for k in self._data.keys() if not isinstance(self._data[k], dict)]


class Configuration:
    """Root configuration object."""
    
    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize with configuration data."""
        if not isinstance(data, dict):
            raise ConfigError(f"Configuration data must be a dict, got {type(data).__name__}")
        self._data = data
    
    def get_section(self, name: str) -> ConfigSection:
        """Get a top-level configuration section."""
        if name not in self._data:
            raise ConfigError(f"Section '{name}' not found")
        if not isinstance(self._data[name], dict):
            raise ConfigError(f"'{name}' is not a section")
        return ConfigSection(name, self._data[name])
    
    def has_section(self, name: str) -> bool:
        """Check if a section exists."""
        return name in self._data and isinstance(self._data[name], dict)
    
    def sections(self) -> list[str]:
        """Get names of all top-level sections."""
        return [k for k in self._data.keys() if isinstance(self._data[k], dict)]
    
    def keys(self) -> list[str]:
        """Get all top-level keys."""
        return list(self._data.keys())
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Configuration:
        """Create Configuration from dictionary."""
        return cls(data)


class ValidatedConfiguration(Configuration):
    """Configuration with schema validation."""
    
    REQUIRED_SECTIONS: list[str] = []
    REQUIRED_KEYS: dict[str, list[str]] = {}
    
    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize and validate configuration."""
        super().__init__(data)
        self._validate()
    
    def _validate(self) -> None:
        """Validate configuration against schema."""
        # Check required sections
        for section in self.REQUIRED_SECTIONS:
            if section not in self._data:
                raise ConfigError(f"Required section '{section}' not found")
            if not isinstance(self._data[section], dict):
                raise ConfigError(f"Required section '{section}' must be a dict")
        
        # Check required keys in sections
        for section, keys in self.REQUIRED_KEYS.items():
            if section not in self._data:
                continue  # Already caught above
            section_data = self._data[section]
            for key in keys:
                if key not in section_data:
                    raise ConfigError(f"Required key '{key}' not found in section '{section}'")


class DatabaseConfiguration(ValidatedConfiguration):
    """Configuration specifically for database settings."""
    
    REQUIRED_SECTIONS = ["database"]
    REQUIRED_KEYS = {"database": ["host", "port"]}
    
    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize database configuration."""
        super().__init__(data)
    
    def get_connection_string(self) -> str:
        """Build a database connection string."""
        db_section = self.get_section("database")
        host = db_section.get_str("host")
        port = db_section.get_int("port")
        name = db_section.get_str("name", "")
        user = db_section.get_str("user", "")
        password = db_section.get_str("password", "")
        
        # Build connection string
        if user and password:
            auth = f"{user}:{password}@"
        elif user:
            auth = f"{user}@"
        else:
            auth = ""
        
        base = f"{auth}{host}:{port}"
        if name:
            base += f"/{name}"
        
        return base
