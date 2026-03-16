"""Problem 08: Plugin Registry Metaclass - Solution.

Plugin system with auto-registration, categories, versions, and dependencies.
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
    """
    
    _registry: dict[str, dict[str, type]] = {}
    _all_plugins: dict[str, type] = {}  # Flat registry for dependency lookup
    
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
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Skip registration for BasePlugin itself
        if name == 'BasePlugin':
            return cls
        
        # Get plugin metadata
        category = namespace.get('plugin_category', '')
        plugin_name = namespace.get('plugin_name', '')
        
        if not category or not plugin_name:
            return cls  # Not a valid plugin definition
        
        # Check dependencies
        dependencies = namespace.get('plugin_dependencies', [])
        if dependencies:
            missing = mcs._validate_dependencies(dependencies, category)
            if missing:
                # Log warning but don't prevent registration
                # In production, you might want to raise an error
                pass
        
        # Register in category
        if category not in mcs._registry:
            mcs._registry[category] = {}
        mcs._registry[category][plugin_name] = cls
        
        # Register in flat registry for dependency lookups
        mcs._all_plugins[plugin_name] = cls
        
        return cls
    
    @classmethod
    def get_registry(mcs) -> dict[str, dict[str, type]]:
        """Get a copy of the plugin registry.
        
        Returns:
            Hierarchical registry dictionary
        """
        return {
            cat: plugins.copy()
            for cat, plugins in mcs._registry.items()
        }
    
    @classmethod
    def get_plugins_by_category(mcs, category: str) -> dict[str, type]:
        """Get all plugins in a category.
        
        Args:
            category: The category to query
            
        Returns:
            Dictionary of plugin_name -> plugin_class
        """
        return mcs._registry.get(category, {}).copy()
    
    @classmethod
    def get_plugin(mcs, category: str, name: str) -> type | None:
        """Get a specific plugin by category and name.
        
        Args:
            category: Plugin category
            name: Plugin name
            
        Returns:
            The plugin class or None
        """
        return mcs._registry.get(category, {}).get(name)
    
    @classmethod
    def clear_registry(mcs) -> None:
        """Clear the entire plugin registry."""
        mcs._registry.clear()
        mcs._all_plugins.clear()
    
    @staticmethod
    def _validate_dependencies(
        dependencies: list[str],
        category: str | None,
    ) -> list[str]:
        """Validate plugin dependencies exist.
        
        Args:
            dependencies: List of required plugin names
            category: Plugin category (for error context)
            
        Returns:
            List of missing dependencies
        """
        missing = []
        for dep in dependencies:
            if dep not in PluginMeta._all_plugins:
                missing.append(dep)
        return missing


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
        self.config = config or {}
        self._active = False
    
    def activate(self) -> str:
        """Activate the plugin.
        
        Returns:
            Activation status message
        """
        self._active = True
        return f"Plugin {self.plugin_name} v{self.plugin_version} activated"
    
    def deactivate(self) -> str:
        """Deactivate the plugin.
        
        Returns:
            Deactivation status message
        """
        self._active = False
        return f"Plugin {self.plugin_name} deactivated"
    
    def get_info(self) -> dict[str, Any]:
        """Get plugin information.
        
        Returns:
            Dictionary with plugin metadata
        """
        return {
            'name': self.plugin_name,
            'category': self.plugin_category,
            'version': self.plugin_version,
            'priority': self.plugin_priority,
            'dependencies': self.plugin_dependencies,
            'active': self._active,
        }


class CSVParser(BasePlugin):
    """CSV file parser plugin."""
    
    plugin_category = "parsers"
    plugin_name = "csv"
    plugin_version = "2.0.0"
    plugin_priority = 10
    
    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize CSV parser."""
        super().__init__(config)
        self.delimiter = config.get('delimiter', ',') if config else ','
    
    def parse(self, content: str) -> list[list[str]]:
        """Parse CSV content.
        
        Args:
            content: Raw CSV content
            
        Returns:
            Parsed CSV as list of rows
        """
        lines = content.strip().split('\n')
        return [line.split(self.delimiter) for line in lines]
    
    def activate(self) -> str:
        """Activate CSV parser."""
        return super().activate()


class JSONParser(BasePlugin):
    """JSON file parser plugin."""
    
    plugin_category = "parsers"
    plugin_name = "json"
    plugin_version = "1.5.0"
    plugin_priority = 20
    plugin_dependencies = ["csv"]
    
    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize JSON parser."""
        super().__init__(config)
    
    def parse(self, content: str) -> dict[str, Any]:
        """Parse JSON content.
        
        Args:
            content: Raw JSON content
            
        Returns:
            Parsed JSON as dictionary
        """
        import json
        return json.loads(content)
    
    def activate(self) -> str:
        """Activate JSON parser."""
        return super().activate()


class PDFExporter(BasePlugin):
    """PDF export plugin."""
    
    plugin_category = "exporters"
    plugin_name = "pdf"
    plugin_version = "1.0.0"
    plugin_priority = 5
    
    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize PDF exporter."""
        super().__init__(config)
    
    def export(self, data: Any, filename: str) -> str:
        """Export data to PDF.
        
        Args:
            data: Data to export
            filename: Output filename
            
        Returns:
            Export status message
        """
        return f"Exported to {filename}.pdf"
    
    def activate(self) -> str:
        """Activate PDF exporter."""
        return super().activate()
