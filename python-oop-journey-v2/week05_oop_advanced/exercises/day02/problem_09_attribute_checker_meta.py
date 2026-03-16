"""Problem 09: Required Attribute Checker Metaclass

Topic: Metaclasses
Difficulty: Medium

Implement a metaclass that verifies required class attributes are defined
at class creation time. This helps catch missing configuration early.

Classes to implement:
- RequiredAttributesMeta: Metaclass that checks for required attributes
- ConfigurableClass: Base class with required attribute checking
- Multiple configuration classes

Requirements:
- Define required attributes via __required_attributes__ tuple
- Verify each required attribute exists at class creation time
- Support type hints in the check (if attribute is annotated)
- Allow optional default value checking
- Provide clear error messages about missing attributes
"""

from __future__ import annotations

from typing import Any


class RequiredAttributesMeta(type):
    """Metaclass that verifies required attributes exist at class creation.
    
    Classes using this metaclass should define __required_attributes__ as a
tuple of attribute names that must be present.
    
    Example:
        class MyClass(metaclass=RequiredAttributesMeta):
            __required_attributes__ = ('name', 'version')
            name = "myapp"  # Required, must be defined
            version = "1.0" # Required, must be defined
    """
    
    def __new__(
        mcs: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:
        """Create class after verifying required attributes.
        
        Args:
            mcs: This metaclass
            name: Name of the class being created
            bases: Base classes
            namespace: Class namespace dictionary
            
        Returns:
            The newly created class
            
        Raises:
            TypeError: If required attributes are missing
        """
        raise NotImplementedError("Implement __new__")
    
    @staticmethod
    def _collect_required_attributes(bases: tuple[type, ...]) -> set[str]:
        """Collect required attributes from base classes.
        
        Args:
            bases: Base classes to inspect
            
        Returns:
            Set of required attribute names
        """
        raise NotImplementedError("Implement _collect_required_attributes")


class ConfigurableClass(metaclass=RequiredAttributesMeta):
    """Base class for configurable components.
    
    Subclasses should define __required_attributes__ to enforce
    that certain configuration options are always present.
    """
    
    __required_attributes__: tuple[str, ...] = ()
    
    def get_missing_attributes(self) -> list[str]:
        """Check which required attributes are not set on this instance.
        
        Returns:
            List of missing attribute names
        """
        raise NotImplementedError("Implement get_missing_attributes")
    
    def is_fully_configured(self) -> bool:
        """Check if all required attributes are set.
        
        Returns:
            True if all required attributes have values
        """
        raise NotImplementedError("Implement is_fully_configured")


class DatabaseConfig(ConfigurableClass):
    """Database configuration with required attributes.
    
    Required attributes:
    - host: Database host address
    - port: Database port number
    - database: Database name
    """
    
    __required_attributes__ = ('host', 'port', 'database')
    
    host: str = ""
    port: int = 0
    database: str = ""
    username: str = ""
    password: str = ""
    
    def __init__(
        self,
        host: str = "",
        port: int = 0,
        database: str = "",
        username: str = "",
        password: str = "",
    ) -> None:
        """Initialize database config.
        
        Args:
            host: Database host
            port: Database port
            database: Database name
            username: Optional username
            password: Optional password
        """
        raise NotImplementedError("Implement __init__")
    
    def connection_string(self) -> str:
        """Build database connection string.
        
        Returns:
            Connection string if configured, empty string otherwise
        """
        raise NotImplementedError("Implement connection_string")


class APIConfig(ConfigurableClass):
    """API configuration with required attributes.
    
    Required attributes:
    - base_url: API base URL
    - api_version: API version string
    """
    
    __required_attributes__ = ('base_url', 'api_version')
    
    base_url: str = ""
    api_version: str = ""
    timeout: int = 30
    retries: int = 3
    
    def __init__(
        self,
        base_url: str = "",
        api_version: str = "",
        timeout: int = 30,
        retries: int = 3,
    ) -> None:
        """Initialize API config.
        
        Args:
            base_url: API base URL
            api_version: API version
            timeout: Request timeout
            retries: Retry attempts
        """
        raise NotImplementedError("Implement __init__")
    
    def full_url(self, endpoint: str) -> str:
        """Build full API URL.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Full URL
        """
        raise NotImplementedError("Implement full_url")


class LoggingConfig(ConfigurableClass):
    """Logging configuration with required attributes.
    
    Required attributes:
    - level: Log level (DEBUG, INFO, WARNING, ERROR)
    - format: Log format string
    """
    
    __required_attributes__ = ('level', 'format')
    
    level: str = "INFO"
    format: str = "%(message)s"
    output: str = "stdout"
    
    def __init__(
        self,
        level: str = "INFO",
        format: str = "%(message)s",
        output: str = "stdout",
    ) -> None:
        """Initialize logging config.
        
        Args:
            level: Log level
            format: Log format string
            output: Output destination
        """
        raise NotImplementedError("Implement __init__")
    
    def is_valid_level(self) -> bool:
        """Check if log level is valid.
        
        Returns:
            True if level is one of DEBUG, INFO, WARNING, ERROR
        """
        raise NotImplementedError("Implement is_valid_level")


# Hints for Attribute Checker Metaclass (Hard):
# 
# Hint 1 - Conceptual nudge:
# You need to validate that instances have certain required attributes after __init__.
# Override __call__ to intercept instance creation.
#
# Hint 2 - Structural plan:
# - In __call__, create the instance using super().__call__
# - After creation, check if all required_attributes are present (use hasattr)
# - Raise AttributeError if any are missing, listing what's missing
# - Also check that attribute types match __annotations__ if present
#
# Hint 3 - Edge-case warning:
# Make sure to handle inheritance - subclasses should inherit parent's required
# attributes unless they override __required_attributes__.
