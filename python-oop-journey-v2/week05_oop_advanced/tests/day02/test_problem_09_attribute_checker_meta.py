"""Tests for Problem 09: Required Attribute Checker Metaclass."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day02.problem_09_attribute_checker_meta import (
    APIConfig,
    ConfigurableClass,
    DatabaseConfig,
    LoggingConfig,
    RequiredAttributesMeta,
)


class TestRequiredAttributesMeta:
    """Tests for the RequiredAttributesMeta metaclass."""
    
    def test_metaclass_exists(self) -> None:
        """Test that RequiredAttributesMeta is defined."""
        assert isinstance(RequiredAttributesMeta, type)
    
    def test_valid_class_creates(self) -> None:
        """Test that class with all required attributes creates successfully."""
        class ValidClass(metaclass=RequiredAttributesMeta):
            __required_attributes__ = ('required1',)
            required1 = "value"
        
        assert ValidClass.required1 == "value"
    
    def test_missing_required_attribute_raises(self) -> None:
        """Test that missing required attributes raise TypeError."""
        with pytest.raises(TypeError) as exc_info:
            class InvalidClass(metaclass=RequiredAttributesMeta):
                __required_attributes__ = ('missing',)
        
        error_msg = str(exc_info.value).lower()
        assert "missing" in error_msg
        assert "required attribute" in error_msg
    
    def test_inherited_required_attributes(self) -> None:
        """Test that required attributes are inherited from bases."""
        # Create a parent with required attributes
        class Parent(metaclass=RequiredAttributesMeta):
            __required_attributes__ = ('required_from_parent',)
            required_from_parent = "value"
        
        # Child should need to inherit or define required_from_parent
        # Since Parent has it, Child should be OK
        class Child(Parent):
            pass
        
        assert hasattr(Child, 'required_from_parent')
    
    def test_required_attributes_from_parent(self) -> None:
        """Test child class must have parent's required attributes."""
        class Parent(metaclass=RequiredAttributesMeta):
            __required_attributes__ = ('parent_attr',)
            parent_attr = "parent_value"
        
        # Child should be able to inherit parent's attribute
        class Child(Parent):
            pass
        
        assert hasattr(Child, 'parent_attr')


class TestConfigurableClass:
    """Tests for the ConfigurableClass base class."""
    
    def test_configurable_class_init(self) -> None:
        """Test ConfigurableClass initialization."""
        class TestConfig(ConfigurableClass):
            pass
        
        config = TestConfig()
        config.name = "test"
        config.value = 42
        assert config.name == "test"
        assert config.value == 42
    
    def test_is_fully_configured_true(self) -> None:
        """Test is_fully_configured returns True when all set."""
        class TestConfig(ConfigurableClass):
            __required_attributes__ = ()  # No requirements
        
        config = TestConfig()
        config.name = "test"
        
        assert config.is_fully_configured() is True
    
    def test_is_fully_configured_false(self) -> None:
        """Test is_fully_configured returns False when missing."""
        # Create a class that checks for instance-level attributes
        class TestConfig(ConfigurableClass):
            __required_attributes__ = ()  # No class-level requirements
        
        config = TestConfig()
        # Instance has no attributes set
        
        # With no required attributes, should be configured
        assert config.is_fully_configured() is True


class TestDatabaseConfig:
    """Tests for the DatabaseConfig class."""
    
    def test_database_config_has_required_attributes(self) -> None:
        """Test DatabaseConfig has all required class attributes."""
        assert hasattr(DatabaseConfig, 'host')
        assert hasattr(DatabaseConfig, 'port')
        assert hasattr(DatabaseConfig, 'database')
    
    def test_database_config_init(self) -> None:
        """Test DatabaseConfig initialization."""
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            database="mydb",
            username="admin",
            password="secret",
        )
        
        assert config.host == "localhost"
        assert config.port == 5432
        assert config.database == "mydb"
        assert config.username == "admin"
        assert config.password == "secret"
    
    def test_database_config_connection_string(self) -> None:
        """Test connection_string method."""
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            database="mydb",
        )
        
        conn_str = config.connection_string()
        assert "localhost" in conn_str
        assert "5432" in conn_str
        assert "mydb" in conn_str
    
    def test_database_config_connection_string_with_auth(self) -> None:
        """Test connection_string with authentication."""
        config = DatabaseConfig(
            host="db.example.com",
            port=3306,
            database="app",
            username="admin",
        )
        
        conn_str = config.connection_string()
        assert "admin" in conn_str
        assert "db.example.com" in conn_str
    
    def test_database_config_not_configured(self) -> None:
        """Test connection_string returns empty when not configured."""
        config = DatabaseConfig()
        assert config.connection_string() == ""


class TestAPIConfig:
    """Tests for the APIConfig class."""
    
    def test_api_config_has_required_attributes(self) -> None:
        """Test APIConfig has all required class attributes."""
        assert hasattr(APIConfig, 'base_url')
        assert hasattr(APIConfig, 'api_version')
    
    def test_api_config_init(self) -> None:
        """Test APIConfig initialization."""
        config = APIConfig(
            base_url="https://api.example.com",
            api_version="v2",
            timeout=60,
            retries=5,
        )
        
        assert config.base_url == "https://api.example.com"
        assert config.api_version == "v2"
        assert config.timeout == 60
        assert config.retries == 5
    
    def test_api_config_defaults(self) -> None:
        """Test APIConfig default values."""
        config = APIConfig()
        
        assert config.timeout == 30
        assert config.retries == 3
    
    def test_api_config_full_url(self) -> None:
        """Test full_url method."""
        config = APIConfig(
            base_url="https://api.example.com",
            api_version="v2",
        )
        
        url = config.full_url("/users")
        assert url == "https://api.example.com/v2/users"
    
    def test_api_config_full_url_with_trailing_slash(self) -> None:
        """Test full_url handles trailing slash correctly."""
        config = APIConfig(
            base_url="https://api.example.com/",
            api_version="v2",
        )
        
        url = config.full_url("users")
        assert url == "https://api.example.com/v2/users"


class TestLoggingConfig:
    """Tests for the LoggingConfig class."""
    
    def test_logging_config_has_required_attributes(self) -> None:
        """Test LoggingConfig has all required class attributes."""
        assert hasattr(LoggingConfig, 'level')
        assert hasattr(LoggingConfig, 'format')
    
    def test_logging_config_init(self) -> None:
        """Test LoggingConfig initialization."""
        config = LoggingConfig(
            level="DEBUG",
            format="%(asctime)s - %(message)s",
            output="file",
        )
        
        assert config.level == "DEBUG"
        assert config.format == "%(asctime)s - %(message)s"
        assert config.output == "file"
    
    def test_logging_config_defaults(self) -> None:
        """Test LoggingConfig default values."""
        config = LoggingConfig()
        
        assert config.level == "INFO"
        assert config.format == "%(message)s"
        assert config.output == "stdout"
    
    def test_is_valid_level_valid(self) -> None:
        """Test is_valid_level with valid levels."""
        config = LoggingConfig()
        
        for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            config.level = level
            assert config.is_valid_level() is True
    
    def test_is_valid_level_invalid(self) -> None:
        """Test is_valid_level with invalid level."""
        config = LoggingConfig(level="INVALID")
        assert config.is_valid_level() is False
