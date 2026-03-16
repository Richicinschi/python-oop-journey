"""Problem 05: Batch Job Runner - Solution

Batch job processing system with progress tracking.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class SkipItemException(Exception):
    """Exception to signal that an item should be skipped (not counted as processed or failed)."""
    pass


class JobStatus(Enum):
    """Status states for a batch job."""
    PENDING = auto()
    RUNNING = auto()
    PAUSED = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


@dataclass(frozen=True)
class JobProgress:
    """Immutable progress snapshot for a batch job."""
    total_items: int
    processed_items: int
    failed_items: int
    skipped_items: int
    current_item: str
    start_time: datetime | None
    end_time: datetime | None
    
    def __init__(
        self,
        total_items: int,
        processed_items: int = 0,
        failed_items: int = 0,
        skipped_items: int = 0,
        current_item: str = "",
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> None:
        object.__setattr__(self, "total_items", total_items)
        object.__setattr__(self, "processed_items", processed_items)
        object.__setattr__(self, "failed_items", failed_items)
        object.__setattr__(self, "skipped_items", skipped_items)
        object.__setattr__(self, "current_item", current_item)
        object.__setattr__(self, "start_time", start_time)
        object.__setattr__(self, "end_time", end_time)
    
    @property
    def percent_complete(self) -> float:
        if self.total_items == 0:
            return 100.0
        completed = self.processed_items + self.failed_items + self.skipped_items
        return (completed / self.total_items) * 100
    
    @property
    def items_remaining(self) -> int:
        completed = self.processed_items + self.failed_items + self.skipped_items
        return max(0, self.total_items - completed)
    
    @property
    def duration_seconds(self) -> float:
        if not self.start_time:
            return 0.0
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()
    
    @property
    def estimated_remaining_seconds(self) -> float:
        processed = self.processed_items + self.failed_items
        if processed == 0 or not self.start_time:
            return 0.0
        elapsed = self.duration_seconds
        rate = processed / elapsed if elapsed > 0 else 0
        if rate == 0:
            return 0.0
        return self.items_remaining / rate


@dataclass(frozen=True)
class JobResult:
    """Immutable result of job execution."""
    success: bool
    status: JobStatus
    processed_count: int
    failed_count: int
    skipped_count: int
    errors: tuple[str, ...]
    start_time: datetime
    end_time: datetime
    metadata: dict[str, Any]
    
    def __init__(
        self,
        success: bool,
        status: JobStatus,
        processed_count: int,
        failed_count: int,
        skipped_count: int,
        errors: list[str],
        start_time: datetime,
        end_time: datetime,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        object.__setattr__(self, "success", success)
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "processed_count", processed_count)
        object.__setattr__(self, "failed_count", failed_count)
        object.__setattr__(self, "skipped_count", skipped_count)
        object.__setattr__(self, "errors", tuple(errors))
        object.__setattr__(self, "start_time", start_time)
        object.__setattr__(self, "end_time", end_time)
        object.__setattr__(self, "metadata", metadata or {})
    
    @property
    def duration_seconds(self) -> float:
        return (self.end_time - self.start_time).total_seconds()
    
    @property
    def total_processed(self) -> int:
        return self.processed_count + self.failed_count + self.skipped_count


class BatchJob(ABC, Generic[T, R]):
    """Abstract base class for batch processing jobs."""
    
    def __init__(self, name: str, items: list[T]) -> None:
        self._name = name
        self._items = items
        self._status = JobStatus.PENDING
        self._processed = 0
        self._failed = 0
        self._skipped = 0
        self._errors: list[str] = []
        self._current_item = ""
        self._start_time: datetime | None = None
        self._end_time: datetime | None = None
        self._progress_callback: Callable[[JobProgress], None] | None = None
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def status(self) -> JobStatus:
        return self._status
    
    @property
    def progress(self) -> JobProgress:
        return JobProgress(
            total_items=len(self._items),
            processed_items=self._processed,
            failed_items=self._failed,
            skipped_items=self._skipped,
            current_item=self._current_item,
            start_time=self._start_time,
            end_time=self._end_time,
        )
    
    def on_progress(self, callback: Callable[[JobProgress], None]) -> None:
        self._progress_callback = callback
    
    def run(self) -> JobResult:
        self._status = JobStatus.RUNNING
        self._start_time = datetime.now()
        
        try:
            for item in self._items:
                self._current_item = str(item)[:50]  # Truncate for display
                
                try:
                    self._process_item(item)
                    self._processed += 1
                except SkipItemException:
                    self._skipped += 1
                except Exception as e:
                    self._failed += 1
                    self._errors.append(f"Failed to process {self._current_item}: {e}")
                
                if self._progress_callback:
                    self._progress_callback(self.progress)
            
            self._status = JobStatus.COMPLETED
            self._end_time = datetime.now()
            
            return JobResult(
                success=self._failed == 0,
                status=self._status,
                processed_count=self._processed,
                failed_count=self._failed,
                skipped_count=self._skipped,
                errors=self._errors,
                start_time=self._start_time,
                end_time=self._end_time,
            )
            
        except Exception as e:
            self._status = JobStatus.FAILED
            self._end_time = datetime.now()
            self._errors.append(f"Job failed: {e}")
            
            return JobResult(
                success=False,
                status=self._status,
                processed_count=self._processed,
                failed_count=self._failed,
                skipped_count=self._skipped,
                errors=self._errors,
                start_time=self._start_time or datetime.now(),
                end_time=self._end_time,
            )
    
    @abstractmethod
    def _process_item(self, item: T) -> R:
        pass


class DataProcessingJob(BatchJob[dict[str, Any], dict[str, Any]]):
    """Concrete batch job for processing data records."""
    
    def __init__(
        self,
        name: str,
        records: list[dict[str, Any]],
        transformer: Callable[[dict[str, Any]], dict[str, Any]],
        filter_fn: Callable[[dict[str, Any]], bool] | None = None,
    ) -> None:
        super().__init__(name, records)
        self._transformer = transformer
        self._filter_fn = filter_fn
        self._transformed: list[dict[str, Any]] = []
    
    def _process_item(self, item: dict[str, Any]) -> dict[str, Any]:
        if self._filter_fn and not self._filter_fn(item):
            raise SkipItemException()
        
        result = self._transformer(item)
        self._transformed.append(result)
        return result
    
    def get_transformed_data(self) -> list[dict[str, Any]]:
        return self._transformed.copy()


class BatchJobRunner:
    """Manages and executes multiple batch jobs."""
    
    def __init__(self) -> None:
        self._pending: list[BatchJob] = []
        self._completed: list[BatchJob] = []
        self._results: list[JobResult] = []
    
    @property
    def pending_count(self) -> int:
        return len(self._pending)
    
    @property
    def completed_count(self) -> int:
        return len(self._completed)
    
    def submit_job(self, job: BatchJob) -> None:
        self._pending.append(job)
    
    def run_next(self) -> JobResult | None:
        if not self._pending:
            return None
        
        job = self._pending.pop(0)
        result = job.run()
        self._completed.append(job)
        self._results.append(result)
        return result
    
    def run_all(self) -> list[JobResult]:
        results = []
        while self._pending:
            result = self.run_next()
            if result:
                results.append(result)
        return results
    
    def get_results(self) -> list[JobResult]:
        return self._results.copy()
    
    def clear_completed(self) -> int:
        count = len(self._completed)
        self._completed.clear()
        return count
