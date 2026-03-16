"""Tests for Problem 06: Observable Attribute."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day01.problem_06_observable_attribute import (
    Observable, Stock, FormField
)


class TestObservable:
    """Tests for the Observable descriptor."""
    
    def test_basic_observable(self) -> None:
        class TestClass:
            value = Observable(0)
            
            def __init__(self) -> None:
                self.value = 10
        
        obj = TestClass()
        assert obj.value == 10
    
    def test_callback_called_on_change(self) -> None:
        callback_calls = []
        
        class TestClass:
            value = Observable(0)
            
            def __init__(self) -> None:
                self.value = 10
            
            def on_change(self, callback) -> None:
                type(self).value.add_callback(self, callback)
        
        obj = TestClass()
        obj.on_change(lambda inst, old, new: callback_calls.append((old, new)))
        
        obj.value = 20
        assert len(callback_calls) == 1
        assert callback_calls[0] == (10, 20)
    
    def test_callback_not_called_when_value_unchanged(self) -> None:
        callback_calls = []
        
        class TestClass:
            value = Observable(0)
            
            def __init__(self) -> None:
                self.value = 10
        
        obj = TestClass()
        TestClass.value.add_callback(obj, lambda inst, old, new: callback_calls.append((old, new)))
        
        obj.value = 10  # Same value
        assert len(callback_calls) == 0
    
    def test_multiple_callbacks(self) -> None:
        calls1 = []
        calls2 = []
        
        class TestClass:
            value = Observable(0)
            
            def __init__(self) -> None:
                self.value = 10
        
        obj = TestClass()
        TestClass.value.add_callback(obj, lambda inst, old, new: calls1.append(new))
        TestClass.value.add_callback(obj, lambda inst, old, new: calls2.append(new))
        
        obj.value = 20
        assert calls1 == [20]
        assert calls2 == [20]


class TestStock:
    """Tests for the Stock class."""
    
    def test_stock_creation(self) -> None:
        stock = Stock("AAPL", 150.0, 1000000)
        assert stock.symbol == "AAPL"
        assert stock.price == 150.0
        assert stock.volume == 1000000
    
    def test_price_change_callback(self) -> None:
        stock = Stock("AAPL", 150.0)
        price_changes = []
        
        stock.on_price_change(lambda inst, old, new: price_changes.append((old, new)))
        
        stock.price = 155.0
        assert price_changes == [(150.0, 155.0)]
    
    def test_volume_change_callback(self) -> None:
        stock = Stock("AAPL", 150.0, 1000)
        volume_changes = []
        
        stock.on_volume_change(lambda inst, old, new: volume_changes.append((old, new)))
        
        stock.volume = 2000
        assert volume_changes == [(1000, 2000)]
    
    def test_different_instances_independent(self) -> None:
        stock1 = Stock("AAPL", 150.0)
        stock2 = Stock("GOOGL", 2500.0)
        
        changes1 = []
        changes2 = []
        
        stock1.on_price_change(lambda inst, old, new: changes1.append(new))
        stock2.on_price_change(lambda inst, old, new: changes2.append(new))
        
        stock1.price = 155.0
        assert changes1 == [155.0]
        assert changes2 == []


class TestFormField:
    """Tests for the FormField class."""
    
    def test_field_creation(self) -> None:
        field = FormField("username", "Username", "john_doe")
        assert field.name == "username"
        assert field.label == "Username"
        assert field.value == "john_doe"
        assert field.dirty is False
    
    def test_value_change_callback(self) -> None:
        field = FormField("username", "Username")
        changes = []
        
        field.on_change(lambda inst, old, new: changes.append((old, new)))
        
        field.value = "jane_doe"
        assert changes == [(None, "jane_doe")]
    
    def test_clear_resets_field(self) -> None:
        field = FormField("username", "Username", "john_doe")
        field.dirty = True
        field.error = "Some error"
        
        field.clear()
        assert field.value is None
        assert field.error == ""
        assert field.dirty is False
    
    def test_is_valid_no_error(self) -> None:
        field = FormField("username", "Username", "john_doe")
        assert field.is_valid() is True
    
    def test_is_valid_with_error(self) -> None:
        field = FormField("username", "Username", "john_doe")
        field.error = "Invalid username"
        assert field.is_valid() is False
