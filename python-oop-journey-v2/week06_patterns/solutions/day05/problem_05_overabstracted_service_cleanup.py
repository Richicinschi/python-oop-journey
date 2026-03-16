"""Problem 05: Overabstracted Service Cleanup - Solution.

Simplifies over-engineered framework to clean, direct implementations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class TaskOutcome:
    """Result of task execution."""
    success: bool
    data: Any
    message: str
    execution_time_ms: float | None = None


class SimpleTaskRunner:
    """Simple, direct task runner without over-abstraction."""
    
    def __init__(self, task: Callable[[], Any]) -> None:
        self._task = task
        self._execution_count = 0
    
    def run(self) -> TaskOutcome:
        """Execute the task."""
        try:
            result = self._task()
            self._execution_count += 1
            return TaskOutcome(
                success=True,
                data=result,
                message=str(result) if result else "Task completed successfully",
            )
        except Exception as e:
            return TaskOutcome(
                success=False,
                data=None,
                message=f"Task failed: {e}",
            )
    
    def get_execution_count(self) -> int:
        return self._execution_count


class TaskWithInput:
    """Task that accepts input parameters."""
    
    def __init__(self, task_func: Callable[[dict[str, Any]], Any]) -> None:
        self._task_func = task_func
    
    def run(self, input_data: dict[str, Any]) -> TaskOutcome:
        """Execute the task with input data."""
        try:
            result = self._task_func(input_data)
            return TaskOutcome(
                success=True,
                data=result,
                message=str(result) if result else "Task completed",
            )
        except Exception as e:
            return TaskOutcome(
                success=False,
                data=None,
                message=f"Task failed: {e}",
            )


class ValidatedTask:
    """Task with validation - composed, not inherited."""
    
    def __init__(
        self,
        task_func: Callable[[dict[str, Any]], Any],
        validator: Callable[[dict[str, Any]], tuple[bool, str]],
    ) -> None:
        self._task_func = task_func
        self._validator = validator
    
    def run(self, input_data: dict[str, Any]) -> TaskOutcome:
        """Execute with validation."""
        is_valid, error_message = self._validator(input_data)
        if not is_valid:
            return TaskOutcome(
                success=False,
                data=None,
                message=f"Validation failed: {error_message}",
            )
        
        try:
            result = self._task_func(input_data)
            return TaskOutcome(
                success=True,
                data=result,
                message=str(result) if result else "Task completed",
            )
        except Exception as e:
            return TaskOutcome(
                success=False,
                data=None,
                message=f"Task failed: {e}",
            )


class DataProcessor:
    """Simple data processor - direct implementation."""
    
    def __init__(self) -> None:
        self._processed_count = 0
        self._failed_count = 0
    
    def process_item(self, item: dict[str, Any]) -> dict[str, Any]:
        """Process a single data item."""
        try:
            result = {
                "original": item,
                "processed": True,
                "timestamp": "2024-01-01T00:00:00",
            }
            self._processed_count += 1
            return result
        except Exception:
            self._failed_count += 1
            raise
    
    def process_batch(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Process multiple items."""
        results = []
        for item in items:
            try:
                results.append(self.process_item(item))
            except Exception:
                self._failed_count += 1
                results.append({"original": item, "error": True})
        return results
    
    def get_stats(self) -> dict[str, int]:
        """Get processing statistics."""
        return {
            "processed": self._processed_count,
            "failed": self._failed_count,
        }


class ReportGenerator:
    """Simple report generator - no over-engineering."""
    
    def __init__(self, title: str) -> None:
        self._title = title
        self._sections: list[dict[str, Any]] = []
    
    def add_section(self, heading: str, content: str) -> None:
        """Add a section to the report."""
        self._sections.append({
            "type": "text",
            "heading": heading,
            "content": content,
        })
    
    def add_data_table(self, headers: list[str], rows: list[list[Any]]) -> None:
        """Add a data table to the report."""
        self._sections.append({
            "type": "table",
            "headers": headers,
            "rows": rows,
        })
    
    def generate(self) -> str:
        """Generate the final report."""
        lines = [f"# {self._title}", ""]
        
        for section in self._sections:
            if section["type"] == "text":
                lines.append(f"## {section['heading']}")
                lines.append(section["content"])
                lines.append("")
            elif section["type"] == "table":
                lines.append(f"| {' | '.join(section['headers'])} |")
                lines.append(f"| {' | '.join(['---'] * len(section['headers']))} |")
                for row in section["rows"]:
                    lines.append(f"| {' | '.join(str(cell) for cell in row)} |")
                lines.append("")
        
        return "\n".join(lines)
    
    def get_section_count(self) -> int:
        """Get number of sections in report."""
        return len(self._sections)
