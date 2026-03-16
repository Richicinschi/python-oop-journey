"""Tests for Problem 05: Configuration Object."""

from __future__ import annotations

import pytest

from week07_real_world.solutions.day01.problem_05_configuration_object import (
    ConfigError,
    ConfigSection,
    Configuration,
    DatabaseConfiguration,
    ValidatedConfiguration,
)


class TestConfigError:
    """Tests for ConfigError exception."""
    
    def test_config_error_is_exception(self) -> None:
        """Test that ConfigError is an Exception."""
        assert issubclass(ConfigError, Exception)
    
    def test_config_error_can_be_raised(self) -> None:
        """Test that ConfigError can be raised and caught."""
        with pytest.raises(ConfigError, match="Test error"):
            raise ConfigError("Test error")


class TestConfigSection:
    """Tests for ConfigSection."""
    
    def test_get_existing_key(self) -> None:
        """Test getting an existing key."""
        section = ConfigSection("test", {"key": "value"})
        assert section.get("key") == "value"
    
    def test_get_missing_key_with_default(self) -> None:
        """Test getting missing key with default."""
        section = ConfigSection("test", {"key": "value"})
        assert section.get("missing", "default") == "default"
    
    def test_get_missing_key_no_default(self) -> None:
        """Test getting missing key without default."""
        section = ConfigSection("test", {"key": "value"})
        assert section.get("missing") is None
    
    def test_require_existing_key(self) -> None:
        """Test requiring an existing key."""
        section = ConfigSection("test", {"key": "value"})
        assert section.require("key") == "value"
    
    def test_require_missing_key(self) -> None:
        """Test requiring a missing key raises error."""
        section = ConfigSection("test", {"key": "value"})
        with pytest.raises(ConfigError, match="Required key 'missing' missing"):
            section.require("missing")
    
    def test_get_str_existing(self) -> None:
        """Test get_str with existing string value."""
        section = ConfigSection("test", {"name": "Test"})
        assert section.get_str("name") == "Test"
    
    def test_get_str_conversion(self) -> None:
        """Test get_str converts non-strings."""
        section = ConfigSection("test", {"count": 42})
        assert section.get_str("count") == "42"
    
    def test_get_str_default(self) -> None:
        """Test get_str with default."""
        section = ConfigSection("test", {})
        assert section.get_str("name", "Default") == "Default"
    
    def test_get_int_existing(self) -> None:
        """Test get_int with existing int."""
        section = ConfigSection("test", {"port": 8080})
        assert section.get_int("port") == 8080
    
    def test_get_int_from_string(self) -> None:
        """Test get_int converts string."""
        section = ConfigSection("test", {"port": "8080"})
        assert section.get_int("port") == 8080
    
    def test_get_int_default(self) -> None:
        """Test get_int with default."""
        section = ConfigSection("test", {})
        assert section.get_int("port", 3000) == 3000
    
    def test_get_int_invalid_value(self) -> None:
        """Test get_int with invalid value."""
        section = ConfigSection("test", {"port": "not-a-number"})
        with pytest.raises(ConfigError, match="Cannot convert 'port' to int"):
            section.get_int("port")
    
    def test_get_bool_true_values(self) -> None:
        """Test get_bool with various true values."""
        true_values = [True, "true", "True", "TRUE", "yes", "YES", "1", "on", "ON"]
        for val in true_values:
            section = ConfigSection("test", {"flag": val})
            assert section.get_bool("flag") is True, f"Failed for {val}"
    
    def test_get_bool_false_values(self) -> None:
        """Test get_bool with various false values."""
        false_values = [False, "false", "False", "no", "0", "off", "", None]
        for val in false_values:
            section = ConfigSection("test", {"flag": val})
            assert section.get_bool("flag") is False, f"Failed for {val}"
    
    def test_get_bool_default(self) -> None:
        """Test get_bool with default."""
        section = ConfigSection("test", {})
        assert section.get_bool("flag", True) is True
    
    def test_get_list_existing_list(self) -> None:
        """Test get_list with existing list."""
        section = ConfigSection("test", {"items": ["a", "b", "c"]})
        assert section.get_list("items") == ["a", "b", "c"]
    
    def test_get_list_from_string(self) -> None:
        """Test get_list converts comma-separated string."""
        section = ConfigSection("test", {"items": "a, b, c"})
        assert section.get_list("items") == ["a", "b", "c"]
    
    def test_get_list_from_single_value(self) -> None:
        """Test get_list converts single value."""
        section = ConfigSection("test", {"items": "single"})
        assert section.get_list("items") == ["single"]
    
    def test_get_list_default(self) -> None:
        """Test get_list with default."""
        section = ConfigSection("test", {})
        assert section.get_list("items", ["default"]) == ["default"]
    
    def test_get_list_empty_string(self) -> None:
        """Test get_list with empty string."""
        section = ConfigSection("test", {"items": ""})
        assert section.get_list("items") == []
    
    def test_get_section_nested(self) -> None:
        """Test getting nested section."""
        section = ConfigSection("test", {
            "nested": {"key": "value"}
        })
        nested = section.get_section("nested")
        assert isinstance(nested, ConfigSection)
        assert nested.get("key") == "value"
    
    def test_get_section_not_found(self) -> None:
        """Test getting non-existent section."""
        section = ConfigSection("test", {})
        with pytest.raises(ConfigError, match="Section 'missing' not found"):
            section.get_section("missing")
    
    def test_get_section_not_a_dict(self) -> None:
        """Test getting section that is not a dict."""
        section = ConfigSection("test", {"nested": "not-a-dict"})
        with pytest.raises(ConfigError, match="'nested' in 'test' is not a section"):
            section.get_section("nested")
    
    def test_has_key(self) -> None:
        """Test has_key method."""
        section = ConfigSection("test", {"exists": "value"})
        assert section.has_key("exists") is True
        assert section.has_key("missing") is False
    
    def test_has_section(self) -> None:
        """Test has_section method."""
        section = ConfigSection("test", {
            "valid": {"nested": "value"},
            "invalid": "not-a-dict"
        })
        assert section.has_section("valid") is True
        assert section.has_section("invalid") is False
        assert section.has_section("missing") is False
    
    def test_keys(self) -> None:
        """Test keys method."""
        section = ConfigSection("test", {
            "key1": "value1",
            "key2": "value2",
            "nested": {"key": "value"}  # Should not be included
        })
        keys = section.keys()
        assert "key1" in keys
        assert "key2" in keys
        assert "nested" not in keys


