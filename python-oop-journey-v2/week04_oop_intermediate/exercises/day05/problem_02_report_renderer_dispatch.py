"""Problem 02: Report Renderer Dispatch.

Topic: Polymorphism
Difficulty: Easy

Create different report renderers that output reports in various formats.
Demonstrate polymorphic rendering through a common ReportRenderer interface.

TODO:
1. Create ReportRenderer ABC with:
   - render(self, data: dict) -> str (abstract)
   - get_format_name(self) -> str (abstract)

2. Create JSONRenderer class:
   - render returns JSON string representation of data
   - get_format_name returns "JSON"

3. Create XMLRenderer class:
   - render returns XML string representation of data
   - get_format_name returns "XML"

4. Create MarkdownRenderer class:
   - render returns Markdown table representation of data
   - get_format_name returns "Markdown"

5. Implement render_report_to_all_formats(renderers: list, data: dict) -> dict[str, str]
   that renders data using all renderers and returns format->output mapping.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class ReportRenderer(ABC):
    """Abstract base class for report renderers."""
    
    @abstractmethod
    def render(self, data: dict) -> str:
        """Render data to string format.
        
        Args:
            data: Dictionary of data to render.
        
        Returns:
            String representation in the specific format.
        """
        raise NotImplementedError("render must be implemented")
    
    @abstractmethod
    def get_format_name(self) -> str:
        """Return the format name.
        
        Returns:
            String name of the format.
        """
        raise NotImplementedError("get_format_name must be implemented")


class JSONRenderer(ReportRenderer):
    """Renders reports as JSON."""
    
    def render(self, data: dict) -> str:
        """Render data as JSON string."""
        # TODO: Use json.dumps to convert data to JSON string
        raise NotImplementedError("Implement JSON rendering")
    
    def get_format_name(self) -> str:
        """Return format name."""
        # TODO: Return "JSON"
        raise NotImplementedError("Implement get_format_name")


class XMLRenderer(ReportRenderer):
    """Renders reports as XML."""
    
    def render(self, data: dict) -> str:
        """Render data as XML string.
        
        Format should be:
        <report>
          <key1>value1</key1>
          <key2>value2</key2>
        </report>
        """
        # TODO: Convert dict to simple XML format
        raise NotImplementedError("Implement XML rendering")
    
    def get_format_name(self) -> str:
        """Return format name."""
        # TODO: Return "XML"
        raise NotImplementedError("Implement get_format_name")


class MarkdownRenderer(ReportRenderer):
    """Renders reports as Markdown table."""
    
    def render(self, data: dict) -> str:
        """Render data as Markdown table.
        
        Format should be:
        | Key | Value |
        |-----|-------|
        | key1 | value1 |
        | key2 | value2 |
        """
        # TODO: Convert dict to Markdown table
        raise NotImplementedError("Implement Markdown rendering")
    
    def get_format_name(self) -> str:
        """Return format name."""
        # TODO: Return "Markdown"
        raise NotImplementedError("Implement get_format_name")


def render_report_to_all_formats(
    renderers: list[ReportRenderer],
    data: dict
) -> dict[str, str]:
    """Render data using all renderers polymorphically.
    
    Args:
        renderers: List of ReportRenderer instances.
        data: Dictionary of data to render.
    
    Returns:
        Dictionary mapping format names to rendered output.
    """
    # TODO: Iterate through renderers, call render() and get_format_name()
    # Build and return a dict of format_name -> rendered_output
    raise NotImplementedError("Implement render_report_to_all_formats")
