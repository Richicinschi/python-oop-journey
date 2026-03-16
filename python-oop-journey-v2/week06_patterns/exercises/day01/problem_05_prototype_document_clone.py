"""Problem 05: Prototype Document Clone

Topic: Prototype Pattern
Difficulty: Medium

Implement the Prototype pattern to clone documents with various properties.
The pattern allows creating new objects by copying existing ones.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Self, Any
from datetime import datetime


class Prototype(ABC):
    """Prototype interface.
    
    Declares the clone method that all concrete prototypes must implement.
    """
    
    @abstractmethod
    def clone(self) -> Self:
        """Create a deep copy of the object.
        
        Returns:
            A deep copy of this object
        """
        raise NotImplementedError("Implement Prototype.clone")


class Document(Prototype):
    """Concrete prototype: Document.
    
    Represents a document that can be cloned to create new documents
    based on existing ones.
    """
    
    def __init__(self, title: str, content: str, author: str) -> None:
        """Initialize a document.
        
        Args:
            title: Document title
            content: Document content
            author: Document author
        """
        raise NotImplementedError("Implement Document.__init__")
    
    def clone(self) -> Self:
        """Create a deep copy of the document.
        
        Returns:
            A deep copy of this document
        """
        raise NotImplementedError("Implement Document.clone")
    
    def update_title(self, new_title: str) -> None:
        """Update the document title.
        
        Args:
            new_title: New title for the document
        """
        raise NotImplementedError("Implement Document.update_title")
    
    def update_content(self, new_content: str) -> None:
        """Update the document content.
        
        Args:
            new_content: New content for the document
        """
        raise NotImplementedError("Implement Document.update_content")
    
    def update_author(self, new_author: str) -> None:
        """Update the document author.
        
        Args:
            new_author: New author for the document
        """
        raise NotImplementedError("Implement Document.update_author")
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the document.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        raise NotImplementedError("Implement Document.add_metadata")
    
    def get_metadata(self, key: str) -> Any:
        """Get metadata value.
        
        Args:
            key: Metadata key
            
        Returns:
            Metadata value or None if not found
        """
        raise NotImplementedError("Implement Document.get_metadata")
    
    def __str__(self) -> str:
        """Return string representation.
        
        Returns:
            Format: "'{title}' by {author}"
        """
        raise NotImplementedError("Implement Document.__str__")
    
    def to_dict(self) -> dict[str, Any]:
        """Convert document to dictionary.
        
        Returns:
            Dictionary representation of the document
        """
        raise NotImplementedError("Implement Document.to_dict")


class Report(Document):
    """Specialized document: Report.
    
    Extends Document with report-specific properties.
    """
    
    def __init__(self, title: str, content: str, author: str, report_type: str) -> None:
        """Initialize a report.
        
        Args:
            title: Report title
            content: Report content
            author: Report author
            report_type: Type of report (e.g., 'financial', 'technical')
        """
        raise NotImplementedError("Implement Report.__init__")
    
    def clone(self) -> Self:
        """Create a deep copy of the report."""
        raise NotImplementedError("Implement Report.clone")
    
    def set_department(self, department: str) -> None:
        """Set the department for this report.
        
        Args:
            department: Department name
        """
        raise NotImplementedError("Implement Report.set_department")
    
    def get_department(self) -> str:
        """Get the department.
        
        Returns:
            Department name
        """
        raise NotImplementedError("Implement Report.get_department")


class Contract(Document):
    """Specialized document: Contract.
    
    Extends Document with contract-specific properties.
    """
    
    def __init__(self, title: str, content: str, author: str, parties: list[str]) -> None:
        """Initialize a contract.
        
        Args:
            title: Contract title
            content: Contract content
            author: Contract author
            parties: List of parties involved
        """
        raise NotImplementedError("Implement Contract.__init__")
    
    def clone(self) -> Self:
        """Create a deep copy of the contract."""
        raise NotImplementedError("Implement Contract.clone")
    
    def add_party(self, party: str) -> None:
        """Add a party to the contract.
        
        Args:
            party: Party name to add
        """
        raise NotImplementedError("Implement Contract.add_party")
    
    def get_parties(self) -> list[str]:
        """Get all parties.
        
        Returns:
            List of party names
        """
        raise NotImplementedError("Implement Contract.get_parties")


class DocumentRegistry:
    """Registry for document prototypes.
    
    Manages a collection of document prototypes that can be
    cloned to create new documents.
    """
    
    def __init__(self) -> None:
        """Initialize the registry."""
        raise NotImplementedError("Implement DocumentRegistry.__init__")
    
    def register(self, name: str, document: Prototype) -> None:
        """Register a document prototype.
        
        Args:
            name: Name to register under
            document: Document prototype to store
        """
        raise NotImplementedError("Implement DocumentRegistry.register")
    
    def unregister(self, name: str) -> None:
        """Unregister a document prototype.
        
        Args:
            name: Name of the prototype to remove
        """
        raise NotImplementedError("Implement DocumentRegistry.unregister")
    
    def create(self, name: str) -> Prototype:
        """Create a clone of a registered prototype.
        
        Args:
            name: Name of the registered prototype
            
        Returns:
            A clone of the registered document
            
        Raises:
            KeyError: If name is not registered
        """
        raise NotImplementedError("Implement DocumentRegistry.create")
    
    def is_registered(self, name: str) -> bool:
        """Check if a name is registered.
        
        Args:
            name: Name to check
            
        Returns:
            True if registered, False otherwise
        """
        raise NotImplementedError("Implement DocumentRegistry.is_registered")
    
    def list_prototypes(self) -> list[str]:
        """List all registered prototype names.
        
        Returns:
            List of registered names
        """
        raise NotImplementedError("Implement DocumentRegistry.list_prototypes")
