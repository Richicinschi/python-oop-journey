# Day 4: Data Processing with Objects

## Learning Objectives

After completing this day, you will understand:
- How to model data pipelines using OOP concepts
- Creating dataset models with statistical capabilities
- Processing event streams with object-oriented designs
- Building validation pipelines using the Chain of Responsibility pattern
- Implementing batch job runners with progress tracking

## Theory

### Data Pipelines as Object Hierarchies

Data processing pipelines transform raw data through multiple stages. Using OOP, each stage becomes a class with a clear interface:

```python
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class PipelineStage(ABC, Generic[T, U]):
    """Abstract base for a pipeline stage."""
    
    @abstractmethod
    def process(self, data: T) -> U:
        """Process input data and return transformed output."""
        pass
    
    def __or__(self, other: PipelineStage[U, Any]) -> Pipeline:
        """Enable stage chaining with | operator."""
        return Pipeline([self, other])


class Pipeline:
    """A chain of pipeline stages."""
    
    def __init__(self, stages: list[PipelineStage] | None = None) -> None:
        self._stages = stages or []
    
    def add_stage(self, stage: PipelineStage) -> Pipeline:
        """Add a stage and return self for fluent interface."""
        self._stages.append(stage)
        return self
    
    def execute(self, data: Any) -> Any:
        """Execute all stages in sequence."""
        result = data
        for stage in self._stages:
            result = stage.process(result)
        return result
    
    def __or__(self, other: PipelineStage) -> Pipeline:
        """Enable adding stages with | operator."""
        self._stages.append(other)
        return self
```

### Dataset Models with Statistics

Object-oriented datasets encapsulate data and provide analytical methods:

```python
from dataclasses import dataclass, field
from typing import TypeVar, Generic

T = TypeVar("T")


@dataclass
class ColumnStats:
    """Statistics for a single column."""
    name: str
    count: int
    mean: float
    std: float
    min_val: float
    max_val: float


class Dataset(Generic[T]):
    """Generic dataset with statistical capabilities."""
    
    def __init__(self, name: str, data: list[dict[str, T]]) -> None:
        self._name = name
        self._data = data
        self._columns = list(data[0].keys()) if data else []
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def row_count(self) -> int:
        return len(self._data)
    
    @property
    def column_count(self) -> int:
        return len(self._columns)
    
    def column_stats(self, column: str) -> ColumnStats:
        """Calculate statistics for a numeric column."""
        values = [row[column] for row in self._data if column in row]
        # ... statistical calculations
        return ColumnStats(column, len(values), mean, std, min_val, max_val)
    
    def filter(self, predicate: Callable[[dict[str, T]], bool]) -> Dataset[T]:
        """Return a new dataset with filtered rows."""
        filtered = [row for row in self._data if predicate(row)]
        return Dataset(f"{self._name}_filtered", filtered)
```

### Event Stream Processing

Event streams require continuous processing with stateful handlers:

```python
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable


class Event:
    """Represents a domain event."""
    
    def __init__(self, event_type: str, payload: dict, timestamp: datetime | None = None) -> None:
        self.event_type = event_type
        self.payload = payload
        self.timestamp = timestamp or datetime.now()
        self.processed = False


class EventHandler(ABC):
    """Abstract event handler."""
    
    @abstractmethod
    def can_handle(self, event: Event) -> bool:
        """Check if this handler can process the event."""
        pass
    
    @abstractmethod
    def handle(self, event: Event) -> None:
        """Process the event."""
        pass


class EventStreamProcessor:
    """Processes a stream of events through registered handlers."""
    
    def __init__(self) -> None:
        self._handlers: list[EventHandler] = []
        self._event_count = 0
        self._processed_count = 0
    
    def register_handler(self, handler: EventHandler) -> None:
        """Register an event handler."""
        self._handlers.append(handler)
    
    def process_event(self, event: Event) -> bool:
        """Process a single event through all matching handlers."""
        self._event_count += 1
        handled = False
        
        for handler in self._handlers:
            if handler.can_handle(event):
                handler.handle(event)
                handled = True
        
        if handled:
            event.processed = True
            self._processed_count += 1
        
        return handled
```

### Validation Pipeline Pattern

Validation logic chains naturally using the Chain of Responsibility pattern:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ValidationResult:
    """Result of a validation check."""
    is_valid: bool
    errors: list[str]
    warnings: list[str]


class Validator(ABC):
    """Abstract validator that can chain to the next validator."""
    
    def __init__(self) -> None:
        self._next: Validator | None = None
    
    def set_next(self, validator: Validator) -> Validator:
        """Set the next validator in the chain."""
        self._next = validator
        return validator
    
    @abstractmethod
    def validate(self, data: Any) -> ValidationResult:
        """Perform validation and pass to next if valid."""
        pass
    
    def _validate_next(self, data: Any) -> ValidationResult:
        """Continue validation with the next validator."""
        if self._next:
            return self._next.validate(data)
        return ValidationResult(True, [], [])


class RequiredFieldValidator(Validator):
    """Validates that required fields exist."""
    
    def __init__(self, fields: list[str]) -> None:
        super().__init__()
        self._fields = fields
    
    def validate(self, data: dict) -> ValidationResult:
        missing = [f for f in self._fields if f not in data or data[f] is None]
        if missing:
            return ValidationResult(False, [f"Missing fields: {missing}"], [])
        return self._validate_next(data)
