"""Problem 04: Validation Pipeline

Topic: Data Processing with Objects
Difficulty: Medium

Implement a chain-of-responsibility validation pipeline using OOP.

Validation pipelines check data quality through a series of validators.
Each validator checks one aspect and can either stop the chain (fail)
or continue to the next validator (pass).

Classes to implement:
- ValidationResult - Result of validation with errors and warnings
- Validator (ABC) - Abstract base for validators with chain support
- RequiredFieldValidator - Validates required fields exist
- TypeValidator - Validates field types
- RangeValidator - Validates numeric ranges
- PatternValidator - Validates string patterns (regex)
- ValidationPipeline - Manages and executes a chain of validators
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Pattern
import re


@dataclass(frozen=True)
class ValidationResult:
    """Immutable result of a validation check.
    
    Attributes:
        is_valid: True if validation passed (no errors)
        errors: List of error messages
        warnings: List of warning messages (non-fatal issues)
    """
    is_valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    
    def __init__(
        self,
        is_valid: bool,
        errors: list[str] | None = None,
        warnings: list[str] | None = None,
    ) -> None:
        """Initialize validation result.
        
        Args:
            is_valid: Whether validation passed
            errors: List of error messages
            warnings: List of warning messages
        """
        raise NotImplementedError("Implement __init__")
    
    def merge(self, other: ValidationResult) -> ValidationResult:
        """Merge another result into this one.
        
        Args:
            other: Result to merge
            
        Returns:
            New result combining both
        """
        raise NotImplementedError("Implement merge")
    
    @staticmethod
    def success() -> ValidationResult:
        """Create a successful validation result."""
        raise NotImplementedError("Implement success")
    
    @staticmethod
    def error(message: str) -> ValidationResult:
        """Create an error result with single message."""
        raise NotImplementedError("Implement error")


class Validator(ABC):
    """Abstract base for validators implementing chain of responsibility.
    
    Validators can be chained together. Each validator checks data and
    either returns errors (stopping the chain) or passes to the next
    validator.
    
    Example:
        validator = (
            RequiredFieldValidator(["name", "email"])
            .set_next(TypeValidator({"age": int}))
            .set_next(RangeValidator("age", 0, 120))
        )
        result = validator.validate({"name": "Alice", "age": 30})
    """
    
    def __init__(self, name: str) -> None:
        """Initialize validator.
        
        Args:
            name: Validator name for identification
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def name(self) -> str:
        """Get validator name."""
        raise NotImplementedError("Implement name")
    
    def set_next(self, validator: Validator) -> Validator:
        """Set the next validator in the chain.
        
        Args:
            validator: Next validator
            
        Returns:
            The next validator (for fluent chaining)
        """
        raise NotImplementedError("Implement set_next")
    
    def has_next(self) -> bool:
        """Check if there's a next validator."""
        raise NotImplementedError("Implement has_next")
    
    @abstractmethod
    def validate(self, data: dict[str, Any]) -> ValidationResult:
        """Validate data and continue chain if valid.
        
        Args:
            data: Data to validate
            
        Returns:
            Combined result from this validator and the rest of chain
        """
        raise NotImplementedError("Implement validate")
    
    def _continue_chain(self, data: dict[str, Any]) -> ValidationResult:
        """Continue validation with next validator in chain.
        
        Args:
            data: Data to validate
            
        Returns:
            Result from rest of chain, or success if no next validator
        """
        raise NotImplementedError("Implement _continue_chain")


class RequiredFieldValidator(Validator):
    """Validates that required fields exist and are not None/empty.
    
    Checks:
    - Field exists in data
    - Field value is not None
    - For strings: value is not empty
    """
    
    def __init__(self, required_fields: list[str]) -> None:
        """Initialize with list of required field names.
        
        Args:
            required_fields: List of field names that must be present
        """
        raise NotImplementedError("Implement __init__")
    
    def validate(self, data: dict[str, Any]) -> ValidationResult:
        """Check all required fields exist.
        
        Args:
            data: Data to validate
            
        Returns:
            Validation result, continues chain on success
        """
        raise NotImplementedError("Implement validate")


