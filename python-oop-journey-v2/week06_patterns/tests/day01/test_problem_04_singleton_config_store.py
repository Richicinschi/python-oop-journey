"""Tests for Problem 04: Singleton Config Store."""

from __future__ import annotations

import pytest
import threading
from typing import Any

from week06_patterns.solutions.day01.problem_04_singleton_config_store import (
    ConfigStore, AppConfig
)


class TestConfigStoreSingleton:
    """Tests for ConfigStore singleton behavior."""
    
    def setup_method(self) -> None:
        """Reset singleton before each test."""
        ConfigStore.reset_instance()
    
    def teardown_method(self) -> None:
        """Reset singleton after each test."""
        ConfigStore.reset_instance()
    
    def test_singleton_returns_same_instance(self) -> None:
        store1 = ConfigStore()
        store2 = ConfigStore()
        assert store1 is store2
    
    def test_singleton_identity(self) -> None:
        store1 = ConfigStore()
        store2 = ConfigStore()
        assert id(store1) == id(store2)
    
    def test_changes_visible_across_references(self) -> None:
        store1 = ConfigStore()
        store1.set("key1", "value1")
        
        store2 = ConfigStore()
        assert store2.get("key1") == "value1"
    
    def test_reset_creates_new_instance(self) -> None:
        store1 = ConfigStore()
        store1.set("key", "value")
        
        ConfigStore.reset_instance()
        store2 = ConfigStore()
        
        assert store1 is not store2
        assert store2.get("key") is None


class TestConfigStoreOperations:
    """Tests for ConfigStore operations."""
    
    def setup_method(self) -> None:
        ConfigStore.reset_instance()
    
    def teardown_method(self) -> None:
        ConfigStore.reset_instance()
    
    def test_set_and_get(self) -> None:
        store = ConfigStore()
        store.set("name", "test")
        assert store.get("name") == "test"
    
    def test_get_with_default(self) -> None:
        store = ConfigStore()
        assert store.get("missing", "default") == "default"
    
    def test_get_without_default(self) -> None:
        store = ConfigStore()
        assert store.get("missing") is None
    
    def test_has_existing_key(self) -> None:
        store = ConfigStore()
        store.set("key", "value")
        assert store.has("key") is True
    
    def test_has_missing_key(self) -> None:
        store = ConfigStore()
        assert store.has("missing") is False
    
    def test_delete_existing_key(self) -> None:
        store = ConfigStore()
        store.set("key", "value")
        store.delete("key")
        assert store.has("key") is False
    
    def test_delete_missing_key(self) -> None:
        store = ConfigStore()
        store.delete("missing")  # Should not raise
        assert store.has("missing") is False
    
    def test_clear(self) -> None:
        store = ConfigStore()
        store.set("key1", "value1")
        store.set("key2", "value2")
        store.clear()
        assert store.keys() == []
    
    def test_keys(self) -> None:
        store = ConfigStore()
        store.set("b", 2)
        store.set("a", 1)
        keys = store.keys()
        assert "a" in keys
        assert "b" in keys
    
    def test_load_from_dict(self) -> None:
        store = ConfigStore()
        store.load_from_dict({"a": 1, "b": 2})
        assert store.get("a") == 1
        assert store.get("b") == 2
    
    def test_to_dict(self) -> None:
        store = ConfigStore()
        store.set("a", 1)
        store.set("b", 2)
        config = store.to_dict()
        assert config == {"a": 1, "b": 2}
    
    def test_to_dict_returns_copy(self) -> None:
        store = ConfigStore()
        store.set("key", "value")
        config = store.to_dict()
        config["key"] = "modified"
        assert store.get("key") == "value"


class TestConfigStoreTypes:
    """Tests for ConfigStore with various types."""
    
    def setup_method(self) -> None:
        ConfigStore.reset_instance()
    
    def teardown_method(self) -> None:
        ConfigStore.reset_instance()
    
    def test_string_value(self) -> None:
        store = ConfigStore()
        store.set("key", "string")
        assert store.get("key") == "string"
    
    def test_int_value(self) -> None:
        store = ConfigStore()
        store.set("key", 42)
        assert store.get("key") == 42
    
    def test_bool_value(self) -> None:
        store = ConfigStore()
        store.set("key", True)
        assert store.get("key") is True
    
    def test_list_value(self) -> None:
        store = ConfigStore()
        store.set("key", [1, 2, 3])
        assert store.get("key") == [1, 2, 3]
    
    def test_dict_value(self) -> None:
        store = ConfigStore()
        store.set("key", {"nested": "value"})
        assert store.get("key") == {"nested": "value"}


class TestConfigStoreThreadSafety:
    """Tests for ConfigStore thread safety."""
    
    def setup_method(self) -> None:
        ConfigStore.reset_instance()
    
    def teardown_method(self) -> None:
        ConfigStore.reset_instance()
    
    def test_thread_safe_singleton_creation(self) -> None:
        """Test that singleton is thread-safe during creation."""
        instances: list[ConfigStore] = []
        
        def create_instance() -> None:
            instance = ConfigStore()
            instances.append(instance)
        
        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # All instances should be the same object
        assert len(set(id(i) for i in instances)) == 1
    
    def test_concurrent_access(self) -> None:
        """Test that concurrent access works correctly."""
        store = ConfigStore()
        errors: list[Exception] = []
        
        def writer(thread_id: int) -> None:
            try:
                for i in range(100):
                    store.set(f"thread_{thread_id}_key_{i}", i)
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=writer, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(errors) == 0
        assert len(store.keys()) == 500


class TestAppConfig:
    """Tests for AppConfig alternative implementation."""
    
    def setup_method(self) -> None:
        AppConfig.reset_instance()
    
    def teardown_method(self) -> None:
        AppConfig.reset_instance()
    
    def test_get_instance_returns_same_instance(self) -> None:
        config1 = AppConfig.get_instance()
        config2 = AppConfig.get_instance()
        assert config1 is config2
    
    def test_database_url(self) -> None:
        config = AppConfig.get_instance()
        config.set_database_url("postgresql://localhost/db")
        assert config.get_database_url() == "postgresql://localhost/db"
    
    def test_debug_mode(self) -> None:
        config = AppConfig.get_instance()
        assert config.is_debug_mode() is False
        config.set_debug_mode(True)
        assert config.is_debug_mode() is True
    
    def test_changes_persist_across_get_instance_calls(self) -> None:
        config1 = AppConfig.get_instance()
        config1.set_database_url("test://url")
        
        config2 = AppConfig.get_instance()
        assert config2.get_database_url() == "test://url"
    
    def test_reset_creates_new_instance(self) -> None:
        config1 = AppConfig.get_instance()
        config1.set_database_url("test://url")
        
        AppConfig.reset_instance()
        config2 = AppConfig.get_instance()
        
        assert config1 is not config2
        assert config2.get_database_url() == ""
