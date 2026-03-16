"""Tests for Problem 06: Exception Assertion Suite."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day06.problem_06_exception_assertion_suite import (
    ValidationError,
    NotFoundError,
    validate_positive_integer,
    validate_email,
    divide_safely,
    find_in_list,
    parse_positive_float,
)


class TestValidatePositiveInteger:
    """Tests for validate_positive_integer function."""

    def test_valid_positive_integer(self) -> None:
        """Test validation of valid positive integers."""
        assert validate_positive_integer("count", 1) == 1
        assert validate_positive_integer("count", 100) == 100

    def test_zero_raises_validation_error(self) -> None:
        """Test that zero raises ValidationError."""
        with pytest.raises(ValidationError, match="must be a positive integer"):
            validate_positive_integer("count", 0)

    def test_negative_raises_validation_error(self) -> None:
        """Test that negative number raises ValidationError."""
        with pytest.raises(ValidationError, match="must be a positive integer"):
            validate_positive_integer("count", -5)

    def test_negative_large_raises_validation_error(self) -> None:
        """Test that large negative raises ValidationError with value in message."""
        with pytest.raises(ValidationError, match="-1000"):
            validate_positive_integer("count", -1000)

    def test_string_raises_type_error(self) -> None:
        """Test that string raises TypeError."""
        with pytest.raises(TypeError, match="must be an integer"):
            validate_positive_integer("count", "10")

    def test_float_raises_type_error(self) -> None:
        """Test that float raises TypeError."""
        with pytest.raises(TypeError, match="float"):
            validate_positive_integer("count", 10.5)

    def test_none_raises_type_error(self) -> None:
        """Test that None raises TypeError."""
        with pytest.raises(TypeError, match="NoneType"):
            validate_positive_integer("count", None)

    def test_error_includes_field_name(self) -> None:
        """Test that error message includes the field name."""
        with pytest.raises(ValidationError, match="age"):
            validate_positive_integer("age", -5)


class TestValidateEmail:
    """Tests for validate_email function."""

    def test_valid_email(self) -> None:
        """Test validation of valid email addresses."""
        assert validate_email("test@example.com") == "test@example.com"
        assert validate_email("user.name@domain.co.uk") == "user.name@domain.co.uk"

    def test_email_without_at_symbol(self) -> None:
        """Test email without @ raises ValidationError."""
        with pytest.raises(ValidationError, match="Invalid email format"):
            validate_email("testexample.com")

    def test_email_without_domain(self) -> None:
        """Test email without domain raises ValidationError."""
        with pytest.raises(ValidationError, match="Invalid email format"):
            validate_email("test@")

    def test_email_without_local_part(self) -> None:
        """Test email without local part raises ValidationError."""
        with pytest.raises(ValidationError, match="Invalid email format"):
            validate_email("@example.com")

    def test_email_multiple_at_symbols(self) -> None:
        """Test email with multiple @ symbols raises ValidationError."""
        with pytest.raises(ValidationError, match="Invalid email format"):
            validate_email("test@foo@example.com")

    def test_email_with_spaces(self) -> None:
        """Test email with spaces raises ValidationError."""
        with pytest.raises(ValidationError, match="cannot contain spaces"):
            validate_email("test user@example.com")

    def test_non_string_raises_validation_error(self) -> None:
        """Test that non-string raises ValidationError."""
        with pytest.raises(ValidationError, match="must be a string"):
            validate_email(123)


class TestDivideSafely:
    """Tests for divide_safely function."""

    def test_normal_division(self) -> None:
        """Test normal division works correctly."""
        assert divide_safely(10, 2) == 5.0
        assert divide_safely(7, 2) == 3.5

    def test_division_with_negative(self) -> None:
        """Test division with negative numbers."""
        assert divide_safely(-10, 2) == -5.0
        assert divide_safely(-10, -2) == 5.0

    def test_division_by_zero_raises(self) -> None:
        """Test division by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError, match="Cannot divide 10 by zero"):
            divide_safely(10, 0)

    def test_division_by_zero_includes_dividend(self) -> None:
        """Test that error message includes the dividend value."""
        with pytest.raises(ZeroDivisionError, match="100 by zero"):
            divide_safely(100, 0)

    def test_non_numeric_dividend_raises(self) -> None:
        """Test non-numeric dividend raises TypeError."""
        with pytest.raises(TypeError, match="Dividend must be a number"):
            divide_safely("10", 2)

    def test_non_numeric_divisor_raises(self) -> None:
        """Test non-numeric divisor raises TypeError."""
        with pytest.raises(TypeError, match="Divisor must be a number"):
            divide_safely(10, "2")

    def test_type_names_in_error(self) -> None:
        """Test that type names appear in error messages."""
        with pytest.raises(TypeError, match="str"):
            divide_safely("not a number", 2)


