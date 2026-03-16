"""Reference solution for Problem 02: Immutable Config Model."""

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
        ssl_param = "true" if self.ssl_enabled else "false"
        return f"{self.username}@{self.host}:{self.port}/{self.name}?ssl={ssl_param}"


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
        return AppConfig(
            app_name=self.app_name,
            debug=debug,
            database=self.database,
            cache=self.cache,
            allowed_hosts=self.allowed_hosts,
            secret_key=self.secret_key
        )
    
    def with_database(self, database: DatabaseSettings) -> AppConfig:
        """Return a new config with different database settings.
        
        Args:
            database: New database settings
            
        Returns:
            New AppConfig with updated database
        """
        return AppConfig(
            app_name=self.app_name,
            debug=self.debug,
            database=database,
            cache=self.cache,
            allowed_hosts=self.allowed_hosts,
            secret_key=self.secret_key
        )
    
    def is_production(self) -> bool:
        """Check if this is a production configuration.
        
        Returns:
            True if not debug and allowed_hosts is not ["*"]
        """
        return not self.debug and self.allowed_hosts != ("*",)
