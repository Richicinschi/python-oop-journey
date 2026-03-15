"""Activity log model for tracking user actions."""

from datetime import datetime
from enum import Enum as PyEnum
from uuid import uuid4

from sqlalchemy import String, DateTime, ForeignKey, JSON, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base


class ActivityType(str, PyEnum):
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


class Activity(Base):
    """Activity log entry for user actions."""

    __tablename__ = "activities"
    __table_args__ = (
        # Composite index for user activity queries with date sorting
        Index("idx_activity_user_created", "user_id", "created_at", postgresql_using="btree"),
        # Composite index for filtering by user and activity type
        Index("idx_activity_user_type", "user_id", "activity_type", postgresql_using="btree"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    activity_type: Mapped[ActivityType] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    item_slug: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )
    meta_data: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="activities")

    def __repr__(self) -> str:
        return f"<Activity user={self.user_id} type={self.activity_type} item={self.item_slug}>"
