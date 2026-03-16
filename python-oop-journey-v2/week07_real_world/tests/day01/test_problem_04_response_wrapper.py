"""Tests for Problem 04: API Response Wrapper."""

from __future__ import annotations

import pytest

from week07_real_world.solutions.day01.problem_04_response_wrapper import (
    APIResponse,
    ErrorDetail,
    ErrorResponse,
    PaginationInfo,
)


class TestPaginationInfo:
    """Tests for PaginationInfo."""
    
    def test_total_pages_calculation(self) -> None:
        """Test total_pages calculation."""
        # Exact division
        info = PaginationInfo(page=1, per_page=10, total=50)
        assert info.total_pages == 5
        
        # With remainder
        info = PaginationInfo(page=1, per_page=10, total=55)
        assert info.total_pages == 6
        
        # Zero total
        info = PaginationInfo(page=1, per_page=10, total=0)
        assert info.total_pages == 0
    
    def test_has_next(self) -> None:
        """Test has_next property."""
        # First page of many
        info = PaginationInfo(page=1, per_page=10, total=50)
        assert info.has_next is True
        
        # Last page
        info = PaginationInfo(page=5, per_page=10, total=50)
        assert info.has_next is False
        
        # Middle page
        info = PaginationInfo(page=3, per_page=10, total=50)
        assert info.has_next is True
    
    def test_has_prev(self) -> None:
        """Test has_prev property."""
        # First page
        info = PaginationInfo(page=1, per_page=10, total=50)
        assert info.has_prev is False
        
        # Second page
        info = PaginationInfo(page=2, per_page=10, total=50)
        assert info.has_prev is True
    
    def test_is_first(self) -> None:
        """Test is_first property."""
        info = PaginationInfo(page=1, per_page=10, total=50)
        assert info.is_first is True
        
        info = PaginationInfo(page=2, per_page=10, total=50)
        assert info.is_first is False
    
    def test_is_last(self) -> None:
        """Test is_last property."""
        info = PaginationInfo(page=5, per_page=10, total=50)
        assert info.is_last is True
        
        info = PaginationInfo(page=4, per_page=10, total=50)
        assert info.is_last is False
        
        # Beyond last page
        info = PaginationInfo(page=6, per_page=10, total=50)
        assert info.is_last is True


class TestAPIResponse:
    """Tests for APIResponse."""
    
    def test_default_values(self) -> None:
        """Test default response values."""
        response = APIResponse(data={"id": 1})
        
        assert response.success is True
        assert response.message == ""
        assert response.pagination is None
        assert response.meta == {}
    
    def test_success_response_factory(self) -> None:
        """Test success_response factory method."""
        response = APIResponse.success_response({"id": 1}, "Created successfully")
        
        assert response.success is True
        assert response.data == {"id": 1}
        assert response.message == "Created successfully"
    
    def test_error_response_factory(self) -> None:
        """Test error_response factory method."""
        response = APIResponse.error_response("Something went wrong")
        
        assert response.success is False
        assert response.message == "Something went wrong"
    
    def test_error_response_with_data(self) -> None:
        """Test error_response with error details."""
        error_data = {"field": "email", "issue": "invalid"}
        response = APIResponse.error_response("Validation failed", error_data)
        
        assert response.success is False
        assert response.data == error_data
    
    def test_paginated_response_factory(self) -> None:
        """Test paginated_response factory method."""
        items = [{"id": 1}, {"id": 2}]
        response = APIResponse.paginated_response(
            data=items,
            page=2,
            per_page=5,
            total=12,
            message="Users retrieved"
        )
        
        assert response.success is True
        assert response.data == items
        assert response.message == "Users retrieved"
        assert response.pagination is not None
        assert response.pagination.page == 2
        assert response.pagination.per_page == 5
        assert response.pagination.total == 12
    
    def test_with_meta(self) -> None:
        """Test adding metadata."""
        response = APIResponse.success_response({"id": 1})
        new_response = response.with_meta("version", "1.0")
        
        assert new_response.meta["version"] == "1.0"
        assert new_response.data == {"id": 1}
        # Original should be unchanged
        assert "version" not in response.meta
    
    def test_with_meta_multiple(self) -> None:
        """Test adding multiple metadata entries."""
        response = APIResponse.success_response({"id": 1})
        response = response.with_meta("version", "1.0")
        response = response.with_meta("request_id", "abc123")
        
        assert response.meta["version"] == "1.0"
        assert response.meta["request_id"] == "abc123"
    
    def test_generic_typing(self) -> None:
        """Test that APIResponse works with different types."""
        # With dict
        response1: APIResponse[dict] = APIResponse.success_response({"key": "value"})
        assert response1.data["key"] == "value"
        
        # With list
        response2: APIResponse[list[int]] = APIResponse.success_response([1, 2, 3])
        assert len(response2.data) == 3
        
        # With string
        response3: APIResponse[str] = APIResponse.success_response("Hello")
        assert response3.data == "Hello"


