"""Tests for progress persistence system."""

import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.progress import Progress, ProblemStatus
from api.models.draft import Draft
from api.models.bookmark import Bookmark, ItemType
from api.models.activity import Activity, ActivityType
from api.models.user import User
from api.services.progress import ProgressService
from api.services.draft import DraftService
from api.services.bookmark import BookmarkService
from api.services.activity import ActivityService


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user."""
    user = User(email="test@example.com")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def progress_service(db_session: AsyncSession) -> ProgressService:
    """Create a progress service."""
    return ProgressService(db_session)


@pytest.fixture
def draft_service(db_session: AsyncSession) -> DraftService:
    """Create a draft service."""
    return DraftService(db_session)


@pytest.fixture
def bookmark_service(db_session: AsyncSession) -> BookmarkService:
    """Create a bookmark service."""
    return BookmarkService(db_session)


@pytest.fixture
def activity_service(db_session: AsyncSession) -> ActivityService:
    """Create an activity service."""
    return ActivityService(db_session)


class TestProgressService:
    """Test progress tracking functionality."""

    async def test_create_progress(self, test_user, progress_service):
        """Test creating a new progress entry."""
        progress = await progress_service.get_or_create_progress(
            test_user.id, "week01_day01_problem01"
        )
        
        assert progress is not None
        assert progress.user_id == test_user.id
        assert progress.problem_slug == "week01_day01_problem01"
        assert progress.status == ProblemStatus.NOT_STARTED
        assert progress.attempts_count == 0

    async def test_update_progress_status(self, test_user, progress_service):
        """Test updating progress status."""
        progress = await progress_service.update_progress(
            test_user.id,
            "week01_day01_problem01",
            status=ProblemStatus.IN_PROGRESS,
            week_slug="week01",
            day_slug="day01",
        )
        
        assert progress.status == ProblemStatus.IN_PROGRESS
        assert progress.week_slug == "week01"
        assert progress.day_slug == "day01"
        assert progress.first_attempted_at is not None

    async def test_solve_problem(self, test_user, progress_service):
        """Test marking a problem as solved."""
        progress = await progress_service.update_progress(
            test_user.id,
            "week01_day01_problem01",
            status=ProblemStatus.SOLVED,
        )
        
        assert progress.status == ProblemStatus.SOLVED
        assert progress.solved_at is not None

    async def test_record_attempt(self, test_user, progress_service):
        """Test recording an attempt."""
        progress = await progress_service.record_attempt(
            test_user.id, "week01_day01_problem01"
        )
        
        assert progress.attempts_count == 1
        assert progress.last_attempted_at is not None

    async def test_get_week_progress(self, test_user, progress_service):
        """Test getting week progress statistics."""
        # Create some progress entries
        await progress_service.update_progress(
            test_user.id, "problem1", status=ProblemStatus.SOLVED, week_slug="week01"
        )
        await progress_service.update_progress(
            test_user.id, "problem2", status=ProblemStatus.IN_PROGRESS, week_slug="week01"
        )
        await progress_service.update_progress(
            test_user.id, "problem3", status=ProblemStatus.NOT_STARTED, week_slug="week01"
        )
        
        stats = await progress_service.get_week_progress(test_user.id, "week01")
        
        assert stats["total_problems"] == 3
        assert stats["completed"] == 1
        assert stats["in_progress"] == 1
        assert stats["not_started"] == 1

    async def test_calculate_streak(self, test_user, progress_service, activity_service):
        """Test streak calculation."""
        # Log activities for consecutive days
        today = datetime.now(timezone.utc)
        
        for i in range(3):
            activity_date = today - timedelta(days=i)
            await activity_service.log_activity(
                test_user.id,
                ActivityType.SOLVED_PROBLEM,
                item_slug=f"problem{i}",
            )
        
        streak = await progress_service.calculate_streak(test_user.id)
        assert streak >= 1  # At least today counts


class TestDraftService:
    """Test draft functionality."""

    async def test_save_draft(self, test_user, draft_service):
        """Test saving a draft."""
        draft = await draft_service.save_draft(
            test_user.id,
            "week01_day01_problem01",
            "print('Hello World')",
            is_auto_save=False,
        )
        
        assert draft is not None
        assert draft.code == "print('Hello World')"
        assert draft.is_auto_save is False

    async def test_get_draft(self, test_user, draft_service):
        """Test retrieving a draft."""
        await draft_service.save_draft(
            test_user.id,
            "week01_day01_problem01",
            "code here",
        )
        
        draft = await draft_service.get_draft(test_user.id, "week01_day01_problem01")
        
        assert draft is not None
        assert draft.code == "code here"

    async def test_delete_draft(self, test_user, draft_service):
        """Test deleting a draft."""
        await draft_service.save_draft(
            test_user.id,
            "week01_day01_problem01",
            "code to delete",
        )
        
        deleted = await draft_service.delete_draft(test_user.id, "week01_day01_problem01")
        assert deleted is True
        
        draft = await draft_service.get_draft(test_user.id, "week01_day01_problem01")
        assert draft is None


class TestBookmarkService:
    """Test bookmark functionality."""

    async def test_create_bookmark(self, test_user, bookmark_service):
        """Test creating a bookmark."""
        bookmark = await bookmark_service.create_bookmark(
            test_user.id,
            ItemType.PROBLEM,
            "week01_day01_problem01",
            notes="Important problem",
        )
        
        assert bookmark is not None
        assert bookmark.item_type == ItemType.PROBLEM
        assert bookmark.notes == "Important problem"

    async def test_is_bookmarked(self, test_user, bookmark_service):
        """Test checking bookmark status."""
        await bookmark_service.create_bookmark(
            test_user.id, ItemType.PROBLEM, "problem1"
        )
        
        is_bookmarked = await bookmark_service.is_bookmarked(
            test_user.id, ItemType.PROBLEM, "problem1"
        )
        assert is_bookmarked is True

    async def test_toggle_bookmark(self, test_user, bookmark_service):
        """Test toggling a bookmark."""
        # First toggle - create
        is_bookmarked, bookmark = await bookmark_service.toggle_bookmark(
            test_user.id, ItemType.WEEK, "week01"
        )
        assert is_bookmarked is True
        assert bookmark is not None
        
        # Second toggle - delete
        is_bookmarked, bookmark = await bookmark_service.toggle_bookmark(
            test_user.id, ItemType.WEEK, "week01"
        )
        assert is_bookmarked is False


class TestActivityService:
    """Test activity logging functionality."""

    async def test_log_activity(self, test_user, activity_service):
        """Test logging an activity."""
        activity = await activity_service.log_activity(
            test_user.id,
            ActivityType.SOLVED_PROBLEM,
            item_slug="problem1",
            metadata={"time_spent": 300},
        )
        
        assert activity is not None
        assert activity.activity_type == ActivityType.SOLVED_PROBLEM
        assert activity.metadata == {"time_spent": 300}

    async def test_get_recent_activity(self, test_user, activity_service):
        """Test retrieving recent activity."""
        # Log some activities
        for i in range(5):
            await activity_service.log_activity(
                test_user.id,
                ActivityType.ATTEMPTED_PROBLEM,
                item_slug=f"problem{i}",
            )
        
        activities = await activity_service.get_recent_activity(test_user.id, limit=3)
        assert len(activities) == 3

    async def test_get_activity_summary(self, test_user, activity_service):
        """Test getting activity summary."""
        # Log activities
        await activity_service.log_activity(
            test_user.id, ActivityType.STARTED_PROBLEM, "problem1"
        )
        await activity_service.log_activity(
            test_user.id, ActivityType.SOLVED_PROBLEM, "problem1"
        )
        await activity_service.log_activity(
            test_user.id, ActivityType.VIEWED_THEORY, "week01_day01"
        )
        
        summary = await activity_service.get_activity_summary(test_user.id, days=7)
        
        assert summary["total_activities"] == 3
        assert summary["problems_started"] == 1
        assert summary["problems_solved"] == 1
        assert summary["theory_views"] == 1
