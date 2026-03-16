"""Reference solution for Problem 03: Composite File Tree."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class FileSystemComponent(ABC):
    """Component interface - common interface for files and directories."""
    
    def __init__(self, name: str) -> None:
        self._name = name
    
    @property
    def name(self) -> str:
        """Return the component's name."""
        return self._name
    
    @property
    @abstractmethod
    def size(self) -> int:
        """Return the component's size in bytes."""
        pass
    
    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """Return a string representation of this component."""
        pass
    
    @abstractmethod
    def search(self, keyword: str) -> list[str]:
        """Search for components matching the keyword."""
        pass


class File(FileSystemComponent):
    """Leaf - represents a file in the file system."""
    
    def __init__(self, name: str, size: int, created: datetime | None = None) -> None:
        super().__init__(name)
        self._size = size
        self._created = created or datetime.now()
    
    @property
    def size(self) -> int:
        """Return the file size."""
        return self._size
    
    @property
    def created(self) -> datetime:
        """Return the file creation time."""
        return self._created
    
    def display(self, indent: int = 0) -> str:
        """Display file with size."""
        spaces = "  " * indent
        return f"{spaces}[FILE] {self._name} ({self._size} bytes)"
    
    def search(self, keyword: str) -> list[str]:
        """Return [name] if keyword in name, else empty list."""
        if keyword.lower() in self._name.lower():
            return [self._name]
        return []


class Directory(FileSystemComponent):
    """Composite - represents a directory that can contain files and subdirectories."""
    
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._children: list[FileSystemComponent] = []
    
    @property
    def size(self) -> int:
        """Return total size of all children."""
        return sum(child.size for child in self._children)
    
    def add(self, component: FileSystemComponent) -> None:
        """Add a child component to this directory."""
        self._children.append(component)
    
    def remove(self, component: FileSystemComponent) -> None:
        """Remove a child component from this directory."""
        if component in self._children:
            self._children.remove(component)
    
    def get_children(self) -> list[FileSystemComponent]:
        """Return a copy of the children list."""
        return self._children.copy()
    
    def display(self, indent: int = 0) -> str:
        """Display directory and all children recursively."""
        spaces = "  " * indent
        lines = [f"{spaces}[DIR] {self._name}/"]
        for child in self._children:
            lines.append(child.display(indent + 1))
        return "\n".join(lines)
    
    def search(self, keyword: str) -> list[str]:
        """Search in this directory and all children."""
        results: list[str] = []
        if keyword.lower() in self._name.lower():
            results.append(self._name)
        for child in self._children:
            results.extend(child.search(keyword))
        return results
    
    def count_files(self) -> int:
        """Count total number of files in this directory and subdirectories."""
        count = 0
        for child in self._children:
            if isinstance(child, File):
                count += 1
            elif isinstance(child, Directory):
                count += child.count_files()
        return count
    
    def count_directories(self) -> int:
        """Count total number of directories (including self) in this subtree."""
        count = 1  # Count self
        for child in self._children:
            if isinstance(child, Directory):
                count += child.count_directories()
        return count


class FileSystemBuilder:
    """Builder utility for constructing file system trees."""
    
    def __init__(self, root_name: str = "root") -> None:
        self._root = Directory(root_name)
    
    def add_file(self, path: str, size: int) -> FileSystemBuilder:
        """Add a file at the specified path."""
        parts = path.split("/")
        current = self._root
        
        # Navigate/create directories
        for part in parts[:-1]:
            found = None
            for child in current.get_children():
                if child.name == part and isinstance(child, Directory):
                    found = child
                    break
            if found is None:
                new_dir = Directory(part)
                current.add(new_dir)
                found = new_dir
            current = found
        
        # Add file
        current.add(File(parts[-1], size))
        return self
    
    def build(self) -> Directory:
        """Return the constructed file system root."""
        return self._root


def create_sample_file_system() -> Directory:
    """Create a sample file system for testing."""
    root = Directory("root")
    
    # documents/
    documents = Directory("documents")
    documents.add(File("resume.pdf", 4500))
    documents.add(File("cover_letter.txt", 1200))
    root.add(documents)
    
    # photos/
    photos = Directory("photos")
    vacation = Directory("vacation")
    vacation.add(File("beach.jpg", 2048))
    vacation.add(File("mountain.jpg", 3072))
    photos.add(vacation)
    photos.add(File("portrait.png", 1536))
    root.add(photos)
    
    # readme.txt at root
    root.add(File("readme.txt", 512))
    
    return root
