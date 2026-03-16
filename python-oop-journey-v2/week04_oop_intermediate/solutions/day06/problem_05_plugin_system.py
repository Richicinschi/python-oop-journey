"""Reference solution for Problem 05: Plugin System."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Plugin(ABC):
    """Abstract base class for plugins."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def initialize(self) -> str:
        pass

    @abstractmethod
    def execute(self, data: dict[str, Any]) -> dict[str, Any]:
        pass

    @abstractmethod
    def shutdown(self) -> str:
        pass

    @property
    @abstractmethod
    def plugin_type(self) -> str:
        pass


class LoggerPlugin(Plugin):
    """Plugin that logs operations."""

    def __init__(self, name: str, log_level: str = "INFO") -> None:
        super().__init__(name)
        self._logs: list[str] = []
        self._log_level = log_level

    def initialize(self) -> str:
        return f"Logger '{self.name}' initialized at {self._log_level} level"

    def execute(self, data: dict[str, Any]) -> dict[str, Any]:
        log_entry = f"[{self._log_level}] Processing: {data}"
        self._logs.append(log_entry)
        return {**data, "_logged": True}

    def shutdown(self) -> str:
        return f"Logger '{self.name}' shutdown, {len(self._logs)} entries logged"

    @property
    def plugin_type(self) -> str:
        return "logging"

    def get_logs(self) -> list[str]:
        return self._logs.copy()


class AnalyticsPlugin(Plugin):
    """Plugin that tracks analytics."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._event_count = 0
        self._data_volume = 0

    def initialize(self) -> str:
        return f"Analytics '{self.name}' initialized"

    def execute(self, data: dict[str, Any]) -> dict[str, Any]:
        self._event_count += 1
        self._data_volume += len(str(data))
        return {**data, "_tracked": True}

    def shutdown(self) -> str:
        return f"Analytics '{self.name}' shutdown, {self._event_count} events tracked"

    @property
    def plugin_type(self) -> str:
        return "analytics"

    def get_stats(self) -> dict[str, int]:
        return {
            "events": self._event_count,
            "data_volume": self._data_volume,
        }


class CachePlugin(Plugin):
    """Plugin that provides caching."""

    def __init__(self, name: str, max_size: int = 100) -> None:
        super().__init__(name)
        self._cache: dict[str, Any] = {}
        self._max_size = max_size
        self._hits = 0
        self._misses = 0

    def initialize(self) -> str:
        return f"Cache '{self.name}' initialized with max size {self._max_size}"

    def execute(self, data: dict[str, Any]) -> dict[str, Any]:
        key = str(data)
        if key in self._cache:
            self._hits += 1
            return {**self._cache[key], "_cached": True}
        self._misses += 1
        self._cache[key] = data
        if len(self._cache) > self._max_size:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        return {**data, "_cached": False}

    def shutdown(self) -> str:
        return f"Cache '{self.name}' shutdown, hit rate: {self._hits}/{self._hits + self._misses}"

    @property
    def plugin_type(self) -> str:
        return "cache"

    def clear_cache(self) -> None:
        self._cache.clear()

    def get_cache_size(self) -> int:
        return len(self._cache)


class ValidationPlugin(Plugin):
    """Plugin that validates data."""

    def __init__(self, name: str, required_fields: list[str]) -> None:
        super().__init__(name)
        self._required_fields = required_fields
        self._validation_errors: list[str] = []

    def initialize(self) -> str:
        return f"Validation '{self.name}' initialized"

    def execute(self, data: dict[str, Any]) -> dict[str, Any]:
        errors = []
        for field in self._required_fields:
            if field not in data or data[field] is None:
                errors.append(f"Missing required field: {field}")
        self._validation_errors.extend(errors)
        if errors:
            return {**data, "_valid": False, "_errors": errors}
        return {**data, "_valid": True}

    def shutdown(self) -> str:
        return f"Validation '{self.name}' shutdown, {len(self._validation_errors)} total errors"

    @property
    def plugin_type(self) -> str:
        return "validation"


class PluginManager:
    """Manages the lifecycle of plugins."""

    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}

    def register_plugin(self, plugin: Plugin) -> str:
        if plugin.name in self._plugins:
            return f"Plugin '{plugin.name}' already registered"
        self._plugins[plugin.name] = plugin
        return plugin.initialize()

    def unregister_plugin(self, plugin_name: str) -> str:
        if plugin_name not in self._plugins:
            return f"Plugin '{plugin_name}' not found"
        plugin = self._plugins.pop(plugin_name)
        return plugin.shutdown()

    def execute_all(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        for plugin in self._plugins.values():
            result = plugin.execute(result)
        return result

    def get_plugins_by_type(self, plugin_type: str) -> list[Plugin]:
        return [p for p in self._plugins.values() if p.plugin_type == plugin_type]

    def get_plugin_names(self) -> list[str]:
        return list(self._plugins.keys())


class Application:
    """Application that uses plugins via composition."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._plugin_manager = PluginManager()

    def add_plugin(self, plugin: Plugin) -> str:
        return self._plugin_manager.register_plugin(plugin)

    def remove_plugin(self, plugin_name: str) -> str:
        return self._plugin_manager.unregister_plugin(plugin_name)

    def process_request(self, request_data: dict[str, Any]) -> dict[str, Any]:
        return self._plugin_manager.execute_all(request_data)

    def get_plugin_info(self) -> dict[str, Any]:
        return {
            "application": self.name,
            "plugins": self._plugin_manager.get_plugin_names(),
            "plugin_count": len(self._plugin_manager.get_plugin_names()),
        }
