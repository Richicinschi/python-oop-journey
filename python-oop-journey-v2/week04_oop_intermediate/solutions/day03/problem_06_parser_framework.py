"""Solution for Problem 06: Parser Framework.

Demonstrates abstract methods with concrete helper methods for batch processing.
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
        pass
    
    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return list of supported file extensions."""
        pass
    
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
        pass
    
    @abstractmethod
    def validate(self, data: str) -> tuple[bool, Optional[str]]:
        """Validate data without parsing.
        
        Args:
            data: String data to validate.
        
        Returns:
            Tuple of (is_valid, error_message).
            If valid, error_message is None.
        """
        pass
    
    def parse_many(self, data_items: list[str]) -> list[dict[str, Any] | list[dict[str, Any]]]:
        """Parse multiple data items.
        
        This is a concrete method that uses the abstract parse method.
        
        Args:
            data_items: List of data strings to parse.
        
        Returns:
            List of parsed results.
        """
        return [self.parse(item) for item in data_items]
    
    def parse_file(self, file_path: str) -> dict[str, Any] | list[dict[str, Any]]:
        """Parse data from a file.
        
        This is a concrete method that uses the abstract parse method.
        
        Args:
            file_path: Path to the file to parse.
        
        Returns:
            Parsed data.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return self.parse(f.read())


class JSONParser(Parser):
    """Parser for JSON data."""
    
    @property
    def format_name(self) -> str:
        """Return format name."""
        return "JSON"
    
    @property
    def supported_extensions(self) -> list[str]:
        """Return supported extensions."""
        return [".json"]
    
    def parse(self, data: str) -> dict[str, Any] | list[dict[str, Any]]:
        """Parse JSON string."""
        try:
            result = json.loads(data)
            if not isinstance(result, (dict, list)):
                raise ValueError("JSON must be an object or array")
            return result
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
    
    def validate(self, data: str) -> tuple[bool, Optional[str]]:
        """Validate JSON data."""
        try:
            json.loads(data)
            return (True, None)
        except json.JSONDecodeError as e:
            return (False, str(e))


class CSVParser(Parser):
    """Parser for CSV data.
    
    Attributes:
        has_header: Whether CSV has header row.
    """
    
    def __init__(self, has_header: bool = True) -> None:
        """Initialize CSV parser.
        
        Args:
            has_header: Whether CSV has header row.
        """
        self.has_header = has_header
    
    @property
    def format_name(self) -> str:
        """Return format name."""
        return "CSV"
    
    @property
    def supported_extensions(self) -> list[str]:
        """Return supported extensions."""
        return [".csv"]
    
    def parse(self, data: str) -> list[dict[str, Any]]:
        """Parse CSV string into list of dictionaries."""
        try:
            f = io.StringIO(data)
            if self.has_header:
                reader = csv.DictReader(f)
                return [{k: self._convert_value(v) for k, v in row.items()} for row in reader]
            else:
                reader = csv.reader(f)
                rows = list(reader)
                return [{f"column_{i}": self._convert_value(v) for i, v in enumerate(row)} for row in rows]
        except csv.Error as e:
            raise ValueError(f"Invalid CSV: {e}")
    
    def _convert_value(self, value: str) -> Any:
        """Try to convert string value to appropriate type."""
        # Try int
        try:
            return int(value)
        except ValueError:
            pass
        # Try float
        try:
            return float(value)
        except ValueError:
            pass
        # Return as string
        return value
    
    def validate(self, data: str) -> tuple[bool, Optional[str]]:
        """Validate CSV data."""
        try:
            f = io.StringIO(data)
            if self.has_header:
                reader = csv.DictReader(f)
                list(reader)  # Try to read all rows
            else:
                reader = csv.reader(f)
                list(reader)  # Try to read all rows
            return (True, None)
        except csv.Error as e:
            return (False, str(e))


class YAMLParser(Parser):
    """Parser for YAML data.
    
    Note: This parser raises ImportError if PyYAML is not installed.
    
    Attributes:
        _yaml: The yaml module (if available).
    """
    
    def __init__(self) -> None:
        """Initialize YAML parser.
        
        Raises:
            ImportError: If PyYAML is not installed.
        """
        try:
            import yaml
            self._yaml = yaml
        except ImportError as e:
            raise ImportError("PyYAML is required for YAMLParser. Install with: pip install pyyaml") from e
    
    @property
    def format_name(self) -> str:
        """Return format name."""
        return "YAML"
    
    @property
    def supported_extensions(self) -> list[str]:
        """Return supported extensions."""
        return [".yaml", ".yml"]
    
    def parse(self, data: str) -> dict[str, Any] | list[dict[str, Any]]:
        """Parse YAML string."""
        try:
            result = self._yaml.safe_load(data)
            if result is None:
                return {}
            if not isinstance(result, (dict, list)):
                raise ValueError("YAML must be a mapping or sequence")
            return result
        except self._yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML: {e}")
    
    def validate(self, data: str) -> tuple[bool, Optional[str]]:
        """Validate YAML data."""
        try:
            self._yaml.safe_load(data)
            return (True, None)
        except self._yaml.YAMLError as e:
            return (False, str(e))
