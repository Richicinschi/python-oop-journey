"""Tests for Problem 05: Report Generators."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day02.problem_05_report_generators import (
    CSVReport,
    HTMLReport,
    PDFReport,
    ReportGenerator,
)


class TestReportGenerator:
    """Tests for ReportGenerator base class."""

    def test_init_sets_attributes(self) -> None:
        """Test that attributes are set."""
        data = [{"name": "Alice", "value": 100}]
        report = ReportGenerator("Test Report", data)
        assert report.title == "Test Report"
        assert report.data == data

    def test_init_validates_empty_title(self) -> None:
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="empty"):
            ReportGenerator("", [])

    def test_init_validates_data_type(self) -> None:
        """Test that non-list data raises ValueError."""
        with pytest.raises(ValueError, match="list"):
            ReportGenerator("Test", "not a list")

    def test_generate_calls_all_steps(self) -> None:
        """Test generate() calls all template method steps."""
        report = ReportGenerator("Test", [])
        result = report.generate()
        assert "Report: Test" in result
        assert "Records: 0" in result
        assert "---" in result

    def test_get_record_count_returns_length(self) -> None:
        """Test get_record_count() returns data length."""
        data = [{"a": 1}, {"b": 2}]
        report = ReportGenerator("Test", data)
        assert report.get_record_count() == 2


class TestPDFReport:
    """Tests for PDFReport class."""

    def test_page_sizes_constant(self) -> None:
        """Test PAGE_SIZES exists."""
        expected = ("Letter", "A4", "Legal")
        assert PDFReport.PAGE_SIZES == expected

    def test_init_default_page_size(self) -> None:
        """Test default page size is Letter."""
        report = PDFReport("Test", [])
        assert report.page_size == "Letter"

    def test_init_validates_page_size(self) -> None:
        """Test that invalid page size raises ValueError."""
        with pytest.raises(ValueError, match="Page size"):
            PDFReport("Test", [], page_size="Invalid")

    def test_init_default_header_footer(self) -> None:
        """Test default include_header and include_footer are True."""
        report = PDFReport("Test", [])
        assert report.include_header is True
        assert report.include_footer is True

    def test_prepare_extends_parent(self) -> None:
        """Test _prepare() extends parent's result."""
        report = PDFReport("Test", [])
        result = report._prepare()
        assert "PDF Report: Test" in result
        assert "Page Size: Letter" in result

    def test_format_includes_header_when_enabled(self) -> None:
        """Test _format() includes header when enabled."""
        report = PDFReport("Test Title", [], include_header=True)
        result = report._format()
        assert "Header: Test Title" in result

    def test_format_excludes_header_when_disabled(self) -> None:
        """Test _format() excludes header when disabled."""
        report = PDFReport("Test Title", [], include_header=False)
        result = report._format()
        assert "Header:" not in result

    def test_finalize_includes_footer_when_enabled(self) -> None:
        """Test _finalize() includes footer when enabled."""
        report = PDFReport("Test", [{}] * 5, include_footer=True)
        result = report._finalize()
        assert "Footer: Page 1 of 1" in result

    def test_finalize_calculates_pages(self) -> None:
        """Test _finalize() calculates total pages correctly."""
        report = PDFReport("Test", [{}] * 25, include_footer=True)
        result = report._finalize()
        assert "of 3" in result  # 25 records / 10 per page = 3 pages

    def test_get_page_size_returns_value(self) -> None:
        """Test get_page_size() returns page size."""
        report = PDFReport("Test", [], page_size="A4")
        assert report.get_page_size() == "A4"

    def test_inheritance_from_report_generator(self) -> None:
        """Test that PDFReport inherits from ReportGenerator."""
        assert issubclass(PDFReport, ReportGenerator)


