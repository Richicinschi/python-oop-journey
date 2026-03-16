"""Tests for Problem 06: Parser Framework."""

from __future__ import annotations

import os
import shutil
import pytest
import tempfile
from abc import ABC
from pathlib import Path

from week04_oop_intermediate.solutions.day03.problem_06_parser_framework import (
    Parser,
    JSONParser,
    CSVParser,
)


@pytest.fixture
def safe_tmp_path():
    """Provide a temporary path that works in restricted environments."""
    test_dir = Path(os.getcwd()) / ".test_tmp"
    test_dir.mkdir(exist_ok=True)
    try:
        yield test_dir
    finally:
        if test_dir.exists():
            shutil.rmtree(test_dir, ignore_errors=True)


class TestParserABC:
    """Test suite for Parser abstract base class."""
    
    def test_parser_is_abstract(self) -> None:
        """Test that Parser cannot be instantiated."""
        assert issubclass(Parser, ABC)
        with pytest.raises(TypeError, match="abstract"):
            Parser()
    
    def test_parser_has_abstract_properties(self) -> None:
        """Test that Parser defines abstract properties."""
        assert hasattr(Parser, 'format_name')
        assert hasattr(Parser, 'supported_extensions')
    
    def test_parser_has_abstract_methods(self) -> None:
        """Test that Parser defines abstract methods."""
        assert hasattr(Parser, 'parse')
        assert hasattr(Parser, 'validate')
    
    def test_parser_has_concrete_parse_many(self) -> None:
        """Test that Parser provides concrete parse_many method."""
        parser = JSONParser()
        items = ['{"a": 1}', '{"b": 2}']
        results = parser.parse_many(items)
        assert len(results) == 2
        assert results[0] == {"a": 1}
        assert results[1] == {"b": 2}
    
    def test_parser_has_concrete_parse_file(self, safe_tmp_path: Path) -> None:
        """Test that Parser provides concrete parse_file method."""
        test_file = safe_tmp_path / "test.json"
        test_file.write_text('{"key": "value"}')
        
        parser = JSONParser()
        result = parser.parse_file(str(test_file))
        assert result == {"key": "value"}


class TestJSONParser:
    """Test suite for JSONParser."""
    
    def test_format_name(self) -> None:
        """Test format_name property."""
        parser = JSONParser()
        assert parser.format_name == "JSON"
    
    def test_supported_extensions(self) -> None:
        """Test supported_extensions property."""
        parser = JSONParser()
        assert parser.supported_extensions == [".json"]
    
    def test_parse_object(self) -> None:
        """Test parsing JSON object."""
        parser = JSONParser()
        result = parser.parse('{"name": "Alice", "age": 30}')
        assert result == {"name": "Alice", "age": 30}
    
    def test_parse_array(self) -> None:
        """Test parsing JSON array."""
        parser = JSONParser()
        result = parser.parse('[{"a": 1}, {"b": 2}]')
        assert result == [{"a": 1}, {"b": 2}]
    
    def test_parse_nested(self) -> None:
        """Test parsing nested JSON."""
        parser = JSONParser()
        result = parser.parse('{"user": {"name": "Alice", "prefs": {"theme": "dark"}}}')
        assert result["user"]["name"] == "Alice"
        assert result["user"]["prefs"]["theme"] == "dark"
    
    def test_parse_invalid_json_raises(self) -> None:
        """Test that invalid JSON raises ValueError."""
        parser = JSONParser()
        with pytest.raises(ValueError, match="Invalid JSON"):
            parser.parse('{"invalid json')
    
    def test_parse_empty_object(self) -> None:
        """Test parsing empty JSON object."""
        parser = JSONParser()
        result = parser.parse('{}')
        assert result == {}
    
    def test_validate_valid(self) -> None:
        """Test validation of valid JSON."""
        parser = JSONParser()
        is_valid, error = parser.validate('{"valid": true}')
        assert is_valid is True
        assert error is None
    
    def test_validate_invalid(self) -> None:
        """Test validation of invalid JSON."""
        parser = JSONParser()
        is_valid, error = parser.validate('{"invalid')
        assert is_valid is False
        assert error is not None


