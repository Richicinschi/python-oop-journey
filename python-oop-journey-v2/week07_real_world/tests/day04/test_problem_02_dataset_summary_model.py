"""Tests for Problem 02: Dataset Summary Model."""

from __future__ import annotations

import math

import pytest

from week07_real_world.solutions.day04.problem_02_dataset_summary_model import (
    ColumnStats,
    Dataset,
)


class TestColumnStats:
    """Tests for ColumnStats dataclass."""
    
    def test_column_stats_creation(self) -> None:
        stats = ColumnStats("age", 10, 25.5, 5.2, 18.0, 65.0, 2)
        
        assert stats.name == "age"
        assert stats.count == 10
        assert stats.mean == 25.5
        assert stats.std == 5.2
        assert stats.min_val == 18.0
        assert stats.max_val == 65.0
        assert stats.null_count == 2
    
    def test_column_stats_default_null_count(self) -> None:
        stats = ColumnStats("score", 5, 85.0, 10.0, 70.0, 100.0)
        assert stats.null_count == 0
    
    def test_column_stats_range(self) -> None:
        stats = ColumnStats("age", 10, 25.5, 5.2, 18.0, 65.0)
        assert stats.range_val == 47.0  # 65 - 18
    
    def test_column_stats_range_zero(self) -> None:
        stats = ColumnStats("constant", 5, 42.0, 0.0, 42.0, 42.0)
        assert stats.range_val == 0.0
    
    def test_column_stats_immutability(self) -> None:
        stats = ColumnStats("age", 10, 25.5, 5.2, 18.0, 65.0)
        
        with pytest.raises(AttributeError):
            stats.name = "new_name"


class TestDatasetCreation:
    """Tests for Dataset creation and basic properties."""
    
    def test_empty_dataset(self) -> None:
        ds = Dataset("empty", [])
        
        assert ds.name == "empty"
        assert ds.row_count == 0
        assert ds.column_count == 0
        assert ds.columns == []
    
    def test_dataset_with_data(self) -> None:
        data = [
            {"name": "Alice", "age": 30, "salary": 50000},
            {"name": "Bob", "age": 25, "salary": 45000},
        ]
        ds = Dataset("employees", data)
        
        assert ds.name == "employees"
        assert ds.row_count == 2
        assert ds.column_count == 3
        assert set(ds.columns) == {"name", "age", "salary"}
    
    def test_get_column(self) -> None:
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        ds = Dataset("people", data)
        
        ages = ds.get_column("age")
        assert ages == [30, 25]
        
        names = ds.get_column("name")
        assert names == ["Alice", "Bob"]
    
    def test_get_column_missing(self) -> None:
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob"},  # Missing age
        ]
        ds = Dataset("people", data)
        
        ages = ds.get_column("age")
        assert ages == [30, None]


class TestDatasetFilter:
    """Tests for Dataset filtering."""
    
    def test_filter_by_condition(self) -> None:
        data = [
            {"name": "Alice", "salary": 50000},
            {"name": "Bob", "salary": 45000},
            {"name": "Charlie", "salary": 60000},
        ]
        ds = Dataset("employees", data)
        
        high_earners = ds.filter(lambda r: r["salary"] > 46000)
        
        assert high_earners.row_count == 2
        assert high_earners.name == "employees_filtered"
        
        # Original dataset unchanged
        assert ds.row_count == 3
    
    def test_filter_no_matches(self) -> None:
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        ds = Dataset("people", data)
        
        result = ds.filter(lambda r: r["age"] > 100)
        assert result.row_count == 0
    
    def test_filter_all_match(self) -> None:
        data = [
            {"name": "Alice", "active": True},
            {"name": "Bob", "active": True},
        ]
        ds = Dataset("people", data)
        
        result = ds.filter(lambda r: r["active"])
        assert result.row_count == 2
    
    def test_filter_chain(self) -> None:
        data = [
            {"name": "Alice", "age": 30, "active": True},
            {"name": "Bob", "age": 25, "active": False},
            {"name": "Charlie", "age": 35, "active": True},
        ]
        ds = Dataset("people", data)
        
        result = ds.filter(lambda r: r["active"]).filter(lambda r: r["age"] > 28)
        assert result.row_count == 2  # Alice and Charlie


