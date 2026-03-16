"""Reference solution for Problem 03: Plugin Registry."""

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
    _registry[name] = func


def get_plugin(name: str) -> Callable[..., Any] | None:
    """Retrieve a registered plugin by name.
    
    Args:
        name: The plugin identifier
        
    Returns:
        The registered function, or None if not found
    """
    return _registry.get(name)


def list_plugins() -> list[str]:
    """Get a list of all registered plugin names.
    
    Returns:
        List of plugin names (sorted alphabetically)
    """
    return sorted(_registry.keys())


def unregister_plugin(name: str) -> bool:
    """Remove a plugin from the registry.
    
    Args:
        name: The plugin identifier to remove
        
    Returns:
        True if plugin was found and removed, False otherwise
    """
    if name in _registry:
        del _registry[name]
        return True
    return False


def clear_registry() -> None:
    """Remove all plugins from the registry."""
    _registry.clear()
