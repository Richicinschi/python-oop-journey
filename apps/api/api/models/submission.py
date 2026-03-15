"""Submission model for project submissions and reviews."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import String, DateTime, ForeignKey, Text, JSON, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base


class Submission(Base):
    """Project submission model for tracking user submissions and reviews."""

    __tablename__ = "submissions"

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
    project_slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    week_slug: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )
    day_slug: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )
    
    # Code snapshot - stored as JSON to capture all files
    files: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
    
    # Submission timing
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    
    # Review status
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending_review",
        index=True,
    )
    
    # Reviewer information
    reviewer_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    reviewed_by: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Test results - stored as JSON
    test_results: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
    
    # Code metrics - stored as JSON
    metrics: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
    
    # Gamification fields
    is_exemplary: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    showcase_opt_in: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    # Notification tracking
    notification_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    notification_sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="submissions",
    )
    reviewer: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[reviewed_by],
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Submission id={self.id} user={self.user_id} project={self.project_slug} status={self.status}>"


class SubmissionComment(Base):
    """Comments on specific lines of code in submissions."""

    __tablename__ = "submission_comments"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    submission_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("submissions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    line_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    is_resolved: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Relationships
    submission: Mapped["Submission"] = relationship("Submission", lazy="selectin")
    user: Mapped["User"] = relationship("User", lazy="selectin")

    def __repr__(self) -> str:
        return f"<SubmissionComment id={self.id} submission={self.submission_id} line={self.line_number}>"
