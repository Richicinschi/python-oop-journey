"""Reference solution for Problem 10: Weak Reference Descriptor."""

from __future__ import annotations

from typing import Any, Callable
from weakref import WeakKeyDictionary


class WeakAttribute:
    """A descriptor that uses weak references for storage."""
    
    def __init__(self, default: Any = None) -> None:
        self.default = default
        self.name = ""
        self._data: WeakKeyDictionary = WeakKeyDictionary()
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        return self._data.get(instance, self.default)
    
    def __set__(self, instance: object, value: Any) -> None:
        self._data[instance] = value
    
    def __delete__(self, instance: object) -> None:
        if instance in self._data:
            del self._data[instance]
        else:
            raise AttributeError(f"'{self.name}' not set")
    
    def __contains__(self, instance: object) -> bool:
        return instance in self._data
    
    def get_reference_count(self) -> int:
        return len(self._data)


class CachedComputation:
    """A descriptor for cached computations using weak storage."""
    
    def __init__(self, compute_func: Callable[[Any], Any] | None = None) -> None:
        self.compute_func = compute_func
        self.name = ""
        self._cache: WeakKeyDictionary = WeakKeyDictionary()
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        if self.compute_func is None:
            self.compute_func = getattr(owner, f"_compute_{name}", None)
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        
        if instance not in self._cache:
            if self.compute_func:
                value = self.compute_func(instance)
                self._cache[instance] = value
        
        return self._cache.get(instance)
    
    def invalidate(self, instance: object) -> None:
        if instance in self._cache:
            del self._cache[instance]


class TemporaryData:
    """A class holding temporary data via weak attributes."""
    
    buffer = WeakAttribute()
    cache = WeakAttribute()
    metadata = WeakAttribute()
    
    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
    
    def load_buffer(self, data: bytes) -> None:
        self.buffer = data
    
    def has_buffer(self) -> bool:
        return self in type(self).buffer._data
    
    def get_buffer_size(self) -> int:
        buf = self.buffer
        return len(buf) if buf else 0


class ExpensiveObject:
    """An object with expensive computed properties cached weakly."""
    
    def __init__(self, data: list[int]) -> None:
        self.data = data
        self._sorted_data = CachedComputation()
        self._hash_value = CachedComputation()
    
    @property
    def sorted_data(self) -> list[int]:
        if hasattr(self, '_sorted_data_cache'):
            return self._sorted_data_cache
        result = sorted(self.data)
        self._sorted_data_cache = result
        return result
    
    @property
    def hash_value(self) -> int:
        if hasattr(self, '_hash_cache'):
            return self._hash_cache
        result = hash(tuple(self.data))
        self._hash_cache = result
        return result
