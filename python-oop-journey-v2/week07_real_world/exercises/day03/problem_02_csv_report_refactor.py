"""Problem 02: CSV Report Generator Refactor

Topic: Refactoring Script to Classes
Difficulty: Medium

Refactor a script-style CSV report generator into an object-oriented design.

BEFORE (Procedural Script):
    records = read_sales_data("sales.csv")
    total = calculate_total_sales(records)
    by_region = calculate_sales_by_region(records)
    generate_report(records, "report.csv")

AFTER (OOP):
    data = SalesData.from_csv("sales.csv")
    formatter = CSVReportFormatter()
    generator = ReportGenerator(formatter)
    generator.generate_to_file(data, "report.csv")

Your task:
1. Create SalesRecord as an immutable value object
2. Create SalesData class to encapsulate data and queries
3. Create ReportFormatter ABC with CSVReportFormatter implementation
4. Create ReportGenerator to orchestrate report creation
5. Support filtering and data transformation methods
"""

from __future__ import annotations

import csv
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


# ============================================================================
# PROCEDURAL CODE (Before) - DO NOT MODIFY
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
# YOUR IMPLEMENTATION (After) - TODO: Implement these classes
# ============================================================================


@dataclass(frozen=True)
class SalesRecord:
    """Immutable sales record value object.
    
    Attributes:
        id: Unique record identifier
        region: Sales region (e.g., "North", "South")
        amount: Sale amount (must be non-negative)
        date: Date string (ISO format preferred)
    
    TODO:
    1. Define fields with type hints
    2. Add __post_init__ validation for amount >= 0
    3. Implement from_dict class method to create from CSV row
    """
    
    def __post_init__(self) -> None:
        """TODO: Validate amount >= 0."""
        raise NotImplementedError("Implement validation")
    
    @classmethod
    def from_dict(cls, data: dict[str, str]) -> SalesRecord:
        """TODO: Create SalesRecord from dictionary (CSV row).
        
        Expected keys: id, region, amount, date
        amount should be converted to float
        """
        raise NotImplementedError("Implement from_dict")


class SalesData:
    """Encapsulates sales data with query methods.
    
    This is the main data container that replaces the list[dict]
    from the procedural approach.
    
    TODO:
    1. Accept list[SalesRecord] in __init__
    2. Implement from_csv class method
    3. Implement total_sales property
    4. Implement sales_by_region method
    5. Implement filter_by_region method
    6. Implement sales_by_date_range method
    """
    
    def __init__(self, records: list[SalesRecord]) -> None:
        """TODO: Initialize with list of SalesRecord."""
        raise NotImplementedError("Implement __init__")
    
    @classmethod
    def from_csv(cls, filepath: str) -> SalesData:
        """TODO: Load sales data from CSV file.
        
        1. Open and read CSV file
        2. Convert each row to SalesRecord using from_dict
        3. Return new SalesData instance
        """
        raise NotImplementedError("Implement from_csv")
    
    @property
    def records(self) -> tuple[SalesRecord, ...]:
        """TODO: Return immutable view of records."""
        raise NotImplementedError("Implement records property")
    
    @property
    def total_sales(self) -> float:
        """TODO: Return sum of all amounts."""
        raise NotImplementedError("Implement total_sales")
    
    def sales_by_region(self) -> dict[str, float]:
        """TODO: Return dict mapping region to total sales.
        
        Example: {"North": 1500.0, "South": 2300.0}
        """
        raise NotImplementedError("Implement sales_by_region")
    
    def filter_by_region(self, region: str) -> SalesData:
        """TODO: Return new SalesData with only records from region.
        
        This creates a new instance - original is unchanged.
        """
        raise NotImplementedError("Implement filter_by_region")
    
    def sales_by_date_range(self, start: str, end: str) -> SalesData:
        """TODO: Filter records by date range [start, end], return new SalesData.
        
        Date format should match the stored date format.
        """
        raise NotImplementedError("Implement sales_by_date_range")
    
    def __len__(self) -> int:
        """TODO: Return number of records."""
        raise NotImplementedError("Implement __len__")


class ReportFormatter(ABC):
    """Abstract base class for report formatters.
    
    This defines the Strategy pattern for different output formats.
    
    TODO:
    1. Make this an ABC
    2. Define abstract format method
    """
    
    @abstractmethod
    def format(self, data: SalesData) -> str:
        """TODO: Format SalesData as string.
        
        Args:
            data: SalesData to format
            
        Returns:
            Formatted report string
        """
        raise NotImplementedError("Implement format")


class CSVReportFormatter(ReportFormatter):
    """Format reports as CSV.
    
    TODO:
    1. Inherit from ReportFormatter
    2. Implement format to output CSV with:
       - Header: Metric,Value
       - Row: Total Sales, $X.XX
       - Empty line
       - Header: Region,Sales
       - Rows for each region sorted alphabetically
    """
    
    def format(self, data: SalesData) -> str:
        """TODO: Format as CSV string."""
        raise NotImplementedError("Implement CSV formatting")


class MarkdownReportFormatter(ReportFormatter):
    """Format reports as Markdown table.
    
    TODO:
    1. Inherit from ReportFormatter
    2. Implement format to output Markdown:
       # Sales Report
       
       ## Summary
       | Metric | Value |
       |--------|-------|
       | Total Sales | $X.XX |
       
       ## By Region
       | Region | Sales |
       |--------|-------|
       | North | $X.XX |
       | ... | ... |
    """
    
    def format(self, data: SalesData) -> str:
        """TODO: Format as Markdown string."""
        raise NotImplementedError("Implement Markdown formatting")


class ReportGenerator:
    """High-level report generation orchestrator.
    
    Uses composition to work with any ReportFormatter.
    
    TODO:
    1. Accept formatter in __init__ and store it
    2. Implement generate method that returns formatted string
    3. Implement generate_to_file method that writes to file
    """
    
    def __init__(self, formatter: ReportFormatter) -> None:
        """TODO: Initialize with formatter strategy."""
        raise NotImplementedError("Implement __init__")
    
    def generate(self, data: SalesData) -> str:
        """TODO: Generate report using the formatter."""
        raise NotImplementedError("Implement generate")
    
    def generate_to_file(self, data: SalesData, filepath: str) -> None:
        """TODO: Generate report and write to file.
        
        Use Path(filepath).write_text()
        """
        raise NotImplementedError("Implement generate_to_file")
