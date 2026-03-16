"""Problem 02: Immutable Config Model

Topic: Frozen dataclasses
Difficulty: Easy-Medium

Create an immutable AppConfig dataclass for application configuration.
Frozen dataclasses are perfect for settings that shouldn't change at runtime.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DatabaseSettings:
    """Database connection settings (immutable).
    
    Attributes:
        host: Database server hostname
        port: Database server port
        name: Database name
        username: Connection username
        password: Connection password (excluded from repr)
        pool_size: Connection pool size (default: 10)
        ssl_enabled: Whether to use SSL (default: True)
    """
    
    host: str
    port: int
    name: str
    username: str
    password: str = field(repr=False)
    pool_size: int = 10
    ssl_enabled: bool = True
    
    def connection_string(self) -> str:
        """Build a connection string (without password).
        
        Returns:
            Format: "user@host:port/db?ssl=true"
        """
        raise NotImplementedError("Implement DatabaseSettings.connection_string")


@dataclass(frozen=True)
class CacheSettings:
    """Cache configuration (immutable).
    
    Attributes:
        backend: Cache backend type (e.g., "redis", "memcached")
        ttl_seconds: Default time-to-live in seconds
        max_entries: Maximum number of cached items
        enabled: Whether caching is enabled (default: True)
    """
    
    backend: str
    ttl_seconds: int
    max_entries: int
    enabled: bool = True


@dataclass(frozen=True)
class AppConfig:
    """Main application configuration (immutable).
    
    Combines database and cache settings with app-level config.
    
    Attributes:
        app_name: Application name
        debug: Debug mode flag (default: False)
        database: Database settings object
        cache: Cache settings object
        allowed_hosts: List of allowed hostnames (default: ["*"])
        secret_key: Secret key for signing (excluded from repr)
    """
    
    app_name: str
    debug: bool = False
    database: DatabaseSettings = field(
        default_factory=lambda: DatabaseSettings(
            host="localhost", port=5432, name="app_db",
            username="app_user", password="default_pass"
        )
    )
    cache: CacheSettings = field(
        default_factory=lambda: CacheSettings(
            backend="memory", ttl_seconds=300, max_entries=1000
        )
    )
    allowed_hosts: tuple[str, ...] = field(default_factory=lambda: ("*",))
    secret_key: str = field(default="change-me", repr=False)
    
    def with_debug(self, debug: bool) -> AppConfig:
        """Return a new config with different debug setting.
        
        Since the dataclass is frozen, we create a new instance.
        
        Args:
            debug: New debug value
            
        Returns:
            New AppConfig with updated debug setting
        """
        raise NotImplementedError("Implement AppConfig.with_debug")
    
    def with_database(self, database: DatabaseSettings) -> AppConfig:
        """Return a new config with different database settings.
        
        Args:
            database: New database settings
            
        Returns:
            New AppConfig with updated database
        """
        raise NotImplementedError("Implement AppConfig.with_database")
    
    def is_production(self) -> bool:
        """Check if this is a production configuration.
        
        Returns:
            True if not debug and allowed_hosts is not ["*"]
        """
        raise NotImplementedError("Implement AppConfig.is_production")


# Hints for Immutable Config Model (Medium):
# 
# Hint 1 - Conceptual nudge:
# Use @dataclass(frozen=True) to make the dataclass immutable. Frozen dataclasses
# don't allow field modification after creation.
#
# Hint 2 - Structural plan:
# - Define the dataclass with frozen=True
# - For "modification" methods like with_debug(), return a NEW instance with
#   updated values using dataclasses.replace() or manual construction
# - Validation goes in __post_init__ which runs after __init__
#
# Hint 3 - Edge-case warning:
# Remember that frozen=True only prevents top-level mutation. If fields are
# mutable objects (lists, dicts), those can still be modified unless you make
# defensive copies in __post_init__.
