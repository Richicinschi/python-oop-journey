"""Tests for Problem 05: Prototype Document Clone."""

from __future__ import annotations

import pytest
from copy import deepcopy

from week06_patterns.solutions.day01.problem_05_prototype_document_clone import (
    Prototype, Document, Report, Contract, DocumentRegistry
)


class TestDocument:
    """Tests for Document class."""
    
    def test_init(self) -> None:
        doc = Document("Title", "Content", "Author")
        assert doc.title == "Title"
        assert doc.content == "Content"
        assert doc.author == "Author"
        assert doc.metadata == {}
    
    def test_update_title(self) -> None:
        doc = Document("Title", "Content", "Author")
        doc.update_title("New Title")
        assert doc.title == "New Title"
    
    def test_update_content(self) -> None:
        doc = Document("Title", "Content", "Author")
        doc.update_content("New Content")
        assert doc.content == "New Content"
    
    def test_update_author(self) -> None:
        doc = Document("Title", "Content", "Author")
        doc.update_author("New Author")
        assert doc.author == "New Author"
    
    def test_add_and_get_metadata(self) -> None:
        doc = Document("Title", "Content", "Author")
        doc.add_metadata("key", "value")
        assert doc.get_metadata("key") == "value"
    
    def test_get_missing_metadata(self) -> None:
        doc = Document("Title", "Content", "Author")
        assert doc.get_metadata("missing") is None
    
    def test_str(self) -> None:
        doc = Document("Title", "Content", "Author")
        assert str(doc) == "'Title' by Author"
    
    def test_to_dict(self) -> None:
        doc = Document("Title", "Content", "Author")
        doc.add_metadata("key", "value")
        d = doc.to_dict()
        assert d["title"] == "Title"
        assert d["content"] == "Content"
        assert d["author"] == "Author"
        assert d["metadata"] == {"key": "value"}


class TestDocumentClone:
    """Tests for Document cloning functionality."""
    
    def test_clone_creates_new_object(self) -> None:
        original = Document("Title", "Content", "Author")
        clone = original.clone()
        assert original is not clone
    
    def test_clone_copies_all_attributes(self) -> None:
        original = Document("Title", "Content", "Author")
        clone = original.clone()
        assert clone.title == "Title"
        assert clone.content == "Content"
        assert clone.author == "Author"
    
    def test_clone_is_independent(self) -> None:
        original = Document("Title", "Content", "Author")
        clone = original.clone()
        clone.update_title("New Title")
        assert original.title == "Title"
        assert clone.title == "New Title"
    
    def test_clone_copies_metadata(self) -> None:
        original = Document("Title", "Content", "Author")
        original.add_metadata("key", "value")
        clone = original.clone()
        assert clone.get_metadata("key") == "value"
    
    def test_clone_metadata_is_deep_copy(self) -> None:
        original = Document("Title", "Content", "Author")
        original.add_metadata("key", "value")
        clone = original.clone()
        clone.add_metadata("key", "modified")
        assert original.get_metadata("key") == "value"
        assert clone.get_metadata("key") == "modified"
    
    def test_clone_preserves_isinstance(self) -> None:
        original = Document("Title", "Content", "Author")
        clone = original.clone()
        assert isinstance(clone, Document)


class TestReport:
    """Tests for Report class."""
    
    def test_init(self) -> None:
        report = Report("Report Title", "Content", "Author", "financial")
        assert report.title == "Report Title"
        assert report.report_type == "financial"
        assert report.department == ""
    
    def test_set_and_get_department(self) -> None:
        report = Report("Report Title", "Content", "Author", "financial")
        report.set_department("Finance")
        assert report.get_department() == "Finance"
    
    def test_report_clone(self) -> None:
        original = Report("Title", "Content", "Author", "technical")
        original.set_department("Engineering")
        clone = original.clone()
        
        assert clone.title == "Title"
        assert clone.report_type == "technical"
        assert clone.get_department() == "Engineering"
        assert isinstance(clone, Report)
    
    def test_report_clone_is_independent(self) -> None:
        original = Report("Title", "Content", "Author", "technical")
        clone = original.clone()
        clone.set_department("Marketing")
        assert original.get_department() == ""
        assert clone.get_department() == "Marketing"


