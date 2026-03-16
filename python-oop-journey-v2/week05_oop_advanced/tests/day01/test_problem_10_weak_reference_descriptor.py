"""Tests for Problem 10: Weak Reference Descriptor."""

from __future__ import annotations

import gc
import pytest

from week05_oop_advanced.solutions.day01.problem_10_weak_reference_descriptor import (
    WeakAttribute, CachedComputation, TemporaryData, ExpensiveObject
)


class TestWeakAttribute:
    """Tests for the WeakAttribute descriptor."""
    
    def test_value_stored_and_retrieved(self) -> None:
        class TestClass:
            value = WeakAttribute(default="default")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        obj.value = "test"
        assert obj.value == "test"
    
    def test_default_value_when_not_set(self) -> None:
        class TestClass:
            value = WeakAttribute(default="default")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        assert obj.value == "default"
    
    def test_instance_in_storage(self) -> None:
        class TestClass:
            value = WeakAttribute()
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        obj.value = "test"
        
        descriptor = TestClass.__dict__['value']
        assert obj in descriptor
    
    def test_reference_count_tracked(self) -> None:
        class TestClass:
            value = WeakAttribute()
            
            def __init__(self) -> None:
                pass
        
        descriptor = TestClass.__dict__['value']
        initial_count = descriptor.get_reference_count()
        
        obj = TestClass()
        obj.value = "test"
        
        assert descriptor.get_reference_count() == initial_count + 1
    
    def test_entry_removed_after_gc(self) -> None:
        class TestClass:
            value = WeakAttribute()
        
        descriptor = TestClass.__dict__['value']
        
        def create_and_set() -> None:
            obj = TestClass()
            obj.value = "test"
            assert descriptor.get_reference_count() == 1
        
        create_and_set()
        gc.collect()
        
        assert descriptor.get_reference_count() == 0
    
    def test_delete_raises_when_not_set(self) -> None:
        class TestClass:
            value = WeakAttribute()
        
        obj = TestClass()
        with pytest.raises(AttributeError):
            del obj.value


class TestCachedComputation:
    """Tests for the CachedComputation descriptor."""
    
    def test_value_computed_and_cached(self) -> None:
        call_count = 0
        
        class TestClass:
            def __init__(self) -> None:
                self.data = [3, 1, 2]
            
            def _compute_sorted(self) -> list[int]:
                nonlocal call_count
                call_count += 1
                return sorted(self.data)
            
            sorted_data = CachedComputation(_compute_sorted)
        
        obj = TestClass()
        assert call_count == 0
        
        result1 = obj.sorted_data
        assert call_count == 1
        assert result1 == [1, 2, 3]
        
        result2 = obj.sorted_data
        assert call_count == 1  # Not called again
        assert result1 == result2


class TestTemporaryData:
    """Tests for the TemporaryData class."""
    
    def test_creation(self) -> None:
        data = TemporaryData("session-123")
        assert data.session_id == "session-123"
    
    def test_buffer_loaded(self) -> None:
        data = TemporaryData("session-123")
        data.load_buffer(b"test data")
        assert data.has_buffer() is True
        assert data.get_buffer_size() == 9
    
    def test_no_buffer_initially(self) -> None:
        data = TemporaryData("session-123")
        assert data.has_buffer() is False
        assert data.get_buffer_size() == 0
    
    def test_buffer_gc_cleanup(self) -> None:
        descriptor = TemporaryData.__dict__['buffer']
        
        def create_with_buffer() -> None:
            data = TemporaryData("session-123")
            data.load_buffer(b"test data")
            assert descriptor.get_reference_count() == 1
        
        create_with_buffer()
        gc.collect()
        
        assert descriptor.get_reference_count() == 0


class TestExpensiveObject:
    """Tests for the ExpensiveObject class."""
    
    def test_creation(self) -> None:
        obj = ExpensiveObject([3, 1, 4, 1, 5])
        assert obj.data == [3, 1, 4, 1, 5]
    
    def test_sorted_data_computed(self) -> None:
        obj = ExpensiveObject([3, 1, 4, 1, 5])
        assert obj.sorted_data == [1, 1, 3, 4, 5]
    
    def test_hash_value_computed(self) -> None:
        obj = ExpensiveObject([1, 2, 3])
        hash_val = obj.hash_value
        assert isinstance(hash_val, int)
        # Same data should give same hash
        assert hash_val == hash(tuple([1, 2, 3]))
    
    def test_sorted_data_cached(self) -> None:
        obj = ExpensiveObject([3, 1, 2])
        s1 = obj.sorted_data
        s2 = obj.sorted_data
        assert s1 is s2
