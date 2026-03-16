"""Tests for Problem 05: Storage Backend ABC."""

from __future__ import annotations

import pytest
import tempfile
from abc import ABC
from pathlib import Path

from week04_oop_intermediate.solutions.day03.problem_05_storage_backend_abc import (
    StorageBackend,
    InMemoryStorage,
    FileStorage,
)


class TestStorageBackendABC:
    """Test suite for StorageBackend abstract base class."""
    
    def test_storage_backend_is_abstract(self) -> None:
        """Test that StorageBackend cannot be instantiated."""
        assert issubclass(StorageBackend, ABC)
        with pytest.raises(TypeError, match="abstract"):
            StorageBackend()
    
    def test_storage_backend_has_abstract_backend_name(self) -> None:
        """Test that StorageBackend defines abstract backend_name property."""
        assert hasattr(StorageBackend, 'backend_name')
    
    def test_storage_backend_has_abstract_methods(self) -> None:
        """Test that StorageBackend defines abstract methods."""
        assert hasattr(StorageBackend, 'save')
        assert hasattr(StorageBackend, 'load')
        assert hasattr(StorageBackend, 'delete')
        assert hasattr(StorageBackend, 'exists')


class TestInMemoryStorage:
    """Test suite for InMemoryStorage."""
    
    def test_backend_name(self) -> None:
        """Test backend_name property."""
        storage = InMemoryStorage()
        assert storage.backend_name == "in_memory"
    
    def test_save_and_load(self) -> None:
        """Test saving and loading data."""
        storage = InMemoryStorage()
        data = {"name": "Alice", "age": 30}
        assert storage.save("user1", data) is True
        
        loaded = storage.load("user1")
        assert loaded == data
    
    def test_load_nonexistent_key(self) -> None:
        """Test loading non-existent key returns None."""
        storage = InMemoryStorage()
        assert storage.load("nonexistent") is None
    
    def test_exists(self) -> None:
        """Test exists method."""
        storage = InMemoryStorage()
        assert storage.exists("key1") is False
        storage.save("key1", {"data": "value"})
        assert storage.exists("key1") is True
    
    def test_delete_existing_key(self) -> None:
        """Test deleting existing key."""
        storage = InMemoryStorage()
        storage.save("key1", {"data": "value"})
        assert storage.exists("key1") is True
        assert storage.delete("key1") is True
        assert storage.exists("key1") is False
    
    def test_delete_nonexistent_key(self) -> None:
        """Test deleting non-existent key returns True."""
        storage = InMemoryStorage()
        assert storage.delete("nonexistent") is True
    
    def test_clear(self) -> None:
        """Test clearing all data."""
        storage = InMemoryStorage()
        storage.save("key1", {"data": "1"})
        storage.save("key2", {"data": "2"})
        assert storage.exists("key1")
        assert storage.exists("key2")
        
        storage.clear()
        assert storage.exists("key1") is False
        assert storage.exists("key2") is False
    
    def test_save_overwrites_existing(self) -> None:
        """Test saving overwrites existing data."""
        storage = InMemoryStorage()
        storage.save("key1", {"data": "old"})
        storage.save("key1", {"data": "new"})
        
        loaded = storage.load("key1")
        assert loaded == {"data": "new"}
    
    def test_load_returns_copy(self) -> None:
        """Test that load returns a copy, not reference."""
        storage = InMemoryStorage()
        original = {"data": "value", "nested": {"key": "val"}}
        storage.save("key1", original)
        
        loaded = storage.load("key1")
        loaded["data"] = "modified"
        loaded["nested"]["key"] = "modified"
        
        # Original stored data should be unchanged
        reloaded = storage.load("key1")
        assert reloaded["data"] == "value"


class TestFileStorage:
    """Test suite for FileStorage."""
    
    def test_backend_name(self) -> None:
        """Test backend_name property."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = FileStorage(tmpdir)
            assert storage.backend_name == "file"
    
    def test_initialization_creates_directory(self) -> None:
        """Test that initialization creates directory if needed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = Path(tmpdir) / "new_subdir"
            assert not new_dir.exists()
            FileStorage(new_dir)
            assert new_dir.exists()
    
    def test_save_and_load(self) -> None:
        """Test saving and loading data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = FileStorage(tmpdir)
            data = {"name": "Alice", "age": 30}
            assert storage.save("user1", data) is True
            
            loaded = storage.load("user1")
            assert loaded == data
    
    def test_load_nonexistent_key(self) -> None:
        """Test loading non-existent key returns None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = FileStorage(tmpdir)
            assert storage.load("nonexistent") is None
    
    def test_exists(self) -> None:
        """Test exists method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = FileStorage(tmpdir)
            assert storage.exists("key1") is False
            storage.save("key1", {"data": "value"})
            assert storage.exists("key1") is True
    
    def test_delete_existing_key(self) -> None:
        """Test deleting existing key."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = FileStorage(tmpdir)
            storage.save("key1", {"data": "value"})
            assert storage.exists("key1") is True
            assert storage.delete("key1") is True
            assert storage.exists("key1") is False
    
    def test_delete_nonexistent_key(self) -> None:
        """Test deleting non-existent key returns True."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = FileStorage(tmpdir)
            assert storage.delete("nonexistent") is True
    
    def test_save_overwrites_existing(self) -> None:
        """Test saving overwrites existing data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = FileStorage(tmpdir)
            storage.save("key1", {"data": "old"})
            storage.save("key1", {"data": "new"})
            
            loaded = storage.load("key1")
            assert loaded == {"data": "new"}
    
    def test_file_created_with_json_extension(self) -> None:
        """Test that files are created with .json extension."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = FileStorage(tmpdir)
            storage.save("test_key", {"data": "value"})
            
            file_path = Path(tmpdir) / "test_key.json"
            assert file_path.exists()
