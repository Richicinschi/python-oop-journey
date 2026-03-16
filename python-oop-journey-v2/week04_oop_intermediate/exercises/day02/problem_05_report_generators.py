"""Problem 05: Report Generators

Topic: Template method pattern with super()
Difficulty: Medium

Create a report generator hierarchy using the template method pattern.
Base class defines the algorithm steps, children override specific steps.

Classes to implement:
- ReportGenerator: Base with generate() template method
- PDFReport: Generates PDF reports with headers, page numbers
- CSVReport: Generates CSV reports with headers, quoting
- HTMLReport: Generates HTML reports with styling, tables

Example:
    >>> base = ReportGenerator("Sales Report", [{"item": "A", "value": 100}])
    >>> base.generate()
    'Report: Sales Report\\nRecords: 1\\n---'
    
    >>> pdf = PDFReport("Sales", [{"item": "A", "value": 100}], "Letter")
    >>> pdf.generate()
    'PDF Report: Sales\\nPage Size: Letter\\nHeader: Sales\\nRecords: 1\\nFooter: Page 1 of 1'
    
    >>> csv = CSVReport("Sales", [{"item": "A", "value": 100}], delimiter=";")
    >>> csv.generate()
    'CSV Report: Sales\\nHeader: item;value\\nRow 1: A;100'

Requirements:
    - ReportGenerator: title, data (list[dict])
    - generate(): Template method calling _prepare(), _format(), _finalize()
    - PDFReport: page_size, include_header/footer, page numbers
    - CSVReport: delimiter, include_header, quote handling
    - HTMLReport: table styling, include_css, title in <h1>
    - Children use super() to extend _prepare(), _format(), _finalize()
    - Data validation in base class (title must be non-empty)
"""

from __future__ import annotations


class ReportGenerator:
    """Base report generator using template method pattern."""

    def __init__(self, title: str, data: list[dict[str, object]]) -> None:
        """Initialize report generator.
        
        Args:
            title: Report title
            data: List of record dictionaries
            
        Raises:
            ValueError: If title is empty or data is not a list
        """
        raise NotImplementedError("Initialize with validation")

    def generate(self) -> str:
        """Template method that defines the report generation algorithm.
        
        Steps:
        1. _prepare() - Setup and validation
        2. _format() - Format the data
        3. _finalize() - Final processing and return
        
        Returns:
            Generated report as string
        """
        raise NotImplementedError("Call _prepare(), _format(), _finalize() in sequence")

    def _prepare(self) -> str:
        """Prepare step - setup and initial processing.
        
        Returns:
            Preparation result string
        """
        raise NotImplementedError("Return basic preparation string")

    def _format(self) -> str:
        """Format step - format the data.
        
        Returns:
            Formatted data string
        """
        raise NotImplementedError("Return basic format string with record count")

    def _finalize(self) -> str:
        """Finalize step - final processing.
        
        Returns:
            Finalization string
        """
        raise NotImplementedError("Return basic finalization string")

    def get_record_count(self) -> int:
        """Return number of records in report."""
        raise NotImplementedError("Return len(self.data)")


class PDFReport(ReportGenerator):
    """PDF report generator with headers and page numbers."""

    PAGE_SIZES = ("Letter", "A4", "Legal")
    DEFAULT_PAGE_SIZE = "Letter"

    def __init__(
        self,
        title: str,
        data: list[dict[str, object]],
        page_size: str = "Letter",
        include_header: bool = True,
        include_footer: bool = True
    ) -> None:
        """Initialize PDF report.
        
        Args:
            title: Report title
            data: Report data
            page_size: Page size (Letter, A4, Legal)
            include_header: Whether to include header
            include_footer: Whether to include footer with page numbers
            
        Raises:
            ValueError: If page_size not in PAGE_SIZES
        """
        raise NotImplementedError("Use super().__init__() and add PDF settings")

    def _prepare(self) -> str:
        """Prepare PDF with page size info.
        
        Extends parent with page size information.
        Format: '{parent}\\nPage Size: {page_size}'
        """
        raise NotImplementedError("Extend with super()")

    def _format(self) -> str:
        """Format PDF content with header.
        
        Extends parent with header if enabled.
        Format: '{parent}\\nHeader: {title}' (if include_header)
        """
        raise NotImplementedError("Extend with super()")

    def _finalize(self) -> str:
        """Finalize PDF with footer.
        
        Extends parent with footer if enabled.
        Format: '{parent}\\nFooter: Page 1 of 1' (if include_footer)
        """
        raise NotImplementedError("Extend with super()")

    def get_page_size(self) -> str:
        """Return page size."""
        raise NotImplementedError("Return page_size")


class CSVReport(ReportGenerator):
    """CSV report generator with delimiter options."""

    def __init__(
        self,
        title: str,
        data: list[dict[str, object]],
        delimiter: str = ",",
        include_header: bool = True,
        quote_all: bool = False
    ) -> None:
        """Initialize CSV report.
        
        Args:
            title: Report title
            data: Report data
            delimiter: Field delimiter character
            include_header: Whether to include column headers
            quote_all: Whether to quote all fields
        """
        raise NotImplementedError("Use super().__init__() and add CSV settings")

    def _prepare(self) -> str:
        """Prepare CSV report info.
        
        Format: 'CSV {parent}'
        """
        raise NotImplementedError("Extend with super()")

    def _format(self) -> str:
        """Format CSV content.
        
        Returns header row if include_header is True:
        'Header: col1{delimiter}col2...'
        
        Then data rows:
        'Row 1: val1{delimiter}val2...'
        """
        raise NotImplementedError("Format CSV with delimiter")

    def _finalize(self) -> str:
        """Finalize CSV report.
        
        Returns quote info if quote_all is True.
        """
        raise NotImplementedError("Extend with super()")

    def get_delimiter(self) -> str:
        """Return delimiter character."""
        raise NotImplementedError("Return delimiter")


class HTMLReport(ReportGenerator):
    """HTML report generator with table formatting."""

    def __init__(
        self,
        title: str,
        data: list[dict[str, object]],
        include_css: bool = True,
        table_class: str = "report-table"
    ) -> None:
        """Initialize HTML report.
        
        Args:
            title: Report title (used in <h1> and <title>)
            data: Report data
            include_css: Whether to include basic CSS styling
            table_class: CSS class for table element
        """
        raise NotImplementedError("Use super().__init__() and add HTML settings")

    def _prepare(self) -> str:
        """Prepare HTML with DOCTYPE and head.
        
        Format: '<!DOCTYPE html>\\n<html>\\n<head><title>{title}</title>...'
        Include CSS if enabled.
        """
        raise NotImplementedError("Generate HTML head section")

    def _format(self) -> str:
        """Format HTML body with table.
        
        Generate:
        <body>
        <h1>{title}</h1>
        <table class="{table_class}">
        <thead><tr><th>...</th></tr></thead>
        <tbody><tr><td>...</td></tr></tbody>
        </table>
        </body>
        """
        raise NotImplementedError("Generate HTML table")

    def _finalize(self) -> str:
        """Finalize HTML with closing tags."""
        raise NotImplementedError("Close HTML tags")

    def generate(self) -> str:
        """Generate complete HTML document."""
        raise NotImplementedError("Call parent template method")
