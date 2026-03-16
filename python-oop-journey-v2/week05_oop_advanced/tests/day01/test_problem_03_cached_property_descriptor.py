"""Tests for Problem 03: Cached Property Descriptor."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day01.problem_03_cached_property_descriptor import (
    CachedProperty, DataProcessor, WebPage
)


class TestCachedProperty:
    """Tests for the CachedProperty descriptor."""
    
    def test_descriptor_is_non_data_descriptor(self) -> None:
        """CachedProperty only implements __get__, not __set__."""
        class TestClass:
            @CachedProperty
            def value(self) -> int:
                return 42
        
        obj = TestClass()
        # First access computes value
        assert obj.value == 42
        # Value should be in instance dict now
        assert 'value' in obj.__dict__
    
    def test_value_computed_once(self) -> None:
        call_count = 0
        
        class TestClass:
            @CachedProperty
            def value(self) -> int:
                nonlocal call_count
                call_count += 1
                return 42
        
        obj = TestClass()
        assert call_count == 0
        
        # First access
        v1 = obj.value
        assert call_count == 1
        
        # Second access - should use cached value
        v2 = obj.value
        assert call_count == 1  # Not called again
        assert v1 == v2


class TestDataProcessor:
    """Tests for the DataProcessor class."""
    
    def test_total_computation(self) -> None:
        processor = DataProcessor([1, 2, 3, 4, 5])
        assert processor.total == 15.0
    
    def test_average_computation(self) -> None:
        processor = DataProcessor([1, 2, 3, 4, 5])
        assert processor.average == 3.0
    
    def test_variance_computation(self) -> None:
        processor = DataProcessor([1, 2, 3, 4, 5])
        # Variance = sum((x - mean)^2) / n
        # Mean = 3
        # Variance = (4 + 1 + 0 + 1 + 4) / 5 = 2.0
        assert processor.variance == 2.0
    
    def test_cache_invalidation(self) -> None:
        processor = DataProcessor([1, 2, 3])
        
        # Access to cache
        _ = processor.total
        assert 'total' in processor.__dict__
        
        # Invalidate
        processor.invalidate_cache()
        assert 'total' not in processor.__dict__
    
    def test_average_uses_cached_total(self) -> None:
        processor = DataProcessor([1, 2, 3, 4, 5])
        
        # Access average (which depends on total)
        avg = processor.average
        assert avg == 3.0
        
        # Both should be cached
        assert 'average' in processor.__dict__
    
    def test_empty_data(self) -> None:
        processor = DataProcessor([])
        assert processor.total == 0
        assert processor.average == 0.0
        assert processor.variance == 0.0


class TestWebPage:
    """Tests for the WebPage class."""
    
    def test_content_fetch(self) -> None:
        page = WebPage("https://example.com")
        content = page.content
        assert "https://example.com" in content
    
    def test_content_caching(self) -> None:
        page = WebPage("https://example.com")
        
        # First access
        c1 = page.content
        # Second access - should be cached
        c2 = page.content
        assert c1 is c2
    
    def test_word_count(self) -> None:
        page = WebPage("https://example.com")
        count = page.word_count
        assert isinstance(count, int)
        assert count > 0
    
    def test_word_count_uses_cached_content(self) -> None:
        page = WebPage("https://example.com")
        
        # Access word_count (depends on content)
        count = page.word_count
        assert 'content' in page.__dict__
        assert count > 0
