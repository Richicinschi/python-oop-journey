"""Problem 01: Pipeline Stage Objects - Solution

Data pipeline framework using object-oriented design.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


class PipelineStage(ABC, Generic[T, U]):
    """Abstract base class for a pipeline stage."""
    
    def __init__(self, name: str) -> None:
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name
    
    @abstractmethod
    def process(self, data: T) -> U:
        """Process input data and return transformed output."""
        pass
    
    def __or__(self, other: PipelineStage[U, V]) -> Pipeline:
        return Pipeline([self, other])


class FilterStage(PipelineStage[list[T], list[T]]):
    """Pipeline stage that filters items based on a predicate."""
    
    def __init__(self, name: str, predicate: Callable[[T], bool]) -> None:
        super().__init__(name)
        self._predicate = predicate
    
    def process(self, data: list[T]) -> list[T]:
        return [item for item in data if self._predicate(item)]


class TransformStage(PipelineStage[list[T], list[U]]):
    """Pipeline stage that transforms each item using a function."""
    
    def __init__(self, name: str, transformer: Callable[[T], U]) -> None:
        super().__init__(name)
        self._transformer = transformer
    
    def process(self, data: list[T]) -> list[U]:
        return [self._transformer(item) for item in data]


class AggregateStage(PipelineStage[list[T], dict[str, Any]]):
    """Pipeline stage that aggregates data into summary statistics."""
    
    def __init__(self, name: str) -> None:
        super().__init__(name)
    
    def process(self, data: list[T]) -> dict[str, Any]:
        if not data:
            return {
                "count": 0,
                "sum": 0,
                "min": 0,
                "max": 0,
                "mean": 0.0,
            }
        
        # Filter to numeric values
        numeric_data = []
        for item in data:
            if isinstance(item, (int, float)):
                numeric_data.append(item)
        
        if not numeric_data:
            return {
                "count": 0,
                "sum": 0,
                "min": 0,
                "max": 0,
                "mean": 0.0,
            }
        
        count = len(numeric_data)
        total = sum(numeric_data)
        min_val = min(numeric_data)
        max_val = max(numeric_data)
        mean = total / count
        
        return {
            "count": count,
            "sum": total,
            "min": min_val,
            "max": max_val,
            "mean": mean,
        }


class Pipeline:
    """A chain of pipeline stages that can be executed together."""
    
    def __init__(self, stages: list[PipelineStage] | None = None) -> None:
        self._stages = stages or []
    
    @property
    def stage_count(self) -> int:
        return len(self._stages)
    
    @property
    def stage_names(self) -> list[str]:
        return [stage.name for stage in self._stages]
    
    def add_stage(self, stage: PipelineStage) -> Pipeline:
        self._stages.append(stage)
        return self
    
    def execute(self, data: Any) -> Any:
        result = data
        for stage in self._stages:
            result = stage.process(result)
        return result
    
    def __or__(self, other: PipelineStage) -> Pipeline:
        self._stages.append(other)
        return self
