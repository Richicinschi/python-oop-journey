"""Problem 06: Tracked Class Creation Metaclass - Solution.

Tracks statistics about class creation for monitoring, debugging,
and understanding code structure.
"""

from __future__ import annotations

from typing import Any
from datetime import datetime


class TrackedMeta(type):
    """Metaclass that tracks class creation statistics.
    
    Tracks:
    - Total number of classes created
    - Creation timestamp for each class
    - Inheritance depth of each class
    - Class names in creation order
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
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Track creation
        mcs._creation_count += 1
        depth = mcs._calculate_depth(bases)
        
        creation_record = {
            'name': name,
            'timestamp': datetime.now(),
            'depth': depth,
            'bases': [b.__name__ for b in bases if hasattr(b, '__name__')],
            'order': mcs._creation_count,
        }
        mcs._creation_log.append(creation_record)
        
        return cls
    
    @classmethod
    def get_creation_count(mcs) -> int:
        """Get total number of classes created with this metaclass.
        
        Returns:
            Total class count
        """
        return mcs._creation_count
    
    @classmethod
    def get_creation_log(mcs) -> list[dict[str, Any]]:
        """Get detailed log of all class creations.
        
        Returns:
            List of creation records with metadata
        """
        return mcs._creation_log.copy()
    
    @classmethod
    def get_class_names(mcs) -> list[str]:
        """Get list of all created class names in order.
        
        Returns:
            List of class names
        """
        return [record['name'] for record in mcs._creation_log]
    
    @classmethod
    def reset_stats(mcs) -> None:
        """Reset all tracking statistics."""
        mcs._creation_count = 0
        mcs._creation_log = []
    
    @staticmethod
    def _calculate_depth(bases: tuple[type, ...]) -> int:
        """Calculate the inheritance depth of a class.
        
        Args:
            bases: Base classes
            
        Returns:
            Inheritance depth (0 for root classes)
        """
        if not bases:
            return 0
        
        # Check if any base class uses TrackedMeta and has a _depth attribute
        max_base_depth = 0
        for base in bases:
            # Try to get depth from tracked creation log
            for record in TrackedMeta._creation_log:
                if record['name'] == base.__name__:
                    max_base_depth = max(max_base_depth, record['depth'] + 1)
                    break
            else:
                # Fallback: use MRO depth
                if hasattr(base, '__mro__'):
                    mro_depth = len([c for c in base.__mro__ if c is not object])
                    max_base_depth = max(max_base_depth, mro_depth)
        
        return max_base_depth


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
        # Find this class in the creation log
        for record in TrackedMeta._creation_log:
            if record['name'] == cls.__name__:
                return {
                    'name': record['name'],
                    'creation_order': record['order'],
                    'depth': record['depth'],
                    'bases': record['bases'],
                }
        return {'name': cls.__name__, 'error': 'Not found in creation log'}


class ServiceA(TrackedClass):
    """Example service class A."""
    
    def process(self) -> str:
        """Process method."""
        return "ServiceA processing"


class ServiceB(TrackedClass):
    """Example service class B."""
    
    def handle(self) -> str:
        """Handle method."""
        return "ServiceB handling"


class ServiceAEnhanced(ServiceA):
    """Enhanced version of ServiceA (depth = 2)."""
    
    def enhanced_process(self) -> str:
        """Enhanced processing."""
        return "ServiceAEnhanced enhanced processing"


class ServiceAAdvanced(ServiceAEnhanced):
    """Advanced version (depth = 3)."""
    
    def advanced_process(self) -> str:
        """Advanced processing."""
        return "ServiceAAdvanced advanced processing"


class StandaloneService(metaclass=TrackedMeta):
    """Standalone service not inheriting from TrackedClass."""
    
    def execute(self) -> str:
        """Execute method."""
        return "StandaloneService executing"
