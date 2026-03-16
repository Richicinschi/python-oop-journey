"""Tests for Problem 05: Plugin System."""

from __future__ import annotations

import pytest
from week04_oop_intermediate.solutions.day06.problem_05_plugin_system import (
    AnalyticsPlugin,
    Application,
    CachePlugin,
    LoggerPlugin,
    Plugin,
    PluginManager,
    ValidationPlugin,
)


class TestLoggerPlugin:
    """Tests for LoggerPlugin class."""

    def test_creation(self) -> None:
        plugin = LoggerPlugin("test-logger")
        assert plugin.name == "test-logger"

    def test_initialize(self) -> None:
        plugin = LoggerPlugin("test-logger", "DEBUG")
        result = plugin.initialize()
        assert "Logger" in result
        assert "DEBUG" in result

    def test_execute(self) -> None:
        plugin = LoggerPlugin("test-logger")
        result = plugin.execute({"key": "value"})
        assert result["_logged"] is True
        assert result["key"] == "value"

    def test_get_logs(self) -> None:
        plugin = LoggerPlugin("test-logger")
        plugin.execute({"data": 1})
        plugin.execute({"data": 2})
        logs = plugin.get_logs()
        assert len(logs) == 2

    def test_plugin_type(self) -> None:
        plugin = LoggerPlugin("test-logger")
        assert plugin.plugin_type == "logging"

    def test_is_plugin(self) -> None:
        plugin = LoggerPlugin("test-logger")
        assert isinstance(plugin, Plugin)


class TestAnalyticsPlugin:
    """Tests for AnalyticsPlugin class."""

    def test_plugin_type(self) -> None:
        plugin = AnalyticsPlugin("analytics")
        assert plugin.plugin_type == "analytics"

    def test_execute_tracks_events(self) -> None:
        plugin = AnalyticsPlugin("analytics")
        plugin.execute({"event": "click"})
        plugin.execute({"event": "view"})
        stats = plugin.get_stats()
        assert stats["events"] == 2

    def test_shutdown_message(self) -> None:
        plugin = AnalyticsPlugin("analytics")
        plugin.execute({})
        result = plugin.shutdown()
        assert "1 events tracked" in result


class TestCachePlugin:
    """Tests for CachePlugin class."""

    def test_plugin_type(self) -> None:
        plugin = CachePlugin("cache")
        assert plugin.plugin_type == "cache"

    def test_execute_caches_data(self) -> None:
        plugin = CachePlugin("cache")
        result1 = plugin.execute({"key": "value"})
        assert result1["_cached"] is False
        result2 = plugin.execute({"key": "value"})
        assert result2["_cached"] is True

    def test_clear_cache(self) -> None:
        plugin = CachePlugin("cache")
        plugin.execute({"key": "value"})
        plugin.clear_cache()
        assert plugin.get_cache_size() == 0

    def test_get_cache_size(self) -> None:
        plugin = CachePlugin("cache")
        plugin.execute({"a": 1})
        plugin.execute({"b": 2})
        assert plugin.get_cache_size() == 2


class TestValidationPlugin:
    """Tests for ValidationPlugin class."""

    def test_plugin_type(self) -> None:
        plugin = ValidationPlugin("validator", ["name", "email"])
        assert plugin.plugin_type == "validation"

    def test_execute_valid_data(self) -> None:
        plugin = ValidationPlugin("validator", ["name", "email"])
        result = plugin.execute({"name": "John", "email": "john@example.com"})
        assert result["_valid"] is True

    def test_execute_invalid_data(self) -> None:
        plugin = ValidationPlugin("validator", ["name", "email"])
        result = plugin.execute({"name": "John"})  # missing email
        assert result["_valid"] is False
        assert "_errors" in result


class TestPluginManager:
    """Tests for PluginManager class."""

    def test_register_plugin(self) -> None:
        manager = PluginManager()
        plugin = LoggerPlugin("logger")
        result = manager.register_plugin(plugin)
        assert "initialized" in result

    def test_register_duplicate(self) -> None:
        manager = PluginManager()
        plugin1 = LoggerPlugin("logger")
        plugin2 = LoggerPlugin("logger")
        manager.register_plugin(plugin1)
        result = manager.register_plugin(plugin2)
        assert "already registered" in result

    def test_unregister_plugin(self) -> None:
        manager = PluginManager()
        plugin = LoggerPlugin("logger")
        manager.register_plugin(plugin)
        result = manager.unregister_plugin("logger")
        assert "shutdown" in result

    def test_unregister_not_found(self) -> None:
        manager = PluginManager()
        result = manager.unregister_plugin("nonexistent")
        assert "not found" in result

    def test_execute_all(self) -> None:
        manager = PluginManager()
        manager.register_plugin(LoggerPlugin("logger"))
        result = manager.execute_all({"test": "data"})
        assert result["test"] == "data"
        assert result["_logged"] is True

    def test_get_plugins_by_type(self) -> None:
        manager = PluginManager()
        manager.register_plugin(LoggerPlugin("log1"))
        manager.register_plugin(LoggerPlugin("log2"))
        manager.register_plugin(AnalyticsPlugin("analytics"))
        loggers = manager.get_plugins_by_type("logging")
        assert len(loggers) == 2

    def test_get_plugin_names(self) -> None:
        manager = PluginManager()
        manager.register_plugin(LoggerPlugin("log1"))
        manager.register_plugin(AnalyticsPlugin("analytics"))
        names = manager.get_plugin_names()
        assert sorted(names) == ["analytics", "log1"]


class TestApplication:
    """Tests for Application class."""

    def test_creation(self) -> None:
        app = Application("MyApp")
        assert app.name == "MyApp"

    def test_add_plugin(self) -> None:
        app = Application("MyApp")
        result = app.add_plugin(LoggerPlugin("logger"))
        assert "initialized" in result

    def test_remove_plugin(self) -> None:
        app = Application("MyApp")
        app.add_plugin(LoggerPlugin("logger"))
        result = app.remove_plugin("logger")
        assert "shutdown" in result

    def test_process_request(self) -> None:
        app = Application("MyApp")
        app.add_plugin(LoggerPlugin("logger"))
        result = app.process_request({"action": "test"})
        assert result["action"] == "test"
        assert result["_logged"] is True

    def test_get_plugin_info(self) -> None:
        app = Application("MyApp")
        app.add_plugin(LoggerPlugin("logger"))
        info = app.get_plugin_info()
        assert info["application"] == "MyApp"
        assert "logger" in info["plugins"]
        assert info["plugin_count"] == 1

    def test_composition_extensibility(self) -> None:
        """Test that Application can combine plugins flexibly."""
        app = Application("TestApp")
        
        # Add different plugin types
        app.add_plugin(LoggerPlugin("log"))
        app.add_plugin(ValidationPlugin("val", ["id"]))
        app.add_plugin(CachePlugin("cache"))
        app.add_plugin(AnalyticsPlugin("analytics"))
        
        info = app.get_plugin_info()
        assert info["plugin_count"] == 4
        
        # All plugins process the request
        result = app.process_request({"id": "123", "data": "test"})
        assert result["_logged"] is True
        assert result["_valid"] is True
        assert result["_tracked"] is True
