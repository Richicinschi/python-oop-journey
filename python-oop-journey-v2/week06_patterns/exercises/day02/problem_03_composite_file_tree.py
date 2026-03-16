"""Problem 03: Composite File Tree

Topic: Composite Pattern
Difficulty: Medium

Implement a file system tree structure using the Composite pattern.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class FileSystemComponent(ABC):
    """Component interface - common interface for files and directories.
    
    This interface allows clients to treat files and directories uniformly.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize with a name.
        
        Args:
            name: The name of this component
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the component's name."""
        raise NotImplementedError("Implement name")
    
    @property
    @abstractmethod
    def size(self) -> int:
        """Return the component's size in bytes.
        
        For files: the actual file size.
        For directories: sum of all children's sizes.
        """
        raise NotImplementedError("Implement size")
    
    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """Return a string representation of this component.
        
        Args:
            indent: Number of spaces to indent for tree visualization
            
        Returns:
            Formatted string showing the component
        """
        raise NotImplementedError("Implement display")
    
    @abstractmethod
    def search(self, keyword: str) -> list[str]:
        """Search for components matching the keyword.
        
        Args:
            keyword: The search term to look for in names
            
        Returns:
            List of matching component paths
        """
        raise NotImplementedError("Implement search")


class File(FileSystemComponent):
    """Leaf - represents a file in the file system.
    
    Cannot contain other components.
    """
    
    def __init__(self, name: str, size: int, created: datetime | None = None) -> None:
        """Initialize a file.
        
        Args:
            name: File name
            size: File size in bytes
            created: Creation date/time (defaults to now)
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def name(self) -> str:
        """Return the file name."""
        raise NotImplementedError("Implement name")
    
    @property
    def size(self) -> int:
        """Return the file size."""
        raise NotImplementedError("Implement size")
    
    @property
    def created(self) -> datetime:
        """Return the file creation time."""
        raise NotImplementedError("Implement created")
    
    def display(self, indent: int = 0) -> str:
        """Display file with size.
        
        Format: "  [FILE] name (size bytes)"
        """
        raise NotImplementedError("Implement display")
    
    def search(self, keyword: str) -> list[str]:
        """Return [name] if keyword in name, else empty list."""
        raise NotImplementedError("Implement search")


class Directory(FileSystemComponent):
    """Composite - represents a directory that can contain files and subdirectories.
    
    Can contain other FileSystemComponents (both Files and Directories).
    """
    
    def __init__(self, name: str) -> None:
        """Initialize an empty directory.
        
        Args:
            name: Directory name
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def name(self) -> str:
        """Return the directory name."""
        raise NotImplementedError("Implement name")
    
    @property
    def size(self) -> int:
        """Return total size of all children."""
        raise NotImplementedError("Implement size")
    
    def add(self, component: FileSystemComponent) -> None:
        """Add a child component to this directory.
        
        Args:
            component: The File or Directory to add
        """
        raise NotImplementedError("Implement add")
    
    def remove(self, component: FileSystemComponent) -> None:
        """Remove a child component from this directory.
        
        Args:
            component: The component to remove
        """
        raise NotImplementedError("Implement remove")
    
    def get_children(self) -> list[FileSystemComponent]:
        """Return a copy of the children list."""
        raise NotImplementedError("Implement get_children")
    
    def display(self, indent: int = 0) -> str:
        """Display directory and all children recursively.
        
        Format:
          [DIR] name/
            [FILE] child1 (size bytes)
            [DIR] child2/
              ...
        """
        raise NotImplementedError("Implement display")
    
    def search(self, keyword: str) -> list[str]:
        """Search in this directory and all children.
        
        Returns paths of matching components.
        """
        raise NotImplementedError("Implement search")
    
    def count_files(self) -> int:
        """Count total number of files in this directory and subdirectories."""
        raise NotImplementedError("Implement count_files")
    
    def count_directories(self) -> int:
        """Count total number of directories (including self) in this subtree."""
        raise NotImplementedError("Implement count_directories")


class FileSystemBuilder:
    """Builder utility for constructing file system trees.
    
    Provides a convenient way to build complex file structures.
    """
    
    def __init__(self, root_name: str = "root") -> None:
        """Initialize with a root directory.
        
        Args:
            root_name: Name of the root directory
        """
        raise NotImplementedError("Implement __init__")
    
    def add_file(self, path: str, size: int) -> FileSystemBuilder:
        """Add a file at the specified path.
        
        Args:
            path: Path like "dir1/dir2/file.txt"
            size: File size in bytes
            
        Returns:
            self for chaining
        """
        raise NotImplementedError("Implement add_file")
    
    def build(self) -> Directory:
        """Return the constructed file system root."""
        raise NotImplementedError("Implement build")


def create_sample_file_system() -> Directory:
    """Create a sample file system for testing.
    
    Creates this structure:
    root/
      documents/
        resume.pdf (4500)
        cover_letter.txt (1200)
      photos/
        vacation/
          beach.jpg (2048)
          mountain.jpg (3072)
        portrait.png (1536)
      readme.txt (512)
    
    Returns:
        The root directory
    """
    raise NotImplementedError("Implement create_sample_file_system")
