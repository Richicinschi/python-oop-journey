"""Tests for Problem 02: Report Renderer Dispatch."""

from __future__ import annotations

import json

import pytest
from week04_oop_intermediate.solutions.day05.problem_02_report_renderer_dispatch import (
    HTMLRenderer,
    JSONRenderer,
    PDFRenderer,
    Report,
    ReportGenerator,
    ReportRenderer,
)


class TestReport:
    """Tests for Report class."""

    def test_report_creation(self) -> None:
        data = {"sales": 1000, "profit": 200}
        report = Report("Q1 Report", data)
        assert report.title == "Q1 Report"
        assert report.data == data

    def test_get_summary(self) -> None:
        data = {"a": 1, "b": 2, "c": 3}
        report = Report("Test Report", data)
        summary = report.get_summary()
        assert "Test Report" in summary
        assert "3" in summary


class TestPDFRenderer:
    """Tests for PDFRenderer class."""

    def test_render(self) -> None:
        report = Report("Sales Report", {"Q1": 100, "Q2": 200})
        renderer = PDFRenderer()
        output = renderer.render(report)
        assert "=== PDF Report: Sales Report ===" in output
        assert "Q1: 100" in output
        assert "Q2: 200" in output
        assert "[PDF Content]" in output
        assert "[End PDF]" in output

    def test_mime_type(self) -> None:
        renderer = PDFRenderer()
        assert renderer.get_mime_type() == "application/pdf"

    def test_is_renderer(self) -> None:
        renderer = PDFRenderer()
        assert isinstance(renderer, ReportRenderer)


class TestHTMLRenderer:
    """Tests for HTMLRenderer class."""

    def test_render(self) -> None:
        report = Report("Sales Report", {"Q1": 100, "Q2": 200})
        renderer = HTMLRenderer()
        output = renderer.render(report)
        assert "<html>" in output
        assert "<body>" in output
        assert "<h1>Sales Report</h1>" in output
        assert "<ul>" in output
        assert "<li>Q1: 100</li>" in output
        assert "</body></html>" in output

    def test_mime_type(self) -> None:
        renderer = HTMLRenderer()
        assert renderer.get_mime_type() == "text/html"


class TestJSONRenderer:
    """Tests for JSONRenderer class."""

    def test_render(self) -> None:
        report = Report("Sales Report", {"Q1": 100, "Q2": 200})
        renderer = JSONRenderer()
        output = renderer.render(report)
        data = json.loads(output)
        assert data["title"] == "Sales Report"
        assert data["data"]["Q1"] == 100
        assert data["data"]["Q2"] == 200

    def test_mime_type(self) -> None:
        renderer = JSONRenderer()
        assert renderer.get_mime_type() == "application/json"


class TestReportGenerator:
    """Tests for ReportGenerator class."""

    def test_generate_with_pdf(self) -> None:
        report = Report("Test", {"value": 42})
        generator = ReportGenerator(PDFRenderer())
        output = generator.generate(report)
        assert "PDF Report" in output

    def test_generate_with_html(self) -> None:
        report = Report("Test", {"value": 42})
        generator = ReportGenerator(HTMLRenderer())
        output = generator.generate(report)
        assert "<html>" in output

    def test_generate_with_json(self) -> None:
        report = Report("Test", {"value": 42})
        generator = ReportGenerator(JSONRenderer())
        output = generator.generate(report)
        data = json.loads(output)
        assert data["title"] == "Test"

    def test_set_renderer(self) -> None:
        generator = ReportGenerator(PDFRenderer())
        generator.set_renderer(HTMLRenderer())
        assert generator.get_output_format() == "text/html"

    def test_get_output_format(self) -> None:
        generator = ReportGenerator(JSONRenderer())
        assert generator.get_output_format() == "application/json"

    def test_polymorphic_generation(self) -> None:
        """Test that generator works polymorphically with all renderers."""
        report = Report("Polymorphic Test", {"key": "value"})
        renderers = [PDFRenderer(), HTMLRenderer(), JSONRenderer()]
        for renderer in renderers:
            generator = ReportGenerator(renderer)
            output = generator.generate(report)
            assert len(output) > 0
            assert isinstance(output, str)
