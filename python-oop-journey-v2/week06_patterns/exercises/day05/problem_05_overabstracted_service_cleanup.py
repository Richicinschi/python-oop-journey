"""Problem 05: Overabstracted Service Cleanup

Topic: Pattern Tradeoffs and Anti-patterns
Difficulty: Medium

Simplify an over-engineered service that has too many layers of abstraction.

The `AbstractTaskProcessingFramework` is a perfect example of over-engineering:
- Multiple abstract base classes for simple operations
- Complex context objects
- Pre/post processors for operations that don't need them
- 200 lines of framework for 5 lines of actual logic

Your task: Simplify this to a clean, direct implementation while
maintaining the ability to:
- Execute tasks
- Handle errors
- Log results
- Be testable

The key insight: Don't abstract until you have multiple implementations
that actually need the abstraction.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable


# BEFORE: Over-abstracted framework (do not modify - for reference)
class AbstractTaskExecutor(ABC):
    """Abstract base for task execution."""
    
    @abstractmethod
    def pre_execute(self, context: TaskContext) -> None: ...
    
    @abstractmethod
    def execute(self, context: TaskContext) -> TaskResult: ...
    
    @abstractmethod
    def post_execute(self, context: TaskContext, result: TaskResult) -> None: ...


class AbstractValidator(ABC):
    """Abstract base for validation."""
    
    @abstractmethod
    def validate(self, context: TaskContext) -> ValidationResult: ...


class AbstractPreprocessor(ABC):
    """Abstract base for preprocessing."""
    
    @abstractmethod
    def process(self, context: TaskContext) -> None: ...


class AbstractPostprocessor(ABC):
    """Abstract base for postprocessing."""
    
    @abstractmethod
    def process(self, context: TaskContext, result: TaskResult) -> None: ...


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str]


@dataclass
class TaskResult:
    success: bool
    data: Any
    message: str


class TaskContext:
    """Complex context object."""
    
    def __init__(self) -> None:
        self.data: dict[str, Any] = {}
        self.metadata: dict[str, Any] = {}
        self.validators: list[AbstractValidator] = []
        self.preprocessors: list[AbstractPreprocessor] = []
        self.postprocessors: list[AbstractPostprocessor] = []
    
    def add_validator(self, validator: AbstractValidator) -> None:
        self.validators.append(validator)
    
    def add_preprocessor(self, preprocessor: AbstractPreprocessor) -> None:
        self.preprocessors.append(preprocessor)


class OverEngineeredTaskExecutor(AbstractTaskExecutor):
    """Way too complex for what it does."""
    
    def __init__(self, context: TaskContext) -> None:
        self._context = context
        self._executed_count = 0
    
    def pre_execute(self, context: TaskContext) -> None:
        for preprocessor in context.preprocessors:
            preprocessor.process(context)
    
    def execute(self, context: TaskContext) -> TaskResult:
        # Validate
        for validator in context.validators:
            result = validator.validate(context)
            if not result.is_valid:
                return TaskResult(False, None, f"Validation failed: {result.errors}")
        
        # Do actual work (this is usually just a few lines!)
        actual_result = self._do_actual_work(context.data)
        self._executed_count += 1
        
        return TaskResult(True, actual_result, "Success")
    
    def _do_actual_work(self, data: dict[str, Any]) -> Any:
        # The actual work is often very simple!
        return f"Processed: {data.get('input', 'nothing')}"
    
    def post_execute(self, context: TaskContext, result: TaskResult) -> None:
        for postprocessor in context.postprocessors:
            postprocessor.process(context, result)
    
    def run(self) -> TaskResult:
        """Full execution pipeline."""
        self.pre_execute(self._context)
        result = self.execute(self._context)
        self.post_execute(self._context, result)
        return result


# AFTER: Clean, simple implementation (implement these)

@dataclass
class TaskOutcome:
    """Result of task execution.
    
    Simple, clear result type without framework baggage.
    """
    success: bool
    data: Any
    message: str
    execution_time_ms: float | None = None


class SimpleTaskRunner:
    """Simple, direct task runner without over-abstraction.
    
    This class provides a clean, straightforward way to run tasks
    with error handling and logging - no complex framework needed.
    
    Example:
        def my_task():
            return "Task completed"
        
        runner = SimpleTaskRunner(my_task)
        result = runner.run()
        print(result.message)  # "Task completed"
    """
    
    def __init__(self, task: Callable[[], Any]) -> None:
        """Initialize with a task function.
        
        Args:
            task: Function that performs the actual work
        """
        raise NotImplementedError("Implement __init__")
    
    def run(self) -> TaskOutcome:
        """Execute the task.
        
        Returns:
            TaskOutcome with success status and result data
        """
        raise NotImplementedError("Implement run")
    
    def get_execution_count(self) -> int:
        """Get number of successful executions."""
        raise NotImplementedError("Implement get_execution_count")


class TaskWithInput:
    """Task that accepts input parameters.
    
    A simple class for tasks that need input - no abstract base classes,
    no complex context objects.
    """
    
    def __init__(self, task_func: Callable[[dict[str, Any]], Any]) -> None:
        """Initialize with a task function that accepts input.
        
        Args:
            task_func: Function(input_dict) -> result
        """
        raise NotImplementedError("Implement __init__")
    
    def run(self, input_data: dict[str, Any]) -> TaskOutcome:
        """Execute the task with input data.
        
        Args:
            input_data: Input parameters for the task
        
        Returns:
            TaskOutcome with result
        """
        raise NotImplementedError("Implement run")


class ValidatedTask:
    """Task with validation - composed, not inherited.
    
    Demonstrates how to add validation without a complex framework.
    Just compose a validator function with a task.
    """
    
    def __init__(
        self,
        task_func: Callable[[dict[str, Any]], Any],
        validator: Callable[[dict[str, Any]], tuple[bool, str]],
    ) -> None:
        """Initialize task with validation.
        
        Args:
            task_func: Function to execute if validation passes
            validator: Function(input) -> (is_valid, error_message)
        """
        raise NotImplementedError("Implement __init__")
    
    def run(self, input_data: dict[str, Any]) -> TaskOutcome:
        """Execute with validation.
        
        Args:
            input_data: Input to validate and process
        
        Returns:
            TaskOutcome (fails fast if validation fails)
        """
        raise NotImplementedError("Implement run")


class DataProcessor:
    """Simple data processor - direct implementation.
    
    No abstract base classes, no complex pipelines.
    Just straightforward data processing.
    """
    
    def __init__(self) -> None:
        raise NotImplementedError("Implement __init__")
    
    def process_item(self, item: dict[str, Any]) -> dict[str, Any]:
        """Process a single data item.
        
        Args:
            item: Data item to process
        
        Returns:
            Processed item
        """
        raise NotImplementedError("Implement process_item")
    
    def process_batch(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Process multiple items.
        
        Args:
            items: List of items to process
        
        Returns:
            List of processed items
        """
        raise NotImplementedError("Implement process_batch")
    
    def get_stats(self) -> dict[str, int]:
        """Get processing statistics.
        
        Returns:
            Dict with 'processed' and 'failed' counts
        """
        raise NotImplementedError("Implement get_stats")


class ReportGenerator:
    """Simple report generator - no over-engineering.
    
    Demonstrates that simple requirements need simple solutions.
    """
    
    def __init__(self, title: str) -> None:
        """Initialize with report title.
        
        Args:
            title: Report title
        """
        raise NotImplementedError("Implement __init__")
    
    def add_section(self, heading: str, content: str) -> None:
        """Add a section to the report.
        
        Args:
            heading: Section heading
            content: Section content
        """
        raise NotImplementedError("Implement add_section")
    
    def add_data_table(self, headers: list[str], rows: list[list[Any]]) -> None:
        """Add a data table to the report.
        
        Args:
            headers: Column headers
            rows: Table rows
        """
        raise NotImplementedError("Implement add_data_table")
    
    def generate(self) -> str:
        """Generate the final report.
        
        Returns:
            Formatted report string
        """
        raise NotImplementedError("Implement generate")
    
    def get_section_count(self) -> int:
        """Get number of sections in report."""
        raise NotImplementedError("Implement get_section_count")
