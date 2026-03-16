"""Reference solution for Problem 05: Report Generators."""

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
        if not title:
            raise ValueError("Title cannot be empty")
        if not isinstance(data, list):
            raise ValueError("Data must be a list")
        self.title = title
        self.data = data

    def generate(self) -> str:
        """Template method that defines the report generation algorithm."""
        parts = [
            self._prepare(),
            self._format(),
            self._finalize(),
        ]
        return "\n".join(parts)

    def _prepare(self) -> str:
        """Prepare step - setup and initial processing."""
        return f"Report: {self.title}"

    def _format(self) -> str:
        """Format step - format the data."""
        return f"Records: {len(self.data)}"

    def _finalize(self) -> str:
        """Finalize step - final processing."""
        return "---"

    def get_record_count(self) -> int:
        """Return number of records in report."""
        return len(self.data)


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
        """Initialize PDF report."""
        super().__init__(title, data)
        if page_size not in self.PAGE_SIZES:
            raise ValueError(f"Page size must be one of {self.PAGE_SIZES}")
        self.page_size = page_size
        self.include_header = include_header
        self.include_footer = include_footer

    def _prepare(self) -> str:
        """Prepare PDF with page size info."""
        base = super()._prepare()
        return f"PDF {base}\nPage Size: {self.page_size}"

    def _format(self) -> str:
        """Format PDF content with header."""
        base = super()._format()
        if self.include_header:
            return f"{base}\nHeader: {self.title}"
        return base

    def _finalize(self) -> str:
        """Finalize PDF with footer."""
        base = super()._finalize()
        if self.include_footer:
            total_pages = max(1, (len(self.data) + 9) // 10)
            return f"Footer: Page 1 of {total_pages}"
        return base

    def get_page_size(self) -> str:
        """Return page size."""
        return self.page_size


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
        """Initialize CSV report."""
        super().__init__(title, data)
        self.delimiter = delimiter
        self.include_header = include_header
        self.quote_all = quote_all

    def _prepare(self) -> str:
        """Prepare CSV report info."""
        base = super()._prepare()
        return f"CSV {base}"

    def _format(self) -> str:
        """Format CSV content."""
        lines = []
        
        if self.data:
            headers = list(self.data[0].keys())
            
            if self.include_header:
                header_line = self.delimiter.join(headers)
                if self.quote_all:
                    header_line = self.delimiter.join(f'"{h}"' for h in headers)
                lines.append(f"Header: {header_line}")
            
            for i, record in enumerate(self.data, 1):
                values = [str(record.get(h, "")) for h in headers]
                row_line = self.delimiter.join(values)
                if self.quote_all:
                    row_line = self.delimiter.join(f'"{v}"' for v in values)
                lines.append(f"Row {i}: {row_line}")
        
        return "\n".join(lines) if lines else "No data"

    def _finalize(self) -> str:
        """Finalize CSV report."""
        base = super()._finalize()
        if self.quote_all:
            return f"{base}\nQuoted: true"
        return base

    def get_delimiter(self) -> str:
        """Return delimiter character."""
        return self.delimiter


class HTMLReport(ReportGenerator):
    """HTML report generator with table formatting."""

    def __init__(
        self,
        title: str,
        data: list[dict[str, object]],
        include_css: bool = True,
        table_class: str = "report-table"
    ) -> None:
        """Initialize HTML report."""
        super().__init__(title, data)
        self.include_css = include_css
        self.table_class = table_class

    def _prepare(self) -> str:
        """Prepare HTML with DOCTYPE and head."""
        css = ""
        if self.include_css:
            css = """<style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>"""
        
        return f"""<!DOCTYPE html>
<html>
<head><title>{self.title}</title>{css}</head>"""

    def _format(self) -> str:
        """Format HTML body with table."""
        lines = ["<body>", f"<h1>{self.title}</h1>"]
        
        if self.data:
            lines.append(f'<table class="{self.table_class}">')
            
            # Header
            headers = list(self.data[0].keys())
            lines.append("<thead><tr>")
            for h in headers:
                lines.append(f"<th>{h}</th>")
            lines.append("</tr></thead>")
            
            # Body
            lines.append("<tbody>")
            for record in self.data:
                lines.append("<tr>")
                for h in headers:
                    lines.append(f"<td>{record.get(h, '')}</td>")
                lines.append("</tr>")
            lines.append("</tbody>")
            
            lines.append("</table>")
        else:
            lines.append("<p>No data available</p>")
        
        return "\n".join(lines)

    def _finalize(self) -> str:
        """Finalize HTML with closing tags."""
        return "</body>\n</html>"

    def generate(self) -> str:
        """Generate complete HTML document."""
        return super().generate()
