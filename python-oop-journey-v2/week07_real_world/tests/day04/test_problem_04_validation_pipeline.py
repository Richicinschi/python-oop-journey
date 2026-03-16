"""Tests for Problem 04: Validation Pipeline."""

from __future__ import annotations

import pytest

from week07_real_world.solutions.day04.problem_04_validation_pipeline import (
    PatternValidator,
    RangeValidator,
    RequiredFieldValidator,
    TypeValidator,
    ValidationPipeline,
    ValidationResult,
    Validator,
)


class TestValidationResult:
    """Tests for ValidationResult."""
    
    def test_success_result(self) -> None:
        result = ValidationResult.success()
        
        assert result.is_valid is True
        assert result.errors == ()
        assert result.warnings == ()
    
    def test_error_result(self) -> None:
        result = ValidationResult.error("Something went wrong")
        
        assert result.is_valid is False
        assert result.errors == ("Something went wrong",)
    
    def test_custom_result(self) -> None:
        result = ValidationResult(
            True,
            errors=[],
            warnings=["This is a warning"],
        )
        
        assert result.is_valid is True  # No errors
        assert result.warnings == ("This is a warning",)
    
    def test_result_with_errors_is_invalid(self) -> None:
        result = ValidationResult(
            True,  # Explicitly True, but has errors
            errors=["An error"],
        )
        
        assert result.is_valid is False  # Errors override is_valid
    
    def test_merge_two_results(self) -> None:
        r1 = ValidationResult(True, ["error1"], ["warn1"])
        r2 = ValidationResult(False, ["error2"], ["warn2"])
        
        merged = r1.merge(r2)
        
        assert merged.is_valid is False
        assert "error1" in merged.errors
        assert "error2" in merged.errors
        assert "warn1" in merged.warnings
        assert "warn2" in merged.warnings
    
    def test_result_immutability(self) -> None:
        result = ValidationResult(True, [], [])
        
        with pytest.raises(AttributeError):
            result.is_valid = False


class TestRequiredFieldValidator:
    """Tests for RequiredFieldValidator."""
    
    def test_all_fields_present(self) -> None:
        validator = RequiredFieldValidator(["name", "email"])
        result = validator.validate({"name": "Alice", "email": "alice@example.com"})
        
        assert result.is_valid is True
    
    def test_missing_field(self) -> None:
        validator = RequiredFieldValidator(["name", "email"])
        result = validator.validate({"name": "Alice"})
        
        assert result.is_valid is False
        assert any("Missing" in err for err in result.errors)
    
    def test_null_field(self) -> None:
        validator = RequiredFieldValidator(["name"])
        result = validator.validate({"name": None})
        
        assert result.is_valid is False
    
    def test_empty_string_field(self) -> None:
        validator = RequiredFieldValidator(["name"])
        result = validator.validate({"name": ""})
        
        assert result.is_valid is False
        assert any("Empty" in err for err in result.errors)
    
    def test_whitespace_only_string(self) -> None:
        validator = RequiredFieldValidator(["name"])
        result = validator.validate({"name": "   "})
        
        assert result.is_valid is False
    
    def test_chains_on_success(self) -> None:
        v1 = RequiredFieldValidator(["name"])
        v2 = RequiredFieldValidator(["email"])
        v1.set_next(v2)
        
        result = v1.validate({"name": "Alice", "email": "alice@example.com"})
        
        assert result.is_valid is True


class TestTypeValidator:
    """Tests for TypeValidator."""
    
    def test_correct_types(self) -> None:
        validator = TypeValidator({"age": int, "name": str, "active": bool})
        result = validator.validate({"age": 30, "name": "Alice", "active": True})
        
        assert result.is_valid is True
    
    def test_wrong_type(self) -> None:
        validator = TypeValidator({"age": int})
        result = validator.validate({"age": "thirty"})
        
        assert result.is_valid is False
        assert any("int" in err and "str" in err for err in result.errors)
    
    def test_missing_field_skipped(self) -> None:
        validator = TypeValidator({"age": int, "name": str})
        result = validator.validate({"age": 30})  # name is missing
        
        assert result.is_valid is True  # Only validates if present
    
    def test_null_field_skipped(self) -> None:
        validator = TypeValidator({"age": int})
        result = validator.validate({"age": None})
        
        assert result.is_valid is True
    
    def test_multiple_type_errors(self) -> None:
        validator = TypeValidator({"age": int, "score": float})
        result = validator.validate({"age": "thirty", "score": "ninety"})
        
        assert result.is_valid is False
        assert len(result.errors) == 2


class TestRangeValidator:
    """Tests for RangeValidator."""
    
    def test_value_within_range(self) -> None:
        validator = RangeValidator("age", min_val=0, max_val=120)
        result = validator.validate({"age": 30})
        
        assert result.is_valid is True
    
    def test_value_below_minimum(self) -> None:
        validator = RangeValidator("age", min_val=0)
        result = validator.validate({"age": -5})
        
        assert result.is_valid is False
        assert any("below minimum" in err for err in result.errors)
    
    def test_value_above_maximum(self) -> None:
        validator = RangeValidator("score", max_val=100)
        result = validator.validate({"score": 150})
        
        assert result.is_valid is False
        assert any("above maximum" in err for err in result.errors)
    
    def test_missing_field_skipped(self) -> None:
        validator = RangeValidator("age", min_val=0, max_val=120)
        result = validator.validate({})  # age missing
        
        assert result.is_valid is True
    
    def test_null_field_skipped(self) -> None:
        validator = RangeValidator("age", min_val=0, max_val=120)
        result = validator.validate({"age": None})
        
        assert result.is_valid is True
    
    def test_non_numeric_field_skipped(self) -> None:
        validator = RangeValidator("name", min_val=0)
        result = validator.validate({"name": "Alice"})
        
        assert result.is_valid is True
    
    def test_exact_bounds(self) -> None:
        validator = RangeValidator("score", min_val=0, max_val=100)
        
        assert validator.validate({"score": 0}).is_valid is True
        assert validator.validate({"score": 100}).is_valid is True


