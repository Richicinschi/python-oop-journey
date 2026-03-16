"""Tests for Problem 06: Singleton Decorator."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day03.problem_06_singleton_decorator import (
    singleton, Database, Configuration
)


class TestSingletonDecorator:
    """Tests for the singleton decorator."""
    
    def test_singleton_returns_same_instance(self) -> None:
        """Test that singleton returns the same instance."""
        db1 = Database()
        db2 = Database()
        
        assert db1 is db2
    
    def test_singleton_instance_shares_state(self) -> None:
        """Test that singleton instances share state."""
        db1 = Database()
        db1.connected = True
        
        db2 = Database()
        assert db2.connected is True
    
    def test_singleton_constructor_called_once(self) -> None:
        """Test that __init__ is called only once."""
        # Reset by creating fresh singleton test
        
        call_count = 0
        
        @singleton
        class Counter:
            def __init__(self) -> None:
                nonlocal call_count
                call_count += 1
                self.value = call_count
        
        c1 = Counter()
        c2 = Counter()
        c3 = Counter()
        
        assert call_count == 1
        assert c1.value == c2.value == c3.value == 1
    
    def test_singleton_configuration(self) -> None:
        """Test singleton with Configuration class."""
        config1 = Configuration()
        config1.set("debug", True)
        config1.set("timeout", 30)
        
        config2 = Configuration()
        
        assert config1 is config2
        assert config2.get("debug") is True
        assert config2.get("timeout") == 30
    
    def test_singleton_preserves_class_methods(self) -> None:
        """Test that singleton preserves class methods."""
        # Note: Due to singleton pattern, first instantiation wins
        # Create a fresh singleton instance
        import sys
        # We can't easily reset the singleton, so we just verify methods work
        db = Database()
        
        assert db.connect().startswith("Connected to")
        assert db.disconnect() == "Disconnected"


class TestSingletonEdgeCases:
    """Tests for singleton edge cases."""
    
    def test_singleton_with_different_args_ignores_them(self) -> None:
        """Test that singleton ignores args after first instantiation."""
        # Note: Due to previous tests, singleton is already instantiated
        # We just verify that the singleton returns the same instance
        db1 = Database("first")
        db2 = Database("second")
        
        # Both should be the same instance
        assert db1 is db2
    
    def test_singleton_multiple_classes(self) -> None:
        """Test that different classes have separate singletons."""
        db = Database()
        config = Configuration()
        
        assert db is not config  # Different singletons
        
        db2 = Database()
        config2 = Configuration()
        
        assert db is db2
        assert config is config2