class TestCSVParser:
    """Test suite for CSVParser."""
    
    def test_format_name(self) -> None:
        """Test format_name property."""
        parser = CSVParser()
        assert parser.format_name == "CSV"
    
    def test_supported_extensions(self) -> None:
        """Test supported_extensions property."""
        parser = CSVParser()
        assert parser.supported_extensions == [".csv"]
    
    def test_parse_with_header(self) -> None:
        """Test parsing CSV with header."""
        parser = CSVParser(has_header=True)
        csv_data = "name,age,city\nAlice,30,NYC\nBob,25,LA"
        result = parser.parse(csv_data)
        
        assert len(result) == 2
        assert result[0]["name"] == "Alice"
        assert result[0]["age"] == 30  # Should be converted to int
        assert result[1]["city"] == "LA"
    
    def test_parse_without_header(self) -> None:
        """Test parsing CSV without header."""
        parser = CSVParser(has_header=False)
        csv_data = "Alice,30,NYC\nBob,25,LA"
        result = parser.parse(csv_data)
        
        assert len(result) == 2
        assert result[0]["column_0"] == "Alice"
        assert result[0]["column_1"] == 30
    
    def test_parse_converts_numeric_values(self) -> None:
        """Test that numeric values are converted."""
        parser = CSVParser()
        csv_data = "name,value\nAlice,100\nBob,3.14"
        result = parser.parse(csv_data)
        
        assert result[0]["value"] == 100  # int
        assert result[1]["value"] == 3.14  # float
    
    def test_parse_single_row(self) -> None:
        """Test parsing single row CSV."""
        parser = CSVParser()
        csv_data = "name,age\nAlice,30"
        result = parser.parse(csv_data)
        
        assert len(result) == 1
        assert result[0] == {"name": "Alice", "age": 30}
    
    def test_validate_valid(self) -> None:
        """Test validation of valid CSV."""
        parser = CSVParser()
        is_valid, error = parser.validate("a,b\n1,2")
        assert is_valid is True
        assert error is None
    
    def test_validate_empty(self) -> None:
        """Test validation of empty CSV."""
        parser = CSVParser()
        is_valid, error = parser.validate("")
        # Empty string is technically valid CSV
        assert is_valid is True


class TestParserIntegration:
    """Integration tests for Parser framework."""
    
    def test_parse_many_with_different_parsers(self) -> None:
        """Test parse_many with different parser types."""
        json_parser = JSONParser()
        csv_parser = CSVParser()
        
        json_items = ['{"a": 1}', '{"b": 2}']
        csv_items = ["name,age\nAlice,30", "name,age\nBob,25"]
        
        json_results = json_parser.parse_many(json_items)
        csv_results = csv_parser.parse_many(csv_items)
        
        assert len(json_results) == 2
        assert json_results[0]["a"] == 1
        
        assert len(csv_results) == 2
        assert csv_results[0][0]["name"] == "Alice"
    
    def test_parse_file_json(self, safe_tmp_path: Path) -> None:
        """Test parse_file with JSON."""
        test_file = safe_tmp_path / "data.json"
        test_file.write_text('[{"id": 1}, {"id": 2}]')
        
        parser = JSONParser()
        result = parser.parse_file(str(test_file))
        assert result == [{"id": 1}, {"id": 2}]
    
    def test_parse_file_csv(self, safe_tmp_path: Path) -> None:
        """Test parse_file with CSV."""
        test_file = safe_tmp_path / "data.csv"
        test_file.write_text("name,value\nAlice,100\nBob,200")
        
        parser = CSVParser()
        result = parser.parse_file(str(test_file))
        assert len(result) == 2
        assert result[0]["name"] == "Alice"
