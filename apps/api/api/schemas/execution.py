"""Code execution schemas."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class ExecutionStatus(str, Enum):
    """Execution status enum."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class CodeExecutionRequest(BaseModel):
    """Code execution request."""

    code: str = Field(..., description="Python code to execute", max_length=100000)
    timeout: int = Field(default=10, ge=1, le=30, description="Execution timeout in seconds")
    test_code: str | None = Field(
        default=None, description="Optional test code to run against", max_length=50000
    )
    problem_slug: str | None = Field(
        default=None, description="Optional problem slug for validation", max_length=255
    )

    @field_validator("code")
    @classmethod
    def validate_code_not_empty(cls, v: str) -> str:
        """Validate code is not empty."""
        if not v.strip():
            raise ValueError("Code cannot be empty")
        return v

    @field_validator("timeout")
    @classmethod
    def validate_timeout(cls, v: int) -> int:
        """Validate timeout is within acceptable range (1-30 seconds)."""
        if v < 1:
            raise ValueError("Timeout must be at least 1 second")
        if v > 30:
            raise ValueError("Timeout cannot exceed 30 seconds")
        return v


class CodeValidationRequest(BaseModel):
    """Code validation request."""

    code: str = Field(..., description="Python code to validate syntax", max_length=100000)
    test_code: str | None = Field(
        default=None, description="Optional test code to validate", max_length=50000
    )


class ExecutionResult(BaseModel):
    """Raw execution result from sandbox."""

    success: bool = Field(..., description="Whether execution succeeded")
    stdout: str = Field(default="", description="Standard output")
    stderr: str = Field(default="", description="Standard error")
    exit_code: int = Field(default=0, description="Process exit code")
    timeout: bool = Field(default=False, description="Whether execution timed out")
    error: str | None = Field(default=None, description="Error message if failed")
    duration_ms: int = Field(default=0, description="Execution duration in milliseconds")
    memory_usage_mb: float | None = Field(default=None, description="Peak memory usage in MB")


class CodeExecutionResponse(BaseModel):
    """Code execution response."""

    success: bool = Field(..., description="Whether execution succeeded")
    output: str = Field(default="", description="Standard output")
    error: str | None = Field(default=None, description="Error message if failed")
    execution_time_ms: int = Field(default=0, description="Execution time in milliseconds")
    exit_code: int | None = Field(default=None, description="Process exit code")
    timeout: bool = Field(default=False, description="Whether execution timed out")
    
    # Test results
    tests_passed: int | None = Field(default=None, description="Number of tests passed")
    tests_failed: int | None = Field(default=None, description="Number of tests failed")
    test_results: list[dict] | None = Field(default=None, description="Detailed test results")


class ValidationResponse(BaseModel):
    """Code validation response."""

    valid: bool = Field(..., description="Whether code is valid")
    error: str | None = Field(default=None, description="Error message if invalid")
    syntax_error_line: int | None = Field(default=None, description="Line number of syntax error")
    syntax_error_col: int | None = Field(default=None, description="Column of syntax error")


class TestResult(BaseModel):
    """Individual test result."""

    name: str = Field(..., description="Test name")
    passed: bool = Field(..., description="Whether test passed")
    output: str = Field(default="", description="Test output")
    error: str | None = Field(default=None, description="Error message if failed")
    duration_ms: int = Field(default=0, description="Test execution time in milliseconds")


class CodeValidationExecutionRequest(BaseModel):
    """Request for code validation with test execution."""

    code: str = Field(..., description="Python code to execute and validate", max_length=100000)
    test_code: str = Field(..., description="Test code to run against the solution", max_length=50000)
    timeout: int = Field(default=10, ge=1, le=30, description="Execution timeout in seconds")


class CodeValidationExecutionResponse(BaseModel):
    """Response for code validation with test execution."""

    success: bool = Field(..., description="Whether execution completed")
    passed: bool = Field(..., description="Whether all tests passed")
    tests_run: int = Field(default=0, description="Number of tests run")
    tests_passed: int = Field(default=0, description="Number of tests passed")
    tests_failed: int = Field(default=0, description="Number of tests failed")
    test_results: list[TestResult] = Field(default_factory=list, description="Individual test results")
    stdout: str = Field(default="", description="Combined standard output")
    stderr: str = Field(default="", description="Combined standard error")
    execution_time_ms: int = Field(default=0, description="Total execution time in milliseconds")
    error: str | None = Field(default=None, description="Error message if execution failed")


