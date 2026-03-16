"""Tests for Problem 05: Overabstracted Service Cleanup."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day05.problem_05_overabstracted_service_cleanup import (
    DataProcessor,
    ReportGenerator,
    SimpleTaskRunner,
    TaskOutcome,
    TaskWithInput,
    ValidatedTask,
)


class TestTaskOutcome:
    """Tests for TaskOutcome dataclass."""
    
    def test_outcome_creation(self) -> None:
        outcome = TaskOutcome(success=True, data="result", message="Done")
        assert outcome.success is True
        assert outcome.data == "result"
        assert outcome.message == "Done"


class TestSimpleTaskRunner:
    """Tests for SimpleTaskRunner."""
    
    def test_successful_task(self) -> None:
        def simple_task():
            return "Task result"
        
        runner = SimpleTaskRunner(simple_task)
        outcome = runner.run()
        
        assert outcome.success is True
        assert outcome.data == "Task result"
        assert "Task result" in outcome.message
    
    def test_execution_count(self) -> None:
        counter = 0
        
        def counting_task():
            nonlocal counter
            counter += 1
            return f"Run #{counter}"
        
        runner = SimpleTaskRunner(counting_task)
        
        runner.run()
        assert runner.get_execution_count() == 1
        
        runner.run()
        assert runner.get_execution_count() == 2
    
    def test_task_with_exception(self) -> None:
        def failing_task():
            raise ValueError("Something went wrong")
        
        runner = SimpleTaskRunner(failing_task)
        outcome = runner.run()
        
        assert outcome.success is False
        assert "failed" in outcome.message.lower()
        assert "Something went wrong" in outcome.message
    
    def test_task_returns_none(self) -> None:
        def none_task():
            return None
        
        runner = SimpleTaskRunner(none_task)
        outcome = runner.run()
        
        assert outcome.success is True
        assert outcome.message == "Task completed successfully"


class TestTaskWithInput:
    """Tests for TaskWithInput."""
    
    def test_task_with_input(self) -> None:
        def greet_task(input_data):
            name = input_data.get("name", "World")
            return f"Hello, {name}!"
        
        task = TaskWithInput(greet_task)
        outcome = task.run({"name": "Alice"})
        
        assert outcome.success is True
        assert outcome.data == "Hello, Alice!"
    
    def test_task_with_default_input(self) -> None:
        def greet_task(input_data):
            name = input_data.get("name", "World")
            return f"Hello, {name}!"
        
        task = TaskWithInput(greet_task)
        outcome = task.run({})
        
        assert outcome.data == "Hello, World!"
    
    def test_task_with_exception(self) -> None:
        def bad_task(input_data):
            raise KeyError("missing_key")
        
        task = TaskWithInput(bad_task)
        outcome = task.run({})
        
        assert outcome.success is False
        assert "failed" in outcome.message.lower()


class TestValidatedTask:
    """Tests for ValidatedTask."""
    
    def test_validation_passes(self) -> None:
        def validator(data):
            if data.get("value", 0) > 0:
                return True, ""
            return False, "Value must be positive"
        
        def task_func(data):
            return data["value"] * 2
        
        task = ValidatedTask(task_func, validator)
        outcome = task.run({"value": 5})
        
        assert outcome.success is True
        assert outcome.data == 10
    
    def test_validation_fails(self) -> None:
        def validator(data):
            if data.get("value", 0) > 0:
                return True, ""
            return False, "Value must be positive"
        
        def task_func(data):
            return data["value"] * 2
        
        task = ValidatedTask(task_func, validator)
        outcome = task.run({"value": -5})
        
        assert outcome.success is False
        assert "Validation failed" in outcome.message
        assert "positive" in outcome.message
    
    def test_task_fails_after_validation(self) -> None:
        def validator(data):
            return True, ""
        
        def failing_task(data):
            raise RuntimeError("Task error")
        
        task = ValidatedTask(failing_task, validator)
        outcome = task.run({})
        
        assert outcome.success is False
        assert "Task failed" in outcome.message


class TestDataProcessor:
    """Tests for DataProcessor."""
    
    def test_process_item(self) -> None:
        processor = DataProcessor()
        item = {"id": 1, "name": "Test"}
        
        result = processor.process_item(item)
        
        assert result["original"] == item
        assert result["processed"] is True
    
    def test_process_batch(self) -> None:
        processor = DataProcessor()
        items = [
            {"id": 1, "name": "Item1"},
            {"id": 2, "name": "Item2"},
        ]
        
        results = processor.process_batch(items)
        
        assert len(results) == 2
        assert all(r["processed"] for r in results)
    
    def test_get_stats(self) -> None:
        processor = DataProcessor()
        
        assert processor.get_stats() == {"processed": 0, "failed": 0}
        
        processor.process_item({"id": 1})
        assert processor.get_stats()["processed"] == 1
    
    def test_batch_handles_errors(self) -> None:
        processor = DataProcessor()
        # Batch processing handles errors gracefully
        items = [{"id": 1}, {"id": 2}]
        
        results = processor.process_batch(items)
        
        # All items should have results
        assert len(results) == 2


class TestReportGenerator:
    """Tests for ReportGenerator."""
    
    def test_create_report_with_title(self) -> None:
        generator = ReportGenerator("Monthly Report")
        report = generator.generate()
        
        assert "# Monthly Report" in report
    
    def test_add_text_section(self) -> None:
        generator = ReportGenerator("Test Report")
        generator.add_section("Introduction", "This is the intro.")
        
        report = generator.generate()
        
        assert "## Introduction" in report
        assert "This is the intro." in report
    
    def test_add_data_table(self) -> None:
        generator = ReportGenerator("Test Report")
        generator.add_data_table(
            headers=["Name", "Value"],
            rows=[["Alice", "100"], ["Bob", "200"]],
        )
        
        report = generator.generate()
        
        assert "| Name | Value |" in report
        assert "| Alice | 100 |" in report
        assert "| Bob | 200 |" in report
    
    def test_get_section_count(self) -> None:
        generator = ReportGenerator("Test Report")
        assert generator.get_section_count() == 0
        
        generator.add_section("S1", "Content 1")
        assert generator.get_section_count() == 1
        
        generator.add_data_table(["A"], [["B"]])
        assert generator.get_section_count() == 2
    
    def test_complete_report(self) -> None:
        generator = ReportGenerator("Sales Report")
        generator.add_section("Summary", "Q4 sales were strong.")
        generator.add_data_table(
            headers=["Product", "Sales"],
            rows=[["Widget", "1000"], ["Gadget", "500"]],
        )
        generator.add_section("Conclusion", "Great quarter!")
        
        report = generator.generate()
        
        # Verify structure
        assert "# Sales Report" in report
        assert "## Summary" in report
        assert "## Conclusion" in report
        assert "| Product | Sales |" in report
        assert "| Widget | 1000 |" in report


class TestSimplicityBenefits:
    """Tests demonstrating benefits of simple design."""
    
    def test_no_complex_setup_needed(self) -> None:
        """Simple tasks don't need complex framework setup."""
        # Just create and run - no context, preprocessors, etc.
        task = SimpleTaskRunner(lambda: "Hello")
        outcome = task.run()
        
        assert outcome.success is True
        assert outcome.data == "Hello"
    
    def test_direct_and_obvious_execution(self) -> None:
        """Execution path is clear and direct."""
        executed = []
        
        def trace_task():
            executed.append("task")
            return "done"
        
        task = SimpleTaskRunner(trace_task)
        task.run()
        
        # Direct execution - no hidden steps
        assert executed == ["task"]
    
    def test_easy_to_test_individual_components(self) -> None:
        """Each component can be tested in isolation."""
        # Test validator separately
        def validator(data):
            is_valid = data.get("valid", False)
            return is_valid, "" if is_valid else "Invalid"
        
        assert validator({"valid": True}) == (True, "")
        assert validator({"valid": False}) == (False, "Invalid")
        
        # Test task function separately
        def task_func(data):
            return data["value"] * 2
        
        assert task_func({"value": 5}) == 10
        
        # Combine them
        validated = ValidatedTask(task_func, validator)
        outcome = validated.run({"valid": True, "value": 5})
        assert outcome.data == 10
    
    def test_yagni_principle(self) -> None:
        """You Aren't Gonna Need It - simple until complexity needed."""
        # Start with simple runner
        simple = SimpleTaskRunner(lambda: "simple")
        assert simple.run().success
        
        # Add input when needed
        with_input = TaskWithInput(lambda d: d["x"])
        assert with_input.run({"x": 42}).data == 42
        
        # Add validation when needed
        validated = ValidatedTask(
            lambda d: d["value"],
            lambda d: (d.get("value") is not None, "Missing value"),
        )
        assert validated.run({"value": 123}).success
        assert not validated.run({}).success
