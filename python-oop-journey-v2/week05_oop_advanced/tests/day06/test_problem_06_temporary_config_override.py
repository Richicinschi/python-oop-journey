"""Tests for Problem 06: Temporary Config Override."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day06.problem_06_temporary_config_override import (
    Config,
    ConfigOverride,
    NestedConfig,
    NestedConfigOverride,
)


class TestConfig:
    """Tests for the Config class."""
    
    def test_init_empty(self) -> None:
        """Test empty initialization."""
        config = Config()
        assert "key" not in config
    
    def test_init_with_values(self) -> None:
        """Test initialization with values."""
        config = Config({"host": "localhost", "port": 8080})
        
        assert config.host == "localhost"
        assert config.port == 8080
    
    def test_attribute_access(self) -> None:
        """Test getting and setting via attribute access."""
        config = Config()
        config.debug = True
        
        assert config.debug is True
    
    def test_attribute_access_missing_raises(self) -> None:
        """Test accessing missing attribute raises AttributeError."""
        config = Config()
        
        with pytest.raises(AttributeError):
            _ = config.nonexistent
    
    def test_dict_access(self) -> None:
        """Test getting and setting via dictionary access."""
        config = Config()
        config["key"] = "value"
        
        assert config["key"] == "value"
    
    def test_contains(self) -> None:
        """Test key existence check."""
        config = Config({"key": "value"})
        
        assert "key" in config
        assert "missing" not in config
    
    def test_get_with_default(self) -> None:
        """Test get with default value."""
        config = Config()
        
        assert config.get("missing", "default") == "default"
        assert config.get("missing") is None
    
    def test_update(self) -> None:
        """Test updating multiple values."""
        config = Config({"a": 1})
        config.update({"b": 2, "c": 3})
        
        assert config.a == 1
        assert config.b == 2
        assert config.c == 3
    
    def test_snapshot(self) -> None:
        """Test snapshot creates a copy."""
        config = Config({"list": [1, 2, 3]})
        snap = config.snapshot()
        
        config.list.append(4)
        
        assert snap["list"] == [1, 2, 3]
    
    def test_str_representation(self) -> None:
        """Test string representation."""
        config = Config({"key": "value"})
        result = str(config)
        
        assert "Config" in result
        assert "key" in result


class TestConfigOverride:
    """Tests for the ConfigOverride context manager."""
    
    def test_override_temporarily_changes_value(self) -> None:
        """Test that override temporarily changes the value."""
        config = Config({"debug": False, "level": "INFO"})
        
        with config.override({"debug": True, "level": "DEBUG"}):
            assert config.debug is True
            assert config.level == "DEBUG"
        
        # After context, values restored
        assert config.debug is False
        assert config.level == "INFO"
    
    def test_override_restores_on_exception(self) -> None:
        """Test that override restores values even on exception."""
        config = Config({"key": "original"})
        
        try:
            with config.override({"key": "overridden"}):
                assert config.key == "overridden"
                raise ValueError("Test error")
        except ValueError:
            pass
        
        # Value should be restored despite exception
        assert config.key == "original"
    
    def test_override_new_key_removed_after(self) -> None:
        """Test that new keys added via override are removed after."""
        config = Config({"existing": "value"})
        
        with config.override({"new_key": "new_value"}):
            assert config.new_key == "new_value"
        
        assert "new_key" not in config
    
    def test_override_isolation(self) -> None:
        """Test that overrides don't leak between contexts."""
        config = Config({"key": 1})
        
        with config.override({"key": 100}):
            assert config.key == 100
        
        with config.override({"key": 200}):
            assert config.key == 200
        
        assert config.key == 1
    
    def test_nested_overrides(self) -> None:
        """Test nested override contexts."""
        config = Config({"a": 1, "b": 2})
        
        with config.override({"a": 10}):
            assert config.a == 10
            
            with config.override({"b": 20}):
                assert config.a == 10  # Parent override still active
                assert config.b == 20
            
            assert config.b == 2  # Inner override restored
            assert config.a == 10  # Outer override still active
        
        assert config.a == 1  # All restored
        assert config.b == 2


