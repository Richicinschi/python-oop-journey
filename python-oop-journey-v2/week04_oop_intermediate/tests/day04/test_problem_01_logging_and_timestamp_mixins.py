"""Tests for Problem 01: Logging and Timestamp Mixins."""

from __future__ import annotations

import time
from datetime import datetime

import pytest

from week04_oop_intermediate.solutions.day04.problem_01_logging_and_timestamp_mixins import (
    Base,
    Document,
    LoggerMixin,
    TimestampMixin,
)


class TestLoggerMixin:
    """Tests for the LoggerMixin class."""
    
    def test_logger_mixin_init(self) -> None:
        """Test that LoggerMixin initializes _logs as empty list."""
        
        class TestClass(LoggerMixin):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        assert obj._logs == []
        assert obj.get_logs() == []
    
    def test_logger_mixin_log_single(self) -> None:
        """Test logging a single message."""
        
        class TestClass(LoggerMixin):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.log("Test message")
        
        logs = obj.get_logs()
        assert len(logs) == 1
        assert logs[0]["message"] == "Test message"
        assert logs[0]["level"] == "INFO"
        assert isinstance(logs[0]["timestamp"], datetime)
    
    def test_logger_mixin_log_multiple(self) -> None:
        """Test logging multiple messages."""
        
        class TestClass(LoggerMixin):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.log("Message 1")
        obj.log("Message 2", "DEBUG")
        obj.log("Message 3", "ERROR")
        
        logs = obj.get_logs()
        assert len(logs) == 3
        assert logs[0]["message"] == "Message 1"
        assert logs[1]["level"] == "DEBUG"
        assert logs[2]["level"] == "ERROR"
    
    def test_logger_mixin_get_logs_returns_copy(self) -> None:
        """Test that get_logs returns a copy, not the original."""
        
        class TestClass(LoggerMixin):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        obj.log("Message")
        
        logs1 = obj.get_logs()
        logs2 = obj.get_logs()
        
        assert logs1 is not logs2
        assert logs1 == logs2
        
        # Modifying returned list should not affect internal state
        logs1.append({"message": "Hacked!"})
        assert len(obj.get_logs()) == 1


class TestTimestampMixin:
    """Tests for the TimestampMixin class."""
    
    def test_timestamp_mixin_init(self) -> None:
        """Test that TimestampMixin sets created_at to current time."""
        
        class TestClass(TimestampMixin):
            def __init__(self) -> None:
                super().__init__()
        
        before = datetime.now()
        obj = TestClass()
        after = datetime.now()
        
        assert isinstance(obj.created_at, datetime)
        assert before <= obj.created_at <= after
    
    def test_timestamp_mixin_created_at_property(self) -> None:
        """Test that created_at is accessible as a property."""
        
        class TestClass(TimestampMixin):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        assert obj.created_at == obj._created_at
    
    def test_timestamp_mixin_get_age_seconds(self) -> None:
        """Test that get_age_seconds returns correct age."""
        
        class TestClass(TimestampMixin):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        age1 = obj.get_age_seconds()
        time.sleep(0.05)
        age2 = obj.get_age_seconds()
        
        assert age1 >= 0
        assert age2 > age1
        assert age2 - age1 >= 0.04  # Allow some tolerance
    
    def test_timestamp_mixin_age_increases(self) -> None:
        """Test that age increases over time."""
        
        class TestClass(TimestampMixin):
            def __init__(self) -> None:
                super().__init__()
        
        obj = TestClass()
        age_before = obj.get_age_seconds()
        time.sleep(0.1)
        age_after = obj.get_age_seconds()
        
        assert age_after > age_before


class TestBase:
    """Tests for the Base class that combines both mixins."""
    
    def test_base_has_logger_functionality(self) -> None:
        """Test that Base inherits LoggerMixin functionality."""
        obj = Base()
        obj.log("Test")
        assert len(obj.get_logs()) == 1
    
    def test_base_has_timestamp_functionality(self) -> None:
        """Test that Base inherits TimestampMixin functionality."""
        obj = Base()
        assert isinstance(obj.created_at, datetime)
        assert obj.get_age_seconds() >= 0
    
    def test_base_mro(self) -> None:
        """Test the Method Resolution Order of Base."""
        expected_mro = (Base, LoggerMixin, TimestampMixin, object)
        assert Base.__mro__ == expected_mro


class TestDocument:
    """Tests for the Document class."""
    
    def test_document_init(self) -> None:
        """Test Document initialization."""
        doc = Document("Test Title", "Test Content", "alice")
        
        assert doc.title == "Test Title"
        assert doc.content == "Test Content"
        assert doc.author == "alice"
    
    def test_document_logs_creation(self) -> None:
        """Test that Document logs its creation."""
        doc = Document("Test", "Content", "bob")
        
        logs = doc.get_logs()
        assert len(logs) >= 1
        assert "created" in logs[0]["message"].lower()
        assert "bob" in logs[0]["message"]
    
    def test_document_has_timestamp(self) -> None:
        """Test that Document has timestamp functionality."""
        doc = Document("Test", "Content", "charlie")
        
        assert isinstance(doc.created_at, datetime)
        assert doc.get_age_seconds() >= 0
    
    def test_document_update_content(self) -> None:
        """Test updating document content."""
        doc = Document("Test", "Original", "alice")
        initial_log_count = len(doc.get_logs())
        
        doc.update_content("Updated Content", "bob")
        
        assert doc.content == "Updated Content"
        assert len(doc.get_logs()) == initial_log_count + 1
        
        latest_log = doc.get_logs()[-1]
        assert "bob" in latest_log["message"]
        assert "updated" in latest_log["message"].lower()
    
    def test_document_str(self) -> None:
        """Test string representation."""
        doc = Document("My Doc", "Content", "alice")
        
        result = str(doc)
        
        assert "My Doc" in result
        assert "alice" in result
    
    def test_document_multiple_updates(self) -> None:
        """Test multiple content updates."""
        doc = Document("Test", "Initial", "user1")
        
        doc.update_content("Update 1", "user2")
        doc.update_content("Update 2", "user3")
        doc.update_content("Update 3", "user4")
        
        assert doc.content == "Update 3"
        logs = doc.get_logs()
        assert len(logs) == 4  # creation + 3 updates
    
    def test_document_mro(self) -> None:
        """Test the MRO of Document."""
        expected_mro = (Document, Base, LoggerMixin, TimestampMixin, object)
        assert Document.__mro__ == expected_mro