class ExecutionJobResponse(BaseModel):
    """Async execution job response."""

    job_id: str = Field(..., description="Unique job identifier")
    status: ExecutionStatus = Field(..., description="Current job status")
    message: str = Field(default="Job submitted successfully")
    result_url: str | None = Field(default=None, description="URL to check result")


class ExecutionJobResult(BaseModel):
    """Async execution job result."""

    job_id: str = Field(..., description="Unique job identifier")
    status: ExecutionStatus = Field(..., description="Current job status")
    result: CodeExecutionResponse | None = Field(default=None, description="Execution result if completed")
    created_at: datetime | None = Field(default=None, description="Job creation time")
    started_at: datetime | None = Field(default=None, description="Job start time")
    completed_at: datetime | None = Field(default=None, description="Job completion time")


class ExecutionMetrics(BaseModel):
    """Execution metrics for monitoring."""

    total_executions: int = Field(..., description="Total number of executions")
    successful_executions: int = Field(..., description="Number of successful executions")
    failed_executions: int = Field(..., description="Number of failed executions")
    timeout_executions: int = Field(..., description="Number of timeout executions")
    average_execution_time_ms: float = Field(..., description="Average execution time")
    average_memory_usage_mb: float | None = Field(default=None, description="Average memory usage")
    peak_memory_usage_mb: float | None = Field(default=None, description="Peak memory usage")
    failure_rate: float = Field(..., description="Failure rate as percentage")
    time_period: str = Field(..., description="Time period for metrics")


class ExecutionLogEntry(BaseModel):
    """Execution log entry."""

    id: str = Field(..., description="Log entry ID")
    user_id: str | None = Field(default=None, description="User ID if authenticated")
    code_length: int = Field(..., description="Length of executed code")
    status: ExecutionStatus = Field(..., description="Execution status")
    duration_ms: int = Field(..., description="Execution duration")
    exit_code: int | None = Field(default=None, description="Process exit code")
    error_type: str | None = Field(default=None, description="Type of error if failed")
    created_at: datetime = Field(..., description="Execution timestamp")
    ip_address: str | None = Field(default=None, description="Client IP address")
    user_agent: str | None = Field(default=None, description="Client user agent")


# ============================================================================
# Project Execution Schemas (Multi-File Support)
# ============================================================================


class ProjectFile(BaseModel):
    """A file in a project."""

    path: str = Field(..., description="File path relative to project root")
    content: str = Field(..., description="File content")


class ProjectFileValidation(BaseModel):
    """Validation result for a single project file."""

    file_path: str = Field(..., description="Path to the file")
    valid: bool = Field(..., description="Whether the file is valid")
    message: str = Field(default="", description="Validation message")
    line: int | None = Field(default=None, description="Line number of error (if any)")
    column: int | None = Field(default=None, description="Column number of error (if any)")


class ProjectValidationResponse(BaseModel):
    """Response for project validation."""

    valid: bool = Field(..., description="Whether all files are valid")
    validations: list[ProjectFileValidation] = Field(
        default_factory=list, description="Individual file validations"
    )
    message: str = Field(default="", description="Overall validation message")


class ProjectExecutionRequest(BaseModel):
    """Request for multi-file project execution."""

    files: dict[str, str] = Field(
        ..., description="Dictionary mapping file paths to content"
    )
    entry_point: str = Field(
        ..., description="Path to entry point file (e.g., 'src/main.py')"
    )
    timeout: int = Field(
        default=30, ge=1, le=30, description="Execution timeout in seconds"
    )

    @field_validator("files")
    @classmethod
    def validate_files_not_empty(cls, v: dict[str, str]) -> dict[str, str]:
        """Validate files dict is not empty."""
        if not v:
            raise ValueError("Files cannot be empty")
        return v

    @field_validator("entry_point")
    @classmethod
    def validate_entry_point(cls, v: str) -> str:
        """Validate entry point is a Python file."""
        if not v.endswith(".py"):
            raise ValueError("Entry point must be a Python file (.py)")
        return v


