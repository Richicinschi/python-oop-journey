"""Problem 04: Cached Validated Objects.

Implement caching and validation mixins for data objects.

Classes to implement:
- Cacheable: Mixin that provides caching with TTL
- Validatable: Mixin that provides data validation
- DataObject: Base class using both mixins
- Product: A product with caching and validation

Example:
    >>> product = Product(1, {"name": "Widget", "price": 10.0})
    >>> product.is_valid()
    True
    >>> product.validate()
    []
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta
from typing import Any


class Cacheable:
    """Mixin that provides simple caching with TTL.
    
    Attributes:
        _cache: Dictionary storing cached values.
        _cache_timestamps: Dictionary storing cache entry timestamps.
        _default_ttl: Default time-to-live in seconds.
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the cacheable mixin."""
        super().__init__(*args, **kwargs)
        self._cache: dict[str, Any] = {}
        self._cache_timestamps: dict[str, datetime] = {}
        self._default_ttl: int = 60
    
    def cache_set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set a cached value with optional TTL.
        
        Args:
            key: The cache key.
            value: The value to cache.
            ttl: Time-to-live in seconds (uses default if None).
        """
        self._cache[key] = value
        self._cache_timestamps[key] = datetime.now()
        # Store TTL per key (default to class default)
        if ttl is not None:
            self._cache[key + "__ttl__"] = ttl
    
    def cache_get(self, key: str) -> Any:
        """Get a cached value if not expired.
        
        Args:
            key: The cache key.
        
        Returns:
            The cached value.
        
        Raises:
            KeyError: If key not found or expired.
        """
        if not self.cache_has(key):
            raise KeyError(f"Key '{key}' not found or expired")
        return self._cache[key]
    
    def cache_has(self, key: str) -> bool:
        """Check if a key exists and is not expired.
        
        Args:
            key: The cache key.
        
        Returns:
            True if key exists and not expired, False otherwise.
        """
        if key not in self._cache:
            return False
        if self._is_expired(key):
            return False
        return True
    
    def cache_clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
        self._cache_timestamps.clear()
    
    def _is_expired(self, key: str) -> bool:
        """Check if a cache entry is expired.
        
        Args:
            key: The cache key.
        
        Returns:
            True if expired or doesn't exist, False otherwise.
        """
        if key not in self._cache_timestamps:
            return True
        
        timestamp = self._cache_timestamps[key]
        ttl = self._cache.get(key + "__ttl__", self._default_ttl)
        expiry = timestamp + timedelta(seconds=ttl)
        return datetime.now() > expiry


class Validatable:
    """Mixin that provides data validation.
    
    Subclasses should implement _validate() method.
    """
    
    def _validate(self) -> list[str]:
        """Validate the object's data.
        
        Returns:
            List of validation error messages (empty if valid).
        """
        return []
    
    def validate(self) -> list[str]:
        """Validate and return list of errors.
        
        Returns:
            List of validation error messages.
        """
        return self._validate()
    
    def is_valid(self) -> bool:
        """Check if the object is valid.
        
        Returns:
            True if no validation errors, False otherwise.
        """
        return len(self.validate()) == 0


class DataObject(Cacheable, Validatable):
    """Base data object with caching and validation.
    
    Attributes:
        _data: The internal data dictionary.
        _cache: From Cacheable.
        _cache_timestamps: From Cacheable.
    
    Args:
        id: The object's unique identifier.
        data: The initial data dictionary.
    """
    
    def __init__(self, id: int, data: dict[str, Any]) -> None:
        """Initialize a data object.
        
        Args:
            id: The object's unique identifier.
            data: The initial data dictionary.
        """
        super().__init__()
        self.id = id
        self._data = data.copy()
    
    def get_data(self) -> dict[str, Any]:
        """Get a copy of the data.
        
        Returns:
            Copy of the internal data dictionary.
        """
        return self._data.copy()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from data.
        
        Args:
            key: The data key.
            default: Default value if key not found.
        
        Returns:
            The value or default.
        """
        return self._data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in data and invalidate cache.
        
        Args:
            key: The data key.
            value: The value to set.
        """
        self._data[key] = value
        self.cache_clear()
    
    def _validate(self) -> list[str]:
        """Basic validation - can be overridden.
        
        Returns:
            Empty list (subclasses can add validation).
        """
        return []


class Product(DataObject):
    """A product with caching and validation.
    
    Validation rules:
    - name: Required, non-empty string
    - price: Required, must be >= 0
    - quantity: Optional, if present must be >= 0
    
    Attributes:
        id: The product's unique identifier.
        _data: The product's data.
    
    Args:
        id: The product's unique identifier.
        data: The product data with name, price, and optional quantity.
    """
    
    def __init__(self, id: int, data: dict[str, Any]) -> None:
        """Initialize a product.
        
        Args:
            id: The product's unique identifier.
            data: The product data with name, price, and optional quantity.
        """
        super().__init__(id, data)
    
    def _validate(self) -> list[str]:
        """Validate product data.
        
        Returns:
            List of validation error messages.
        """
        errors: list[str] = []
        
        # Validate name
        name = self._data.get("name")
        if name is None or not isinstance(name, str) or not name.strip():
            errors.append("name is required and must be a non-empty string")
        
        # Validate price
        price = self._data.get("price")
        if price is None:
            errors.append("price is required")
        elif not isinstance(price, (int, float)):
            errors.append("price must be a number")
        elif price < 0:
            errors.append("price must be >= 0")
        
        # Validate quantity if present
        if "quantity" in self._data:
            quantity = self._data.get("quantity")
            if not isinstance(quantity, (int, float)):
                errors.append("quantity must be a number")
            elif quantity < 0:
                errors.append("quantity must be >= 0")
        
        return errors
    
    @property
    def name(self) -> str:
        """Get the product name.
        
        Returns:
            The product name or empty string.
        """
        return self._data.get("name", "")
    
    @property
    def price(self) -> float:
        """Get the product price.
        
        Returns:
            The product price or 0.0.
        """
        return float(self._data.get("price", 0.0))
    
    def get_total_value(self) -> float:
        """Calculate total value (price * quantity).
        
        Returns:
            Total value of the product in stock.
        """
        return self.price * self._data.get("quantity", 0)
