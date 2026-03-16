"""Reference solution for Problem 02: CSV Report Generator Refactor."""

from __future__ import annotations

import csv
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


# ============================================================================
# PROCEDURAL CODE (Before) - Kept for reference
# ============================================================================

def read_sales_data_procedural(filepath: str) -> list[dict]:
    """Read sales data from CSV file."""
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def calculate_total_sales_procedural(records: list[dict]) -> float:
    """Sum all sales amounts."""
    return sum(float(r["amount"]) for r in records)


def calculate_sales_by_region_procedural(records: list[dict]) -> dict[str, float]:
    """Aggregate sales by region."""
    totals: dict[str, float] = {}
    for record in records:
        region = record["region"]
        amount = float(record["amount"])
        totals[region] = totals.get(region, 0.0) + amount
    return totals


def generate_report_procedural(data_file: str, output_file: str) -> None:
    """Generate a sales report."""
    records = read_sales_data_procedural(data_file)
    total = calculate_total_sales_procedural(records)
    by_region = calculate_sales_by_region_procedural(records)
    
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total Sales", f"${total:.2f}"])
        writer.writerow([])
        writer.writerow(["Region", "Sales"])
        for region, amount in sorted(by_region.items()):
            writer.writerow([region, f"${amount:.2f}"])


# ============================================================================
# OOP IMPLEMENTATION (After)
# ============================================================================


@dataclass(frozen=True)
class SalesRecord:
    """Immutable sales record value object."""
    
    id: str
    region: str
    amount: float
    date: str
    
    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError(f"Amount cannot be negative: {self.amount}")
    
    @classmethod
    def from_dict(cls, data: dict[str, str]) -> SalesRecord:
        return cls(
            id=data["id"],
            region=data["region"],
            amount=float(data["amount"]),
            date=data["date"],
        )


class SalesData:
    """Encapsulates sales data with query methods."""
    
    def __init__(self, records: list[SalesRecord]) -> None:
        self._records = records
    
    @classmethod
    def from_csv(cls, filepath: str) -> SalesData:
        with open(filepath, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        return cls([SalesRecord.from_dict(r) for r in rows])
    
    @property
    def records(self) -> tuple[SalesRecord, ...]:
        return tuple(self._records)
    
    @property
    def total_sales(self) -> float:
        return sum(r.amount for r in self._records)
    
    def sales_by_region(self) -> dict[str, float]:
        totals: dict[str, float] = {}
        for record in self._records:
            totals[record.region] = totals.get(record.region, 0.0) + record.amount
        return totals
    
    def filter_by_region(self, region: str) -> SalesData:
        filtered = [r for r in self._records if r.region == region]
        return SalesData(filtered)
    
    def sales_by_date_range(self, start: str, end: str) -> SalesData:
        filtered = [r for r in self._records if start <= r.date <= end]
        return SalesData(filtered)
    
    def __len__(self) -> int:
        return len(self._records)


class ReportFormatter(ABC):
    """Abstract base class for report formatters."""
    
    @abstractmethod
    def format(self, data: SalesData) -> str:
        """Format SalesData as string."""
        pass


class CSVReportFormatter(ReportFormatter):
    """Format reports as CSV."""
    
    def format(self, data: SalesData) -> str:
        lines = []
        lines.append("Metric,Value")
        lines.append(f"Total Sales,${data.total_sales:.2f}")
        lines.append("")
        lines.append("Region,Sales")
        for region, amount in sorted(data.sales_by_region().items()):
            lines.append(f"{region},${amount:.2f}")
        return "\n".join(lines)


class MarkdownReportFormatter(ReportFormatter):
    """Format reports as Markdown table."""
    
    def format(self, data: SalesData) -> str:
        lines = ["# Sales Report", ""]
        lines.extend(["## Summary", "| Metric | Value |", "|--------|-------|"])
        lines.append(f"| Total Sales | ${data.total_sales:.2f} |")
        lines.extend(["", "## By Region", "| Region | Sales |", "|--------|-------|"])
        for region, amount in sorted(data.sales_by_region().items()):
            lines.append(f"| {region} | ${amount:.2f} |")
        return "\n".join(lines)


class ReportGenerator:
    """High-level report generation orchestrator."""
    
    def __init__(self, formatter: ReportFormatter) -> None:
        self._formatter = formatter
    
    def generate(self, data: SalesData) -> str:
        return self._formatter.format(data)
    
    def generate_to_file(self, data: SalesData, filepath: str) -> None:
        Path(filepath).write_text(self.generate(data), encoding="utf-8")
