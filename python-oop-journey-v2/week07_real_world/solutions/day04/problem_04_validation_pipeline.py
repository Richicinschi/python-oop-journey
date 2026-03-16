"""Problem 04: Validation Pipeline - Solution

Chain-of-responsibility validation pipeline.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ValidationResult:
    """Immutable result of a validation check."""
    is_valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    
    def __init__(
        self,
        is_valid: bool,
        errors: list[str] | None = None,
        warnings: list[str] | None = None,
    ) -> None:
        errors_tuple = tuple(errors or [])
        warnings_tuple = tuple(warnings or [])
        object.__setattr__(self, "is_valid", is_valid and len(errors_tuple) == 0)
        object.__setattr__(self, "errors", errors_tuple)
        object.__setattr__(self, "warnings", warnings_tuple)
    
    def merge(self, other: ValidationResult) -> ValidationResult:
        combined_errors = list(self.errors) + list(other.errors)
        combined_warnings = list(self.warnings) + list(other.warnings)
        is_valid = self.is_valid and other.is_valid
        return ValidationResult(is_valid, combined_errors, combined_warnings)
    
    @staticmethod
    def success() -> ValidationResult:
        return ValidationResult(True, [], [])
    
    @staticmethod
    def error(message: str) -> ValidationResult:
        return ValidationResult(False, [message], [])


class Validator(ABC):
    """Abstract base for validators implementing chain of responsibility."""
    
    def __init__(self, name: str) -> None:
        self._name = name
        self._next: Validator | None = None
    
    @property
    def name(self) -> str:
        return self._name
    
    def set_next(self, validator: Validator) -> Validator:
        self._next = validator
        return validator
    
    def has_next(self) -> bool:
        return self._next is not None
    
    @abstractmethod
    def validate(self, data: dict[str, Any]) -> ValidationResult:
        pass
    
    def _continue_chain(self, data: dict[str, Any]) -> ValidationResult:
        if self._next:
            return self._next.validate(data)
        return ValidationResult.success()


class RequiredFieldValidator(Validator):
    """Validates that required fields exist and are not None/empty."""
    
    def __init__(self, required_fields: list[str]) -> None:
        super().__init__("required_fields")
        self._required_fields = required_fields
    
    def validate(self, data: dict[str, Any]) -> ValidationResult:
        missing = []
        empty = []
        
        for field in self._required_fields:
            if field not in data:
                missing.append(field)
            elif data[field] is None:
                missing.append(field)
            elif isinstance(data[field], str) and not data[field].strip():
                empty.append(field)
        
        errors = []
        if missing:
            errors.append(f"Missing required fields: {missing}")
        if empty:
            errors.append(f"Empty required fields: {empty}")
        
        if errors:
            return ValidationResult(False, errors, [])
        
        return self._continue_chain(data)


class TypeValidator(Validator):
    """Validates that fields have expected types."""
    
    def __init__(self, type_map: dict[str, type]) -> None:
        super().__init__("type_check")
        self._type_map = type_map
    
    def validate(self, data: dict[str, Any]) -> ValidationResult:
        errors = []
        
        for field, expected_type in self._type_map.items():
            if field in data and data[field] is not None:
                if not isinstance(data[field], expected_type):
                    actual = type(data[field]).__name__
                    errors.append(f"Field '{field}' expected {expected_type.__name__}, got {actual}")
        
        if errors:
            return ValidationResult(False, errors, [])
        
        return self._continue_chain(data)


class RangeValidator(Validator):
    """Validates numeric fields are within a range."""
    
    def __init__(
        self,
        field: str,
        min_val: float | None = None,
        max_val: float | None = None,
    ) -> None:
        super().__init__(f"range_{field}")
        self._field = field
        self._min = min_val
        self._max = max_val
    
    def validate(self, data: dict[str, Any]) -> ValidationResult:
        if self._field not in data or data[self._field] is None:
            return self._continue_chain(data)
        
        value = data[self._field]
        if not isinstance(value, (int, float)):
            return self._continue_chain(data)
        
        errors = []
        if self._min is not None and value < self._min:
            errors.append(f"Field '{self._field}' value {value} is below minimum {self._min}")
        if self._max is not None and value > self._max:
            errors.append(f"Field '{self._field}' value {value} is above maximum {self._max}")
        
        if errors:
            return ValidationResult(False, errors, [])
        
        return self._continue_chain(data)


class PatternValidator(Validator):
    """Validates string fields match a regex pattern."""
    
    def __init__(self, field: str, pattern: str, description: str = "") -> None:
        super().__init__(f"pattern_{field}")
        self._field = field
        self._pattern = re.compile(pattern)
        self._description = description or pattern
    
    def validate(self, data: dict[str, Any]) -> ValidationResult:
        if self._field not in data or data[self._field] is None:
            return self._continue_chain(data)
        
        value = data[self._field]
        if not isinstance(value, str):
            return self._continue_chain(data)
        
        if not self._pattern.match(value):
            error_msg = f"Field '{self._field}' does not match pattern: {self._description}"
            return ValidationResult(False, [error_msg], [])
        
        return self._continue_chain(data)


class ValidationPipeline:
    """Manages and executes a validation chain."""
    
    def __init__(self) -> None:
        self._validators: list[Validator] = []
        self._first: Validator | None = None
        self._last: Validator | None = None
    
    @property
    def validator_count(self) -> int:
        return len(self._validators)
    
    def add_validator(self, validator: Validator) -> ValidationPipeline:
        self._validators.append(validator)
        
        if self._first is None:
            self._first = validator
            self._last = validator
        else:
            self._last.set_next(validator)
            self._last = validator
        
        return self
    
    def validate(self, data: dict[str, Any]) -> ValidationResult:
        if self._first is None:
            return ValidationResult.success()
        return self._first.validate(data)
    
    def validate_batch(
        self,
        items: list[dict[str, Any]],
    ) -> dict[int, ValidationResult]:
        results = {}
        for i, item in enumerate(items):
            results[i] = self.validate(item)
        return results
