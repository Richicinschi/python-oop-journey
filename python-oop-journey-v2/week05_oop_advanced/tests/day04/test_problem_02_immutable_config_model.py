"""Tests for Problem 02: Immutable Config Model."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day04.problem_02_immutable_config_model import (
    AppConfig, CacheSettings, DatabaseSettings
)


class TestDatabaseSettings:
    """Tests for DatabaseSettings dataclass."""
    
    def test_database_settings_creation(self) -> None:
        """Test creating database settings."""
        db = DatabaseSettings(
            host="db.example.com",
            port=5432,
            name="mydb",
            username="admin",
            password="secret123"
        )
        
        assert db.host == "db.example.com"
        assert db.port == 5432
        assert db.name == "mydb"
        assert db.username == "admin"
        assert db.password == "secret123"
    
    def test_database_settings_defaults(self) -> None:
        """Test default values."""
        db = DatabaseSettings(
            host="localhost",
            port=3306,
            name="test",
            username="root",
            password="pass"
        )
        
        assert db.pool_size == 10
        assert db.ssl_enabled is True
    
    def test_database_settings_frozen(self) -> None:
        """Test that database settings are immutable."""
        db = DatabaseSettings(
            host="localhost", port=5432, name="db",
            username="user", password="pass"
        )
        
        with pytest.raises(AttributeError):
            db.host = "other.com"
    
    def test_password_not_in_repr(self) -> None:
        """Test that password is excluded from repr."""
        db = DatabaseSettings(
            host="localhost", port=5432, name="db",
            username="user", password="secret123"
        )
        
        repr_str = repr(db)
        assert "secret123" not in repr_str
        assert "password" not in repr_str.lower()
    
    def test_connection_string_with_ssl(self) -> None:
        """Test connection string generation with SSL."""
        db = DatabaseSettings(
            host="db.example.com",
            port=5432,
            name="mydb",
            username="admin",
            password="secret",
            ssl_enabled=True
        )
        
        assert db.connection_string() == "admin@db.example.com:5432/mydb?ssl=true"
    
    def test_connection_string_without_ssl(self) -> None:
        """Test connection string generation without SSL."""
        db = DatabaseSettings(
            host="localhost",
            port=3306,
            name="test",
            username="root",
            password="pass",
            ssl_enabled=False
        )
        
        assert db.connection_string() == "root@localhost:3306/test?ssl=false"
    
    def test_database_settings_hashable(self) -> None:
        """Test that frozen dataclass can be used as dict key."""
        db = DatabaseSettings(
            host="localhost", port=5432, name="db",
            username="user", password="pass"
        )
        
        # Should be hashable due to frozen=True
        config_map = {db: "production"}
        assert config_map[db] == "production"


class TestCacheSettings:
    """Tests for CacheSettings dataclass."""
    
    def test_cache_settings_creation(self) -> None:
        """Test creating cache settings."""
        cache = CacheSettings(
            backend="redis",
            ttl_seconds=3600,
            max_entries=10000
        )
        
        assert cache.backend == "redis"
        assert cache.ttl_seconds == 3600
        assert cache.max_entries == 10000
        assert cache.enabled is True
    
    def test_cache_settings_disabled(self) -> None:
        """Test creating disabled cache settings."""
        cache = CacheSettings(
            backend="memory",
            ttl_seconds=300,
            max_entries=100,
            enabled=False
        )
        
        assert cache.enabled is False


class TestAppConfig:
    """Tests for AppConfig dataclass."""
    
    def test_app_config_creation(self) -> None:
        """Test creating app config with all fields."""
        db = DatabaseSettings(
            host="db.example.com", port=5432, name="prod",
            username="app", password="secret"
        )
        cache = CacheSettings(backend="redis", ttl_seconds=3600, max_entries=10000)
        
        config = AppConfig(
            app_name="MyApp",
            debug=False,
            database=db,
            cache=cache,
            allowed_hosts=("example.com", "api.example.com"),
            secret_key="super-secret-key"
        )
        
        assert config.app_name == "MyApp"
        assert config.debug is False
        assert config.database.host == "db.example.com"
        assert config.cache.backend == "redis"
        assert config.allowed_hosts == ("example.com", "api.example.com")
        assert config.secret_key == "super-secret-key"
    
    def test_app_config_defaults(self) -> None:
        """Test default values for AppConfig."""
        config = AppConfig(app_name="TestApp")
        
        assert config.debug is False
        assert config.allowed_hosts == ("*",)
        assert config.secret_key == "change-me"
        # Check default database
        assert config.database.host == "localhost"
        assert config.database.port == 5432
        # Check default cache
        assert config.cache.backend == "memory"
    
    def test_app_config_frozen(self) -> None:
        """Test that app config is immutable."""
        config = AppConfig(app_name="TestApp")
        
        with pytest.raises(AttributeError):
            config.app_name = "OtherApp"
        
        with pytest.raises(AttributeError):
            config.debug = True
    
    def test_secret_key_not_in_repr(self) -> None:
        """Test that secret key is excluded from repr."""
        config = AppConfig(
            app_name="TestApp",
            secret_key="super-secret-123"
        )
        
        repr_str = repr(config)
        assert "super-secret-123" not in repr_str
    
    def test_with_debug(self) -> None:
        """Test creating new config with different debug setting."""
        config = AppConfig(app_name="TestApp", debug=False)
        new_config = config.with_debug(True)
        
        assert new_config.debug is True
        assert new_config.app_name == "TestApp"  # Unchanged
        assert config.debug is False  # Original unchanged
    
    def test_with_database(self) -> None:
        """Test creating new config with different database."""
        old_db = DatabaseSettings(
            host="old.db.com", port=5432, name="old",
            username="user", password="pass"
        )
        new_db = DatabaseSettings(
            host="new.db.com", port=3306, name="new",
            username="user", password="pass"
        )
        
        config = AppConfig(app_name="TestApp", database=old_db)
        new_config = config.with_database(new_db)
        
        assert new_config.database.host == "new.db.com"
        assert config.database.host == "old.db.com"  # Original unchanged
    
    def test_is_production_true(self) -> None:
        """Test production detection - production config."""
        config = AppConfig(
            app_name="ProdApp",
            debug=False,
            allowed_hosts=["example.com"]
        )
        
        assert config.is_production() is True
    
    def test_is_production_debug_false(self) -> None:
        """Test production detection - debug mode."""
        config = AppConfig(
            app_name="DevApp",
            debug=True,
            allowed_hosts=["example.com"]
        )
        
        assert config.is_production() is False
    
    def test_is_production_wildcard_hosts(self) -> None:
        """Test production detection - wildcard hosts."""
        config = AppConfig(
            app_name="DevApp",
            debug=False,
            allowed_hosts=("*",)
        )
        
        assert config.is_production() is False
    
    def test_app_config_hashable(self) -> None:
        """Test that frozen AppConfig can be hashed."""
        config = AppConfig(app_name="TestApp")
        
        # Should work with frozen dataclass
        config_set = {config}
        assert config in config_set
    
    def test_nested_mutation_fails(self) -> None:
        """Test that nested objects are also immutable."""
        config = AppConfig(app_name="TestApp")
        
        # The database object itself is frozen
        with pytest.raises(AttributeError):
            config.database.host = "other.com"