class TypeValidator(Validator):
    """Validates that fields have expected types.
    
    Example:
        TypeValidator({"age": int, "name": str, "score": float})
    """
    
    def __init__(self, type_map: dict[str, type]) -> None:
        """Initialize with type mappings.
        
        Args:
            type_map: Dictionary mapping field names to expected types
        """
        raise NotImplementedError("Implement __init__")
    
    def validate(self, data: dict[str, Any]) -> ValidationResult:
        """Check field types match expectations.
        
        Only validates fields that exist in data. Use RequiredFieldValidator
        first if fields must exist.
        
        Args:
            data: Data to validate
            
        Returns:
            Validation result, continues chain on success
        """
        raise NotImplementedError("Implement validate")


class RangeValidator(Validator):
    """Validates numeric fields are within a range.
    
    Supports inclusive min/max bounds. Either bound can be None
    to indicate no limit.
    """
    
    def __init__(
        self,
        field: str,
        min_val: float | None = None,
        max_val: float | None = None,
    ) -> None:
        """Initialize with range constraints.
        
        Args:
            field: Field name to validate
            min_val: Minimum allowed value (inclusive, None = no min)
            max_val: Maximum allowed value (inclusive, None = no max)
        """
        raise NotImplementedError("Implement __init__")
    
    def validate(self, data: dict[str, Any]) -> ValidationResult:
        """Check numeric value is within range.
        
        Skips validation if field doesn't exist or isn't numeric.
        
        Args:
            data: Data to validate
            
        Returns:
            Validation result, continues chain on success
        """
        raise NotImplementedError("Implement validate")


class PatternValidator(Validator):
    """Validates string fields match a regex pattern.
    
    Useful for email, phone numbers, IDs, etc.
    """
    
    def __init__(self, field: str, pattern: str, description: str = "") -> None:
        """Initialize with pattern.
        
        Args:
            field: Field name to validate
            pattern: Regex pattern string
            description: Human-readable description of expected format
        """
        raise NotImplementedError("Implement __init__")
    
    def validate(self, data: dict[str, Any]) -> ValidationResult:
        """Check string value matches pattern.
        
        Skips validation if field doesn't exist or isn't a string.
        
        Args:
            data: Data to validate
            
        Returns:
            Validation result, continues chain on success
        """
        raise NotImplementedError("Implement validate")


class ValidationPipeline:
    """Manages and executes a validation chain.
    
    Provides a cleaner interface for building and running validators.
    
    Example:
        pipeline = ValidationPipeline()
        pipeline.add_validator(RequiredFieldValidator(["email"]))
        pipeline.add_validator(PatternValidator("email", r".+@.+", "email"))
        
        result = pipeline.validate({"email": "test@example.com"})
    """
    
    def __init__(self) -> None:
        """Initialize empty pipeline."""
        raise NotImplementedError("Implement __init__")
    
    @property
    def validator_count(self) -> int:
        """Get number of validators in pipeline."""
        raise NotImplementedError("Implement validator_count")
    
    def add_validator(self, validator: Validator) -> ValidationPipeline:
        """Add a validator to the pipeline.
        
        Args:
            validator: Validator to add
            
        Returns:
            Self for fluent interface
        """
        raise NotImplementedError("Implement add_validator")
    
    def validate(self, data: dict[str, Any]) -> ValidationResult:
        """Run all validators against data.
        
        Args:
            data: Data to validate
            
        Returns:
            Combined validation result from all validators
        """
        raise NotImplementedError("Implement validate")
    
    def validate_batch(
        self,
        items: list[dict[str, Any]],
    ) -> dict[int, ValidationResult]:
        """Validate multiple data items.
        
        Args:
            items: List of data dictionaries to validate
            
        Returns:
            Dictionary mapping index to validation result
        """
        raise NotImplementedError("Implement validate_batch")
