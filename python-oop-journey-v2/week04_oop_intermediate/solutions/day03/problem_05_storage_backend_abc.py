"""Solution for Problem 05: Storage Backend ABC.

Demonstrates CRUD operations as abstract methods with concrete implementations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional
from pathlib import Path
import json
import os


class StorageBackend(ABC):
    """Abstract base class for storage backends.
    
    Provides a uniform interface for different storage mechanisms.
    """
    
    @property
    @abstractmethod
    def backend_name(self) -> str:
        """Return the name of this storage backend."""
        pass
    
    @abstractmethod
    def save(self, key: str, data: dict[str, Any]) -> bool:
        """Save data to storage.
        
        Args:
            key: Unique identifier for the data.
            data: Dictionary of data to store.
        
        Returns:
            True if save was successful, False otherwise.
        """
        pass
    
    @abstractmethod
    def load(self, key: str) -> Optional[dict[str, Any]]:
        """Load data from storage.
        
        Args:
            key: Unique identifier for the data.
        
        Returns:
            The stored data dictionary, or None if not found.
        """
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete data from storage.
        
        Args:
            key: Unique identifier for the data.
        
        Returns:
            True if deletion was successful or key didn't exist.
        """
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists in storage.
        
        Args:
            key: Unique identifier for the data.
        
        Returns:
            True if key exists, False otherwise.
        """
        pass


class InMemoryStorage(StorageBackend):
    """In-memory storage using dictionaries.
    
    Attributes:
        _data: Dictionary storing all data.
    """
    
    def __init__(self) -> None:
        """Initialize in-memory storage."""
        self._data: dict[str, dict[str, Any]] = {}
    
    @property
    def backend_name(self) -> str:
        """Return backend name."""
        return "in_memory"
    
    def save(self, key: str, data: dict[str, Any]) -> bool:
        """Save data to memory."""
        self._data[key] = data.copy()
        return True
    
    def load(self, key: str) -> Optional[dict[str, Any]]:
        """Load data from memory."""
        result = self._data.get(key)
        return result.copy() if result is not None else None
    
    def delete(self, key: str) -> bool:
        """Delete data from memory."""
        if key in self._data:
            del self._data[key]
        return True
    
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        return key in self._data
    
    def clear(self) -> None:
        """Clear all data from memory."""
        self._data.clear()


class FileStorage(StorageBackend):
    """File-based storage using JSON files.
    
    Attributes:
        base_path: Directory path for storing files.
    """
    
    def __init__(self, base_path: str | Path) -> None:
        """Initialize file storage.
        
        Args:
            base_path: Directory path for storing files.
        
        Raises:
            ValueError: If base_path is not a valid directory.
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    @property
    def backend_name(self) -> str:
        """Return backend name."""
        return "file"
    
    def _get_file_path(self, key: str) -> Path:
        """Get file path for a key."""
        return self.base_path / f"{key}.json"
    
    def save(self, key: str, data: dict[str, Any]) -> bool:
        """Save data to file."""
        try:
            file_path = self._get_file_path(key)
            with open(file_path, "w") as f:
                json.dump(data, f)
            return True
        except (IOError, TypeError):
            return False
    
    def load(self, key: str) -> Optional[dict[str, Any]]:
        """Load data from file."""
        file_path = self._get_file_path(key)
        if not file_path.exists():
            return None
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return None
    
    def delete(self, key: str) -> bool:
        """Delete file."""
        file_path = self._get_file_path(key)
        if file_path.exists():
            file_path.unlink()
        return True
    
    def exists(self, key: str) -> bool:
        """Check if file exists."""
        return self._get_file_path(key).exists()
