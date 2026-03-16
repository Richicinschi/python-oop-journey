"""Tests for Problem 07: Abstract Method Enforcement Metaclass."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day02.problem_07_abstract_meta import (
    AbstractMeta,
    BaseComponent,
    CSVProcessor,
    DataProcessor,
    JSONProcessor,
    MustImplement,
)


class TestMustImplement:
    """Tests for the MustImplement decorator."""
    
    def test_decorator_exists(self) -> None:
        """Test that MustImplement is defined."""
        assert callable(MustImplement)


class TestAbstractMeta:
    """Tests for the AbstractMeta metaclass."""
    
    def test_metaclass_exists(self) -> None:
        """Test that AbstractMeta is defined."""
        assert isinstance(AbstractMeta, type)
    
    def test_abstract_base_can_be_created(self) -> None:
        """Test that abstract base class can be defined."""
        # BaseComponent should be creatable with abstract methods
        assert hasattr(BaseComponent, 'initialize')
        assert hasattr(BaseComponent, 'execute')
    
    def test_concrete_class_with_all_methods(self) -> None:
        """Test that concrete class with all implementations works."""
        # CSVProcessor should implement all abstract methods
        processor = CSVProcessor()
        assert hasattr(processor, 'initialize')
        assert hasattr(processor, 'validate_input')
    
    def test_missing_implementation_raises_typeerror(self) -> None:
        """Test that missing implementation raises TypeError."""
        with pytest.raises(TypeError) as exc_info:
            class Incomplete(BaseComponent, metaclass=AbstractMeta):
                # Missing initialize and execute
                pass
        
        assert "must implement" in str(exc_info.value).lower()
    
    def test_partial_implementation_raises_typeerror(self) -> None:
        """Test that partial implementation raises TypeError."""
        with pytest.raises(TypeError) as exc_info:
            class Partial(BaseComponent, metaclass=AbstractMeta):
                def initialize(self) -> None:
                    pass
                # Missing execute
        
        error_msg = str(exc_info.value).lower()
        assert "must implement" in error_msg
        assert "execute" in error_msg


class TestBaseComponent:
    """Tests for the BaseComponent class."""
    
    def test_has_abstract_methods(self) -> None:
        """Test that BaseComponent defines abstract methods."""
        assert hasattr(BaseComponent, 'initialize')
        assert hasattr(BaseComponent, 'execute')
    
    def test_cleanup_has_default(self) -> None:
        """Test that cleanup has a default implementation."""
        # cleanup is not marked with MustImplement, so it should be optional
        assert hasattr(BaseComponent, 'cleanup')


class TestDataProcessor:
    """Tests for the DataProcessor class."""
    
    def test_is_abstract(self) -> None:
        """Test that DataProcessor is abstract (has abstract methods)."""
        # DataProcessor adds validate_input as abstract but implements execute
        assert hasattr(DataProcessor, 'validate_input')
    
    def test_execute_implemented(self) -> None:
        """Test that execute has default implementation."""
        # DataProcessor provides execute implementation
        assert "executing" in DataProcessor.execute(None).lower()


class TestCSVProcessor:
    """Tests for the CSVProcessor class."""
    
    def test_csv_processor_init(self) -> None:
        """Test CSVProcessor initialization."""
        processor = CSVProcessor()
        assert hasattr(processor, '_initialized')
        assert processor._initialized is False
    
    def test_csv_processor_initialize(self) -> None:
        """Test CSVProcessor initialize method."""
        processor = CSVProcessor()
        processor.initialize()
        assert processor._initialized is True
    
    def test_csv_processor_validate_input_valid(self) -> None:
        """Test CSVProcessor validate_input with valid data."""
        processor = CSVProcessor()
        assert processor.validate_input("a,b,c") is True
    
    def test_csv_processor_validate_input_invalid(self) -> None:
        """Test CSVProcessor validate_input with invalid data."""
        processor = CSVProcessor()
        assert processor.validate_input("nodata") is False
        assert processor.validate_input(123) is False
    
    def test_csv_processor_process_row(self) -> None:
        """Test CSVProcessor process_row method."""
        processor = CSVProcessor()
        result = processor.process_row(["a", "b", "c"])
        assert "data" in result


class TestJSONProcessor:
    """Tests for the JSONProcessor class."""
    
    def test_json_processor_init(self) -> None:
        """Test JSONProcessor initialization."""
        processor = JSONProcessor()
        assert hasattr(processor, '_initialized')
    
    def test_json_processor_initialize(self) -> None:
        """Test JSONProcessor initialize method."""
        processor = JSONProcessor()
        processor.initialize()
        assert processor._initialized is True
    
    def test_json_processor_validate_input_valid(self) -> None:
        """Test JSONProcessor validate_input with valid JSON."""
        processor = JSONProcessor()
        assert processor.validate_input('{"key": "value"}') is True
        assert processor.validate_input('[1, 2, 3]') is True
    
    def test_json_processor_validate_input_invalid(self) -> None:
        """Test JSONProcessor validate_input with invalid data."""
        processor = JSONProcessor()
        assert processor.validate_input("not json") is False
        assert processor.validate_input(123) is False
    
    def test_json_processor_parse_json(self) -> None:
        """Test JSONProcessor parse_json method."""
        processor = JSONProcessor()
        result = processor.parse_json('{"key": "value"}')
        assert result == {"key": "value"}
