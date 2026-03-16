"""Problem 03: Plugin Registry

Topic: Registry pattern, dynamic registration
Difficulty: Medium

Implement a plugin registry system that allows functions to be registered
by name and later retrieved by that name. This is a common pattern for
extensible systems.

Requirements:
    - Provide register_plugin(name, func) to register a function
    - Provide get_plugin(name) to retrieve a registered function
    - Provide list_plugins() to get all registered plugin names
    - Provide unregister_plugin(name) to remove a plugin
    - Provide clear_registry() to remove all plugins
    - Calling get_plugin for non-existent name returns None
    - Registering with duplicate name should overwrite

Example:
    def greet(name):
        return f"Hello, {name}!"
    
    register_plugin("greeting", greet)
    
    plugin_func = get_plugin("greeting")
    print(plugin_func("Alice"))  # Hello, Alice!
    
    print(list_plugins())  # ["greeting"]
    
    unregister_plugin("greeting")
    print(get_plugin("greeting"))  # None
"""

from __future__ import annotations

from typing import Callable, Any

# Module-level registry storage
_registry: dict[str, Callable[..., Any]] = {}


def register_plugin(name: str, func: Callable[..., Any]) -> None:
    """Register a function as a plugin under the given name.
    
    If a plugin with this name already exists, it will be overwritten.
    
    Args:
        name: Unique identifier for the plugin
        func: The callable to register
    """
    raise NotImplementedError("Implement register_plugin")


def get_plugin(name: str) -> Callable[..., Any] | None:
    """Retrieve a registered plugin by name.
    
    Args:
        name: The plugin identifier
        
    Returns:
        The registered function, or None if not found
    """
    raise NotImplementedError("Implement get_plugin")


def list_plugins() -> list[str]:
    """Get a list of all registered plugin names.
    
    Returns:
        List of plugin names (sorted alphabetically)
    """
    raise NotImplementedError("Implement list_plugins")


def unregister_plugin(name: str) -> bool:
    """Remove a plugin from the registry.
    
    Args:
        name: The plugin identifier to remove
        
    Returns:
        True if plugin was found and removed, False otherwise
    """
    raise NotImplementedError("Implement unregister_plugin")


def clear_registry() -> None:
    """Remove all plugins from the registry."""
    raise NotImplementedError("Implement clear_registry")
