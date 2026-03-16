"""Reference solution for Problem 05: Prototype Document Clone."""

from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Self, Any
from datetime import datetime


class Prototype(ABC):
    """Prototype interface."""
    
    @abstractmethod
    def clone(self) -> Self:
        """Create a deep copy of the object."""
        pass


class Document(Prototype):
    """Concrete prototype: Document."""
    
    def __init__(self, title: str, content: str, author: str) -> None:
        self.title = title
        self.content = content
        self.author = author
        self.created_at = datetime.now()
        self.metadata: dict[str, Any] = {}
    
    def clone(self) -> Self:
        """Create a deep copy of the document."""
        return deepcopy(self)
    
    def update_title(self, new_title: str) -> None:
        """Update the document title."""
        self.title = new_title
    
    def update_content(self, new_content: str) -> None:
        """Update the document content."""
        self.content = new_content
    
    def update_author(self, new_author: str) -> None:
        """Update the document author."""
        self.author = new_author
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the document."""
        self.metadata[key] = value
    
    def get_metadata(self, key: str) -> Any:
        """Get metadata value."""
        return self.metadata.get(key)
    
    def __str__(self) -> str:
        """Return string representation."""
        return f"'{self.title}' by {self.author}"
    
    def to_dict(self) -> dict[str, Any]:
        """Convert document to dictionary."""
        return {
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "created_at": self.created_at,
            "metadata": self.metadata.copy(),
        }


class Report(Document):
    """Specialized document: Report."""
    
    def __init__(self, title: str, content: str, author: str, report_type: str) -> None:
        super().__init__(title, content, author)
        self.report_type = report_type
        self.department = ""
    
    def clone(self) -> Self:
        """Create a deep copy of the report."""
        return deepcopy(self)
    
    def set_department(self, department: str) -> None:
        """Set the department for this report."""
        self.department = department
    
    def get_department(self) -> str:
        """Get the department."""
        return self.department


class Contract(Document):
    """Specialized document: Contract."""
    
    def __init__(self, title: str, content: str, author: str, parties: list[str]) -> None:
        super().__init__(title, content, author)
        self.parties = parties.copy()
    
    def clone(self) -> Self:
        """Create a deep copy of the contract."""
        return deepcopy(self)
    
    def add_party(self, party: str) -> None:
        """Add a party to the contract."""
        self.parties.append(party)
    
    def get_parties(self) -> list[str]:
        """Get all parties."""
        return self.parties.copy()


class DocumentRegistry:
    """Registry for document prototypes."""
    
    def __init__(self) -> None:
        self._prototypes: dict[str, Prototype] = {}
    
    def register(self, name: str, document: Prototype) -> None:
        """Register a document prototype (stores a copy)."""
        self._prototypes[name] = document.clone()
    
    def unregister(self, name: str) -> None:
        """Unregister a document prototype."""
        if name in self._prototypes:
            del self._prototypes[name]
    
    def create(self, name: str) -> Prototype:
        """Create a clone of a registered prototype."""
        if name not in self._prototypes:
            raise KeyError(f"Prototype '{name}' not found")
        return self._prototypes[name].clone()
    
    def is_registered(self, name: str) -> bool:
        """Check if a name is registered."""
        return name in self._prototypes
    
    def list_prototypes(self) -> list[str]:
        """List all registered prototype names."""
        return list(self._prototypes.keys())