class TestFindInList:
    """Tests for find_in_list function."""

    def test_find_existing_item(self) -> None:
        """Test finding an item that exists."""
        items = [1, 2, 3, 4, 5]
        result = find_in_list(items, lambda x: x > 3)
        assert result == 4

    def test_find_first_match(self) -> None:
        """Test that first matching item is returned."""
        items = [1, 2, 3, 4, 5]
        result = find_in_list(items, lambda x: x > 2)
        assert result == 3

    def test_find_not_found_raises(self) -> None:
        """Test that not finding item raises NotFoundError."""
        items = [1, 2, 3]
        with pytest.raises(NotFoundError, match="No item matches"):
            find_in_list(items, lambda x: x > 10)

    def test_empty_list_raises(self) -> None:
        """Test searching empty list raises NotFoundError."""
        with pytest.raises(NotFoundError):
            find_in_list([], lambda x: True)

    def test_non_list_raises_type_error(self) -> None:
        """Test that non-list raises TypeError."""
        with pytest.raises(TypeError, match="must be a list"):
            find_in_list("not a list", lambda x: True)

    def test_non_callable_predicate_raises(self) -> None:
        """Test that non-callable predicate raises TypeError."""
        with pytest.raises(TypeError, match="predicate must be callable"):
            find_in_list([1, 2, 3], "not callable")

    def test_find_with_objects(self) -> None:
        """Test finding objects by attribute."""
        users = [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30},
            {"name": "Charlie", "age": 35},
        ]
        result = find_in_list(users, lambda u: u["age"] > 28)
        assert result["name"] == "Bob"


class TestParsePositiveFloat:
    """Tests for parse_positive_float function."""

    def test_valid_positive_float(self) -> None:
        """Test parsing valid positive float strings."""
        assert parse_positive_float("3.14") == 3.14
        assert parse_positive_float("100") == 100.0
        assert parse_positive_float("0.001") == 0.001

    def test_zero_raises_validation_error(self) -> None:
        """Test that zero raises ValidationError."""
        with pytest.raises(ValidationError, match="must be positive"):
            parse_positive_float("0")

    def test_zero_point_zero_raises_validation_error(self) -> None:
        """Test that 0.0 raises ValidationError."""
        with pytest.raises(ValidationError, match="must be positive"):
            parse_positive_float("0.0")

    def test_negative_raises_validation_error(self) -> None:
        """Test that negative string raises ValidationError."""
        with pytest.raises(ValidationError, match="must be positive"):
            parse_positive_float("-5.5")

    def test_invalid_string_raises_validation_error(self) -> None:
        """Test that invalid string raises ValidationError."""
        with pytest.raises(ValidationError, match="Cannot parse"):
            parse_positive_float("not a number")

    def test_non_string_raises_type_error(self) -> None:
        """Test that non-string raises TypeError."""
        with pytest.raises(TypeError, match="must be a string"):
            parse_positive_float(3.14)

    def test_empty_string_raises_validation_error(self) -> None:
        """Test that empty string raises ValidationError."""
        with pytest.raises(ValidationError, match="Cannot parse"):
            parse_positive_float("")


class TestCustomExceptions:
    """Tests for custom exception classes."""

    def test_validation_error_is_value_error(self) -> None:
        """Test that ValidationError is a ValueError subclass."""
        assert issubclass(ValidationError, ValueError)

    def test_not_found_error_is_lookup_error(self) -> None:
        """Test that NotFoundError is a LookupError subclass."""
        assert issubclass(NotFoundError, LookupError)

    def test_can_catch_validation_error_as_value_error(self) -> None:
        """Test that ValidationError can be caught as ValueError."""
        try:
            raise ValidationError("test")
        except ValueError as e:
            assert str(e) == "test"

    def test_can_catch_not_found_error_as_lookup_error(self) -> None:
        """Test that NotFoundError can be caught as LookupError."""
        try:
            raise NotFoundError("test")
        except LookupError as e:
            assert str(e) == "test"