class TestConfiguration:
    """Tests for Configuration."""
    
    def test_init_with_dict(self) -> None:
        """Test initialization with dictionary."""
        config = Configuration({"section": {"key": "value"}})
        assert config.has_section("section")
    
    def test_init_with_non_dict_raises(self) -> None:
        """Test initialization with non-dict raises error."""
        with pytest.raises(ConfigError, match="Configuration data must be a dict"):
            Configuration("not-a-dict")  # type: ignore[arg-type]
    
    def test_get_section(self) -> None:
        """Test getting a section."""
        config = Configuration({"database": {"host": "localhost"}})
        section = config.get_section("database")
        assert section.get("host") == "localhost"
    
    def test_get_section_not_found(self) -> None:
        """Test getting non-existent section."""
        config = Configuration({})
        with pytest.raises(ConfigError, match="Section 'missing' not found"):
            config.get_section("missing")
    
    def test_get_section_not_a_dict(self) -> None:
        """Test getting section that is not a dict."""
        config = Configuration({"database": "not-a-dict"})
        with pytest.raises(ConfigError, match="'database' is not a section"):
            config.get_section("database")
    
    def test_has_section(self) -> None:
        """Test has_section method."""
        config = Configuration({
            "valid": {"key": "value"},
            "invalid": "not-a-dict"
        })
        assert config.has_section("valid") is True
        assert config.has_section("invalid") is False
        assert config.has_section("missing") is False
    
    def test_sections(self) -> None:
        """Test sections method."""
        config = Configuration({
            "section1": {"key": "value"},
            "section2": {"key": "value"},
            "not-a-section": "value"
        })
        sections = config.sections()
        assert "section1" in sections
        assert "section2" in sections
        assert "not-a-section" not in sections
    
    def test_keys(self) -> None:
        """Test keys method."""
        config = Configuration({
            "key1": "value",
            "section": {"nested": "value"}
        })
        keys = config.keys()
        assert "key1" in keys
        assert "section" in keys
    
    def test_from_dict_factory(self) -> None:
        """Test from_dict factory method."""
        config = Configuration.from_dict({"key": "value"})
        assert isinstance(config, Configuration)


