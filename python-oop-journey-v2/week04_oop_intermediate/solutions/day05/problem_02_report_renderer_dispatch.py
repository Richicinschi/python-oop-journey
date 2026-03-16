"""Reference solution for Problem 02: Report Renderer Dispatch."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
import json


class Report:
    """A report with title and data."""

    def __init__(self, title: str, data: dict[str, Any]) -> None:
        self.title = title
        self.data = data

    def get_summary(self) -> str:
        """Return a summary of the report."""
        return f"Report '{self.title}' with {len(self.data)} data items"


class ReportRenderer(ABC):
    """Abstract base for report renderers."""

    @abstractmethod
    def render(self, report: Report) -> str:
        """Render the report in the specific format."""
        pass

    @abstractmethod
    def get_mime_type(self) -> str:
        """Return the MIME type of the rendered format."""
        pass


class PDFRenderer(ReportRenderer):
    """Render reports as PDF-like text representation."""

    def render(self, report: Report) -> str:
        """Render as PDF-style text."""
        lines = [
            f"=== PDF Report: {report.title} ===",
            "[PDF Content]",
        ]
        for key, value in report.data.items():
            lines.append(f"{key}: {value}")
        lines.append("[End PDF]")
        return "\n".join(lines)

    def get_mime_type(self) -> str:
        return "application/pdf"


class HTMLRenderer(ReportRenderer):
    """Render reports as HTML."""

    def render(self, report: Report) -> str:
        """Render as HTML."""
        items = "\n".join(
            f"  <li>{key}: {value}</li>" for key, value in report.data.items()
        )
        return (
            f"<html><body>\n"
            f"<h1>{report.title}</h1>\n"
            f"<ul>\n{items}\n</ul>\n"
            f"</body></html>"
        )

    def get_mime_type(self) -> str:
        return "text/html"


class JSONRenderer(ReportRenderer):
    """Render reports as JSON."""

    def render(self, report: Report) -> str:
        """Render as JSON string."""
        output = {"title": report.title, "data": report.data}
        return json.dumps(output, indent=2)

    def get_mime_type(self) -> str:
        return "application/json"


class ReportGenerator:
    """Generator that can use any renderer polymorphically."""

    def __init__(self, renderer: ReportRenderer) -> None:
        self._renderer = renderer

    def generate(self, report: Report) -> str:
        """Generate report using the assigned renderer."""
        return self._renderer.render(report)

    def set_renderer(self, renderer: ReportRenderer) -> None:
        """Change the renderer at runtime."""
        self._renderer = renderer

    def get_output_format(self) -> str:
        """Return the MIME type of current renderer."""
        return self._renderer.get_mime_type()