```

### Batch Job Runners with Progress Tracking

Batch processing benefits from encapsulated job management:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Callable


class JobStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


@dataclass
class JobProgress:
    """Tracks job execution progress."""
    total_items: int
    processed_items: int = 0
    failed_items: int = 0
    current_item: str = ""
    start_time: datetime | None = None
    end_time: datetime | None = None
    
    @property
    def percent_complete(self) -> float:
        if self.total_items == 0:
            return 100.0
        return (self.processed_items / self.total_items) * 100
    
    @property
    def duration_seconds(self) -> float:
        if not self.start_time:
            return 0.0
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()


class BatchJob(ABC):
    """Abstract base for batch processing jobs."""
    
    def __init__(self, name: str, items: list[Any]) -> None:
        self._name = name
        self._items = items
        self._status = JobStatus.PENDING
        self._progress = JobProgress(total_items=len(items))
        self._error_message: str | None = None
        self._progress_callback: Callable[[JobProgress], None] | None = None
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def status(self) -> JobStatus:
        return self._status
    
    @property
    def progress(self) -> JobProgress:
        return self._progress
    
    def on_progress(self, callback: Callable[[JobProgress], None]) -> None:
        """Register a progress callback."""
        self._progress_callback = callback
    
    def run(self) -> bool:
        """Execute the batch job."""
        self._status = JobStatus.RUNNING
        self._progress.start_time = datetime.now()
        
        try:
            for item in self._items:
                self._progress.current_item = str(item)
                self._process_item(item)
                self._progress.processed_items += 1
                
                if self._progress_callback:
                    self._progress_callback(self._progress)
            
            self._status = JobStatus.COMPLETED
            self._progress.end_time = datetime.now()
            return True
            
        except Exception as e:
            self._status = JobStatus.FAILED
            self._error_message = str(e)
            self._progress.end_time = datetime.now()
            return False
    
    @abstractmethod
    def _process_item(self, item: Any) -> None:
        """Process a single item. Must be implemented by subclasses."""
        pass
```

### Best Practices for Data Processing with Objects

1. **Separate Data from Processing**: Keep data models (DTOs) separate from processing logic
2. **Use Generics for Type Safety**: Leverage Generic[T] for dataset and pipeline type safety
3. **Immutable Transformations**: Pipeline stages should return new data, not mutate input
4. **Progress Observability**: Batch jobs should expose progress for UI/monitoring
5. **Fail-Fast Validation**: Validate early in pipelines to avoid wasted processing
6. **Stateful Handlers**: Event handlers can maintain state for aggregations and windowing
7. **Composition over Inheritance**: Build complex pipelines by composing simple stages

## Common Mistakes

### 1. Mutating Input Data

```python
# Wrong: Modifying input data in place
def process_data(records: list[dict]) -> list[dict]:
    for record in records:
        record['processed'] = True  # Mutates original!
    return records

# Right: Return new data structures
def process_data(records: list[dict]) -> list[dict]:
    return [{**record, 'processed': True} for record in records]
```

### 2. Loading Everything Into Memory

```python
# Wrong: Loading entire dataset at once
def analyze_large_file(filepath: str) -> dict:
    with open(filepath) as f:
        all_lines = f.readlines()  # Memory explosion for large files
    return process(all_lines)

# Right: Process lazily with generators
def analyze_large_file(filepath: str) -> dict:
    with open(filepath) as f:
        return process(line for line in f)  # Generator, memory efficient
```

### 3. Silent Data Loss in Pipelines

```python
# Wrong: Silently skipping invalid records
class DataPipeline:
    def process(self, data: list) -> list:
        results = []
        for item in data:
            try:
                results.append(self._transform(item))
            except Exception:
                pass  # Data lost without warning!
        return results

# Right: Track and report failures
class DataPipeline:
    def __init__(self) -> None:
        self.errors: list[tuple[Any, str]] = []
    
    def process(self, data: list) -> list:
        results = []
        for item in data:
            try:
                results.append(self._transform(item))
            except Exception as e:
                self.errors.append((item, str(e)))
        return results
```

### 4. Tight Coupling Between Stages

```python
# Wrong: Stages know too much about each other
class StageA:
    def process(self) -> dict:
        return {'stage_a_data': ..., 'special_key_for_stage_b': ...}

class StageB:
    def process(self, data: dict) -> dict:
        # Depends on specific key from StageA
        value = data['special_key_for_stage_b']

# Right: Clear interfaces between stages
@dataclass
class StageOutput:
    data: Any
    metadata: ProcessingMetadata

class StageA:
    def process(self) -> StageOutput: ...

class StageB:
    def process(self, input_data: StageOutput) -> StageOutput: ...
```

### 5. Ignoring Backpressure

```python
# Wrong: No rate limiting on event processing
class EventProcessor:
    def process_stream(self, events: Iterator[Event]) -> None:
        for event in events:
            self._handle(event)  # Can be overwhelmed!

# Right: Implement backpressure or batching
class EventProcessor:
    def process_stream(self, events: Iterator[Event], batch_size: int = 100) -> None:
        batch = []
        for event in events:
            batch.append(event)
            if len(batch) >= batch_size:
                self._handle_batch(batch)
                batch = []
        if batch:
            self._handle_batch(batch)
```

## Connection to Weekly Project

The Personal Finance Tracker uses data processing patterns for:

- **Transaction Import Pipelines**: CSV/JSON files flow through validation → transformation → storage stages
- **Report Generation**: Data pipelines aggregate transactions by category, date range, or account
- **Batch Processing**: Importing large transaction histories with progress tracking
- **Event Stream**: Real-time budget alerts when transactions exceed thresholds

The `Dataset` and `Pipeline` patterns help build flexible report generation that can filter, aggregate, and format financial data without loading entire histories into memory.

## Summary

Data processing with objects provides:
- **Encapsulation**: Processing logic is bundled with relevant state
- **Composability**: Stages, validators, and handlers chain together
- **Testability**: Each component can be tested in isolation
- **Extensibility**: New stages, handlers, and validators plug in easily
- **Observability**: Progress, metrics, and status are first-class concepts