class TestPatternValidator:
    """Tests for PatternValidator."""
    
    def test_valid_pattern(self) -> None:
        validator = PatternValidator("email", r"^[\w\.-]+@[\w\.-]+\.\w+$", "email")
        result = validator.validate({"email": "test@example.com"})
        
        assert result.is_valid is True
    
    def test_invalid_pattern(self) -> None:
        validator = PatternValidator("email", r"^[\w\.-]+@[\w\.-]+\.\w+$", "email address")
        result = validator.validate({"email": "not-an-email"})
        
        assert result.is_valid is False
        assert any("email address" in err for err in result.errors)
    
    def test_missing_field_skipped(self) -> None:
        validator = PatternValidator("phone", r"^\d{10}$", "10-digit phone")
        result = validator.validate({})
        
        assert result.is_valid is True
    
    def test_null_field_skipped(self) -> None:
        validator = PatternValidator("phone", r"^\d{10}$", "phone")
        result = validator.validate({"phone": None})
        
        assert result.is_valid is True
    
    def test_non_string_field_skipped(self) -> None:
        validator = PatternValidator("code", r"^\d{4}$", "4-digit code")
        result = validator.validate({"code": 1234})  # int, not string
        
        assert result.is_valid is True


class TestValidationPipeline:
    """Tests for ValidationPipeline."""
    
    def test_empty_pipeline(self) -> None:
        pipeline = ValidationPipeline()
        result = pipeline.validate({"any": "data"})
        
        assert result.is_valid is True
    
    def test_add_validator(self) -> None:
        pipeline = ValidationPipeline()
        result = pipeline.add_validator(RequiredFieldValidator(["name"]))
        
        assert result is pipeline  # Fluent interface
        assert pipeline.validator_count == 1
    
    def test_pipeline_execution(self) -> None:
        pipeline = ValidationPipeline()
        pipeline.add_validator(RequiredFieldValidator(["name", "email"]))
        pipeline.add_validator(TypeValidator({"age": int}))
        
        result = pipeline.validate({
            "name": "Alice",
            "email": "alice@example.com",
            "age": 30,
        })
        
        assert result.is_valid is True
    
    def test_pipeline_stops_on_first_error(self) -> None:
        pipeline = ValidationPipeline()
        pipeline.add_validator(RequiredFieldValidator(["name"]))
        pipeline.add_validator(TypeValidator({"name": int}))  # Wrong type check
        
        result = pipeline.validate({})  # Missing name
        
        assert result.is_valid is False
        # Should only have required field error, not type error
        assert any("Missing" in err for err in result.errors)
    
    def test_validate_batch(self) -> None:
        pipeline = ValidationPipeline()
        pipeline.add_validator(RequiredFieldValidator(["name"]))
        
        items = [
            {"name": "Alice"},
            {"name": ""},  # Invalid
            {"name": "Bob"},
        ]
        
        results = pipeline.validate_batch(items)
        
        assert results[0].is_valid is True
        assert results[1].is_valid is False
        assert results[2].is_valid is True


class TestValidationChainIntegration:
    """Integration tests for validation chains."""
    
    def test_user_registration_validation(self) -> None:
        """Test a complete user registration validation flow."""
        pipeline = ValidationPipeline()
        pipeline.add_validator(RequiredFieldValidator(["username", "email", "age"]))
        pipeline.add_validator(TypeValidator({"age": int}))
        pipeline.add_validator(RangeValidator("age", min_val=13, max_val=120))
        pipeline.add_validator(PatternValidator(
            "email",
            r"^[\w\.-]+@[\w\.-]+\.\w+$",
            "valid email address",
        ))
        
        # Valid user
        valid = {"username": "alice", "email": "alice@example.com", "age": 30}
        assert pipeline.validate(valid).is_valid is True
        
        # Missing field
        missing = {"username": "bob", "age": 25}
        result = pipeline.validate(missing)
        assert result.is_valid is False
        assert any("Missing" in err for err in result.errors)
        
        # Invalid email
        bad_email = {"username": "charlie", "email": "not-an-email", "age": 30}
        result = pipeline.validate(bad_email)
        assert result.is_valid is False
        assert any("email" in err.lower() for err in result.errors)
        
        # Age out of range
        too_young = {"username": "young", "email": "young@example.com", "age": 10}
        result = pipeline.validate(too_young)
        assert result.is_valid is False
    
    def test_manual_chain_construction(self) -> None:
        """Test manually chaining validators without pipeline."""
        v1 = RequiredFieldValidator(["name"])
        v2 = TypeValidator({"age": int})
        v3 = RangeValidator("age", min_val=0)
        
        v1.set_next(v2).set_next(v3)
        
        result = v1.validate({"name": "Alice", "age": 30})
        assert result.is_valid is True
        
        result = v1.validate({"name": "Alice", "age": -5})
        assert result.is_valid is False
