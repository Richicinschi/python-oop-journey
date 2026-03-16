"""Problem 01: Template Report Pipeline

Topic: Template Method Pattern
Difficulty: Medium

Implement a report generation system using the Template Method pattern.
Create a base ReportGenerator with a template method and concrete implementations
for different report types (PDF, CSV, HTML).

HINTS:
- Hint 1 (Conceptual): The template method defines the algorithm skeleton in the 
  base class. Subclasses override specific steps but cannot change the sequence.
- Hint 2 (Structural): Template method calls: _collect_data(), _process_data(), 
  _format_output(), _export(). Abstract methods MUST be implemented by subclasses. 
  Concrete methods CAN be overridden but usually aren't.
- Hint 3 (Edge Case): The template method itself should NOT be overridden. Use 
  naming convention or documentation to indicate this. Handle empty data gracefully.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import override


class ReportGenerator(ABC):
    """Abstract base class for report generators using Template Method pattern.
    
    The template method 'generate_report()' defines the algorithm skeleton:
    1. Collect data
    2. Process/analyze data
    3. Format the report
    4. Export/save the report
    
    Subclasses override specific steps without changing the overall algorithm.
    """
    
    def __init__(self, report_name: str) -> None:
        """Initialize the report generator.
        
        Args:
            report_name: Name of the report being generated
        """
        raise NotImplementedError("Implement ReportGenerator.__init__")
    
    def generate_report(self, data_source: str) -> str:
        """Template method defining the report generation algorithm.
        
        This method defines the skeleton and should NOT be overridden.
        
        Args:
            data_source: Path or identifier for the data source
            
        Returns:
            String describing the generation result
        """
        raise NotImplementedError("Implement ReportGenerator.generate_report")
    
    @abstractmethod
    def _collect_data(self, source: str) -> list[dict]:
        """Step 1: Collect raw data from source.
        
        Args:
            source: Data source identifier
            
        Returns:
            List of data records as dictionaries
        """
        raise NotImplementedError("Implement _collect_data")
    
    @abstractmethod
    def _format_report(self, data: list[dict]) -> str:
        """Step 3: Format the processed data into report format.
        
        Args:
            data: Processed data records
            
        Returns:
            Formatted report content as string
        """
        raise NotImplementedError("Implement _format_report")
    
    def _process_data(self, raw_data: list[dict]) -> list[dict]:
        """Step 2: Process and analyze raw data.
        
        Hook method with default implementation. Can be overridden.
        Default: Sorts by 'name' field if present.
        
        Args:
            raw_data: Raw data records
            
        Returns:
            Processed data records
        """
        raise NotImplementedError("Implement _process_data")
    
    def _export(self, content: str) -> str:
        """Step 4: Export the formatted report.
        
        Hook method with default implementation. Can be overridden.
        Default: Returns a success message with report name.
        
        Args:
            content: Formatted report content
            
        Returns:
            Export result message
        """
        raise NotImplementedError("Implement _export")


class PDFReportGenerator(ReportGenerator):
    """Generates reports in PDF format.
    
    Overrides _collect_data and _format_report.
    Inherits default _process_data and _export.
    """
    
    @override
    def _collect_data(self, source: str) -> list[dict]:
        """Simulate collecting data for PDF report.
        
        Returns sample data with source name included.
        """
        raise NotImplementedError("Implement PDFReportGenerator._collect_data")
    
    @override
    def _format_report(self, data: list[dict]) -> str:
        """Format data as PDF-like structure.
        
        Format: PDF Report Header + data items + Footer
        """
        raise NotImplementedError("Implement PDFReportGenerator._format_report")
    
    @override
    def _export(self, content: str) -> str:
        """Export as PDF file.
        
        Returns: "PDF Export: <report_name> - <content_length> bytes"
        """
        raise NotImplementedError("Implement PDFReportGenerator._export")


class CSVReportGenerator(ReportGenerator):
    """Generates reports in CSV format.
    
    Overrides _collect_data, _format_report, and _process_data.
    """
    
    @override
    def _collect_data(self, source: str) -> list[dict]:
        """Simulate collecting data for CSV report.
        
        Returns sample data with 'id', 'name', 'value' fields.
        """
        raise NotImplementedError("Implement CSVReportGenerator._collect_data")
    
    @override
    def _process_data(self, raw_data: list[dict]) -> list[dict]:
        """Process data: filter out records with value < 0.
        
        Args:
            raw_data: Raw data records
            
        Returns:
            Filtered records with non-negative values
        """
        raise NotImplementedError("Implement CSVReportGenerator._process_data")
    
    @override
    def _format_report(self, data: list[dict]) -> str:
        """Format data as CSV.
        
        Format: header row + data rows with comma separation
        """
        raise NotImplementedError("Implement CSVReportGenerator._format_report")


class HTMLReportGenerator(ReportGenerator):
    """Generates reports in HTML format.
    
    Overrides all steps for HTML-specific processing.
    """
    
    @override
    def _collect_data(self, source: str) -> list[dict]:
        """Simulate collecting data for HTML report."""
        raise NotImplementedError("Implement HTMLReportGenerator._collect_data")
    
    @override
    def _process_data(self, raw_data: list[dict]) -> list[dict]:
        """Process data: add computed 'status' field based on value."""
        raise NotImplementedError("Implement HTMLReportGenerator._process_data")
    
    @override
    def _format_report(self, data: list[dict]) -> str:
        """Format data as HTML table."""
        raise NotImplementedError("Implement HTMLReportGenerator._format_report")
    
    @override
    def _export(self, content: str) -> str:
        """Export as HTML."""
        raise NotImplementedError("Implement HTMLReportGenerator._export")
