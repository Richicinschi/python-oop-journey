"""User and auth schemas."""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class UserBase(BaseModel):
    """Base user schema."""

    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


class UserCreate(UserBase):
    """User creation schema."""

    pass


class UserUpdate(BaseModel):
    """User update schema."""

    display_name: str | None = Field(None, max_length=100)
    avatar_url: str | None = Field(None, max_length=500)


class User(UserBase):
    """User response schema."""

    id: str
    display_name: str | None = None
    avatar_url: str | None = None
    auth_provider: str | None = None  # e.g., "email", "google", "github"
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None
    last_seen: datetime
    is_active: bool
    is_admin: bool

    model_config = {"from_attributes": True}


class ProgressBase(BaseModel):
    """Base progress schema."""

    problem_slug: str
    status: str = "not_started"
    attempts: int = 0


class ProgressCreate(ProgressBase):
    """Progress creation schema."""

    pass


class Progress(ProgressBase):
    """Progress response schema."""

    id: int
    user_id: str
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DraftBase(BaseModel):
    """Base draft schema."""

    problem_slug: str
    code: str


class DraftCreate(DraftBase):
    """Draft creation schema."""

    pass


class Draft(DraftBase):
    """Draft response schema."""

    id: int
    user_id: str
    saved_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class MagicLinkRequest(BaseModel):
    """Magic link request schema."""

    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


class MagicLinkVerify(BaseModel):
    """Magic link verification schema."""

    token: str


class MagicLinkResponse(BaseModel):
    """Magic link response schema."""

    success: bool
    message: str

    model_config = {"extra": "allow"}


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
    expires_in: int


class UserStats(BaseModel):
    """User statistics schema."""

    total_problems: int
    completed_problems: int
    in_progress_problems: int
    completion_percentage: float
    streak_days: int
    favorite_week: str | None


class AuthResponse(BaseModel):
    """Authentication response with user and token."""

    user: User
    access_token: str
    token_type: str = "bearer"
    expires_in: int