class TestErrorDetail:
    """Tests for ErrorDetail."""
    
    def test_error_detail_creation(self) -> None:
        """Test creating ErrorDetail."""
        error = ErrorDetail(code="VALIDATION_ERROR", message="Invalid input")
        assert error.code == "VALIDATION_ERROR"
        assert error.message == "Invalid input"
        assert error.field is None
    
    def test_error_detail_with_field(self) -> None:
        """Test creating ErrorDetail with field."""
        error = ErrorDetail(
            code="REQUIRED_FIELD",
            message="This field is required",
            field="email"
        )
        assert error.field == "email"


class TestErrorResponse:
    """Tests for ErrorResponse."""
    
    def test_default_values(self) -> None:
        """Test default error response values."""
        response = ErrorResponse(message="An error occurred")
        
        assert response.message == "An error occurred"
        assert response.errors == []
        assert response.status_code == 400
    
    def test_add_error(self) -> None:
        """Test adding an error detail."""
        response = ErrorResponse(message="Validation failed")
        response.add_error("INVALID_EMAIL", "Email format is invalid", "email")
        
        assert len(response.errors) == 1
        assert response.errors[0].code == "INVALID_EMAIL"
        assert response.errors[0].field == "email"
    
    def test_add_error_chaining(self) -> None:
        """Test that add_error returns self for chaining."""
        response = (ErrorResponse(message="Validation failed")
            .add_error("INVALID_EMAIL", "Bad email", "email")
            .add_error("TOO_SHORT", "Password too short", "password"))
        
        assert len(response.errors) == 2
    
    def test_validation_error_factory(self) -> None:
        """Test validation_error factory method."""
        response = ErrorResponse.validation_error("email", "Email is required")
        
        assert response.status_code == 422
        assert response.message == "Validation failed"
        assert len(response.errors) == 1
        assert response.errors[0].code == "VALIDATION_ERROR"
        assert response.errors[0].field == "email"
    
    def test_not_found_factory(self) -> None:
        """Test not_found factory method."""
        response = ErrorResponse.not_found("User", "123")
        
        assert response.status_code == 404
        assert "User not found" in response.message
        assert len(response.errors) == 1
        assert response.errors[0].code == "NOT_FOUND"
        assert "123" in response.errors[0].message


class TestIntegration:
    """Integration tests for response wrapper system."""
    
    def test_complete_success_response(self) -> None:
        """Test building a complete success response."""
        items = [{"id": i} for i in range(1, 6)]
        response = (APIResponse
            .paginated_response(items, page=1, per_page=5, total=20)
            .with_meta("request_id", "req-123")
            .with_meta("server", "api-01"))
        
        assert response.success is True
        assert len(response.data) == 5
        assert response.pagination is not None
        assert response.pagination.has_next is True
        assert response.meta["request_id"] == "req-123"
    
    def test_complete_error_response(self) -> None:
        """Test building a complete error response."""
        response = (ErrorResponse
            .validation_error("email", "Invalid format")
            .add_error("TOO_SHORT", "Must be at least 8 characters", "password"))
        
        assert response.status_code == 422
        assert len(response.errors) == 2
        assert any(e.field == "email" for e in response.errors)
        assert any(e.field == "password" for e in response.errors)
