"""Reference solution for Problem 01: Plugin-Driven Game Loop."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol


class GamePlugin(Protocol):
    """Protocol that all game plugins must implement."""
    
    @property
    def name(self) -> str:
        """Return the unique name of this plugin."""
        ...
    
    def initialize(self) -> None:
        """Called once when the plugin is registered."""
        ...
    
    def update(self, delta_time: float) -> None:
        """Called every game tick with time since last update."""
        ...
    
    def shutdown(self) -> None:
        """Called when the plugin is unregistered or game ends."""
        ...


class PluginManager:
    """Manages the lifecycle of game plugins."""
    
    def __init__(self) -> None:
        self._plugins: dict[str, GamePlugin] = {}
        self._enabled: set[str] = set()
    
    def register(self, plugin: GamePlugin) -> None:
        """Register and initialize a plugin."""
        self._plugins[plugin.name] = plugin
        self._enabled.add(plugin.name)
        plugin.initialize()
    
    def unregister(self, name: str) -> bool:
        """Shutdown and remove a plugin by name. Returns True if found."""
        if plugin := self._plugins.pop(name, None):
            self._enabled.discard(name)
            plugin.shutdown()
            return True
        return False
    
    def update_all(self, delta_time: float) -> None:
        """Update all active plugins."""
        for name in self._enabled:
            if plugin := self._plugins.get(name):
                plugin.update(delta_time)
    
    def get_plugin(self, name: str) -> GamePlugin | None:
        """Get a plugin by name."""
        return self._plugins.get(name)
    
    def get_all_names(self) -> list[str]:
        """Get names of all registered plugins."""
        return list(self._plugins.keys())
    
    def shutdown_all(self) -> None:
        """Shutdown all plugins."""
        for plugin in self._plugins.values():
            plugin.shutdown()
        self._plugins.clear()
        self._enabled.clear()
    
    def enable(self, name: str) -> bool:
        """Enable a plugin. Returns True if plugin exists."""
        if name in self._plugins:
            self._enabled.add(name)
            return True
        return False
    
    def disable(self, name: str) -> bool:
        """Disable a plugin. Returns True if plugin exists."""
        if name in self._plugins:
            self._enabled.discard(name)
            return True
        return False
    
    def is_enabled(self, name: str) -> bool:
        """Check if a plugin is enabled."""
        return name in self._enabled


class GameLoop:
    """Main game loop that delegates to plugins."""
    
    def __init__(self, tick_rate: float = 60.0) -> None:
        """
        Initialize game loop.
        
        Args:
            tick_rate: Target updates per second
        """
        self._plugin_manager = PluginManager()
        self._tick_rate = tick_rate
        self._running = False
        self._tick_count = 0
    
    @property
    def plugin_manager(self) -> PluginManager:
        """Return the plugin manager."""
        return self._plugin_manager
    
    @property
    def tick_rate(self) -> float:
        """Return the target tick rate."""
        return self._tick_rate
    
    @property
    def is_running(self) -> bool:
        """Return whether the game loop is currently running."""
        return self._running
    
    @property
    def tick_count(self) -> int:
        """Return number of ticks processed."""
        return self._tick_count
    
    def start(self) -> None:
        """Start the game loop (simulated)."""
        self._running = True
    
    def stop(self) -> None:
        """Stop the game loop."""
        self._running = False
        self._plugin_manager.shutdown_all()
    
    def tick(self, delta_time: float) -> None:
        """Process a single tick. Called internally or for simulation."""
        if self._running:
            self._tick_count += 1
            self._plugin_manager.update_all(delta_time)


# Example plugin implementations

class PhysicsPlugin:
    """Example plugin that simulates physics."""
    
    def __init__(self) -> None:
        self._initialized = False
        self._update_count = 0
        self._total_delta = 0.0
    
    @property
    def name(self) -> str:
        return "physics"
    
    @property
    def update_count(self) -> int:
        return self._update_count
    
    def initialize(self) -> None:
        self._initialized = True
    
    def update(self, delta_time: float) -> None:
        self._update_count += 1
        self._total_delta += delta_time
    
    def shutdown(self) -> None:
        self._initialized = False


class RenderPlugin:
    """Example plugin that handles rendering."""
    
    def __init__(self) -> None:
        self._initialized = False
        self._frame_count = 0
    
    @property
    def name(self) -> str:
        return "render"
    
    @property
    def frame_count(self) -> int:
        return self._frame_count
    
    def initialize(self) -> None:
        self._initialized = True
    
    def update(self, delta_time: float) -> None:
        self._frame_count += 1
    
    def shutdown(self) -> None:
        self._initialized = False


class InputPlugin:
    """Example plugin that handles input."""
    
    def __init__(self) -> None:
        self._initialized = False
        self._input_events: list[str] = []
    
    @property
    def name(self) -> str:
        return "input"
    
    def initialize(self) -> None:
        self._initialized = True
    
    def update(self, delta_time: float) -> None:
        pass  # Input processing would happen here
    
    def shutdown(self) -> None:
        self._initialized = False
    
    def record_input(self, event: str) -> None:
        """Record an input event."""
        self._input_events.append(event)
