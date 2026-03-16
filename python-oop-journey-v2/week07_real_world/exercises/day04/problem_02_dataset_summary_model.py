"""Problem 02: Dataset Summary Model

Topic: Data Processing with Objects
Difficulty: Medium

Implement a Dataset model that encapsulates tabular data and provides
statistical analysis capabilities.

The Dataset class represents a collection of records (rows) with named
columns. It provides methods for filtering, aggregation, and statistical
summarization.

Classes to implement:
- ColumnStats - Statistics for a single column
- Dataset - Container for tabular data with analysis methods
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass
class ColumnStats:
    """Statistics for a single numeric column.
    
    Attributes:
        name: Column name
        count: Number of non-null values
        mean: Arithmetic mean of values
        std: Standard deviation (population std)
        min_val: Minimum value
        max_val: Maximum value
        null_count: Number of null/missing values
    """
    name: str
    count: int
    mean: float
    std: float
    min_val: float
    max_val: float
    null_count: int
    
    def __init__(
        self,
        name: str,
        count: int,
        mean: float,
        std: float,
        min_val: float,
        max_val: float,
        null_count: int = 0,
    ) -> None:
        """Initialize column statistics.
        
        Args:
            name: Column name
            count: Number of non-null values
            mean: Average of values
            std: Standard deviation
            min_val: Minimum value
            max_val: Maximum value
            null_count: Number of null values (default 0)
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def range_val(self) -> float:
        """Calculate the range (max - min)."""
        raise NotImplementedError("Implement range_val")


class Dataset(Generic[T]):
    """A tabular dataset with rows and named columns.
    
    Provides filtering, column statistics, and aggregation operations.
    All operations that transform data return new Dataset instances
    (immutable transformations).
    
    Example:
        data = [
            {"name": "Alice", "age": 30, "salary": 50000},
            {"name": "Bob", "age": 25, "salary": 45000},
        ]
        ds = Dataset("employees", data)
        stats = ds.column_stats("age")
        high_earners = ds.filter(lambda r: r["salary"] > 40000)
    """
    
    def __init__(self, name: str, data: list[dict[str, T]]) -> None:
        """Initialize dataset.
        
        Args:
            name: Dataset name
            data: List of row dictionaries. Each dict represents one row
                  with column names as keys.
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def name(self) -> str:
        """Get the dataset name."""
        raise NotImplementedError("Implement name")
    
    @property
    def row_count(self) -> int:
        """Get the number of rows."""
        raise NotImplementedError("Implement row_count")
    
    @property
    def column_count(self) -> int:
        """Get the number of columns."""
        raise NotImplementedError("Implement column_count")
    
    @property
    def columns(self) -> list[str]:
        """Get list of column names (from first row)."""
        raise NotImplementedError("Implement columns")
    
    def get_column(self, column: str) -> list[T | None]:
        """Get all values for a specific column.
        
        Args:
            column: Column name
            
        Returns:
            List of values for that column. Returns None for rows
            where the column is missing.
        """
        raise NotImplementedError("Implement get_column")
    
    def filter(self, predicate: Callable[[dict[str, T]], bool]) -> Dataset[T]:
        """Filter rows based on a predicate.
        
        Returns a new Dataset containing only rows where predicate
        returns True. Does not modify the original dataset.
        
        Args:
            predicate: Function that takes a row dict and returns bool
            
        Returns:
            New Dataset with filtered rows
        """
        raise NotImplementedError("Implement filter")
    
    def column_stats(self, column: str) -> ColumnStats | None:
        """Calculate statistics for a numeric column.
        
        Args:
            column: Column name to analyze
            
        Returns:
            ColumnStats with statistics, or None if column doesn't exist
            or contains no numeric data.
        """
        raise NotImplementedError("Implement column_stats")
    
    def summary(self) -> dict[str, ColumnStats]:
        """Get statistics for all numeric columns.
        
        Returns:
            Dictionary mapping column names to their statistics.
            Only includes columns with numeric data.
        """
        raise NotImplementedError("Implement summary")
    
    def aggregate(self, column: str, agg_func: Callable[[list[T]], Any]) -> Any:
        """Apply a custom aggregation function to a column.
        
        Args:
            column: Column name
            agg_func: Function that takes a list of values and returns
                     an aggregated result
                     
        Returns:
            Result of the aggregation function
        """
        raise NotImplementedError("Implement aggregate")