class TestDatasetColumnStats:
    """Tests for Dataset column statistics."""
    
    def test_column_stats_basic(self) -> None:
        data = [
            {"age": 20},
            {"age": 30},
            {"age": 40},
        ]
        ds = Dataset("people", data)
        
        stats = ds.column_stats("age")
        
        assert stats is not None
        assert stats.name == "age"
        assert stats.count == 3
        assert stats.mean == 30.0
        assert stats.min_val == 20.0
        assert stats.max_val == 40.0
    
    def test_column_stats_with_nulls(self) -> None:
        data = [
            {"age": 20},
            {"age": None},
            {"age": 30},
            {"age": None},
        ]
        ds = Dataset("people", data)
        
        stats = ds.column_stats("age")
        
        assert stats is not None
        assert stats.count == 2  # Only non-null values
        assert stats.null_count == 2
        assert stats.mean == 25.0
    
    def test_column_stats_nonexistent_column(self) -> None:
        data = [{"age": 30}]
        ds = Dataset("people", data)
        
        stats = ds.column_stats("nonexistent")
        assert stats is None
    
    def test_column_stats_non_numeric(self) -> None:
        data = [
            {"name": "Alice"},
            {"name": "Bob"},
        ]
        ds = Dataset("people", data)
        
        stats = ds.column_stats("name")
        assert stats is None
    
    def test_column_stats_standard_deviation(self) -> None:
        data = [
            {"score": 10},
            {"score": 20},
            {"score": 30},
        ]
        ds = Dataset("scores", data)
        
        stats = ds.column_stats("score")
        
        # Population std: sqrt(((10-20)^2 + (20-20)^2 + (30-20)^2) / 3)
        # = sqrt((100 + 0 + 100) / 3) = sqrt(66.67) ≈ 8.16
        expected_std = math.sqrt(200 / 3)
        assert abs(stats.std - expected_std) < 0.01
    
    def test_summary_all_numeric_columns(self) -> None:
        data = [
            {"age": 25, "salary": 50000, "name": "Alice"},
            {"age": 30, "salary": 60000, "name": "Bob"},
        ]
        ds = Dataset("employees", data)
        
        summary = ds.summary()
        
        # Should only include numeric columns
        assert "age" in summary
        assert "salary" in summary
        assert "name" not in summary
        
        assert summary["age"].count == 2
        assert summary["salary"].count == 2


class TestDatasetAggregate:
    """Tests for Dataset custom aggregation."""
    
    def test_aggregate_sum(self) -> None:
        data = [
            {"value": 10},
            {"value": 20},
            {"value": 30},
        ]
        ds = Dataset("data", data)
        
        result = ds.aggregate("value", sum)
        assert result == 60
    
    def test_aggregate_max(self) -> None:
        data = [
            {"score": 85},
            {"score": 92},
            {"score": 78},
        ]
        ds = Dataset("scores", data)
        
        result = ds.aggregate("score", max)
        assert result == 92
    
    def test_aggregate_with_nulls(self) -> None:
        data = [
            {"value": 10},
            {"value": None},
            {"value": 30},
        ]
        ds = Dataset("data", data)
        
        result = ds.aggregate("value", sum)
        assert result == 40  # None is filtered out
    
    def test_aggregate_custom_function(self) -> None:
        data = [
            {"values": [1, 2, 3]},
            {"values": [4, 5, 6]},
        ]
        ds = Dataset("data", data)
        
        # Count total elements across all lists
        result = ds.aggregate("values", lambda lst: sum(len(x) if isinstance(x, list) else 1 for x in lst))
        assert result == 6  # 3 + 3 = 6 elements total


class TestDatasetIntegration:
    """Integration tests for Dataset operations."""
    
    def test_complete_analysis_workflow(self) -> None:
        """Test a complete data analysis workflow."""
        data = [
            {"department": "Engineering", "salary": 80000, "years": 5},
            {"department": "Sales", "salary": 60000, "years": 3},
            {"department": "Engineering", "salary": 90000, "years": 8},
            {"department": "Sales", "salary": 55000, "years": 2},
            {"department": "HR", "salary": 50000, "years": 4},
        ]
        
        ds = Dataset("employees", data)
        
        # Filter to engineering only
        eng = ds.filter(lambda r: r["department"] == "Engineering")
        assert eng.row_count == 2
        
        # Get salary stats for engineering
        salary_stats = eng.column_stats("salary")
        assert salary_stats is not None
        assert salary_stats.mean == 85000.0
        
        # Get overall summary
        summary = ds.summary()
        assert len(summary) == 2  # salary and years are numeric
    
    def test_empty_dataset_operations(self) -> None:
        ds = Dataset("empty", [])
        
        assert ds.summary() == {}
        assert ds.filter(lambda x: True).row_count == 0
    
    def test_single_row_dataset(self) -> None:
        ds = Dataset("single", [{"value": 42}])
        
        stats = ds.column_stats("value")
        assert stats is not None
        assert stats.count == 1
        assert stats.mean == 42.0
        assert stats.std == 0.0  # Single value has no variance
