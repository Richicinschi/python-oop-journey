"""Tests for Problem 01: Pipeline Stage Objects."""

from __future__ import annotations

import pytest

from week07_real_world.solutions.day04.problem_01_pipeline_stage_objects import (
    AggregateStage,
    FilterStage,
    Pipeline,
    PipelineStage,
    TransformStage,
)


class TestFilterStage:
    """Tests for FilterStage."""
    
    def test_filter_positive_numbers(self) -> None:
        stage = FilterStage("positive", lambda x: x > 0)
        result = stage.process([1, -2, 3, -4, 5])
        assert result == [1, 3, 5]
    
    def test_filter_even_numbers(self) -> None:
        stage = FilterStage("even", lambda x: x % 2 == 0)
        result = stage.process([1, 2, 3, 4, 5, 6])
        assert result == [2, 4, 6]
    
    def test_filter_empty_list(self) -> None:
        stage = FilterStage("positive", lambda x: x > 0)
        result = stage.process([])
        assert result == []
    
    def test_filter_no_matches(self) -> None:
        stage = FilterStage("positive", lambda x: x > 0)
        result = stage.process([-1, -2, -3])
        assert result == []
    
    def test_filter_all_match(self) -> None:
        stage = FilterStage("positive", lambda x: x > 0)
        result = stage.process([1, 2, 3])
        assert result == [1, 2, 3]
    
    def test_filter_with_strings(self) -> None:
        stage = FilterStage("long_words", lambda x: len(x) > 3)
        result = stage.process(["a", "bb", "ccc", "dddd", "eeeee"])
        assert result == ["dddd", "eeeee"]
    
    def test_filter_name_property(self) -> None:
        stage = FilterStage("test_filter", lambda x: True)
        assert stage.name == "test_filter"


class TestTransformStage:
    """Tests for TransformStage."""
    
    def test_transform_double(self) -> None:
        stage = TransformStage("double", lambda x: x * 2)
        result = stage.process([1, 2, 3])
        assert result == [2, 4, 6]
    
    def test_transform_square(self) -> None:
        stage = TransformStage("square", lambda x: x ** 2)
        result = stage.process([1, 2, 3, 4])
        assert result == [1, 4, 9, 16]
    
    def test_transform_empty_list(self) -> None:
        stage = TransformStage("double", lambda x: x * 2)
        result = stage.process([])
        assert result == []
    
    def test_transform_string_length(self) -> None:
        stage = TransformStage("length", len)
        result = stage.process(["a", "bb", "ccc"])
        assert result == [1, 2, 3]
    
    def test_transform_type_change(self) -> None:
        stage = TransformStage("to_string", str)
        result = stage.process([1, 2, 3])
        assert result == ["1", "2", "3"]
    
    def test_transform_name_property(self) -> None:
        stage = TransformStage("test_transform", lambda x: x)
        assert stage.name == "test_transform"


class TestAggregateStage:
    """Tests for AggregateStage."""
    
    def test_aggregate_basic(self) -> None:
        stage = AggregateStage("stats")
        result = stage.process([1, 2, 3, 4, 5])
        
        assert result["count"] == 5
        assert result["sum"] == 15
        assert result["min"] == 1
        assert result["max"] == 5
        assert result["mean"] == 3.0
    
    def test_aggregate_empty_list(self) -> None:
        stage = AggregateStage("stats")
        result = stage.process([])
        
        assert result["count"] == 0
        assert result["sum"] == 0
        assert result["min"] == 0
        assert result["max"] == 0
        assert result["mean"] == 0.0
    
    def test_aggregate_single_value(self) -> None:
        stage = AggregateStage("stats")
        result = stage.process([42])
        
        assert result["count"] == 1
        assert result["sum"] == 42
        assert result["min"] == 42
        assert result["max"] == 42
        assert result["mean"] == 42.0
    
    def test_aggregate_with_floats(self) -> None:
        stage = AggregateStage("stats")
        result = stage.process([1.5, 2.5, 3.5])
        
        assert result["count"] == 3
        assert result["sum"] == 7.5
        assert result["mean"] == 2.5
    
    def test_aggregate_with_negative_numbers(self) -> None:
        stage = AggregateStage("stats")
        result = stage.process([-5, -3, 0, 3, 5])
        
        assert result["count"] == 5
        assert result["sum"] == 0
        assert result["min"] == -5
        assert result["max"] == 5
        assert result["mean"] == 0.0
    
    def test_aggregate_name_property(self) -> None:
        stage = AggregateStage("my_stats")
        assert stage.name == "my_stats"


