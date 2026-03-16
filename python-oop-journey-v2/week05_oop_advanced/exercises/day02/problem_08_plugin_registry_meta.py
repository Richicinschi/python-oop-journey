"""Problem 08: Plugin Registry Metaclass

Topic: Metaclasses
Difficulty: Hard

Implement a metaclass for a plugin system where plugins can auto-register
with categories, versions, and dependencies. This is useful for extensible
application architectures.

Classes to implement:
- PluginMeta: Metaclass for plugin registration
- BasePlugin: Base class for all plugins
- Various plugin implementations

Requirements:
- Plugins specify category, name, and version via class attributes
- Auto-register plugins in a hierarchical registry by category
- Support plugin dependencies (validate they exist)
- Support plugin priority/ordering
- Allow looking up plugins by category and name
"""

from __future__ import annotations

from typing import Any


class PluginMeta(type):
    """Metaclass for plugin registration system.
    
    Plugins are classes that define:
    - plugin_category: str - The category this plugin belongs to
    - plugin_name: str - Unique name within the category
    - plugin_version: str - Version string (default: "1.0.0")
    - plugin_priority: int - Higher = loaded first (default: 0)
    - plugin_dependencies: list[str] - Names of required plugins
    
    The metaclass maintains a hierarchical registry:
    {
        'parsers': {
            'csv': CSVParser,
            'json': JSONParser,
        },
        'exporters': {
            'pdf': PDFExporter,
        }
    }
    """
    
    _registry: dict[str, dict[str, type]] = {}
    
    def __new__(
        mcs: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:
        """Create plugin class and register it.
        
        Args:
            mcs: This metaclass
            name: Name of the plugin class
            bases: Base classes
            namespace: Class namespace
            
        Returns:
            The newly created plugin class
        """
        raise NotImplementedError("Implement __new__")
    
    @classmethod
    def get_registry(mcs) -> dict[str, dict[str, type]]:
        """Get a copy of the plugin registry.
        
        Returns:
            Hierarchical registry dictionary
        """
        raise NotImplementedError("Implement get_registry")
    
    @classmethod
    def get_plugins_by_category(mcs, category: str) -> dict[str, type]:
        """Get all plugins in a category.
        
        Args:
            category: The category to query
            
        Returns:
            Dictionary of plugin_name -> plugin_class
        """
        raise NotImplementedError("Implement get_plugins_by_category")
    
    @classmethod
    def get_plugin(mcs, category: str, name: str) -> type | None:
        """Get a specific plugin by category and name.
        
        Args:
            category: Plugin category
            name: Plugin name
            
        Returns:
            The plugin class or None
        """
        raise NotImplementedError("Implement get_plugin")
    
    @classmethod
    def clear_registry(mcs) -> None:
        """Clear the entire plugin registry."""
        raise NotImplementedError("Implement clear_registry")
    
    @staticmethod
    def _validate_dependencies(
        namespace: dict[str, Any],
        category: str | None,
    ) -> list[str]:
        """Validate plugin dependencies exist.
        
        Args:
            namespace: Class namespace
            category: Plugin category
            
        Returns:
            List of missing dependencies
        """
        raise NotImplementedError("Implement _validate_dependencies")


class BasePlugin(metaclass=PluginMeta):
    """Base class for all plugins.
    
    These class attributes control registration:
    - plugin_category: Required category string
    - plugin_name: Required unique name string
    - plugin_version: Optional version (default: "1.0.0")
    - plugin_priority: Optional priority (default: 0)
    - plugin_dependencies: Optional list of required plugin names
    """
    
    plugin_category: str = ""
    plugin_name: str = ""
    plugin_version: str = "1.0.0"
    plugin_priority: int = 0
    plugin_dependencies: list[str] = []
    
    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize plugin with configuration.
        
        Args:
            config: Plugin configuration dictionary
        """
        raise NotImplementedError("Implement __init__")
    
    def activate(self) -> str:
        """Activate the plugin.
        
        Returns:
            Activation status message
        """
        raise NotImplementedError("Implement activate")


# Hints for Plugin Registry Metaclass (Hard):
# 
# Hint 1 - Conceptual nudge:
# Similar to class registry, but with plugin types and metadata. Each plugin class
# should register itself with its type name and version.
#
# Hint 2 - Structural plan:
# - In __init__, look for plugin_type and plugin_version class attributes
# - Register the class in a nested dict: _plugins[plugin_type][name] = class
# - Provide class methods to get_plugin(), list_plugins(), get_plugin_by_version()
# - Allow filtering by minimum version
#
# Hint 3 - Edge-case warning:
# Handle the case where plugin_type is not defined. What about version comparison?
# You might need to parse version strings like "1.2.3" for proper comparison.
    
    def deactivate(self) -> str:
        """Deactivate the plugin.
        
        Returns:
            Deactivation status message
        """
        raise NotImplementedError("Implement deactivate")
    
    def get_info(self) -> dict[str, Any]:
        """Get plugin information.
        
        Returns:
            Dictionary with plugin metadata
        """
        raise NotImplementedError("Implement get_info")


class CSVParser(BasePlugin):
    """CSV file parser plugin."""
    
    plugin_category = "parsers"
    plugin_name = "csv"
    plugin_version = "2.0.0"
    plugin_priority = 10
    
    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize CSV parser."""
        raise NotImplementedError("Implement __init__")
    
    def parse(self, content: str) -> list[list[str]]:
        """Parse CSV content.
        
        Args:
            content: Raw CSV content
            
        Returns:
            Parsed CSV as list of rows
        """
        raise NotImplementedError("Implement parse")
    
    def activate(self) -> str:
        """Activate CSV parser."""
        raise NotImplementedError("Implement activate")


class JSONParser(BasePlugin):
    """JSON file parser plugin."""
    
    plugin_category = "parsers"
    plugin_name = "json"
    plugin_version = "1.5.0"
    plugin_priority = 20
    plugin_dependencies = ["csv"]  # Depends on CSV parser
    
    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize JSON parser."""
        raise NotImplementedError("Implement __init__")
    
    def parse(self, content: str) -> dict[str, Any]:
        """Parse JSON content.
        
        Args:
            content: Raw JSON content
            
        Returns:
            Parsed JSON as dictionary
        """
        raise NotImplementedError("Implement parse")
    
    def activate(self) -> str:
        """Activate JSON parser."""
        raise NotImplementedError("Implement activate")


class PDFExporter(BasePlugin):
    """PDF export plugin."""
    
    plugin_category = "exporters"
    plugin_name = "pdf"
    plugin_version = "1.0.0"
    plugin_priority = 5
    
    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize PDF exporter."""
        raise NotImplementedError("Implement __init__")
    
    def export(self, data: Any, filename: str) -> str:
        """Export data to PDF.
        
        Args:
            data: Data to export
            filename: Output filename
            
        Returns:
            Export status message
        """
        raise NotImplementedError("Implement export")
    
    def activate(self) -> str:
        """Activate PDF exporter."""
        raise NotImplementedError("Implement activate")