class TestContract:
    """Tests for Contract class."""
    
    def test_init(self) -> None:
        contract = Contract("Contract", "Terms", "Lawyer", ["Party A", "Party B"])
        assert contract.title == "Contract"
        assert contract.get_parties() == ["Party A", "Party B"]
    
    def test_add_party(self) -> None:
        contract = Contract("Contract", "Terms", "Lawyer", ["Party A"])
        contract.add_party("Party B")
        assert contract.get_parties() == ["Party A", "Party B"]
    
    def test_get_parties_returns_copy(self) -> None:
        contract = Contract("Contract", "Terms", "Lawyer", ["Party A"])
        parties = contract.get_parties()
        parties.append("Party B")
        assert contract.get_parties() == ["Party A"]
    
    def test_contract_clone(self) -> None:
        original = Contract("Contract", "Terms", "Lawyer", ["Party A", "Party B"])
        clone = original.clone()
        
        assert clone.title == "Contract"
        assert clone.get_parties() == ["Party A", "Party B"]
        assert isinstance(clone, Contract)
    
    def test_contract_clone_parties_is_deep_copy(self) -> None:
        original = Contract("Contract", "Terms", "Lawyer", ["Party A", "Party B"])
        clone = original.clone()
        clone.add_party("Party C")
        assert original.get_parties() == ["Party A", "Party B"]
        assert clone.get_parties() == ["Party A", "Party B", "Party C"]


class TestDocumentRegistry:
    """Tests for DocumentRegistry class."""
    
    def test_init(self) -> None:
        registry = DocumentRegistry()
        assert registry.list_prototypes() == []
    
    def test_register(self) -> None:
        registry = DocumentRegistry()
        doc = Document("Template", "Content", "Admin")
        registry.register("template", doc)
        assert registry.is_registered("template") is True
    
    def test_unregister(self) -> None:
        registry = DocumentRegistry()
        doc = Document("Template", "Content", "Admin")
        registry.register("template", doc)
        registry.unregister("template")
        assert registry.is_registered("template") is False
    
    def test_create(self) -> None:
        registry = DocumentRegistry()
        doc = Document("Template", "Content", "Admin")
        registry.register("template", doc)
        
        clone = registry.create("template")
        assert isinstance(clone, Document)
        assert clone.title == "Template"
        assert clone is not doc
    
    def test_create_not_registered_raises(self) -> None:
        registry = DocumentRegistry()
        with pytest.raises(KeyError):
            registry.create("missing")
    
    def test_is_registered_false(self) -> None:
        registry = DocumentRegistry()
        assert registry.is_registered("missing") is False
    
    def test_list_prototypes(self) -> None:
        registry = DocumentRegistry()
        registry.register("doc1", Document("Doc1", "Content", "Author"))
        registry.register("doc2", Document("Doc2", "Content", "Author"))
        
        prototypes = registry.list_prototypes()
        assert "doc1" in prototypes
        assert "doc2" in prototypes
        assert len(prototypes) == 2


class TestRegistryIndependence:
    """Tests ensuring registry stores prototypes independently."""
    
    def test_modifying_original_after_register(self) -> None:
        registry = DocumentRegistry()
        original = Document("Template", "Content", "Admin")
        registry.register("template", original)
        
        original.update_title("Modified")
        clone = registry.create("template")
        
        assert clone.title == "Template"
    
    def test_modifying_clone_does_not_affect_original(self) -> None:
        registry = DocumentRegistry()
        original = Document("Template", "Content", "Admin")
        registry.register("template", original)
        
        clone = registry.create("template")
        clone.update_title("Modified")
        
        assert original.title == "Template"


class TestPolymorphism:
    """Tests demonstrating polymorphic behavior."""
    
    def test_prototype_interface(self) -> None:
        doc = Document("Title", "Content", "Author")
        report = Report("Report", "Content", "Author", "type")
        contract = Contract("Contract", "Content", "Author", ["Party"])
        
        prototypes: list[Prototype] = [doc, report, contract]
        
        for proto in prototypes:
            clone = proto.clone()
            assert isinstance(clone, Prototype)
            assert type(clone) == type(proto)
    
    def test_registry_with_different_types(self) -> None:
        registry = DocumentRegistry()
        registry.register("doc", Document("Doc", "Content", "Author"))
        registry.register("report", Report("Report", "Content", "Author", "type"))
        registry.register("contract", Contract("Contract", "Content", "Author", ["Party"]))
        
        doc_clone = registry.create("doc")
        report_clone = registry.create("report")
        contract_clone = registry.create("contract")
        
        assert isinstance(doc_clone, Document)
        assert isinstance(report_clone, Report)
        assert isinstance(contract_clone, Contract)
