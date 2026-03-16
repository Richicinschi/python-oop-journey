"""Tests for Problem 08: Logger Config."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day02.problem_08_logger_config import Logger


class TestLoggerInit:
    """Test suite for Logger initialization."""
    
    def setup_method(self) -> None:
        """Reset log level before each test."""
        Logger._level = "INFO"
    
    def test_init_with_default_level(self) -> None:
        """Test logger uses class level by default."""
        log = Logger("test")
        assert log.name == "test"
        assert log.level == "INFO"
    
    def test_init_uses_current_class_level(self) -> None:
        """Test logger uses current class level."""
        Logger.set_level("DEBUG")
        log = Logger("test")
        assert log.level == "DEBUG"


class TestSetGetLevel:
    """Test suite for set_level and get_level."""
    
    def setup_method(self) -> None:
        """Reset log level before each test."""
        Logger._level = "INFO"
    
    def test_get_level_default(self) -> None:
        """Test default level is INFO."""
        assert Logger.get_level() == "INFO"
    
    def test_set_level(self) -> None:
        """Test setting level."""
        Logger.set_level("DEBUG")
        assert Logger.get_level() == "DEBUG"
        
        Logger.set_level("ERROR")
        assert Logger.get_level() == "ERROR"
    
    def test_set_invalid_level_raises(self) -> None:
        """Test setting invalid level raises ValueError."""
        with pytest.raises(ValueError):
            Logger.set_level("INVALID")


class TestIsLevelEnabled:
    """Test suite for is_level_enabled."""
    
    def setup_method(self) -> None:
        """Reset log level before each test."""
        Logger._level = "INFO"
    
    def test_is_level_enabled_at_info(self) -> None:
        """Test level checking at INFO level."""
        assert Logger.is_level_enabled("INFO") is True
        assert Logger.is_level_enabled("WARNING") is True
        assert Logger.is_level_enabled("ERROR") is True
        assert Logger.is_level_enabled("DEBUG") is False
    
    def test_is_level_enabled_at_debug(self) -> None:
        """Test level checking at DEBUG level."""
        Logger.set_level("DEBUG")
        assert Logger.is_level_enabled("DEBUG") is True
        assert Logger.is_level_enabled("INFO") is True
        assert Logger.is_level_enabled("ERROR") is True
    
    def test_is_level_enabled_at_error(self) -> None:
        """Test level checking at ERROR level."""
        Logger.set_level("ERROR")
        assert Logger.is_level_enabled("ERROR") is True
        assert Logger.is_level_enabled("CRITICAL") is True
        assert Logger.is_level_enabled("WARNING") is False
        assert Logger.is_level_enabled("INFO") is False
    
    def test_is_level_enabled_invalid(self) -> None:
        """Test invalid level returns False."""
        assert Logger.is_level_enabled("INVALID") is False


class TestWithCustomLevel:
    """Test suite for with_custom_level factory."""
    
    def setup_method(self) -> None:
        """Reset log level before each test."""
        Logger._level = "INFO"
    
    def test_with_custom_level(self) -> None:
        """Test creating logger with custom level."""
        log = Logger.with_custom_level("db", "ERROR")
        assert log.name == "db"
        assert log.level == "ERROR"
    
    def test_custom_level_doesnt_affect_global(self) -> None:
        """Test custom level doesn't change global level."""
        original_level = Logger.get_level()
        log = Logger.with_custom_level("db", "DEBUG")
        assert Logger.get_level() == original_level
        assert log.level == "DEBUG"
    
    def test_invalid_custom_level_raises(self) -> None:
        """Test invalid custom level raises ValueError."""
        with pytest.raises(ValueError):
            Logger.with_custom_level("test", "INVALID")


class TestLevelHierarchy:
    """Test suite for level hierarchy correctness."""
    
    def test_level_values(self) -> None:
        """Test that level values are correct."""
        assert Logger._levels["DEBUG"] == 10
        assert Logger._levels["INFO"] == 20
        assert Logger._levels["WARNING"] == 30
        assert Logger._levels["ERROR"] == 40
        assert Logger._levels["CRITICAL"] == 50