class TestNestedConfig:
    """Tests for the NestedConfig class."""
    
    def test_init(self) -> None:
        """Test initialization."""
        config = NestedConfig({
            "database": {"host": "localhost", "port": 5432},
            "api": {"timeout": 30}
        })
        
        assert config.get("database.host") == "localhost"
        assert config.get("database.port") == 5432
        assert config.get("api.timeout") == 30
    
    def test_nested_get_missing(self) -> None:
        """Test getting missing nested key."""
        config = NestedConfig()
        
        assert config.get("missing.key") is None
        assert config.get("missing.key", "default") == "default"
    
    def test_nested_set(self) -> None:
        """Test setting nested values."""
        config = NestedConfig()
        config.set("database.host", "localhost")
        
        assert config.get("database.host") == "localhost"
        assert config["database"] == {"host": "localhost"}
    
    def test_nested_set_deep(self) -> None:
        """Test setting deeply nested values."""
        config = NestedConfig()
        config.set("a.b.c.d", "deep")
        
        assert config.get("a.b.c.d") == "deep"
        assert config["a"]["b"]["c"]["d"] == "deep"
    
    def test_nested_dict_access(self) -> None:
        """Test dictionary-style access."""
        config = NestedConfig({"section": {"key": "value"}})
        
        assert config["section.key"] == "value"
        
        config["new.section"] = "new_value"
        assert config.get("new.section") == "new_value"
    
    def test_nested_snapshot(self) -> None:
        """Test snapshot creates deep copy."""
        config = NestedConfig({"db": {"items": [1, 2, 3]}})
        snap = config.snapshot()
        
        config["db.items"].append(4)
        
        assert snap["db"]["items"] == [1, 2, 3]


class TestNestedConfigOverride:
    """Tests for the NestedConfigOverride context manager."""
    
    def test_nested_override_temporarily_changes(self) -> None:
        """Test that nested override temporarily changes values."""
        config = NestedConfig({
            "database": {"host": "localhost", "port": 5432},
            "api": {"timeout": 30}
        })
        
        with config.override({"database.port": 3306, "api.timeout": 60}):
            assert config.get("database.port") == 3306
            assert config.get("api.timeout") == 60
            assert config.get("database.host") == "localhost"  # Unchanged
        
        # After context, values restored
        assert config.get("database.port") == 5432
        assert config.get("api.timeout") == 30
    
    def test_nested_override_restores_on_exception(self) -> None:
        """Test that nested override restores on exception."""
        config = NestedConfig({"section": {"key": "original"}})
        
        try:
            with config.override({"section.key": "overridden"}):
                assert config.get("section.key") == "overridden"
                raise ValueError("Test error")
        except ValueError:
            pass
        
        assert config.get("section.key") == "original"
    
    def test_nested_override_new_key_removed(self) -> None:
        """Test that new nested keys are removed after override."""
        config = NestedConfig({"existing": {"key": "value"}})
        
        with config.override({"existing.new_key": "new_value"}):
            assert config.get("existing.new_key") == "new_value"
        
        assert config.get("existing.new_key") is None
        assert config.get("existing.key") == "value"
    
    def test_nested_override_complex(self) -> None:
        """Test complex nested override scenario."""
        config = NestedConfig({
            "app": {
                "debug": False,
                "database": {
                    "host": "localhost",
                    "port": 5432,
                    "pool": {"size": 10}
                }
            }
        })
        
        with config.override({
            "app.debug": True,
            "app.database.port": 3306,
            "app.database.pool.size": 20
        }):
            assert config.get("app.debug") is True
            assert config.get("app.database.port") == 3306
            assert config.get("app.database.pool.size") == 20
            assert config.get("app.database.host") == "localhost"  # Unchanged
        
        # All restored
        assert config.get("app.debug") is False
        assert config.get("app.database.port") == 5432
        assert config.get("app.database.pool.size") == 10
