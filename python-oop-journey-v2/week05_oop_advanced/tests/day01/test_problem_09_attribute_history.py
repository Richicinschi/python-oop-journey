"""Tests for Problem 09: Attribute History."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day01.problem_09_attribute_history import (
    History, HistoryEntry, Document, Setting
)


class TestHistory:
    """Tests for the History descriptor."""
    
    def test_history_tracks_changes(self) -> None:
        class TestClass:
            value = History(default="initial")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        obj.value = "first"
        obj.value = "second"
        obj.value = "third"
        
        history = TestClass.__dict__['value'].get_history(obj)
        assert len(history) == 3
        assert history[0].value == "first"
        assert history[1].value == "second"
        assert history[2].value == "third"
    
    def test_history_includes_previous_value(self) -> None:
        class TestClass:
            value = History(default="initial")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        obj.value = "first"
        obj.value = "second"
        
        history = TestClass.__dict__['value'].get_history(obj)
        assert history[0].previous_value == "initial"
        assert history[1].previous_value == "first"
    
    def test_get_previous(self) -> None:
        class TestClass:
            value = History(default="initial")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        obj.value = "first"
        obj.value = "second"
        
        previous = TestClass.__dict__['value'].get_previous(obj)
        assert previous == "first"
    
    def test_get_previous_none_for_first(self) -> None:
        class TestClass:
            value = History(default="initial")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        obj.value = "first"
        
        previous = TestClass.__dict__['value'].get_previous(obj)
        # The first entry's previous is the default
        assert previous is None
    
    def test_rollback(self) -> None:
        class TestClass:
            value = History(default="initial")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        obj.value = "first"
        obj.value = "second"
        obj.value = "third"
        
        success = TestClass.__dict__['value'].rollback(obj, 1)
        assert success is True
        assert obj.value == "second"
    
    def test_rollback_multiple_steps(self) -> None:
        class TestClass:
            value = History(default="initial")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        obj.value = "first"
        obj.value = "second"
        obj.value = "third"
        
        success = TestClass.__dict__['value'].rollback(obj, 2)
        assert success is True
        assert obj.value == "first"
    
    def test_rollback_failure_not_enough_history(self) -> None:
        class TestClass:
            value = History(default="initial")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        obj.value = "first"
        
        success = TestClass.__dict__['value'].rollback(obj, 5)
        assert success is False
    
    def test_clear_history(self) -> None:
        class TestClass:
            value = History(default="initial")
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        obj.value = "first"
        obj.value = "second"
        
        TestClass.__dict__['value'].clear_history(obj)
        history = TestClass.__dict__['value'].get_history(obj)
        assert len(history) == 1
        assert history[0].value == "second"


class TestDocument:
    """Tests for the Document class."""
    
    def test_document_creation(self) -> None:
        doc = Document("Test Doc", "Hello World")
        assert doc.title == "Test Doc"
        assert doc.content == "Hello World"
    
    def test_document_versions(self) -> None:
        doc = Document("Test Doc", "Version 1")
        doc.edit("Version 2")
        doc.edit("Version 3")
        
        versions = doc.get_versions()
        assert len(versions) == 3
        assert versions[0].value == "Version 1"
        assert versions[1].value == "Version 2"
        assert versions[2].value == "Version 3"
    
    def test_document_undo(self) -> None:
        doc = Document("Test Doc", "Version 1")
        doc.edit("Version 2")
        
        success = doc.undo()
        assert success is True
        assert doc.content == "Version 1"


class TestSetting:
    """Tests for the Setting class."""
    
    def test_setting_creation(self) -> None:
        setting = Setting("theme", "UI Theme", "light")
        assert setting.name == "theme"
        assert setting.description == "UI Theme"
        assert setting.value == "light"
    
    def test_setting_update(self) -> None:
        setting = Setting("theme", "UI Theme", "light")
        setting.update("dark")
        assert setting.value == "dark"
    
    def test_setting_changes(self) -> None:
        # Clear any shared history first
        Setting.__dict__['value'].histories.clear()
        
        setting = Setting("theme", "UI Theme", "light")
        setting.update("dark")
        setting.update("auto")
        
        changes = setting.get_changes()
        # Initial + 2 updates = 3 entries
        assert len(changes) == 3
    
    def test_has_changed_true(self) -> None:
        setting = Setting("theme", "UI Theme", "light")
        setting.update("dark")
        assert setting.has_changed() is True
    
    def test_has_changed_false(self) -> None:
        # Clear any shared history first
        Setting.__dict__['value'].histories.clear()
        
        setting = Setting("theme", "UI Theme", "light")
        # Only initial value set, no updates yet
        # has_changed should return False when only one entry exists
        assert setting.has_changed() is False
