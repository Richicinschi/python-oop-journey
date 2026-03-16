"""Problem 05: Plugin System

Topic: Composition vs Inheritance
Difficulty: Medium

Implement a plugin system that uses composition to add functionality
to a core application without inheritance.

Classes to implement:
- Plugin (abstract base for plugins)
- LoggerPlugin, AnalyticsPlugin, CachePlugin, ValidationPlugin
- PluginManager (manages plugin lifecycle)
- Application (composes plugins via PluginManager)

This demonstrates how composition enables extensible systems
where functionality can be added/removed at runtime.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Plugin(ABC):
    """Abstract base class for plugins."""

    def __init__(self, name: str) -> None:
        raise NotImplementedError("Implement __init__")

    @abstractmethod
    def initialize(self) -> str:
        """Called when plugin is loaded."""
        raise NotImplementedError("Implement initialize")

    @abstractmethod
    def execute(self, data: dict[str, Any]) -> dict[str, Any]:
        """Execute plugin functionality."""
        raise NotImplementedError("Implement execute")

    @abstractmethod
    def shutdown(self) -> str:
        """Called when plugin is unloaded."""
        raise NotImplementedError("Implement shutdown")

    @property
    @abstractmethod
    def plugin_type(self) -> str:
        """Return plugin category."""
        raise NotImplementedError("Implement plugin_type")


class LoggerPlugin(Plugin):
    """Plugin that logs operations."""

    def __init__(self, name: str, log_level: str = "INFO") -> None:
        raise NotImplementedError("Implement __init__")

    def initialize(self) -> str:
        raise NotImplementedError("Implement initialize")

    def execute(self, data: dict[str, Any]) -> dict[str, Any]:
        """Log the data and pass through."""
        raise NotImplementedError("Implement execute")

    def shutdown(self) -> str:
        raise NotImplementedError("Implement shutdown")

    @property
    def plugin_type(self) -> str:
        return "logging"

    def get_logs(self) -> list[str]:
        """Return accumulated logs."""
        raise NotImplementedError("Implement get_logs")


class AnalyticsPlugin(Plugin):
    """Plugin that tracks analytics."""

    def __init__(self, name: str) -> None:
        raise NotImplementedError("Implement __init__")

    def initialize(self) -> str:
        raise NotImplementedError("Implement initialize")

    def execute(self, data: dict[str, Any]) -> dict[str, Any]:
        """Track analytics and pass through."""
        raise NotImplementedError("Implement execute")

    def shutdown(self) -> str:
        raise NotImplementedError("Implement shutdown")

    @property
    def plugin_type(self) -> str:
        return "analytics"

    def get_stats(self) -> dict[str, int]:
        """Return analytics statistics."""
        raise NotImplementedError("Implement get_stats")


class CachePlugin(Plugin):
    """Plugin that provides caching."""

    def __init__(self, name: str, max_size: int = 100) -> None:
        raise NotImplementedError("Implement __init__")

    def initialize(self) -> str:
        raise NotImplementedError("Implement initialize")

    def execute(self, data: dict[str, Any]) -> dict[str, Any]:
        """Check cache or store result."""
        raise NotImplementedError("Implement execute")

    def shutdown(self) -> str:
        raise NotImplementedError("Implement shutdown")

    @property
    def plugin_type(self) -> str:
        return "cache"

    def clear_cache(self) -> None:
        raise NotImplementedError("Implement clear_cache")

    def get_cache_size(self) -> int:
        raise NotImplementedError("Implement get_cache_size")


class ValidationPlugin(Plugin):
    """Plugin that validates data."""

    def __init__(self, name: str, required_fields: list[str]) -> None:
        raise NotImplementedError("Implement __init__")

    def initialize(self) -> str:
        raise NotImplementedError("Implement initialize")

    def execute(self, data: dict[str, Any]) -> dict[str, Any]:
        """Validate data and add errors if invalid."""
        raise NotImplementedError("Implement execute")

    def shutdown(self) -> str:
        raise NotImplementedError("Implement shutdown")

    @property
    def plugin_type(self) -> str:
        return "validation"


class PluginManager:
    """Manages the lifecycle of plugins.
    
    This class demonstrates composition - the manager HAS plugins
    rather than being plugins through inheritance.
    """

    def __init__(self) -> None:
        raise NotImplementedError("Implement __init__")

    def register_plugin(self, plugin: Plugin) -> str:
        """Register and initialize a plugin."""
        raise NotImplementedError("Implement register_plugin")

    def unregister_plugin(self, plugin_name: str) -> str:
        """Shutdown and remove a plugin."""
        raise NotImplementedError("Implement unregister_plugin")

    def execute_all(self, data: dict[str, Any]) -> dict[str, Any]:
        """Execute all plugins in sequence, passing data through."""
        raise NotImplementedError("Implement execute_all")

    def get_plugins_by_type(self, plugin_type: str) -> list[Plugin]:
        raise NotImplementedError("Implement get_plugins_by_type")

    def get_plugin_names(self) -> list[str]:
        raise NotImplementedError("Implement get_plugin_names")


class Application:
    """Application that uses plugins via composition.
    
    The application composes a PluginManager rather than inheriting
    from plugin classes. This allows:
    - Dynamic feature addition/removal
    - Testing with mock plugins
    - Feature combinations without subclass explosion
    """

    def __init__(self, name: str) -> None:
        raise NotImplementedError("Implement __init__")

    def add_plugin(self, plugin: Plugin) -> str:
        raise NotImplementedError("Implement add_plugin")

    def remove_plugin(self, plugin_name: str) -> str:
        raise NotImplementedError("Implement remove_plugin")

    def process_request(self, request_data: dict[str, Any]) -> dict[str, Any]:
        """Process request through all plugins."""
        raise NotImplementedError("Implement process_request")

    def get_plugin_info(self) -> dict[str, Any]:
        raise NotImplementedError("Implement get_plugin_info")
