"""Exercise: Parser Framework.

Create an abstract base class for data parsers with abstract parse and
validate methods.

TODO:
1. Create Parser ABC with abstract methods parse and validate
2. Add concrete method parse_many for batch processing
3. Implement JSONParser
4. Implement CSVParser
5. Implement YAMLParser (optional, if PyYAML available)

Hints:
    Hint 1: Use @abstractmethod AND @property decorators together for abstract
    properties. Order matters: @property goes on top, @abstractmethod below.
    
    Hint 2: The concrete parse_many() method should use a list comprehension
    or simple loop to call self.parse() on each item. The concrete parse_file()
    should open the file, read the content, and call self.parse().
    
    Hint 3: For CSV parsing without headers, generate column names like
    "column_0", "column_1", etc. For validation, use try/except to catch
    parsing errors and return (False, error_message). YAML parsing should
    raise ImportError in __init__ if PyYAML is not available.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional
import json
import csv
import io


class Parser(ABC):
    """Abstract base class for data parsers.
    
    Provides a framework for parsing various data formats.
    """
    
    @property
    @abstractmethod
    def format_name(self) -> str:
        """Return the name of the format this parser handles."""
        # TODO: Define abstract property
        raise NotImplementedError("format_name property must be implemented")
    
    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return list of supported file extensions."""
        # TODO: Define abstract property
        raise NotImplementedError("supported_extensions property must be implemented")
    
    @abstractmethod
    def parse(self, data: str) -> dict[str, Any] | list[dict[str, Any]]:
        """Parse data string into Python objects.
        
        Args:
            data: String data to parse.
        
        Returns:
            Parsed data as dictionary or list of dictionaries.
        
        Raises:
            ValueError: If data is invalid or cannot be parsed.
        """
        # TODO: Implement abstract method
        raise NotImplementedError("parse must be implemented")
    
    @abstractmethod
    def validate(self, data: str) -> tuple[bool, Optional[str]]:
        """Validate data without parsing.
        
        Args:
            data: String data to validate.
        
        Returns:
            Tuple of (is_valid, error_message).
            If valid, error_message is None.
        """
        # TODO: Implement abstract method
        raise NotImplementedError("validate must be implemented")
    
    def parse_many(self, data_items: list[str]) -> list[dict[str, Any] | list[dict[str, Any]]]:
        """Parse multiple data items.
        
        This is a concrete method that uses the abstract parse method.
        
        Args:
            data_items: List of data strings to parse.
        
        Returns:
            List of parsed results.
        """
        # TODO: Parse each item using self.parse and return list
        raise NotImplementedError("Implement parse_many")
    
    def parse_file(self, file_path: str) -> dict[str, Any] | list[dict[str, Any]]:
        """Parse data from a file.
        
        This is a concrete method that uses the abstract parse method.
        
        Args:
            file_path: Path to the file to parse.
        
        Returns:
            Parsed data.
        """
        # TODO: Read file and call self.parse
        raise NotImplementedError("Implement parse_file")


class JSONParser(Parser):
    """Parser for JSON data."""
    
    @property
    def format_name(self) -> str:
        """Return format name."""
        # TODO: Return "JSON"
        raise NotImplementedError("Return format name")
    
    @property
    def supported_extensions(self) -> list[str]:
        """Return supported extensions."""
        # TODO: Return [".json"]
        raise NotImplementedError("Return extensions")
    
    def parse(self, data: str) -> dict[str, Any] | list[dict[str, Any]]:
        """Parse JSON string."""
        # TODO: Use json.loads to parse data
        raise NotImplementedError("Implement JSON parsing")
    
    def validate(self, data: str) -> tuple[bool, Optional[str]]:
        """Validate JSON data."""
        # TODO: Try json.loads, return (True, None) or (False, error_message)
        raise NotImplementedError("Implement JSON validation")


class CSVParser(Parser):
    """Parser for CSV data."""
    
    def __init__(self, has_header: bool = True) -> None:
        """Initialize CSV parser.
        
        Args:
            has_header: Whether CSV has header row.
        """
        # TODO: Set has_header flag
        raise NotImplementedError("Initialize CSV parser")
    
    @property
    def format_name(self) -> str:
        """Return format name."""
        # TODO: Return "CSV"
        raise NotImplementedError("Return format name")
    
    @property
    def supported_extensions(self) -> list[str]:
        """Return supported extensions."""
        # TODO: Return [".csv"]
        raise NotImplementedError("Return extensions")
    
    def parse(self, data: str) -> list[dict[str, Any]]:
        """Parse CSV string into list of dictionaries."""
        # TODO: Use csv.DictReader or csv.reader based on has_header
        # TODO: Return list of dictionaries
        raise NotImplementedError("Implement CSV parsing")
    
    def validate(self, data: str) -> tuple[bool, Optional[str]]:
        """Validate CSV data."""
        # TODO: Check if data can be parsed as CSV
        # TODO: Return (True, None) if valid, (False, message) otherwise
        raise NotImplementedError("Implement CSV validation")


class YAMLParser(Parser):
    """Parser for YAML data.
    
    Note: This parser raises ImportError if PyYAML is not installed.
    """
    
    def __init__(self) -> None:
        """Initialize YAML parser.
        
        Raises:
            ImportError: If PyYAML is not installed.
        """
        # TODO: Try to import yaml, raise ImportError if not available
        raise NotImplementedError("Initialize YAML parser with import check")
    
    @property
    def format_name(self) -> str:
        """Return format name."""
        # TODO: Return "YAML"
        raise NotImplementedError("Return format name")
    
    @property
    def supported_extensions(self) -> list[str]:
        """Return supported extensions."""
        # TODO: Return [".yaml", ".yml"]
        raise NotImplementedError("Return extensions")
    
    def parse(self, data: str) -> dict[str, Any] | list[dict[str, Any]]:
        """Parse YAML string."""
        # TODO: Use yaml.safe_load to parse data
        raise NotImplementedError("Implement YAML parsing")
    
    def validate(self, data: str) -> tuple[bool, Optional[str]]:
        """Validate YAML data."""
        # TODO: Try yaml.safe_load, return (True, None) or (False, error_message)
        raise NotImplementedError("Implement YAML validation")
