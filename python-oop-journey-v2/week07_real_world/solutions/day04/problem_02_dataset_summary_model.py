"""Problem 02: Dataset Summary Model - Solution

Dataset model with statistical analysis capabilities.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ColumnStats:
    """Statistics for a single numeric column."""
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
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "count", count)
        object.__setattr__(self, "mean", mean)
        object.__setattr__(self, "std", std)
        object.__setattr__(self, "min_val", min_val)
        object.__setattr__(self, "max_val", max_val)
        object.__setattr__(self, "null_count", null_count)
    
    @property
    def range_val(self) -> float:
        return self.max_val - self.min_val


class Dataset(Generic[T]):
    """A tabular dataset with rows and named columns."""
    
    def __init__(self, name: str, data: list[dict[str, T]]) -> None:
        self._name = name
        self._data = data
        if data:
            self._columns = list(data[0].keys())
        else:
            self._columns = []
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def row_count(self) -> int:
        return len(self._data)
    
    @property
    def column_count(self) -> int:
        return len(self._columns)
    
    @property
    def columns(self) -> list[str]:
        return self._columns.copy()
    
    def get_column(self, column: str) -> list[T | None]:
        return [row.get(column) for row in self._data]
    
    def filter(self, predicate: Callable[[dict[str, T]], bool]) -> Dataset[T]:
        filtered = [row for row in self._data if predicate(row)]
        return Dataset(f"{self._name}_filtered", filtered)
    
    def column_stats(self, column: str) -> ColumnStats | None:
        if column not in self._columns:
            return None
        
        values = []
        null_count = 0
        
        for row in self._data:
            val = row.get(column)
            if val is None:
                null_count += 1
            elif isinstance(val, (int, float)):
                values.append(float(val))
        
        if not values:
            return None
        
        count = len(values)
        total = sum(values)
        mean = total / count
        min_val = min(values)
        max_val = max(values)
        
        # Population standard deviation
        variance = sum((x - mean) ** 2 for x in values) / count
        std = math.sqrt(variance)
        
        return ColumnStats(
            name=column,
            count=count,
            mean=mean,
            std=std,
            min_val=min_val,
            max_val=max_val,
            null_count=null_count,
        )
    
    def summary(self) -> dict[str, ColumnStats]:
        result = {}
        for col in self._columns:
            stats = self.column_stats(col)
            if stats:
                result[col] = stats
        return result
    
    def aggregate(self, column: str, agg_func: Callable[[list[T]], Any]) -> Any:
        values = self.get_column(column)
        # Filter out None values
        values = [v for v in values if v is not None]
        return agg_func(values)
