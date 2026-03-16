"""Problem 01: Plugin Driven Game Loop

Topic: Plugin Pattern
Difficulty: Hard

Implement a plugin-driven game loop using the Plugin pattern.

HINTS:
- Hint 1 (Conceptual): Plugins extend functionality without core code changes. 
  The manager handles lifecycle: register -> initialize -> update -> shutdown.
- Hint 2 (Structural): GamePlugin protocol defines: name property, initialize(), 
  update(delta_time), shutdown(). PluginManager maintains dict of plugins. 
  GameLoop calls manager.update_all() each frame.
- Hint 3 (Edge Case): Handle duplicate plugin names. Calculate delta_time 
  correctly (current - last time). Ensure shutdown is called even if error occurs.

PATTERN EXPLANATION:
The Plugin pattern allows extending an application's functionality at runtime
without modifying the core code. Components (plugins) conform to an interface
and are dynamically loaded and managed.

STRUCTURE:
- Plugin Interface (GamePlugin): Contract that all plugins must implement
- PluginManager: Registers, initializes, and coordinates plugins
- Concrete Plugins: Implement specific functionality (Physics, Render, etc.)

WHEN TO USE:
- For extensible architectures
- When you want third-party extensions
- To keep core code clean and modular

EXAMPLE USAGE:
    manager = PluginManager()
    manager.register(PhysicsPlugin())
    manager.register(RenderPlugin())
    
    # In game loop
    delta_time = 0.016  # 60 FPS
    manager.update_all(delta_time)
    
    # Cleanup
    manager.shutdown_all()

Your task:
1. Create a GamePlugin protocol/interface that plugins must implement
2. Create a PluginManager that manages plugin lifecycle (register, initialize, update, shutdown)
3. Create a GameLoop that runs the main loop and delegates to plugins
4. Create at least two example plugins (e.g., PhysicsPlugin, RenderPlugin)

Requirements:
- Plugins must have: name property, initialize(), update(delta_time), shutdown() methods
- PluginManager tracks registered plugins by name
- GameLoop runs at a configurable tick rate
- Plugins can be enabled/disabled individually
"""

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
        # TODO: Initialize data structures for tracking plugins
        pass
    
    def register(self, plugin: GamePlugin) -> None:
        """Register and initialize a plugin."""
        raise NotImplementedError("Implement register")
    
    def unregister(self, name: str) -> bool:
        """Shutdown and remove a plugin by name. Returns True if found."""
        raise NotImplementedError("Implement unregister")
    
    def update_all(self, delta_time: float) -> None:
        """Update all active plugins."""
        raise NotImplementedError("Implement update_all")
    
    def get_plugin(self, name: str) -> GamePlugin | None:
        """Get a plugin by name."""
        raise NotImplementedError("Implement get_plugin")
    
    def get_all_names(self) -> list[str]:
        """Get names of all registered plugins."""
        raise NotImplementedError("Implement get_all_names")
    
    def shutdown_all(self) -> None:
        """Shutdown all plugins."""
        raise NotImplementedError("Implement shutdown_all")


class GameLoop:
    """Main game loop that delegates to plugins."""
    
    def __init__(self, tick_rate: float = 60.0) -> None:
        """
        Initialize game loop.
        
        Args:
            tick_rate: Target updates per second
        """
        # TODO: Initialize with plugin manager and tick rate
        pass
    
    @property
    def is_running(self) -> bool:
        """Return whether the game loop is currently running."""
        raise NotImplementedError("Implement is_running property")
    
    def start(self) -> None:
        """Start the game loop (simulated)."""
        raise NotImplementedError("Implement start")
    
    def stop(self) -> None:
        """Stop the game loop."""
        raise NotImplementedError("Implement stop")
    
    def tick(self, delta_time: float) -> None:
        """Process a single tick. Called internally or for simulation."""
        raise NotImplementedError("Implement tick")


# TODO: Implement example plugins
# Example: PhysicsPlugin, RenderPlugin, InputPlugin
