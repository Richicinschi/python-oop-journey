"""Tests for Problem 01: Singleton Metaclass."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day02.problem_01_singleton_meta import (
    CacheManager,
    Database,
    SingletonMeta,
)


class TestSingletonMeta:
    """Tests for the SingletonMeta metaclass."""
    
    def test_metaclass_exists(self) -> None:
        """Test that SingletonMeta is defined."""
        assert isinstance(SingletonMeta, type)
        assert SingletonMeta.__name__ == 'SingletonMeta'
    
    def test_singleton_same_instance(self) -> None:
        """Test that multiple instantiations return same instance."""
        db1 = Database()
        db2 = Database()
        assert db1 is db2
    
    def test_different_classes_different_singletons(self) -> None:
        """Test that each class has its own singleton."""
        db = Database()
        cache = CacheManager()
        assert db is not cache
        # Verify they're the correct types
        assert isinstance(db, Database)
        assert isinstance(cache, CacheManager)
    
    def test_singleton_state_shared(self) -> None:
        """Test that state is shared across references."""
        # Clear registry to ensure first instantiation wins
        SingletonMeta._instances.pop(Database, None)
        
        db1 = Database("connection1")
        db2 = Database()  # Should return same instance
        
        # They should be the same object
        assert db1 is db2
        # Connection string from first instantiation persists
        assert db2.connection_string == "connection1"
    
    def test_singleton_with_keyword_args(self) -> None:
        """Test singleton works with keyword arguments."""
        # Clear registry to ensure first instantiation wins
        SingletonMeta._instances.pop(Database, None)
        
        db1 = Database(connection_string="custom")
        db2 = Database(connection_string="ignored")  # Should return first instance
        
        assert db1 is db2
        assert db2.connection_string == "custom"


class TestDatabase:
    """Tests for the Database singleton class."""
    
    def test_database_init(self) -> None:
        """Test Database initialization."""
        # Clear any existing instance for clean test
        SingletonMeta._instances.pop(Database, None)
        
        db = Database("test_connection")
        assert db.connection_string == "test_connection"
        assert db.is_connected is False
    
    def test_database_connect(self) -> None:
        """Test Database connect method."""
        SingletonMeta._instances.pop(Database, None)
        
        db = Database()
        result = db.connect()
        assert "Connected" in result
        assert db.is_connected is True
    
    def test_database_query(self) -> None:
        """Test Database query method."""
        SingletonMeta._instances.pop(Database, None)
        
        db = Database()
        # Before connect, query should fail
        result = db.query("SELECT *")
        assert "Error" in result
        
        db.connect()
        result = db.query("SELECT *")
        assert "Query result" in result


class TestCacheManager:
    """Tests for the CacheManager singleton class."""
    
    def test_cache_manager_init(self) -> None:
        """Test CacheManager initialization."""
        SingletonMeta._instances.pop(CacheManager, None)
        
        cache = CacheManager(50)
        assert cache.max_size == 50
        assert cache.get("key") is None
    
    def test_cache_manager_set_get(self) -> None:
        """Test CacheManager set and get methods."""
        SingletonMeta._instances.pop(CacheManager, None)
        
        cache = CacheManager()
        assert cache.set("key1", "value1") is True
        assert cache.get("key1") == "value1"
    
    def test_cache_manager_max_size(self) -> None:
        """Test CacheManager respects max size."""
        SingletonMeta._instances.pop(CacheManager, None)
        
        cache = CacheManager(2)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        # Third item should fail (at capacity)
        assert cache.set("key3", "value3") is False
        
        # Original items should still be there
        assert cache.get("key1") == "value1"
        assert cache.get("key2") == "value2"
    
    def test_cache_manager_update_existing(self) -> None:
        """Test updating existing keys doesn't count against limit."""
        SingletonMeta._instances.pop(CacheManager, None)
        
        cache = CacheManager(1)
        cache.set("key1", "value1")
        cache.set("key1", "updated")  # Update existing
        
        assert cache.get("key1") == "updated"