class ProjectExecutionResponse(BaseModel):
    """Response for multi-file project execution."""

    success: bool = Field(..., description="Whether execution succeeded")
    stdout: str = Field(default="", description="Standard output")
    stderr: str = Field(default="", description="Standard error")
    exit_code: int | None = Field(default=None, description="Process exit code")
    timeout: bool = Field(default=False, description="Whether execution timed out")
    error: str | None = Field(default=None, description="Error message if failed")
    execution_time_ms: int = Field(default=0, description="Execution time in milliseconds")


class ProjectTestSummary(BaseModel):
    """Summary of test results."""

    total: int = Field(default=0, description="Total number of tests")
    passed: int = Field(default=0, description="Number of passed tests")
    failed: int = Field(default=0, description="Number of failed tests")
    errors: int = Field(default=0, description="Number of tests with errors")
    skipped: int = Field(default=0, description="Number of skipped tests")


class ProjectTestResult(BaseModel):
    """Result of running project tests."""

    success: bool = Field(..., description="Whether all tests passed")
    tests: list[TestResult] = Field(default_factory=list, description="Individual test results")
    summary: ProjectTestSummary = Field(
        default_factory=lambda: ProjectTestSummary(), description="Test summary"
    )
    stdout: str = Field(default="", description="Standard output from test run")
    stderr: str = Field(default="", description="Standard error from test run")
    execution_time_ms: int = Field(default=0, description="Total execution time")
    error: str | None = Field(default=None, description="Error message if execution failed")


class ProjectTemplateFile(BaseModel):
    """A file in a project template."""

    path: str = Field(..., description="File path relative to project root")
    content: str | None = Field(default=None, description="File content (if any)")
    is_directory: bool = Field(default=False, description="Whether this is a directory")


class ProjectTemplate(BaseModel):
    """Project template from curriculum."""

    slug: str = Field(..., description="Project slug")
    title: str = Field(..., description="Project title")
    description: str = Field(default="", description="Project description")
    files: list[ProjectTemplateFile] = Field(default_factory=list, description="Template files")
    required_files: list[str] = Field(default_factory=list, description="Required file paths")
    entry_point: str = Field(default="src/main.py", description="Default entry point")
    week_slug: str | None = Field(default=None, description="Associated week slug")


class ProjectSaveRequest(BaseModel):
    """Request to save project state."""

    files: dict[str, str] = Field(..., description="Project files")
    is_auto_save: bool = Field(default=False, description="Whether this is an auto-save")


class ProjectSaveResponse(BaseModel):
    """Response for project save."""

    success: bool = Field(..., description="Whether save succeeded")
    saved_at: datetime = Field(default_factory=datetime.utcnow, description="Save timestamp")
    message: str = Field(default="", description="Status message")


class ProjectSubmissionResponse(BaseModel):
    """Response for project submission."""

    success: bool = Field(..., description="Whether submission succeeded")
    all_tests_passed: bool = Field(..., description="Whether all tests passed")
    test_result: ProjectTestResult | None = Field(default=None, description="Test results")
    submitted_at: datetime = Field(default_factory=datetime.utcnow, description="Submission timestamp")
    message: str = Field(default="", description="Status message")


class ProjectRunRequest(BaseModel):
    """Request to run a project."""

    files: dict[str, str] = Field(..., description="Project files")
    entry_point: str | None = Field(default=None, description="Override entry point")


class ProjectTestRequest(BaseModel):
    """Request to run project tests."""

    files: dict[str, str] = Field(..., description="Project files")
    test_path: str | None = Field(default=None, description="Specific test file or directory")


class ProjectMetadata(BaseModel):
    """Project metadata response."""

    slug: str = Field(..., description="Project slug")
    title: str = Field(..., description="Project title")
    description: str = Field(default="", description="Project description")
    file_structure: dict[str, Any] = Field(default_factory=dict, description="File tree structure")
    templates: dict[str, str] | None = Field(default=None, description="File templates")
    required_files: list[str] = Field(default_factory=list, description="Required files")
    entry_point: str = Field(default="src/main.py", description="Entry point file")
    week_slug: str | None = Field(default=None, description="Associated week slug")
