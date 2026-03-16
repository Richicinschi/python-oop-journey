"""Problem 10: Weak Reference Descriptor

Topic: Descriptor holding weak refs
Difficulty: Hard

Create a descriptor that uses weak references to store per-instance values,
allowing instances to be garbage collected without descriptor interference.
"""

from __future__ import annotations

from typing import Any, TypeVar, Generic
from weakref import WeakKeyDictionary

T = TypeVar('T')


class WeakAttribute:
    """A descriptor that uses weak references for storage.
    
    This descriptor uses WeakKeyDictionary to store values, which means:
    - Values are associated with instances via weak references
    - When an instance is garbage collected, its entry is automatically removed
    - No memory leaks from descriptor holding references to instances
    - Useful for descriptors that hold large or temporary data
    
    Attributes:
        default: Default value when instance has no entry
        _data: WeakKeyDictionary storing per-instance values
    """
    
    def __init__(self, default: Any = None) -> None:
        """Initialize with optional default.
        
        Args:
            default: Default value for instances not in storage
        """
        raise NotImplementedError("Implement WeakAttribute.__init__")
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Called when descriptor is assigned to class.
        
        Args:
            owner: The class
            name: The attribute name
        """
        raise NotImplementedError("Implement WeakAttribute.__set_name__")
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        """Get value from weak storage.
        
        Args:
            instance: The instance, or None for class access
            owner: The owner class
            
        Returns:
            Stored value or default, or self if class access
        """
        raise NotImplementedError("Implement WeakAttribute.__get__")
    
    def __set__(self, instance: object, value: Any) -> None:
        """Store value using weak reference.
        
        Args:
            instance: The instance (key in weak dict)
            value: The value to store
        """
        raise NotImplementedError("Implement WeakAttribute.__set__")
    
    def __delete__(self, instance: object) -> None:
        """Remove entry from weak storage.
        
        Args:
            instance: The instance
            
        Raises:
            AttributeError: If instance not in storage
        """
        raise NotImplementedError("Implement WeakAttribute.__delete__")
    
    def __contains__(self, instance: object) -> bool:
        """Check if instance has a value stored.
        
        Args:
            instance: The instance to check
            
        Returns:
            True if instance is in weak storage
        """
        raise NotImplementedError("Implement WeakAttribute.__contains__")
    
    def get_reference_count(self) -> int:
        """Get number of instances currently stored.
        
        Returns:
            Number of entries in weak storage
        """
        raise NotImplementedError("Implement WeakAttribute.get_reference_count")


class CachedComputation:
    """A descriptor for cached computations using weak storage.
    
    Stores computed values per instance without preventing garbage collection.
    
    Attributes:
        compute_func: Function to compute value if not cached
    """
    
    def __init__(self, compute_func: Any = None) -> None:
        """Initialize with compute function.
        
        Args:
            compute_func: Function(instance) -> value
        """
        raise NotImplementedError("Implement CachedComputation.__init__")
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Set up the descriptor."""
        raise NotImplementedError("Implement CachedComputation.__set_name__")
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        """Get cached or computed value.
        
        Args:
            instance: The instance
            owner: The owner class
            
        Returns:
            Cached or computed value
        """
        raise NotImplementedError("Implement CachedComputation.__get__")
    
    def invalidate(self, instance: object) -> None:
        """Invalidate cache for an instance.
        
        Args:
            instance: The instance
        """
        raise NotImplementedError("Implement CachedComputation.invalidate")


class TemporaryData:
    """A class holding temporary data via weak attributes.
    
    Demonstrates that weak attributes don't prevent garbage collection.
    
    Attributes (weak):
        buffer: Temporary buffer data
        cache: Temporary cache
        metadata: Session metadata
    """
    
    buffer = WeakAttribute()
    cache = WeakAttribute()
    metadata = WeakAttribute()
    
    def __init__(self, session_id: str) -> None:
        """Initialize with session ID.
        
        Args:
            session_id: Unique session identifier
        """
        raise NotImplementedError("Implement TemporaryData.__init__")
    
    def load_buffer(self, data: bytes) -> None:
        """Load data into buffer.
        
        Args:
            data: Binary data
        """
        raise NotImplementedError("Implement TemporaryData.load_buffer")
    
    def has_buffer(self) -> bool:
        """Check if buffer is loaded.
        
        Returns:
            True if buffer has data
        """
        raise NotImplementedError("Implement TemporaryData.has_buffer")
    
    def get_buffer_size(self) -> int:
        """Get buffer size in bytes.
        
        Returns:
            Size of buffer or 0
        """
        raise NotImplementedError("Implement TemporaryData.get_buffer_size")


class ExpensiveObject:
    """An object with expensive computed properties cached weakly.
    
    Demonstrates weak caching that allows GC when memory is needed.
    
    Attributes:
        data: Source data
        
    Weak-cached Attributes:
        sorted_data: Sorted version of data
        hash_value: Computed hash
    """
    
    def __init__(self, data: list[int]) -> None:
        """Initialize with data.
        
        Args:
            data: List of integers
        """
        raise NotImplementedError("Implement ExpensiveObject.__init__")
    
    @CachedComputation
    def sorted_data(self) -> list[int]:
        """Get sorted data (expensive).
        
        Returns:
            Sorted list of data
        """
        raise NotImplementedError("Implement ExpensiveObject.sorted_data")
    
    @CachedComputation
    def hash_value(self) -> int:
        """Get computed hash (expensive).
        
        Returns:
            Hash of the data
        """
        raise NotImplementedError("Implement ExpensiveObject.hash_value")


# Hints for Weak Reference Descriptor (Hard):
# 
# Hint 1 - Conceptual nudge:
# WeakKeyDictionary is your friend here. It automatically removes entries when the
# key (instance) is garbage collected.
#
# Hint 2 - Structural plan:
# - Initialize a WeakKeyDictionary in __init__
# - Store/retrieve values using self._data[instance] = value
# - __contains__ should check "instance in self._data"
# - For CachedComputation, you need to store the computed value after first access
# - Use a WeakKeyDictionary for the cache in CachedComputation too
#
# Hint 3 - Edge-case warning:
# WeakKeyDictionary cannot have its keys (instances) deleted directly - entries
# disappear when the instance is garbage collected. Test your __delete__ carefully.
# Also, CachedComputation needs to handle the case where the compute function is
# passed as an argument vs used as a decorator.
