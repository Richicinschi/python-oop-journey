"""Tests for Problem 05: Batch Job Runner."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pytest

from week07_real_world.solutions.day04.problem_05_batch_job_runner import (
    BatchJob,
    BatchJobRunner,
    DataProcessingJob,
    JobProgress,
    JobResult,
    JobStatus,
)


class TestJobStatus:
    """Tests for JobStatus enum."""
    
    def test_status_values(self) -> None:
        assert JobStatus.PENDING.name == "PENDING"
        assert JobStatus.RUNNING.name == "RUNNING"
        assert JobStatus.COMPLETED.name == "COMPLETED"
        assert JobStatus.FAILED.name == "FAILED"
        assert JobStatus.CANCELLED.name == "CANCELLED"
        assert JobStatus.PAUSED.name == "PAUSED"


class TestJobProgress:
    """Tests for JobProgress dataclass."""
    
    def test_progress_creation(self) -> None:
        progress = JobProgress(total_items=100)
        
        assert progress.total_items == 100
        assert progress.processed_items == 0
        assert progress.percent_complete == 0.0
    
    def test_percent_complete_calculation(self) -> None:
        progress = JobProgress(
            total_items=100,
            processed_items=50,
            failed_items=25,
            skipped_items=5,  # 80 total completed
        )
        
        assert progress.percent_complete == 80.0
    
    def test_percent_complete_zero_total(self) -> None:
        progress = JobProgress(total_items=0)
        assert progress.percent_complete == 100.0
    
    def test_items_remaining(self) -> None:
        progress = JobProgress(
            total_items=100,
            processed_items=70,
            failed_items=10,
        )
        
        assert progress.items_remaining == 20
    
    def test_duration_seconds_not_started(self) -> None:
        progress = JobProgress(total_items=10)
        assert progress.duration_seconds == 0.0
    
    def test_duration_seconds_running(self) -> None:
        start = datetime.now()
        progress = JobProgress(
            total_items=10,
            start_time=start,
        )
        
        # Should be > 0 since start_time is in the past
        assert progress.duration_seconds >= 0.0
    
    def test_estimated_remaining(self) -> None:
        # Simulate: 50 items in 5 seconds = 10 items/sec
        # 50 remaining should take ~5 seconds
        start = datetime.now()
        progress = JobProgress(
            total_items=100,
            processed_items=45,
            failed_items=5,
            start_time=start,
        )
        
        # This is approximate, just check it's calculated
        assert isinstance(progress.estimated_remaining_seconds, float)
    
    def test_immutability(self) -> None:
        progress = JobProgress(total_items=10)
        
        with pytest.raises(AttributeError):
            progress.total_items = 20


class TestJobResult:
    """Tests for JobResult dataclass."""
    
    def test_result_creation(self) -> None:
        start = datetime.now()
        end = datetime.now()
        
        result = JobResult(
            success=True,
            status=JobStatus.COMPLETED,
            processed_count=95,
            failed_count=5,
            skipped_count=0,
            errors=[],
            start_time=start,
            end_time=end,
            metadata={"key": "value"},
        )
        
        assert result.success is True
        assert result.status == JobStatus.COMPLETED
        assert result.processed_count == 95
        assert result.metadata == {"key": "value"}
    
    def test_duration_calculation(self) -> None:
        start = datetime(2024, 1, 1, 12, 0, 0)
        end = datetime(2024, 1, 1, 12, 0, 5)
        
        result = JobResult(
            success=True,
            status=JobStatus.COMPLETED,
            processed_count=10,
            failed_count=0,
            skipped_count=0,
            errors=[],
            start_time=start,
            end_time=end,
        )
        
        assert result.duration_seconds == 5.0
    
    def test_total_processed(self) -> None:
        result = JobResult(
            success=True,
            status=JobStatus.COMPLETED,
            processed_count=90,
            failed_count=5,
            skipped_count=5,
            errors=[],
            start_time=datetime.now(),
            end_time=datetime.now(),
        )
        
        assert result.total_processed == 100
    
    def test_empty_metadata_default(self) -> None:
        result = JobResult(
            success=True,
            status=JobStatus.COMPLETED,
            processed_count=1,
            failed_count=0,
            skipped_count=0,
            errors=[],
            start_time=datetime.now(),
            end_time=datetime.now(),
            metadata=None,
        )
        
        assert result.metadata == {}


class MockJob(BatchJob[int, int]):
    """Mock job for testing."""
    
    def __init__(self, name: str, items: list[int], fail_on: list[int] | None = None) -> None:
        super().__init__(name, items)
        self._fail_on = fail_on or []
        self.processed_items: list[int] = []
    
    def _process_item(self, item: int) -> int:
        if item in self._fail_on:
            raise ValueError(f"Failed on item {item}")
        self.processed_items.append(item)
        return item * 2


class TestBatchJob:
    """Tests for BatchJob base class."""
    
    def test_job_initial_state(self) -> None:
        job = MockJob("test", [1, 2, 3])
        
        assert job.name == "test"
        assert job.status == JobStatus.PENDING
        assert job.progress.total_items == 3
    
    def test_successful_job_execution(self) -> None:
        job = MockJob("test", [1, 2, 3])
        result = job.run()
        
        assert result.success is True
        assert result.status == JobStatus.COMPLETED
        assert result.processed_count == 3
        assert result.failed_count == 0
    
    def test_job_with_failures(self) -> None:
        job = MockJob("test", [1, 2, 3], fail_on=[2])
        result = job.run()
        
        assert result.success is False
        assert result.status == JobStatus.COMPLETED  # Still completes
        assert result.processed_count == 2  # 1 and 3
        assert result.failed_count == 1  # 2 failed
        assert len(result.errors) == 1
    
    def test_progress_callback(self) -> None:
        job = MockJob("test", [1, 2, 3])
        progress_updates: list[JobProgress] = []
        
        job.on_progress(lambda p: progress_updates.append(p))
        job.run()
        
        assert len(progress_updates) == 3
        # Each update should show progress
        assert progress_updates[0].processed_items == 1
        assert progress_updates[1].processed_items == 2
        assert progress_updates[2].processed_items == 3
    
    def test_progress_tracking(self) -> None:
        job = MockJob("test", [1, 2, 3, 4, 5])
        job.run()
        
        progress = job.progress
        assert progress.total_items == 5
        assert progress.processed_items == 5
        assert progress.percent_complete == 100.0
    
    def test_empty_job(self) -> None:
        job = MockJob("empty", [])
        result = job.run()
        
        assert result.success is True
        assert result.processed_count == 0


class TestDataProcessingJob:
    """Tests for DataProcessingJob."""
    
    def test_transform_records(self) -> None:
        records = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]
        
        job = DataProcessingJob(
            "transform",
            records,
            transformer=lambda r: {"id": r["id"], "upper_name": r["name"].upper()},
        )
        
        result = job.run()
        
        assert result.success is True
        assert job.get_transformed_data() == [
            {"id": 1, "upper_name": "ALICE"},
            {"id": 2, "upper_name": "BOB"},
        ]
    
    def test_filter_records(self) -> None:
        records = [
            {"id": 1, "active": True},
            {"id": 2, "active": False},
            {"id": 3, "active": True},
        ]
        
        job = DataProcessingJob(
            "filter_active",
            records,
            transformer=lambda r: r,
            filter_fn=lambda r: r["active"],
        )
        
        result = job.run()
        
        assert result.processed_count == 2
        assert result.skipped_count == 1
        assert len(job.get_transformed_data()) == 2
    
    def test_filter_and_transform(self) -> None:
        records = [
            {"value": 10},
            {"value": -5},
            {"value": 20},
        ]
        
        job = DataProcessingJob(
            "process",
            records,
            transformer=lambda r: {"doubled": r["value"] * 2},
            filter_fn=lambda r: r["value"] > 0,
        )
        
        result = job.run()
        
        assert result.processed_count == 2
        assert result.skipped_count == 1
        assert job.get_transformed_data() == [
            {"doubled": 20},
            {"doubled": 40},
        ]


class TestBatchJobRunner:
    """Tests for BatchJobRunner."""
    
    def test_empty_runner(self) -> None:
        runner = BatchJobRunner()
        
        assert runner.pending_count == 0
        assert runner.completed_count == 0
    
    def test_submit_job(self) -> None:
        runner = BatchJobRunner()
        job = MockJob("test", [1, 2, 3])
        
        runner.submit_job(job)
        
        assert runner.pending_count == 1
    
    def test_run_next(self) -> None:
        runner = BatchJobRunner()
        job = MockJob("test", [1, 2, 3])
        runner.submit_job(job)
        
        result = runner.run_next()
        
        assert result is not None
        assert result.success is True
        assert runner.pending_count == 0
        assert runner.completed_count == 1
    
    def test_run_next_empty_queue(self) -> None:
        runner = BatchJobRunner()
        result = runner.run_next()
        
        assert result is None
    
    def test_run_all(self) -> None:
        runner = BatchJobRunner()
        runner.submit_job(MockJob("job1", [1, 2]))
        runner.submit_job(MockJob("job2", [3, 4]))
        runner.submit_job(MockJob("job3", [5]))
        
        results = runner.run_all()
        
        assert len(results) == 3
        assert runner.pending_count == 0
        assert runner.completed_count == 3
    
    def test_get_results(self) -> None:
        runner = BatchJobRunner()
        runner.submit_job(MockJob("job1", [1]))
        runner.submit_job(MockJob("job2", [2]))
        
        runner.run_all()
        results = runner.get_results()
        
        assert len(results) == 2
        assert all(isinstance(r, JobResult) for r in results)
    
    def test_clear_completed(self) -> None:
        runner = BatchJobRunner()
        runner.submit_job(MockJob("job", [1]))
        runner.run_all()
        
        cleared = runner.clear_completed()
        
        assert cleared == 1
        assert runner.completed_count == 0
    
    def test_job_order_preserved(self) -> None:
        runner = BatchJobRunner()
        
        job_order = []
        
        class TrackingJob(BatchJob[int, int]):
            def __init__(self, name: str) -> None:
                super().__init__(name, [1])
            
            def _process_item(self, item: int) -> int:
                job_order.append(self.name)
                return item
        
        runner.submit_job(TrackingJob("first"))
        runner.submit_job(TrackingJob("second"))
        runner.submit_job(TrackingJob("third"))
        
        runner.run_all()
        
        assert job_order == ["first", "second", "third"]


class TestBatchJobIntegration:
    """Integration tests for batch job system."""
    
    def test_complete_etl_workflow(self) -> None:
        """Test a complete ETL (Extract, Transform, Load) workflow."""
        
        # Raw data extraction simulation
        raw_data = [
            {"user_id": 1, "email": "alice@example.com", "age": "30"},
            {"user_id": 2, "email": "invalid-email", "age": "25"},
            {"user_id": 3, "email": "bob@example.com", "age": "not-a-number"},
            {"user_id": 4, "email": "charlie@example.com", "age": "35"},
        ]
        
        # Transform: parse age, validate email
        def transform_user(record: dict[str, Any]) -> dict[str, Any]:
            return {
                "id": record["user_id"],
                "email": record["email"],
                "age": int(record["age"]),
                "email_valid": "@" in record["email"] and "." in record["email"].split("@")[-1],
            }
        
        # Filter: only records with valid (numeric) ages
        def is_valid(record: dict[str, Any]) -> bool:
            try:
                int(record["age"])
                return True
            except (ValueError, TypeError):
                return False
        
        job = DataProcessingJob(
            "user_etl",
            raw_data,
            transformer=transform_user,
            filter_fn=is_valid,
        )
        
        # Add progress tracking
        progress_snapshots = []
        job.on_progress(lambda p: progress_snapshots.append(p.percent_complete))
        
        result = job.run()
        
        # Verify results
        assert result.success is True  # Job succeeded even with invalid records
        assert result.processed_count == 3  # Records 1, 2, 4 (3 has invalid age)
        assert result.skipped_count == 1  # Record 3 skipped
        
        transformed = job.get_transformed_data()
        assert len(transformed) == 3
        
        # Check transformed data
        assert all("email_valid" in t for t in transformed)
        assert transformed[1]["email_valid"] is False  # Record 2 has invalid email format
    
    def test_runner_with_multiple_job_types(self) -> None:
        """Test runner handling different job types."""
        runner = BatchJobRunner()
        
        # Data processing job
        runner.submit_job(DataProcessingJob(
            "extract",
            [{"val": 1}, {"val": 2}],
            transformer=lambda r: {"doubled": r["val"] * 2},
        ))
        
        # Mock calculation job
        runner.submit_job(MockJob("calc", [1, 2, 3, 4, 5]))
        
        # Another data job
        runner.submit_job(DataProcessingJob(
            "transform",
            [{"x": 10}, {"x": 20}],
            transformer=lambda r: {"result": r["x"] ** 2},
        ))
        
        results = runner.run_all()
        
        assert len(results) == 3
        assert all(r.success for r in results)
        assert runner.completed_count == 3
