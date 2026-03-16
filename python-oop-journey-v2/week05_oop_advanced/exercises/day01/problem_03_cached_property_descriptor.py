"""Problem 03: Cached Property Descriptor

Topic: Lazy evaluation descriptor
Difficulty: Medium

Create a descriptor that caches the result of expensive computations.
"""

from __future__ import annotations

from typing import Any, Callable


class CachedProperty:
    """A non-data descriptor that caches property values.
    
    Similar to functools.cached_property but implemented manually.
    The descriptor should:
    - Accept a function that computes the value
    - Compute the value only on first access
    - Cache the result in the instance __dict__
    - Allow the cache to be invalidated
    
    This is a NON-DATA descriptor (only implements __get__).
    """
    
    def __init__(self, func: Callable[[Any], Any]) -> None:
        """Initialize with a compute function.
        
        Args:
            func: Function that computes the property value.
                  Takes the instance as argument.
        """
        raise NotImplementedError("Implement CachedProperty.__init__")
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Called when descriptor is assigned to class.
        
        Args:
            owner: The class
            name: The attribute name
        """
        raise NotImplementedError("Implement CachedProperty.__set_name__")
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        """Get the cached value, computing if necessary.
        
        Args:
            instance: The instance, or None for class access
            owner: The owner class
            
        Returns:
            The cached or computed value, or self if class access
            
        Note:
            This is a non-data descriptor. After first access,
            the value is stored in instance.__dict__ and this
            method won't be called for that instance.
        """
        raise NotImplementedError("Implement CachedProperty.__get__")


class DataProcessor:
    """A data processor with cached expensive operations.
    
    Attributes (cached):
        total: Sum of all data values
        average: Average of data values
        variance: Statistical variance of data
    """
    
    def __init__(self, data: list[float]) -> None:
        """Initialize with data.
        
        Args:
            data: List of numeric values
        """
        raise NotImplementedError("Implement DataProcessor.__init__")
    
    @CachedProperty
    def total(self) -> float:
        """Calculate total sum (expensive operation).
        
        Returns:
            Sum of all data values
        """
        raise NotImplementedError("Implement DataProcessor.total")
    
    @CachedProperty
    def average(self) -> float:
        """Calculate average (depends on total).
        
        Returns:
            Average of data values
        """
        raise NotImplementedError("Implement DataProcessor.average")
    
    @CachedProperty
    def variance(self) -> float:
        """Calculate variance (expensive computation).
        
        Returns:
            Statistical variance
        """
        raise NotImplementedError("Implement DataProcessor.variance")
    
    def invalidate_cache(self) -> None:
        """Invalidate all cached properties.
        
        Removes cached values from instance dict so they
        will be recomputed on next access.
        """
        raise NotImplementedError("Implement DataProcessor.invalidate_cache")


class WebPage:
    """A web page with cached content.
    
    Attributes:
        url: The page URL
        
    Cached Attributes:
        content: The page content
        word_count: Number of words in content
    """
    
    def __init__(self, url: str) -> None:
        """Initialize with URL.
        
        Args:
            url: The page URL
        """
        raise NotImplementedError("Implement WebPage.__init__")
    
    @CachedProperty
    def content(self) -> str:
        """Fetch and cache page content.
        
        Returns:
            The page content (simulated)
        """
        raise NotImplementedError("Implement WebPage.content")
    
    @CachedProperty
    def word_count(self) -> int:
        """Count words in content.
        
        Returns:
            Number of words
        """
        raise NotImplementedError("Implement WebPage.word_count")