class TestCSVReport:
    """Tests for CSVReport class."""

    def test_init_default_delimiter(self) -> None:
        """Test default delimiter is comma."""
        report = CSVReport("Test", [])
        assert report.delimiter == ","

    def test_init_default_header_quote(self) -> None:
        """Test default include_header is True and quote_all is False."""
        report = CSVReport("Test", [])
        assert report.include_header is True
        assert report.quote_all is False

    def test_prepare_extends_parent(self) -> None:
        """Test _prepare() extends parent's result."""
        report = CSVReport("Test", [])
        result = report._prepare()
        assert result == "CSV Report: Test"

    def test_format_includes_header(self) -> None:
        """Test _format() includes header row."""
        data = [{"name": "Alice", "value": 100}]
        report = CSVReport("Test", data, include_header=True)
        result = report._format()
        assert "Header: name,value" in result

    def test_format_uses_custom_delimiter(self) -> None:
        """Test _format() uses custom delimiter."""
        data = [{"name": "Alice", "value": 100}]
        report = CSVReport("Test", data, delimiter=";")
        result = report._format()
        assert "Header: name;value" in result

    def test_format_includes_data_rows(self) -> None:
        """Test _format() includes data rows."""
        data = [{"name": "Alice", "value": 100}]
        report = CSVReport("Test", data)
        result = report._format()
        assert "Row 1: Alice,100" in result

    def test_format_quotes_when_enabled(self) -> None:
        """Test _format() quotes all fields when quote_all is True."""
        data = [{"name": "Alice", "value": 100}]
        report = CSVReport("Test", data, quote_all=True)
        result = report._format()
        assert '"name","value"' in result
        assert '"Alice","100"' in result

    def test_format_handles_empty_data(self) -> None:
        """Test _format() handles empty data."""
        report = CSVReport("Test", [])
        result = report._format()
        assert result == "No data"

    def test_get_delimiter_returns_value(self) -> None:
        """Test get_delimiter() returns delimiter."""
        report = CSVReport("Test", [], delimiter="|")
        assert report.get_delimiter() == "|"

    def test_inheritance_from_report_generator(self) -> None:
        """Test that CSVReport inherits from ReportGenerator."""
        assert issubclass(CSVReport, ReportGenerator)


class TestHTMLReport:
    """Tests for HTMLReport class."""

    def test_init_default_css(self) -> None:
        """Test default include_css is True and table_class is set."""
        report = HTMLReport("Test", [])
        assert report.include_css is True
        assert report.table_class == "report-table"

    def test_prepare_includes_doctype(self) -> None:
        """Test _prepare() includes DOCTYPE."""
        report = HTMLReport("Test", [])
        result = report._prepare()
        assert "<!DOCTYPE html>" in result
        assert "<title>Test</title>" in result

    def test_prepare_includes_css_when_enabled(self) -> None:
        """Test _prepare() includes CSS when enabled."""
        report = HTMLReport("Test", [], include_css=True)
        result = report._prepare()
        assert "<style>" in result

    def test_prepare_excludes_css_when_disabled(self) -> None:
        """Test _prepare() excludes CSS when disabled."""
        report = HTMLReport("Test", [], include_css=False)
        result = report._prepare()
        assert "<style>" not in result

    def test_format_includes_table(self) -> None:
        """Test _format() includes table structure."""
        data = [{"name": "Alice", "value": 100}]
        report = HTMLReport("Test", data)
        result = report._format()
        assert '<table class="report-table">' in result
        assert "<thead>" in result
        assert "<tbody>" in result

    def test_format_includes_headers(self) -> None:
        """Test _format() includes table headers."""
        data = [{"name": "Alice", "value": 100}]
        report = HTMLReport("Test", data)
        result = report._format()
        assert "<th>name</th>" in result
        assert "<th>value</th>" in result

    def test_format_includes_data(self) -> None:
        """Test _format() includes table data."""
        data = [{"name": "Alice", "value": 100}]
        report = HTMLReport("Test", data)
        result = report._format()
        assert "<td>Alice</td>" in result
        assert "<td>100</td>" in result

    def test_format_handles_empty_data(self) -> None:
        """Test _format() handles empty data."""
        report = HTMLReport("Test", [])
        result = report._format()
        assert "<p>No data available</p>" in result

    def test_finalize_closes_tags(self) -> None:
        """Test _finalize() closes HTML tags."""
        report = HTMLReport("Test", [])
        result = report._finalize()
        assert "</body>" in result
        assert "</html>" in result

    def test_generate_returns_complete_document(self) -> None:
        """Test generate() returns complete HTML document."""
        data = [{"name": "Alice"}]
        report = HTMLReport("My Report", data)
        result = report.generate()
        assert "<!DOCTYPE html>" in result
        assert "<h1>My Report</h1>" in result
        assert "<table" in result
        assert "</html>" in result

    def test_inheritance_from_report_generator(self) -> None:
        """Test that HTMLReport inherits from ReportGenerator."""
        assert issubclass(HTMLReport, ReportGenerator)
