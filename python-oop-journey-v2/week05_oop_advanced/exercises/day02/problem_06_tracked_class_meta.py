"""Problem 06: Tracked Class Creation Metaclass

Topic: Metaclasses
Difficulty: Medium

Implement a metaclass that tracks statistics about class creation. This is
useful for monitoring, debugging, and understanding code structure.

Classes to implement:
- TrackedMeta: Metaclass that tracks class creation statistics
- TrackedClass: Base class providing tracking functionality
- Multiple example classes to demonstrate tracking

Requirements:
- Track total number of classes created
- Track when each class was created (timestamp)
- Track inheritance depth of each class
- Provide methods to query statistics
- Track per-metaclass statistics (not global)
"""

from __future__ import annotations

from typing import Any


class TrackedMeta(type):
    """Metaclass that tracks class creation statistics.
    
    Tracks:
    - Total number of classes created
    - Creation timestamp for each class
    - Inheritance depth of each class
    - Class names in creation order
    
    Example:
        class MyClass(metaclass=TrackedMeta):
            pass
        
        stats = TrackedMeta.get_stats()
        # Returns information about all created classes
    """
    
    _creation_count: int = 0
    _creation_log: list[dict[str, Any]] = []
    
    def __new__(
        mcs: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:
        """Create class and track its creation.
        
        Args:
            mcs: This metaclass
            name: Name of the class being created
            bases: Base classes
            namespace: Class namespace dictionary
            
        Returns:
            The newly created class
        """
        raise NotImplementedError("Implement __new__")
    
    @classmethod
    def get_creation_count(mcs) -> int:
        """Get total number of classes created with this metaclass.
        
        Returns:
            Total class count
        """
        raise NotImplementedError("Implement get_creation_count")
    
    @classmethod
    def get_creation_log(mcs) -> list[dict[str, Any]]:
        """Get detailed log of all class creations.
        
        Returns:
            List of creation records with metadata
        """
        raise NotImplementedError("Implement get_creation_log")
    
    @classmethod
    def get_class_names(mcs) -> list[str]:
        """Get list of all created class names in order.
        
        Returns:
            List of class names
        """
        raise NotImplementedError("Implement get_class_names")
    
    @classmethod
    def reset_stats(mcs) -> None:
        """Reset all tracking statistics."""
        raise NotImplementedError("Implement reset_stats")
    
    @staticmethod
    def _calculate_depth(bases: tuple[type, ...]) -> int:
        """Calculate the inheritance depth of a class.
        
        Args:
            bases: Base classes
            
        Returns:
            Inheritance depth (0 for root classes)
        """
        raise NotImplementedError("Implement _calculate_depth")


class TrackedClass(metaclass=TrackedMeta):
    """Base class that provides tracking capabilities.
    
    Classes inheriting from this will be tracked automatically.
    """
    
    @classmethod
    def get_class_info(cls) -> dict[str, Any]:
        """Get information about this class.
        
        Returns:
            Dictionary with class metadata
        """
        raise NotImplementedError("Implement get_class_info")


class ServiceA(TrackedClass):
    """Example service class A."""
    
    def process(self) -> str:
        """Process method."""
        raise NotImplementedError("Implement process")


class ServiceB(TrackedClass):
    """Example service class B."""
    
    def handle(self) -> str:
        """Handle method."""
        raise NotImplementedError("Implement handle")


class ServiceAEnhanced(ServiceA):
    """Enhanced version of ServiceA (depth = 2)."""
    
    def enhanced_process(self) -> str:
        """Enhanced processing."""
        raise NotImplementedError("Implement enhanced_process")


class ServiceAAdvanced(ServiceAEnhanced):
    """Advanced version (depth = 3)."""
    
    def advanced_process(self) -> str:
        """Advanced processing."""
        raise NotImplementedError("Implement advanced_process")


class StandaloneService(metaclass=TrackedMeta):
    """Standalone service not inheriting from TrackedClass."""
    
    def execute(self) -> str:
        """Execute method."""
        raise NotImplementedError("Implement execute")


# Hints for Tracked Class Metaclass (Hard):
# 
# Hint 1 - Conceptual nudge:
# You need to capture metadata about class creation (timestamp, module, etc.) and
# store it as class attributes.
#
# Hint 2 - Structural plan:
# - In __init__ (after class is created), set class attributes like __created_at__,
#   __created_by_module__, etc.
# - Use datetime.now().isoformat() for timestamp
# - Use the namespace.get('__module__') for module name
# - Count instances by overriding __call__ to increment a counter
#
# Hint 3 - Edge-case warning:
# Make sure not to overwrite attributes that the class already defines. Use get_*
# methods to provide safe access to the metadata.
