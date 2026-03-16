"""Problem 04: API Response Wrapper

Topic: API Design with Classes - Response Wrappers
Difficulty: Medium

Implement a generic response wrapper system that adds metadata,
pagination info, and error handling to API responses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar


@dataclass
class PaginationInfo:
    """Pagination metadata for paginated responses.
    
    Attributes:
        page: Current page number (1-based)
        per_page: Number of items per page
        total: Total number of items available
        total_pages: Total number of pages
    """
    page: int
    per_page: int
    total: int
    
    @property
    def total_pages(self) -> int:
        """Calculate total pages from total items and per_page."""
        raise NotImplementedError("Implement PaginationInfo.total_pages")
    
    @property
    def has_next(self) -> bool:
        """Return True if there is a next page."""
        raise NotImplementedError("Implement PaginationInfo.has_next")
    
    @property
    def has_prev(self) -> bool:
        """Return True if there is a previous page."""
        raise NotImplementedError("Implement PaginationInfo.has_prev")
    
    @property
    def is_first(self) -> bool:
        """Return True if this is the first page."""
        raise NotImplementedError("Implement PaginationInfo.is_first")
    
    @property
    def is_last(self) -> bool:
        """Return True if this is the last page."""
        raise NotImplementedError("Implement PaginationInfo.is_last")


T = TypeVar('T')


@dataclass
class APIResponse(Generic[T]):
    """Generic API response wrapper.
    
    Wraps any data type with metadata about the response.
    
    Type Parameters:
        T: The type of data being wrapped
        
    Attributes:
        data: The actual response data
        success: Whether the request succeeded
        message: Human-readable message
        pagination: Pagination metadata (for list responses)
        meta: Additional metadata key-value pairs
    """
    data: T
    success: bool = True
    message: str = ""
    pagination: PaginationInfo | None = None
    meta: dict[str, str] = field(default_factory=dict)
    
    @classmethod
    def success_response(cls, data: T, message: str = "") -> APIResponse[T]:
        """Create a successful response.
        
        Args:
            data: The response data
            message: Optional success message
            
        Returns:
            APIResponse with success=True
        """
        raise NotImplementedError("Implement APIResponse.success_response")
    
    @classmethod
    def error_response(cls, message: str, data: T | None = None) -> APIResponse[T]:
        """Create an error response.
        
        Args:
            message: Error message
            data: Optional error details
            
        Returns:
            APIResponse with success=False
        """
        raise NotImplementedError("Implement APIResponse.error_response")
    
    @classmethod
    def paginated_response(
        cls,
        data: list[T],
        page: int,
        per_page: int,
        total: int,
        message: str = ""
    ) -> APIResponse[list[T]]:
        """Create a paginated list response.
        
        Args:
            data: List of items for current page
            page: Current page number
            per_page: Items per page
            total: Total items across all pages
            message: Optional message
            
        Returns:
            APIResponse with pagination metadata
        """
        raise NotImplementedError("Implement APIResponse.paginated_response")
    
    def with_meta(self, key: str, value: str) -> APIResponse[T]:
        """Add metadata to the response.
        
        Returns a new response with the added metadata.
        
        Args:
            key: Metadata key
            value: Metadata value
            
        Returns:
            New APIResponse with additional metadata
        """
        raise NotImplementedError("Implement APIResponse.with_meta")


@dataclass
class ErrorDetail:
    """Detailed error information.
    
    Attributes:
        code: Error code (e.g., "VALIDATION_ERROR")
        field: Field that caused the error (if applicable)
        message: Human-readable error message
    """
    code: str
    message: str
    field: str | None = None


@dataclass
class ErrorResponse:
    """Structured error response for API errors.
    
    Attributes:
        message: General error message
        errors: List of specific error details
        status_code: HTTP status code equivalent
    """
    message: str
    errors: list[ErrorDetail] = field(default_factory=list)
    status_code: int = 400
    
    def add_error(
        self,
        code: str,
        message: str,
        field: str | None = None
    ) -> ErrorResponse:
        """Add an error detail and return self.
        
        Args:
            code: Error code
            message: Error message
            field: Related field (optional)
            
        Returns:
            Self for chaining
        """
        raise NotImplementedError("Implement ErrorResponse.add_error")
    
    @classmethod
    def validation_error(cls, field: str, message: str) -> ErrorResponse:
        """Create a validation error response.
        
        Args:
            field: Field that failed validation
            message: Validation error message
            
        Returns:
            ErrorResponse with status_code=422
        """
        raise NotImplementedError("Implement ErrorResponse.validation_error")
    
    @classmethod
    def not_found(cls, resource: str, identifier: str) -> ErrorResponse:
        """Create a not found error response.
        
        Args:
            resource: Resource type (e.g., "User")
            identifier: Resource identifier
            
        Returns:
            ErrorResponse with status_code=404
        """
        raise NotImplementedError("Implement ErrorResponse.not_found")
