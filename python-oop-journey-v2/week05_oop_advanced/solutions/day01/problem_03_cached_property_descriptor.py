"""Reference solution for Problem 03: Cached Property Descriptor."""

from __future__ import annotations

import time
from typing import Any, Callable


class CachedProperty:
    """A non-data descriptor that caches property values."""
    
    def __init__(self, func: Callable[[Any], Any]) -> None:
        self.func = func
        self.name = ""
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        
        value = self.func(instance)
        setattr(instance, self.name, value)
        return value


class DataProcessor:
    """A data processor with cached expensive operations."""
    
    def __init__(self, data: list[float]) -> None:
        self.data = data
    
    @CachedProperty
    def total(self) -> float:
        time.sleep(0.01)
        return sum(self.data)
    
    @CachedProperty
    def average(self) -> float:
        if not self.data:
            return 0.0
        return self.total / len(self.data)
    
    @CachedProperty
    def variance(self) -> float:
        if not self.data:
            return 0.0
        mean = self.average
        return sum((x - mean) ** 2 for x in self.data) / len(self.data)
    
    def invalidate_cache(self) -> None:
        for attr in ['total', 'average', 'variance']:
            if attr in self.__dict__:
                delattr(self, attr)


class WebPage:
    """A web page with cached content."""
    
    def __init__(self, url: str) -> None:
        self.url = url
    
    @CachedProperty
    def content(self) -> str:
        return f"<html><body>Content of {self.url}</body></html>"
    
    @CachedProperty
    def word_count(self) -> int:
        return len(self.content.split())
