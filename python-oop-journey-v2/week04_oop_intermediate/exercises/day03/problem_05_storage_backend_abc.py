"""Exercise: Storage Backend ABC.

Create an abstract base class for storage backends with CRUD operations.

TODO:
1. Create StorageBackend ABC with abstract methods save, load, delete, exists
2. Add abstract property backend_name -> str
3. Implement InMemoryStorage using dictionaries
4. Implement FileStorage using file system
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
        # TODO: Define abstract property
        raise NotImplementedError("backend_name property must be implemented")
    
    @abstractmethod
    def save(self, key: str, data: dict[str, Any]) -> bool:
        """Save data to storage.
        
        Args:
            key: Unique identifier for the data.
            data: Dictionary of data to store.
        
        Returns:
            True if save was successful, False otherwise.
        """
        # TODO: Implement abstract method
        raise NotImplementedError("save must be implemented")
    
    @abstractmethod
    def load(self, key: str) -> Optional[dict[str, Any]]:
        """Load data from storage.
        
        Args:
            key: Unique identifier for the data.
        
        Returns:
            The stored data dictionary, or None if not found.
        """
        # TODO: Implement abstract method
        raise NotImplementedError("load must be implemented")
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete data from storage.
        
        Args:
            key: Unique identifier for the data.
        
        Returns:
            True if deletion was successful or key didn't exist.
        """
        # TODO: Implement abstract method
        raise NotImplementedError("delete must be implemented")
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists in storage.
        
        Args:
            key: Unique identifier for the data.
        
        Returns:
            True if key exists, False otherwise.
        """
        # TODO: Implement abstract method
        raise NotImplementedError("exists must be implemented")


class InMemoryStorage(StorageBackend):
    """In-memory storage using dictionaries."""
    
    def __init__(self) -> None:
        """Initialize in-memory storage."""
        # TODO: Create empty dictionary for storage
        raise NotImplementedError("Initialize in-memory storage")
    
    @property
    def backend_name(self) -> str:
        """Return backend name."""
        # TODO: Return "in_memory"
        raise NotImplementedError("Return backend name")
    
    def save(self, key: str, data: dict[str, Any]) -> bool:
        """Save data to memory."""
        # TODO: Store data in dictionary
        raise NotImplementedError("Implement save")
    
    def load(self, key: str) -> Optional[dict[str, Any]]:
        """Load data from memory."""
        # TODO: Return data from dictionary or None
        raise NotImplementedError("Implement load")
    
    def delete(self, key: str) -> bool:
        """Delete data from memory."""
        # TODO: Remove key if exists, return True
        raise NotImplementedError("Implement delete")
    
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        # TODO: Return True if key in dictionary
        raise NotImplementedError("Implement exists")
    
    def clear(self) -> None:
        """Clear all data from memory."""
        # TODO: Clear the dictionary
        raise NotImplementedError("Implement clear")


class FileStorage(StorageBackend):
    """File-based storage using JSON files."""
    
    def __init__(self, base_path: str | Path) -> None:
        """Initialize file storage.
        
        Args:
            base_path: Directory path for storing files.
        
        Raises:
            ValueError: If base_path is not a valid directory.
        """
        # TODO: Validate and set base_path, create if doesn't exist
        raise NotImplementedError("Initialize file storage")
    
    @property
    def backend_name(self) -> str:
        """Return backend name."""
        # TODO: Return "file"
        raise NotImplementedError("Return backend name")
    
    def _get_file_path(self, key: str) -> Path:
        """Get file path for a key."""
        # TODO: Return base_path / f"{key}.json"
        raise NotImplementedError("Calculate file path")
    
    def save(self, key: str, data: dict[str, Any]) -> bool:
        """Save data to file."""
        # TODO: Write data as JSON to file
        raise NotImplementedError("Implement save")
    
    def load(self, key: str) -> Optional[dict[str, Any]]:
        """Load data from file."""
        # TODO: Read and parse JSON, return None if file doesn't exist
        raise NotImplementedError("Implement load")
    
    def delete(self, key: str) -> bool:
        """Delete file."""
        # TODO: Remove file if exists, return True
        raise NotImplementedError("Implement delete")
    
    def exists(self, key: str) -> bool:
        """Check if file exists."""
        # TODO: Return True if file exists
        raise NotImplementedError("Implement exists")