class TestValidatedConfiguration:
    """Tests for ValidatedConfiguration."""
    
    def test_valid_configuration_passes(self) -> None:
        """Test valid configuration passes validation."""
        class TestConfig(ValidatedConfiguration):
            REQUIRED_SECTIONS = ["database"]
            REQUIRED_KEYS = {"database": ["host"]}
        
        # Should not raise
        config = TestConfig({"database": {"host": "localhost"}})
        assert config is not None
    
    def test_missing_required_section(self) -> None:
        """Test missing required section raises error."""
        class TestConfig(ValidatedConfiguration):
            REQUIRED_SECTIONS = ["database"]
        
        with pytest.raises(ConfigError, match="Required section 'database' not found"):
            TestConfig({})
    
    def test_required_section_not_a_dict(self) -> None:
        """Test required section that is not a dict raises error."""
        class TestConfig(ValidatedConfiguration):
            REQUIRED_SECTIONS = ["database"]
        
        with pytest.raises(ConfigError, match="Required section 'database' must be a dict"):
            TestConfig({"database": "not-a-dict"})
    
    def test_missing_required_key(self) -> None:
        """Test missing required key raises error."""
        class TestConfig(ValidatedConfiguration):
            REQUIRED_SECTIONS = ["database"]
            REQUIRED_KEYS = {"database": ["host", "port"]}
        
        with pytest.raises(ConfigError, match="Required key 'port' not found"):
            TestConfig({"database": {"host": "localhost"}})


class TestDatabaseConfiguration:
    """Tests for DatabaseConfiguration."""
    
    def test_valid_database_config(self) -> None:
        """Test valid database configuration."""
        config = DatabaseConfiguration({
            "database": {
                "host": "localhost",
                "port": 5432
            }
        })
        assert config is not None
    
    def test_missing_database_section(self) -> None:
        """Test missing database section."""
        with pytest.raises(ConfigError, match="Required section 'database' not found"):
            DatabaseConfiguration({})
    
    def test_missing_host(self) -> None:
        """Test missing host key."""
        with pytest.raises(ConfigError, match="Required key 'host' not found"):
            DatabaseConfiguration({"database": {"port": 5432}})
    
    def test_missing_port(self) -> None:
        """Test missing port key."""
        with pytest.raises(ConfigError, match="Required key 'port' not found"):
            DatabaseConfiguration({"database": {"host": "localhost"}})
    
    def test_connection_string_basic(self) -> None:
        """Test connection string without auth."""
        config = DatabaseConfiguration({
            "database": {
                "host": "localhost",
                "port": 5432
            }
        })
        assert config.get_connection_string() == "localhost:5432"
    
    def test_connection_string_with_name(self) -> None:
        """Test connection string with database name."""
        config = DatabaseConfiguration({
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "mydb"
            }
        })
        assert config.get_connection_string() == "localhost:5432/mydb"
    
    def test_connection_string_with_user(self) -> None:
        """Test connection string with username."""
        config = DatabaseConfiguration({
            "database": {
                "host": "localhost",
                "port": 5432,
                "user": "admin"
            }
        })
        assert config.get_connection_string() == "admin@localhost:5432"
    
    def test_connection_string_with_user_and_password(self) -> None:
        """Test connection string with username and password."""
        config = DatabaseConfiguration({
            "database": {
                "host": "localhost",
                "port": 5432,
                "user": "admin",
                "password": "secret"
            }
        })
        assert config.get_connection_string() == "admin:secret@localhost:5432"
    
    def test_connection_string_complete(self) -> None:
        """Test connection string with all options."""
        config = DatabaseConfiguration({
            "database": {
                "host": "db.example.com",
                "port": 3306,
                "name": "production",
                "user": "app",
                "password": "pass123"
            }
        })
        assert config.get_connection_string() == "app:pass123@db.example.com:3306/production"


class TestIntegration:
    """Integration tests for configuration system."""
    
    def test_complex_configuration(self) -> None:
        """Test complex nested configuration."""
        config = Configuration({
            "database": {
                "host": "localhost",
                "port": 5432,
                "credentials": {
                    "username": "admin",
                    "password": "secret"
                }
            },
            "cache": {
                "enabled": True,
                "ttl": 300,
                "servers": "server1, server2, server3"
            },
            "debug": False
        })
        
        # Access database section
        db = config.get_section("database")
        assert db.get_str("host") == "localhost"
        assert db.get_int("port") == 5432
        
        # Access nested credentials
        creds = db.get_section("credentials")
        assert creds.get_str("username") == "admin"
        
        # Access cache section
        cache = config.get_section("cache")
        assert cache.get_bool("enabled") is True
        assert cache.get_int("ttl") == 300
        assert cache.get_list("servers") == ["server1", "server2", "server3"]
