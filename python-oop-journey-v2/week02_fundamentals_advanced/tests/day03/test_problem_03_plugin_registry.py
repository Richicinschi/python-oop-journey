"""Tests for Problem 03: Plugin Registry."""

from __future__ import annotations

from week02_fundamentals_advanced.solutions.day03.problem_03_plugin_registry import (
    register_plugin,
    get_plugin,
    list_plugins,
    unregister_plugin,
    clear_registry,
)


def test_register_and_get_plugin() -> None:
    """Test registering and retrieving a plugin."""
    clear_registry()
    
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    
    register_plugin("greeting", greet)
    
    plugin = get_plugin("greeting")
    assert plugin is not None
    assert plugin("Alice") == "Hello, Alice!"


def test_get_nonexistent_plugin() -> None:
    """Test getting a plugin that doesn't exist."""
    clear_registry()
    
    plugin = get_plugin("nonexistent")
    assert plugin is None


def test_list_plugins() -> None:
    """Test listing all registered plugins."""
    clear_registry()
    
    def plugin1() -> None:
        pass
    
    def plugin2() -> None:
        pass
    
    register_plugin("plugin1", plugin1)
    register_plugin("plugin2", plugin2)
    
    plugins = list_plugins()
    assert "plugin1" in plugins
    assert "plugin2" in plugins
    assert len(plugins) == 2


def test_list_plugins_sorted() -> None:
    """Test that plugins are returned sorted."""
    clear_registry()
    
    register_plugin("zebra", lambda: None)
    register_plugin("alpha", lambda: None)
    register_plugin("beta", lambda: None)
    
    plugins = list_plugins()
    assert plugins == ["alpha", "beta", "zebra"]


def test_unregister_plugin() -> None:
    """Test unregistering a plugin."""
    clear_registry()
    
    def plugin() -> None:
        pass
    
    register_plugin("test_plugin", plugin)
    assert get_plugin("test_plugin") is not None
    
    result = unregister_plugin("test_plugin")
    assert result is True
    assert get_plugin("test_plugin") is None


def test_unregister_nonexistent_plugin() -> None:
    """Test unregistering a plugin that doesn't exist."""
    clear_registry()
    
    result = unregister_plugin("nonexistent")
    assert result is False


def test_clear_registry() -> None:
    """Test clearing all plugins from registry."""
    clear_registry()
    
    register_plugin("plugin1", lambda: None)
    register_plugin("plugin2", lambda: None)
    
    assert len(list_plugins()) == 2
    
    clear_registry()
    
    assert len(list_plugins()) == 0
    assert get_plugin("plugin1") is None
    assert get_plugin("plugin2") is None


def test_register_overwrite() -> None:
    """Test that registering with same name overwrites."""
    clear_registry()
    
    def original() -> str:
        return "original"
    
    def replacement() -> str:
        return "replacement"
    
    register_plugin("test", original)
    assert get_plugin("test")() == "original"
    
    register_plugin("test", replacement)
    assert get_plugin("test")() == "replacement"
