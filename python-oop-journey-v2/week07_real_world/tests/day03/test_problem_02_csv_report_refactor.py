"""Tests for Problem 02: CSV Report Generator Refactor."""

from __future__ import annotations

import csv
import os
import tempfile

import pytest

from week07_real_world.solutions.day03.problem_02_csv_report_refactor import (
    SalesRecord,
    SalesData,
    ReportFormatter,
    CSVReportFormatter,
    MarkdownReportFormatter,
    ReportGenerator,
    read_sales_data_procedural,
    calculate_total_sales_procedural,
    calculate_sales_by_region_procedural,
)


@pytest.fixture
def sample_csv_file():
    """Create a temporary CSV file with sample data."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "region", "amount", "date"])
        writer.writerow(["1", "North", "100.00", "2024-01-15"])
        writer.writerow(["2", "South", "200.00", "2024-01-16"])
        writer.writerow(["3", "North", "150.00", "2024-01-17"])
        writer.writerow(["4", "East", "300.00", "2024-01-18"])
        filepath = f.name
    
    yield filepath
    
    os.unlink(filepath)


@pytest.fixture
def sample_records():
    """Return list of sample SalesRecords."""
    return [
        SalesRecord("1", "North", 100.0, "2024-01-15"),
        SalesRecord("2", "South", 200.0, "2024-01-16"),
        SalesRecord("3", "North", 150.0, "2024-01-17"),
        SalesRecord("4", "East", 300.0, "2024-01-18"),
    ]


class TestSalesRecord:
    """Tests for SalesRecord value object."""
    
    def test_creation(self) -> None:
        record = SalesRecord("1", "North", 100.0, "2024-01-15")
        assert record.id == "1"
        assert record.region == "North"
        assert record.amount == 100.0
        assert record.date == "2024-01-15"
    
    def test_negative_amount_raises(self) -> None:
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            SalesRecord("1", "North", -100.0, "2024-01-15")
    
    def test_zero_amount_allowed(self) -> None:
        record = SalesRecord("1", "North", 0.0, "2024-01-15")
        assert record.amount == 0.0
    
    def test_from_dict(self) -> None:
        data = {"id": "1", "region": "North", "amount": "100.50", "date": "2024-01-15"}
        record = SalesRecord.from_dict(data)
        assert record.id == "1"
        assert record.region == "North"
        assert record.amount == 100.50
        assert record.date == "2024-01-15"
    
    def test_immutable(self) -> None:
        record = SalesRecord("1", "North", 100.0, "2024-01-15")
        with pytest.raises(AttributeError):
            record.amount = 200.0


class TestSalesData:
    """Tests for SalesData class."""
    
    def test_init(self, sample_records) -> None:
        data = SalesData(sample_records)
        assert len(data) == 4
        assert len(data.records) == 4
    
    def test_from_csv(self, sample_csv_file) -> None:
        data = SalesData.from_csv(sample_csv_file)
        assert len(data) == 4
        assert all(isinstance(r, SalesRecord) for r in data.records)
    
    def test_total_sales(self, sample_records) -> None:
        data = SalesData(sample_records)
        assert data.total_sales == 750.0  # 100 + 200 + 150 + 300
    
    def test_total_sales_empty(self) -> None:
        data = SalesData([])
        assert data.total_sales == 0.0
    
    def test_sales_by_region(self, sample_records) -> None:
        data = SalesData(sample_records)
        by_region = data.sales_by_region()
        assert by_region["North"] == 250.0  # 100 + 150
        assert by_region["South"] == 200.0
        assert by_region["East"] == 300.0
    
    def test_filter_by_region(self, sample_records) -> None:
        data = SalesData(sample_records)
        north_data = data.filter_by_region("North")
        
        assert len(north_data) == 2
        assert all(r.region == "North" for r in north_data.records)
        assert north_data.total_sales == 250.0
        # Original unchanged
        assert len(data) == 4
    
    def test_sales_by_date_range(self, sample_records) -> None:
        data = SalesData(sample_records)
        filtered = data.sales_by_date_range("2024-01-15", "2024-01-16")
        
        assert len(filtered) == 2
        assert filtered.total_sales == 300.0
    
    def test_records_is_immutable(self, sample_records) -> None:
        data = SalesData(sample_records)
        records = data.records
        assert isinstance(records, tuple)
        with pytest.raises(TypeError):
            records[0] = None  # type: ignore


class TestCSVReportFormatter:
    """Tests for CSVReportFormatter."""
    
    def test_format_includes_total(self, sample_records) -> None:
        formatter = CSVReportFormatter()
        data = SalesData(sample_records)
        result = formatter.format(data)
        
        assert "Total Sales,$750.00" in result
    
    def test_format_includes_regions(self, sample_records) -> None:
        formatter = CSVReportFormatter()
        data = SalesData(sample_records)
        result = formatter.format(data)
        
        assert "North,$250.00" in result
        assert "South,$200.00" in result
        assert "East,$300.00" in result
    
    def test_regions_sorted_alphabetically(self, sample_records) -> None:
        formatter = CSVReportFormatter()
        data = SalesData(sample_records)
        result = formatter.format(data)
        
        lines = result.split("\n")
        region_lines = [l for l in lines if l.startswith(("East", "North", "South"))]
        assert region_lines[0].startswith("East")
        assert region_lines[1].startswith("North")
        assert region_lines[2].startswith("South")


class TestMarkdownReportFormatter:
    """Tests for MarkdownReportFormatter."""
    
    def test_format_has_header(self, sample_records) -> None:
        formatter = MarkdownReportFormatter()
        data = SalesData(sample_records)
        result = formatter.format(data)
        
        assert "# Sales Report" in result
    
    def test_format_has_summary_table(self, sample_records) -> None:
        formatter = MarkdownReportFormatter()
        data = SalesData(sample_records)
        result = formatter.format(data)
        
        assert "## Summary" in result
        assert "| Metric | Value |" in result
        assert f"| Total Sales | ${data.total_sales:.2f} |" in result
    
    def test_format_has_region_table(self, sample_records) -> None:
        formatter = MarkdownReportFormatter()
        data = SalesData(sample_records)
        result = formatter.format(data)
        
        assert "## By Region" in result
        assert "| Region | Sales |" in result
        assert "| North | $250.00 |" in result


class TestReportGenerator:
    """Tests for ReportGenerator."""
    
    def test_generate_delegates_to_formatter(self, sample_records) -> None:
        formatter = CSVReportFormatter()
        generator = ReportGenerator(formatter)
        data = SalesData(sample_records)
        
        result = generator.generate(data)
        
        assert "Total Sales" in result
        assert "$750.00" in result
    
    def test_generate_to_file(self, sample_records) -> None:
        import tempfile
        import os
        from pathlib import Path
        
        formatter = CSVReportFormatter()
        generator = ReportGenerator(formatter)
        data = SalesData(sample_records)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            output_file = f.name
        
        try:
            generator.generate_to_file(data, output_file)
            
            assert os.path.exists(output_file)
            content = Path(output_file).read_text()
            assert "Total Sales" in content
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)


class TestReportFormatterIsABC:
    """Tests that ReportFormatter is properly abstract."""
    
    def test_cannot_instantiate_directly(self) -> None:
        with pytest.raises(TypeError):
            ReportFormatter()
    
    def test_subclass_must_implement_format(self) -> None:
        class BadFormatter(ReportFormatter):
            pass
        
        with pytest.raises(TypeError):
            BadFormatter()


class TestProceduralCompatibility:
    """Tests ensuring procedural and OOP produce same results."""
    
    def test_total_sales_match(self, sample_csv_file) -> None:
        # Procedural
        proc_records = read_sales_data_procedural(sample_csv_file)
        proc_total = calculate_total_sales_procedural(proc_records)
        
        # OOP
        oop_data = SalesData.from_csv(sample_csv_file)
        
        assert proc_total == pytest.approx(oop_data.total_sales)
    
    def test_sales_by_region_match(self, sample_csv_file) -> None:
        # Procedural
        proc_records = read_sales_data_procedural(sample_csv_file)
        proc_by_region = calculate_sales_by_region_procedural(proc_records)
        
        # OOP
        oop_data = SalesData.from_csv(sample_csv_file)
        oop_by_region = oop_data.sales_by_region()
        
        assert proc_by_region == oop_by_region
