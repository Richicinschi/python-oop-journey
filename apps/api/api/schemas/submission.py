"""Submission schemas for API requests and responses."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class SubmissionStatus(str, Enum):
    """Submission review status."""

    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    NEEDS_WORK = "needs_work"
    EXEMPLARY = "exemplary"


class TestResult(BaseModel):
    """Individual test result."""

    name: str
    passed: bool
    duration_ms: int
    output: str | None = None
    error: str | None = None


class TestResults(BaseModel):
    """Complete test results for a submission."""

    total: int
    passed: int
    failed: int
    success_rate: float
    tests: list[TestResult]
    stdout: str | None = None
    stderr: str | None = None
    execution_time_ms: int


class CodeMetrics(BaseModel):
    """Code quality metrics for a submission."""

    lines_of_code: int
    total_lines: int
    blank_lines: int
    comment_lines: int
    function_count: int
    class_count: int
    average_function_length: float
    docstring_coverage: float  # percentage
    complexity_score: float | None = None
    lint_errors: int
    lint_warnings: int


class FileSnapshot(BaseModel):
    """Single file in a submission snapshot."""

    path: str
    content: str
    language: str = "python"


class SubmissionBase(BaseModel):
    """Base submission schema."""

    project_slug: str
    files: dict[str, str]  # path -> content mapping
    week_slug: str | None = None
    day_slug: str | None = None


class SubmissionCreate(SubmissionBase):
    """Schema for creating a submission."""

    showcase_opt_in: bool = False


class SubmissionUpdate(BaseModel):
    """Schema for updating submission status (review)."""

    status: SubmissionStatus
    reviewer_notes: str | None = None
    is_exemplary: bool | None = None


class Submission(SubmissionBase):
    """Complete submission response schema."""

    id: str
    user_id: str
    submitted_at: datetime
    status: SubmissionStatus
    reviewer_notes: str | None = None
    reviewed_at: datetime | None = None
    reviewed_by: str | None = None
    reviewer_name: str | None = None
    test_results: TestResults
    metrics: CodeMetrics
    is_exemplary: bool
    showcase_opt_in: bool
    project_name: str | None = None

    model_config = {"from_attributes": True}


class SubmissionListItem(BaseModel):
    """Simplified submission for list views."""

    id: str
    project_slug: str
    project_name: str | None = None
    week_slug: str | None = None
    day_slug: str | None = None
    submitted_at: datetime
    status: SubmissionStatus
    test_summary: dict  # { total, passed, failed }
    metrics_summary: dict  # { lines_of_code, function_count }
    is_exemplary: bool

    model_config = {"from_attributes": True}


class SubmissionList(BaseModel):
    """List of submissions."""

    items: list[SubmissionListItem]
    total: int
    page: int
    page_size: int


class SubmissionFilters(BaseModel):
    """Filters for submission queries."""

    status: SubmissionStatus | None = None
    week_slug: str | None = None
    project_slug: str | None = None
    user_id: str | None = None


class SubmissionChecklist(BaseModel):
    """Pre-submission checklist status."""

    all_tests_pass: bool
    required_files_present: bool
    code_reviewed: bool  # user has self-reviewed
    meets_min_quality: bool
    can_submit: bool
    warnings: list[str]


class SubmissionResponse(BaseModel):
    """Response after creating a submission."""

    submission_id: str
    status: SubmissionStatus
    message: str
    checklist: SubmissionChecklist
    estimated_review_time: str = "24-48 hours"


class SubmissionCommentCreate(BaseModel):
    """Schema for creating a submission comment."""

    file_path: str
    line_number: int = Field(..., ge=1)
    content: str = Field(..., min_length=1, max_length=2000)


class SubmissionCommentUpdate(BaseModel):
    """Schema for updating a submission comment."""

    content: str | None = Field(None, min_length=1, max_length=2000)
    is_resolved: bool | None = None


class SubmissionComment(BaseModel):
    """Submission comment response schema."""

    id: str
    submission_id: str
    user_id: str
    user_name: str | None = None
    file_path: str
    line_number: int
    content: str
    created_at: datetime
    updated_at: datetime
    is_resolved: bool

    model_config = {"from_attributes": True}


class SubmissionCommentList(BaseModel):
    """List of submission comments."""

    items: list[SubmissionComment]
    total: int


class CodeLineComment(BaseModel):
    """Comment attached to a specific line of code."""

    line_number: int
    comments: list[SubmissionComment]


class ReviewQueueItem(BaseModel):
    """Item in the review queue for mentors."""

    id: str
    project_slug: str
    project_name: str | None = None
    user_id: str
    user_name: str | None = None
    submitted_at: datetime
    waiting_hours: float
    test_summary: dict
    metrics_summary: dict
    priority_score: float  # For ordering queue

    model_config = {"from_attributes": True}


class ReviewQueue(BaseModel):
    """Review queue for mentors."""

    pending_count: int
    items: list[ReviewQueueItem]
    my_reviews_today: int
    avg_review_time_hours: float | None = None


class BatchReviewAction(BaseModel):
    """Batch action for reviewing multiple submissions."""

    submission_ids: list[str]
    status: SubmissionStatus
    reviewer_notes: str | None = None


class BatchReviewResult(BaseModel):
    """Result of batch review action."""

    processed: int
    failed: int
    errors: list[str]


class GamificationStats(BaseModel):
    """Gamification stats for submissions."""

    total_submissions: int
    approved_count: int
    exemplary_count: int
    current_streak: int
    longest_streak: int
    badges: list[dict]  # Badge objects
    recent_achievements: list[dict]


class NotificationSettings(BaseModel):
    """Notification preferences for submissions."""

    email_on_review: bool = True
    in_app_notifications: bool = True
    show_in_showcase: bool = False
