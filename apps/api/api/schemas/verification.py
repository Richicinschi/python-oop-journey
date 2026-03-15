"""Verification schemas."""

from enum import Enum
from pydantic import BaseModel, Field


class TestStatus(str, Enum):
    """Test execution status."""
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


class ErrorCategory(str, Enum):
    """Categories of verification errors."""
    WRONG_RETURN_VALUE = "wrong_return_value"
    UNEXPECTED_EXCEPTION = "unexpected_exception"
    MISSING_IMPLEMENTATION = "missing_implementation"
    TIMEOUT = "timeout"
    SYNTAX_ERROR = "syntax_error"
    IMPORT_ERROR = "import_error"
    ASSERTION_ERROR = "assertion_error"
    UNKNOWN_ERROR = "unknown_error"


class TestResult(BaseModel):
    """Individual test result."""
    name: str = Field(..., description="Test name")
    status: TestStatus = Field(..., description="Test status")
    message: str | None = Field(None, description="Test message/output")
    expected: str | None = Field(None, description="Expected value")
    actual: str | None = Field(None, description="Actual value")
    hint: str | None = Field(None, description="Learner-friendly hint")
    error_category: ErrorCategory | None = Field(None, description="Error category")
    traceback: str | None = Field(None, description="Full traceback (for debugging)")
    duration_ms: float = Field(default=0.0, description="Test execution time")


class VerificationSummary(BaseModel):
    """Verification summary statistics."""
    total: int = Field(..., description="Total number of tests")
    passed: int = Field(..., description="Number of passed tests")
    failed: int = Field(..., description="Number of failed tests")
    errors: int = Field(..., description="Number of tests with errors")
    skipped: int = Field(default=0, description="Number of skipped tests")


class VerificationResult(BaseModel):
    """Complete verification result."""
    success: bool = Field(..., description="Whether all tests passed")
    summary: VerificationSummary = Field(..., description="Test summary")
    tests: list[TestResult] = Field(default_factory=list, description="Individual test results")
    stdout: str = Field(default="", description="Standard output")
    stderr: str = Field(default="", description="Standard error")
    execution_time_ms: float = Field(..., description="Total execution time")
    all_tests_passed: bool = Field(..., description="Whether all tests passed")
    next_steps: list[str] = Field(default_factory=list, description="Suggested next steps")


class VerificationRequest(BaseModel):
    """Verification request."""
    code: str = Field(..., description="Learner's code", max_length=100000)
    problem_slug: str = Field(..., description="Problem identifier", max_length=255)
    test_code: str | None = Field(None, description="Optional test code (if not from curriculum)", max_length=50000)


class HintSuggestion(BaseModel):
    """Hint suggestion based on test results."""
    hint_index: int = Field(..., description="Index of the suggested hint (0-based)")
    reason: str = Field(..., description="Why this hint is suggested")
    confidence: str = Field(..., description="Confidence level: low, medium, high")


class SyntaxValidationResponse(BaseModel):
    """API response for syntax validation endpoint."""
    valid: bool = Field(..., description="Whether the syntax is valid")
    error: str | None = Field(None, description="Error message if invalid")
    line: int | None = Field(None, description="Line number of error")
    column: int | None = Field(None, description="Column number of error")
    message: str = Field(..., description="Human-readable message")


class VerificationResponse(BaseModel):
    """API response for verification."""
    success: bool = Field(..., description="Whether the verification completed successfully")
    summary: VerificationSummary = Field(..., description="Test summary")
    tests: list[TestResult] = Field(default_factory=list, description="Individual test results")
    stdout: str = Field(default="", description="Standard output")
    stderr: str = Field(default="", description="Standard error")
    execution_time_ms: float = Field(..., description="Total execution time")
    suggested_hints: list[HintSuggestion] = Field(default_factory=list, description="Suggested hints")
    progress_updated: bool = Field(default=False, description="Whether progress was updated")
    attempts: int | None = Field(None, description="Current attempt count")
