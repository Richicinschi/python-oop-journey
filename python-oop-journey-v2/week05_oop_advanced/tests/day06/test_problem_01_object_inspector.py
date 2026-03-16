"""Tests for Problem 01: Object Inspector."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day06.problem_01_object_inspector import (
    ObjectInspector,
)


class SampleClass:
    """A sample class for testing introspection."""
    
    class_attribute = "class_value"
    
    def __init__(self, name: str, value: int) -> None:
        self.name = name
        self._private = value
        self.__very_private = value * 2
    
    def public_method(self) -> str:
        """A public method."""
        return f"Hello, {self.name}"
    
    def _private_method(self) -> str:
        """A private method."""
        return "private"
    
    @property
    def computed(self) -> int:
        """A computed property."""
        return self._private * 2


class EmptyClass:
    """An empty class for testing."""
    pass


class TestObjectInspector:
    """Tests for the ObjectInspector class."""
    
    def test_init(self) -> None:
        """Test inspector initialization."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        assert inspector.target is obj
    
    def test_list_attributes_basic(self) -> None:
        """Test listing attributes."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        attrs = inspector.list_attributes(include_private=True)
        
        assert 'name' in attrs
        assert 'public_method' in attrs
        assert 'computed' in attrs
        assert '_private' in attrs
    
    def test_list_attributes_excludes_private_by_default(self) -> None:
        """Test that private attributes are excluded by default."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        attrs = inspector.list_attributes(include_private=False)
        
        assert 'name' in attrs
        assert '_private' not in attrs
        assert '_private_method' not in attrs
    
    def test_list_attributes_excludes_dunder(self) -> None:
        """Test that dunder methods are excluded."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        attrs = inspector.list_attributes(include_private=True)
        
        # Dunder methods should not be in the list
        assert '__init__' not in attrs
        assert '__class__' not in attrs
    
    def test_list_attributes_returns_correct_kinds(self) -> None:
        """Test that attribute kinds are correctly identified."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        attrs = inspector.list_attributes(include_private=False)
        
        assert attrs['name']['kind'] == 'data'
        assert attrs['public_method']['kind'] == 'method'
        assert attrs['computed']['kind'] == 'property'
    
    def test_get_attribute_info_existing(self) -> None:
        """Test getting info for an existing attribute."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        info = inspector.get_attribute_info('name')
        
        assert info is not None
        assert info['name'] == 'name'
        assert info['value'] == 'test'
        assert info['kind'] == 'data'
    
    def test_get_attribute_info_method(self) -> None:
        """Test getting info for a method."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        info = inspector.get_attribute_info('public_method')
        
        assert info is not None
        assert info['name'] == 'public_method'
        assert info['kind'] == 'method'
        assert 'A public method' in (info.get('doc') or '')
    
    def test_get_attribute_info_property(self) -> None:
        """Test getting info for a property."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        info = inspector.get_attribute_info('computed')
        
        assert info is not None
        assert info['name'] == 'computed'
        assert info['kind'] == 'property'
        assert info['value'] == 84  # 42 * 2
    
    def test_get_attribute_info_nonexistent(self) -> None:
        """Test getting info for a non-existent attribute."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        info = inspector.get_attribute_info('nonexistent')
        
        assert info is None
    
    def test_filter_by_type_data(self) -> None:
        """Test filtering by data type."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        data_attrs = inspector.filter_by_type('data')
        
        assert 'name' in data_attrs
        assert data_attrs['name'] == 'test'
        assert 'public_method' not in data_attrs
    
    def test_filter_by_type_method(self) -> None:
        """Test filtering by method type."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        method_attrs = inspector.filter_by_type('method')
        
        assert 'public_method' in method_attrs
        assert callable(method_attrs['public_method'])
    
    def test_filter_by_type_property(self) -> None:
        """Test filtering by property type."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        prop_attrs = inspector.filter_by_type('property')
        
        assert 'computed' in prop_attrs
        assert prop_attrs['computed'] == 84
    
    def test_filter_by_type_all(self) -> None:
        """Test filtering with 'all' kind."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        all_attrs = inspector.filter_by_type('all')
        
        assert 'name' in all_attrs
        assert 'public_method' in all_attrs
        assert 'computed' in all_attrs
    
    def test_find_by_pattern(self) -> None:
        """Test finding attributes by pattern."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        matches = inspector.find_by_pattern('method')
        
        assert 'public_method' in matches
    
    def test_find_by_pattern_no_matches(self) -> None:
        """Test finding attributes with no matches."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        matches = inspector.find_by_pattern('xyz_nonexistent')
        
        assert matches == {}
    
    def test_compare_with_same_object(self) -> None:
        """Test comparing an object with itself."""
        obj = SampleClass("test", 42)
        inspector = ObjectInspector(obj)
        
        result = inspector.compare_with(obj)
        
        assert result['only_in_self'] == {}
        assert result['only_in_other'] == {}
        assert result['different'] == {}
        assert 'name' in result['same']
    
    def test_compare_with_different_objects(self) -> None:
        """Test comparing different objects."""
        obj1 = SampleClass("first", 42)
        obj2 = SampleClass("second", 100)
        
        inspector = ObjectInspector(obj1)
        result = inspector.compare_with(obj2)
        
        # 'name' should be different
        assert 'name' in result['different']
        assert result['different']['name'] == ('first', 'second')
        
        # '_private' should be different
        assert '_private' in result['different']
    
    def test_compare_with_different_classes(self) -> None:
        """Test comparing objects of different classes."""
        obj1 = SampleClass("test", 42)
        obj2 = EmptyClass()
        
        inspector = ObjectInspector(obj1)
        result = inspector.compare_with(obj2)
        
        # Should have attributes only in self
        assert 'name' in result['only_in_self']
        assert 'public_method' in result['only_in_self']
    
    def test_with_builtin_types(self) -> None:
        """Test inspector works with built-in types."""
        inspector = ObjectInspector("hello")
        
        attrs = inspector.list_attributes()
        
        # String should have methods like upper, lower
        assert 'upper' in attrs
        assert 'lower' in attrs
        # Built-in methods are classified as 'callable' since they're not Python methods
        assert attrs['upper']['kind'] in ('method', 'callable')
