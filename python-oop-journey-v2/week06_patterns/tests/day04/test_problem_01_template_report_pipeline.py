"""Tests for Problem 01: Template Report Pipeline."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day04.problem_01_template_report_pipeline import (
    ReportGenerator,
    PDFReportGenerator,
    CSVReportGenerator,
    HTMLReportGenerator,
)


class TestReportGeneratorBase:
    """Tests for the base ReportGenerator class structure."""
    
    def test_base_class_is_abstract(self) -> None:
        """Base class should not be instantiable."""
        with pytest.raises(TypeError):
            ReportGenerator("test")
    
    def test_pdf_generator_instantiable(self) -> None:
        """PDF generator can be created."""
        gen = PDFReportGenerator("Sales Report")
        assert gen.report_name == "Sales Report"
    
    def test_csv_generator_instantiable(self) -> None:
        """CSV generator can be created."""
        gen = CSVReportGenerator("Data Export")
        assert gen.report_name == "Data Export"
    
    def test_html_generator_instantiable(self) -> None:
        """HTML generator can be created."""
        gen = HTMLReportGenerator("Dashboard")
        assert gen.report_name == "Dashboard"


class TestPDFReportGenerator:
    """Tests for PDF report generation."""
    
    def test_generate_report_returns_string(self) -> None:
        """PDF report generation returns a string result."""
        gen = PDFReportGenerator("Test")
        result = gen.generate_report("data/source")
        assert isinstance(result, str)
    
    def test_pdf_export_message_format(self) -> None:
        """PDF export includes report name and byte count."""
        gen = PDFReportGenerator("Test")
        result = gen.generate_report("source")
        assert "PDF Export" in result
        assert "Test" in result
        assert "bytes" in result
    
    def test_pdf_collects_data_with_source(self) -> None:
        """PDF collector includes source in data."""
        gen = PDFReportGenerator("Test")
        data = gen._collect_data("my_source")
        assert len(data) == 3
        assert all(item["source"] == "my_source" for item in data)
    
    def test_pdf_formats_report_with_header(self) -> None:
        """PDF format includes header structure."""
        gen = PDFReportGenerator("Test Report")
        data = [{"name": "Item", "value": 100}]
        formatted = gen._format_report(data)
        assert "PDF Report" in formatted
        assert "Test Report" in formatted
        assert "Item" in formatted


class TestCSVReportGenerator:
    """Tests for CSV report generation."""
    
    def test_csv_filters_negative_values(self) -> None:
        """CSV processing filters out negative values."""
        gen = CSVReportGenerator("Test")
        raw = [
            {"id": 1, "name": "A", "value": 100},
            {"id": 2, "name": "B", "value": -50},
            {"id": 3, "name": "C", "value": 75},
        ]
        processed = gen._process_data(raw)
        assert len(processed) == 2
        assert all(item["value"] >= 0 for item in processed)
    
    def test_csv_format_includes_headers(self) -> None:
        """CSV format includes column headers."""
        gen = CSVReportGenerator("Test")
        data = [{"id": 1, "name": "A", "value": 100}]
        formatted = gen._format_report(data)
        assert "id,name,value" in formatted
    
    def test_csv_format_comma_separated(self) -> None:
        """CSV format uses comma separation."""
        gen = CSVReportGenerator("Test")
        data = [{"id": 1, "name": "Test", "value": 100}]
        formatted = gen._format_report(data)
        lines = formatted.strip().split("\n")
        assert len(lines) == 2  # header + data
        assert "1,Test,100" in formatted


class TestHTMLReportGenerator:
    """Tests for HTML report generation."""
    
    def test_html_adds_status_field(self) -> None:
        """HTML processing adds status based on value."""
        gen = HTMLReportGenerator("Test")
        raw = [
            {"name": "Low", "value": 25},
            {"name": "Medium", "value": 75},
            {"name": "High", "value": 150},
        ]
        processed = gen._process_data(raw)
        assert processed[0]["status"] == "low"
        assert processed[1]["status"] == "medium"
        assert processed[2]["status"] == "high"
    
    def test_html_format_includes_table(self) -> None:
        """HTML format includes table structure."""
        gen = HTMLReportGenerator("Test Report")
        data = [{"name": "Item", "value": 100, "status": "high"}]
        formatted = gen._format_report(data)
        assert "<table>" in formatted
        assert "</table>" in formatted
        assert "<html>" in formatted
    
    def test_html_includes_report_name(self) -> None:
        """HTML includes report name in title and header."""
        gen = HTMLReportGenerator("Sales Dashboard")
        data = [{"name": "A", "value": 50, "status": "low"}]
        formatted = gen._format_report(data)
        assert "Sales Dashboard" in formatted


class TestTemplateMethod:
    """Tests verifying the Template Method pattern behavior."""
    
    def test_algorithm_steps_executed_in_order(self) -> None:
        """Template method executes steps in correct order."""
        steps: list[str] = []
        
        class TestGenerator(ReportGenerator):
            def _collect_data(self, source: str) -> list[dict]:
                steps.append("collect")
                return []
            
            def _process_data(self, raw_data: list[dict]) -> list[dict]:
                steps.append("process")
                return raw_data
            
            def _format_report(self, data: list[dict]) -> str:
                steps.append("format")
                return "test"
            
            def _export(self, content: str) -> str:
                steps.append("export")
                return "done"
        
        gen = TestGenerator("Test")
        gen.generate_report("source")
        
        assert steps == ["collect", "process", "format", "export"]
    
    def test_hook_can_be_overridden(self) -> None:
        """Hook methods can be overridden by subclasses."""
        class CustomGenerator(PDFReportGenerator):
            def _process_data(self, raw_data: list[dict]) -> list[dict]:
                # Custom processing - reverse order
                return list(reversed(raw_data))
        
        gen = CustomGenerator("Test")
        data = [{"name": "A"}, {"name": "B"}, {"name": "C"}]
        processed = gen._process_data(data)
        assert processed[0]["name"] == "C"
        assert processed[2]["name"] == "A"
    
    def test_inheritance_structure(self) -> None:
        """All generators inherit from ReportGenerator."""
        assert issubclass(PDFReportGenerator, ReportGenerator)
        assert issubclass(CSVReportGenerator, ReportGenerator)
        assert issubclass(HTMLReportGenerator, ReportGenerator)
