"""Problem 09: Required Attribute Checker Metaclass - Solution.

Verifies required class attributes are defined at class creation time,
helping catch missing configuration early.
"""

from __future__ import annotations

from typing import Any


class RequiredAttributesMeta(type):
    """Metaclass that verifies required attributes exist at class creation.
    
    Classes using this metaclass should define __required_attributes__ as a
tuple of attribute names that must be present.
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
        # Get required attributes from this class
        required = namespace.get('__required_attributes__', ())
        
        # Also collect from bases
        from_bases = mcs._collect_required_attributes(bases)
        all_required = set(required) | from_bases
        
        # Check each required attribute
        for attr in all_required:
            if attr not in namespace:
                # Check if it's inherited
                found_in_base = False
                for base in bases:
                    if hasattr(base, attr):
                        found_in_base = True
                        break
                
                if not found_in_base:
                    raise TypeError(
                        f"Class '{name}' is missing required attribute '{attr}'. "
                        f"Add '{attr}' as a class attribute."
                    )
        
        return super().__new__(mcs, name, bases, namespace)
    
    @staticmethod
    def _collect_required_attributes(bases: tuple[type, ...]) -> set[str]:
        """Collect required attributes from base classes.
        
        Args:
            bases: Base classes to inspect
            
        Returns:
            Set of required attribute names
        """
        required: set[str] = set()
        for base in bases:
            if hasattr(base, '__required_attributes__'):
                required.update(base.__required_attributes__)
        return required


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
        required = getattr(self.__class__, '__required_attributes__', ())
        missing = []
        for attr in required:
            if not hasattr(self, attr) or getattr(self, attr) in (None, ""):
                missing.append(attr)
        return missing
    
    def is_fully_configured(self) -> bool:
        """Check if all required attributes are set.
        
        Returns:
            True if all required attributes have values
        """
        return len(self.get_missing_attributes()) == 0


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
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
    
    def connection_string(self) -> str:
        """Build database connection string.
        
        Returns:
            Connection string if configured, empty string otherwise
        """
        if not self.is_fully_configured():
            return ""
        auth = ""
        if self.username:
            auth = f"{self.username}"
            if self.password:
                auth += ":***@"
            else:
                auth += "@"
        return f"db://{auth}{self.host}:{self.port}/{self.database}"


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
        self.base_url = base_url
        self.api_version = api_version
        self.timeout = timeout
        self.retries = retries
    
    def full_url(self, endpoint: str) -> str:
        """Build full API URL.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Full URL
        """
        if not self.is_fully_configured():
            return ""
        base = self.base_url.rstrip('/')
        path = endpoint.lstrip('/')
        return f"{base}/{self.api_version}/{path}"


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
        self.level = level
        self.format = format
        self.output = output
    
    def is_valid_level(self) -> bool:
        """Check if log level is valid.
        
        Returns:
            True if level is one of DEBUG, INFO, WARNING, ERROR
        """
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR'}
        return self.level.upper() in valid_levels
