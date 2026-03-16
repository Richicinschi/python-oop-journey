"""Reference solution for Problem 04: API Response Wrapper."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar


@dataclass
class PaginationInfo:
    """Pagination metadata for paginated responses."""
    
    page: int
    per_page: int
    total: int
    
    @property
    def total_pages(self) -> int:
        """Calculate total pages from total items and per_page."""
        return (self.total + self.per_page - 1) // self.per_page
    
    @property
    def has_next(self) -> bool:
        """Return True if there is a next page."""
        return self.page < self.total_pages
    
    @property
    def has_prev(self) -> bool:
        """Return True if there is a previous page."""
        return self.page > 1
    
    @property
    def is_first(self) -> bool:
        """Return True if this is the first page."""
        return self.page == 1
    
    @property
    def is_last(self) -> bool:
        """Return True if this is the last page."""
        return self.page >= self.total_pages


T = TypeVar('T')


@dataclass
class APIResponse(Generic[T]):
    """Generic API response wrapper."""
    
    data: T
    success: bool = True
    message: str = ""
    pagination: PaginationInfo | None = None
    meta: dict[str, str] = field(default_factory=dict)
    
    @classmethod
    def success_response(cls, data: T, message: str = "") -> APIResponse[T]:
        """Create a successful response."""
        return cls(data=data, success=True, message=message)
    
    @classmethod
    def error_response(cls, message: str, data: T | None = None) -> APIResponse[T]:
        """Create an error response."""
        # Type safety: if data is None, we need to handle the type
        return cls(data=data, success=False, message=message)  # type: ignore[arg-type]
    
    @classmethod
    def paginated_response(
        cls,
        data: list[T],
        page: int,
        per_page: int,
        total: int,
        message: str = ""
    ) -> APIResponse[list[T]]:
        """Create a paginated list response."""
        pagination = PaginationInfo(page=page, per_page=per_page, total=total)
        return cls(data=data, success=True, message=message, pagination=pagination)
    
    def with_meta(self, key: str, value: str) -> APIResponse[T]:
        """Add metadata to the response."""
        new_meta = self.meta.copy()
        new_meta[key] = value
        return APIResponse(
            data=self.data,
            success=self.success,
            message=self.message,
            pagination=self.pagination,
            meta=new_meta,
        )


@dataclass
class ErrorDetail:
    """Detailed error information."""
    
    code: str
    message: str
    field: str | None = None


@dataclass
class ErrorResponse:
    """Structured error response for API errors."""
    
    message: str
    errors: list[ErrorDetail] = field(default_factory=list)
    status_code: int = 400
    
    def add_error(
        self,
        code: str,
        message: str,
        field: str | None = None
    ) -> ErrorResponse:
        """Add an error detail and return self."""
        self.errors.append(ErrorDetail(code=code, message=message, field=field))
        return self
    
    @classmethod
    def validation_error(cls, field: str, message: str) -> ErrorResponse:
        """Create a validation error response."""
        response = cls(
            message="Validation failed",
            status_code=422
        )
        response.add_error("VALIDATION_ERROR", message, field)
        return response
    
    @classmethod
    def not_found(cls, resource: str, identifier: str) -> ErrorResponse:
        """Create a not found error response."""
        response = cls(
            message=f"{resource} not found",
            status_code=404
        )
        response.add_error(
            "NOT_FOUND",
            f"{resource} with identifier '{identifier}' was not found"
        )
        return response
