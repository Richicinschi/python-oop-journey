"""Reference solution for Problem 01: Template Report Pipeline."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import override


class ReportGenerator(ABC):
    """Abstract base class for report generators using Template Method pattern."""
    
    def __init__(self, report_name: str) -> None:
        self.report_name = report_name
    
    def generate_report(self, data_source: str) -> str:
        """Template method defining the report generation algorithm."""
        raw_data = self._collect_data(data_source)
        processed_data = self._process_data(raw_data)
        formatted = self._format_report(processed_data)
        result = self._export(formatted)
        return result
    
    @abstractmethod
    def _collect_data(self, source: str) -> list[dict]:
        """Step 1: Collect raw data from source."""
        pass
    
    @abstractmethod
    def _format_report(self, data: list[dict]) -> str:
        """Step 3: Format the processed data into report format."""
        pass
    
    def _process_data(self, raw_data: list[dict]) -> list[dict]:
        """Step 2: Process and analyze raw data.
        
        Hook method with default implementation - sorts by 'name' if present.
        """
        if raw_data and 'name' in raw_data[0]:
            return sorted(raw_data, key=lambda x: x.get('name', ''))
        return raw_data
    
    def _export(self, content: str) -> str:
        """Step 4: Export the formatted report.
        
        Hook method with default implementation.
        """
        return f"Report '{self.report_name}' exported: {len(content)} bytes"


class PDFReportGenerator(ReportGenerator):
    """Generates reports in PDF format."""
    
    @override
    def _collect_data(self, source: str) -> list[dict]:
        return [
            {"name": f"PDF_Item_{i}", "value": i * 10, "source": source}
            for i in range(1, 4)
        ]
    
    @override
    def _format_report(self, data: list[dict]) -> str:
        lines = ["=== PDF Report ===", f"Name: {self.report_name}", ""]
        for item in data:
            lines.append(f"- {item['name']}: {item['value']}")
        lines.append("=== End ===")
        return "\n".join(lines)
    
    @override
    def _export(self, content: str) -> str:
        return f"PDF Export: {self.report_name} - {len(content)} bytes"


class CSVReportGenerator(ReportGenerator):
    """Generates reports in CSV format."""
    
    @override
    def _collect_data(self, source: str) -> list[dict]:
        return [
            {"id": 1, "name": "Alpha", "value": 100},
            {"id": 2, "name": "Beta", "value": -50},
            {"id": 3, "name": "Gamma", "value": 75},
        ]
    
    @override
    def _process_data(self, raw_data: list[dict]) -> list[dict]:
        return [item for item in raw_data if item.get('value', 0) >= 0]
    
    @override
    def _format_report(self, data: list[dict]) -> str:
        if not data:
            return "id,name,value"
        headers = list(data[0].keys())
        lines = [",".join(headers)]
        for item in data:
            lines.append(",".join(str(item.get(h, '')) for h in headers))
        return "\n".join(lines)


class HTMLReportGenerator(ReportGenerator):
    """Generates reports in HTML format."""
    
    @override
    def _collect_data(self, source: str) -> list[dict]:
        return [
            {"name": "Item A", "value": 50},
            {"name": "Item B", "value": 150},
            {"name": "Item C", "value": 25},
        ]
    
    @override
    def _process_data(self, raw_data: list[dict]) -> list[dict]:
        processed = []
        for item in raw_data:
            new_item = dict(item)
            value = item.get('value', 0)
            if value > 100:
                new_item['status'] = 'high'
            elif value > 50:
                new_item['status'] = 'medium'
            else:
                new_item['status'] = 'low'
            processed.append(new_item)
        return processed
    
    @override
    def _format_report(self, data: list[dict]) -> str:
        lines = [
            "<html>",
            "<head><title>{}</title></head>".format(self.report_name),
            "<body>",
            f"<h1>{self.report_name}</h1>",
            "<table>",
            "<tr><th>Name</th><th>Value</th><th>Status</th></tr>"
        ]
        for item in data:
            lines.append(
                f"<tr><td>{item['name']}</td><td>{item['value']}</td>"
                f"<td>{item['status']}</td></tr>"
            )
        lines.extend(["</table>", "</body>", "</html>"])
        return "\n".join(lines)
    
    @override
    def _export(self, content: str) -> str:
        return f"HTML Export: {self.report_name} - {len(content)} bytes"
