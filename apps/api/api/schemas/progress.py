"""Progress and tracking schemas."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ProblemStatus(str, Enum):
    """Problem completion status."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SOLVED = "solved"
    NEEDS_REVIEW = "needs_review"


class ProgressBase(BaseModel):
    """Base progress schema."""

    problem_slug: str
    status: ProblemStatus = ProblemStatus.NOT_STARTED


class ProgressCreate(ProgressBase):
    """Progress creation schema."""

    week_slug: str | None = None
    day_slug: str | None = None


class ProgressUpdate(BaseModel):
    """Progress update schema."""

    status: ProblemStatus | None = None
    time_spent_seconds: int | None = None
    add_attempt: bool = False


class Progress(ProgressBase):
    """Progress response schema."""

    id: str
    user_id: str
    week_slug: str | None = None
    day_slug: str | None = None
    attempts_count: int = 0
    solved_at: datetime | None = None
    first_attempted_at: datetime | None = None
    last_attempted_at: datetime | None = None
    time_spent_seconds: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProgressList(BaseModel):
    """List of progress entries."""

    items: list[Progress]
    total: int


class WeekProgress(BaseModel):
    """Progress for a specific week."""

    week_slug: str
    total_problems: int
    completed: int
    in_progress: int
    not_started: int
    completion_percentage: float


class ProgressStats(BaseModel):
    """Overall progress statistics."""

    total_problems: int
    completed: int
    in_progress: int
    not_started: int
    completion_percentage: float
    current_streak: int
    longest_streak: int
    total_time_spent_seconds: int
    last_active_at: datetime | None = None


class DraftBase(BaseModel):
    """Base draft schema."""

    problem_slug: str
    code: str = ""


class DraftCreate(DraftBase):
    """Draft creation schema."""

    is_auto_save: bool = False


class DraftUpdate(BaseModel):
    """Draft update schema."""

    code: str
    is_auto_save: bool = False


class Draft(DraftBase):
    """Draft response schema."""

    id: str
    user_id: str
    saved_at: datetime
    is_auto_save: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class DraftList(BaseModel):
    """List of drafts."""

    items: list[Draft]
    total: int


class ItemType(str, Enum):
    """Types of bookmarkable items."""

    PROBLEM = "problem"
    DAY = "day"
    WEEK = "week"
    THEORY = "theory"


class BookmarkBase(BaseModel):
    """Base bookmark schema."""

    item_type: ItemType
    item_slug: str


class BookmarkCreate(BookmarkBase):
    """Bookmark creation schema."""

    notes: str | None = None


class BookmarkUpdate(BaseModel):
    """Bookmark update schema."""

    notes: str | None = None


class Bookmark(BookmarkBase):
    """Bookmark response schema."""

    id: str
    user_id: str
    notes: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class BookmarkList(BaseModel):
    """List of bookmarks."""

    items: list[Bookmark]
    total: int


class BookmarkCheck(BaseModel):
    """Bookmark check response."""

    is_bookmarked: bool
    bookmark_id: str | None = None


class ActivityType(str, Enum):
    """Types of user activities."""

    STARTED_PROBLEM = "started_problem"
    SOLVED_PROBLEM = "solved_problem"
    ATTEMPTED_PROBLEM = "attempted_problem"
    VIEWED_THEORY = "viewed_theory"
    VIEWED_WEEK = "viewed_week"
    VIEWED_DAY = "viewed_day"
    SAVED_DRAFT = "saved_draft"
    CREATED_BOOKMARK = "created_bookmark"
    DELETED_BOOKMARK = "deleted_bookmark"
    LOGIN = "login"
    LOGOUT = "logout"


class ActivityBase(BaseModel):
    """Base activity schema."""

    activity_type: ActivityType
    item_slug: str | None = None
    metadata: dict | None = None


class ActivityCreate(ActivityBase):
    """Activity creation schema."""

    pass


class Activity(ActivityBase):
    """Activity response schema."""

    id: str
    user_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ActivityList(BaseModel):
    """List of activities."""

    items: list[Activity]
    total: int


class ActivitySummary(BaseModel):
    """Activity summary for a time period."""

    period_days: int
    total_activities: int
    problems_started: int
    problems_solved: int
    problems_attempted: int
    theory_views: int
    unique_days_active: int
