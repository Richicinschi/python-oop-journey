"""Problem 01: Pipeline Stage Objects

Topic: Data Processing with Objects
Difficulty: Medium

Implement a data pipeline framework using object-oriented design.

Each pipeline stage is an object that transforms data. Stages can be
chained together to form complete data processing pipelines.

Classes to implement:
- PipelineStage (abstract base) - generic transformation stage
- FilterStage - filters data based on a predicate
- TransformStage - transforms each item using a function
- AggregateStage - aggregates data into summary statistics
- Pipeline - chains multiple stages together

The Pipeline should support the | operator for intuitive chaining:
    pipeline = filter_stage | transform_stage | aggregate_stage
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


class PipelineStage(ABC, Generic[T, U]):
    """Abstract base class for a pipeline stage.
    
    A pipeline stage transforms data of type T into data of type U.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize the stage with a name.
        
        Args:
            name: Descriptive name for this stage
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def name(self) -> str:
        """Get the stage name."""
        raise NotImplementedError("Implement name property")
    
    @abstractmethod
    def process(self, data: T) -> U:
        """Process input data and return transformed output.
        
        Args:
            data: Input data of type T
            
        Returns:
            Transformed output of type U
        """
        raise NotImplementedError("Implement process method")
    
    def __or__(self, other: PipelineStage[U, V]) -> Pipeline:
        """Enable stage chaining with | operator.
        
        Args:
            other: The next stage in the pipeline
            
        Returns:
            A new Pipeline containing both stages
        """
        raise NotImplementedError("Implement __or__")


class FilterStage(PipelineStage[list[T], list[T]]):
    """Pipeline stage that filters items based on a predicate.
    
    Example:
        filter_even = FilterStage("even_filter", lambda x: x % 2 == 0)
        result = filter_even.process([1, 2, 3, 4, 5])  # [2, 4]
    """
    
    def __init__(self, name: str, predicate: Callable[[T], bool]) -> None:
        """Initialize with a filter predicate.
        
        Args:
            name: Stage name
            predicate: Function that returns True for items to keep
        """
        raise NotImplementedError("Implement __init__")
    
    def process(self, data: list[T]) -> list[T]:
        """Filter data using the predicate.
        
        Args:
            data: List of items to filter
            
        Returns:
            List containing only items where predicate(item) is True
        """
        raise NotImplementedError("Implement process")


class TransformStage(PipelineStage[list[T], list[U]]):
    """Pipeline stage that transforms each item using a function.
    
    Example:
        double = TransformStage("double", lambda x: x * 2)
        result = double.process([1, 2, 3])  # [2, 4, 6]
    """
    
    def __init__(self, name: str, transformer: Callable[[T], U]) -> None:
        """Initialize with a transformation function.
        
        Args:
            name: Stage name
            transformer: Function to apply to each item
        """
        raise NotImplementedError("Implement __init__")
    
    def process(self, data: list[T]) -> list[U]:
        """Transform each item in the data.
        
        Args:
            data: List of items to transform
            
        Returns:
            List of transformed items
        """
        raise NotImplementedError("Implement process")


class AggregateStage(PipelineStage[list[T], dict[str, Any]]):
    """Pipeline stage that aggregates data into summary statistics.
    
    Computes count, sum, min, max, and mean for numeric data.
    
    Example:
        stats = AggregateStage("statistics")
        result = stats.process([1, 2, 3, 4, 5])
        # {"count": 5, "sum": 15, "min": 1, "max": 5, "mean": 3.0}
    """
    
    def __init__(self, name: str) -> None:
        """Initialize the aggregate stage.
        
        Args:
            name: Stage name
        """
        raise NotImplementedError("Implement __init__")
    
    def process(self, data: list[T]) -> dict[str, Any]:
        """Calculate aggregate statistics.
        
        Args:
            data: List of numeric values
            
        Returns:
            Dictionary with count, sum, min, max, and mean.
            Returns zeros/empty values if data is empty.
        """
        raise NotImplementedError("Implement process")


class Pipeline:
    """A chain of pipeline stages that can be executed together.
    
    Supports fluent interface with | operator for building pipelines.
    
    Example:
        pipeline = (
            FilterStage("positive", lambda x: x > 0) |
            TransformStage("square", lambda x: x ** 2) |
            AggregateStage("stats")
        )
        result = pipeline.execute([1, -2, 3, -4, 5])
    """
    
    def __init__(self, stages: list[PipelineStage] | None = None) -> None:
        """Initialize pipeline with optional list of stages.
        
        Args:
            stages: Initial list of pipeline stages
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def stage_count(self) -> int:
        """Get the number of stages in the pipeline."""
        raise NotImplementedError("Implement stage_count")
    
    @property
    def stage_names(self) -> list[str]:
        """Get names of all stages in order."""
        raise NotImplementedError("Implement stage_names")
    
    def add_stage(self, stage: PipelineStage) -> Pipeline:
        """Add a stage and return self for fluent interface.
        
        Args:
            stage: Stage to add
            
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement add_stage")
    
    def execute(self, data: Any) -> Any:
        """Execute all stages in sequence.
        
        Args:
            data: Initial input data
            
        Returns:
            Final output after all stages process the data
        """
        raise NotImplementedError("Implement execute")
    
    def __or__(self, other: PipelineStage) -> Pipeline:
        """Enable adding stages with | operator.
        
        Args:
            other: Stage to add
            
        Returns:
            Self with the new stage added
        """
        raise NotImplementedError("Implement __or__")