class TestPipeline:
    """Tests for Pipeline class."""
    
    def test_empty_pipeline(self) -> None:
        pipeline = Pipeline()
        assert pipeline.stage_count == 0
        result = pipeline.execute([1, 2, 3])
        assert result == [1, 2, 3]
    
    def test_add_stage(self) -> None:
        pipeline = Pipeline()
        stage = FilterStage("positive", lambda x: x > 0)
        result = pipeline.add_stage(stage)
        
        assert result is pipeline  # Fluent interface
        assert pipeline.stage_count == 1
    
    def test_stage_names(self) -> None:
        pipeline = Pipeline()
        pipeline.add_stage(FilterStage("stage1", lambda x: True))
        pipeline.add_stage(TransformStage("stage2", lambda x: x))
        
        assert pipeline.stage_names == ["stage1", "stage2"]
    
    def test_single_stage_pipeline(self) -> None:
        pipeline = Pipeline()
        pipeline.add_stage(FilterStage("even", lambda x: x % 2 == 0))
        
        result = pipeline.execute([1, 2, 3, 4, 5])
        assert result == [2, 4]
    
    def test_multi_stage_pipeline(self) -> None:
        pipeline = Pipeline()
        pipeline.add_stage(FilterStage("positive", lambda x: x > 0))
        pipeline.add_stage(TransformStage("double", lambda x: x * 2))
        
        result = pipeline.execute([1, -2, 3, -4, 5])
        assert result == [2, 6, 10]
    
    def test_filter_transform_aggregate_pipeline(self) -> None:
        pipeline = (
            FilterStage("positive", lambda x: x > 0) |
            TransformStage("square", lambda x: x ** 2) |
            AggregateStage("stats")
        )
        
        result = pipeline.execute([1, -2, 3, -4, 5])
        
        assert result["count"] == 3  # 1, 3, 5 are positive
        assert result["sum"] == 35  # 1 + 9 + 25
        assert result["mean"] == 35 / 3
    
    def test_or_operator_chaining(self) -> None:
        pipeline = Pipeline()
        pipeline = pipeline | FilterStage("even", lambda x: x % 2 == 0)
        pipeline = pipeline | TransformStage("half", lambda x: x // 2)
        
        result = pipeline.execute([1, 2, 3, 4, 5, 6])
        assert result == [1, 2, 3]
    
    def test_stage_or_operator(self) -> None:
        stage1 = FilterStage("even", lambda x: x % 2 == 0)
        stage2 = TransformStage("double", lambda x: x * 2)
        
        pipeline = stage1 | stage2
        
        assert isinstance(pipeline, Pipeline)
        assert pipeline.stage_count == 2
        
        result = pipeline.execute([1, 2, 3, 4])
        assert result == [4, 8]  # 2*2, 4*2


class TestPipelineIntegration:
    """Integration tests for complete pipelines."""
    
    def test_data_processing_workflow(self) -> None:
        """Test a realistic data processing workflow."""
        # Filter valid scores, normalize them, get statistics
        data = [85, 92, -1, 78, 95, -1, 88, 91]
        
        pipeline = (
            FilterStage("valid_scores", lambda x: x >= 0) |  # Remove invalid
            TransformStage("normalize", lambda x: x / 100) |  # Convert to 0-1
            AggregateStage("statistics")  # Get stats
        )
        
        result = pipeline.execute(data)
        
        assert result["count"] == 6  # 6 valid scores
        assert result["min"] == 0.78
        assert result["max"] == 0.95
    
    def test_string_processing_pipeline(self) -> None:
        """Test processing a list of strings."""
        words = ["hello", "world", "python", "code", "programming"]
        
        pipeline = (
            FilterStage("long_words", lambda w: len(w) > 4) |
            TransformStage("uppercase", str.upper) |
            TransformStage("add_exclamation", lambda w: w + "!")
        )
        
        result = pipeline.execute(words)
        assert result == ["HELLO!", "WORLD!", "PYTHON!", "PROGRAMMING!"]
