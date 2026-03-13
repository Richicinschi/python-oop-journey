"""Submission service for managing project submissions and reviews."""

import logging
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select, desc, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.submission import Submission, SubmissionComment
from api.models.user import User
from api.schemas.submission import (
    SubmissionStatus,
    SubmissionCreate,
    SubmissionUpdate,
    CodeMetrics,
    TestResults,
    SubmissionChecklist,
    SubmissionResponse,
    GamificationStats,
)
from api.services.code_review import get_code_review_service

logger = logging.getLogger(__name__)


class SubmissionService:
    """Service for managing submissions and reviews."""

    def __init__(self, session: AsyncSession):
        """Initialize submission service.
        
        Args:
            session: SQLAlchemy async session
        """
        self.session = session
        self.code_review = get_code_review_service()

    async def create_submission(
        self,
        user_id: str,
        data: SubmissionCreate
    ) -> SubmissionResponse:
        """Create a new submission.
        
        Args:
            user_id: User ID submitting the project
            data: Submission creation data
            
        Returns:
            SubmissionResponse with submission details
        """
        logger.info(f"Creating submission for user={user_id} project={data.project_slug}")
        
        # Run automated checks
        checklist = await self._run_pre_submission_checklist(data.files)
        
        # Analyze code quality
        metrics = await self.code_review.analyze_code(data.files)
        
        # Run tests
        test_results = await self.code_review.run_tests(data.files)
        
        # Create submission
        submission = Submission(
            user_id=user_id,
            project_slug=data.project_slug,
            week_slug=data.week_slug,
            day_slug=data.day_slug,
            files=data.files,
            status=SubmissionStatus.PENDING_REVIEW.value,
            test_results=test_results.model_dump(),
            metrics=metrics.model_dump(),
            showcase_opt_in=data.showcase_opt_in,
        )
        
        self.session.add(submission)
        await self.session.commit()
        await self.session.refresh(submission)
        
        logger.info(f"Created submission {submission.id}")
        
        # Update checklist with test results
        checklist.all_tests_pass = test_results.failed == 0 and test_results.total > 0
        checklist.meets_min_quality = (
            metrics.docstring_coverage >= 50 and 
            metrics.lint_errors == 0
        )
        checklist.can_submit = checklist.all_tests_pass
        
        return SubmissionResponse(
            submission_id=submission.id,
            status=SubmissionStatus(submission.status),
            message="Submission created successfully" if checklist.can_submit 
                    else "Submission created but has issues",
            checklist=checklist,
            estimated_review_time="24-48 hours",
        )

    async def get_submission(self, submission_id: str) -> Submission | None:
        """Get a submission by ID.
        
        Args:
            submission_id: Submission ID
            
        Returns:
            Submission if found, None otherwise
        """
        stmt = select(Submission).where(Submission.id == submission_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_submissions(
        self,
        user_id: str,
        limit: int = 100,
        offset: int = 0,
        status: SubmissionStatus | None = None
    ) -> tuple[list[Submission], int]:
        """Get submissions for a user.
        
        Args:
            user_id: User ID
            limit: Maximum number of results
            offset: Pagination offset
            status: Optional status filter
            
        Returns:
            Tuple of (submissions list, total count)
        """
        # Build base query
        base_where = Submission.user_id == user_id
        if status:
            base_where = and_(base_where, Submission.status == status.value)
        
        # Get total count
        count_stmt = select(func.count()).select_from(Submission).where(base_where)
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar() or 0
        
        # Get submissions
        stmt = (
            select(Submission)
            .where(base_where)
            .order_by(desc(Submission.submitted_at))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        submissions = list(result.scalars().all())
        
        return submissions, total

    async def get_pending_reviews(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> tuple[list[Submission], int]:
        """Get submissions pending review.
        
        Args:
            limit: Maximum number of results
            offset: Pagination offset
            
        Returns:
            Tuple of (submissions list, total count)
        """
        # Get total count
        count_stmt = select(func.count()).select_from(Submission).where(
            Submission.status == SubmissionStatus.PENDING_REVIEW.value
        )
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar() or 0
        
        # Get pending submissions
        stmt = (
            select(Submission)
            .where(Submission.status == SubmissionStatus.PENDING_REVIEW.value)
            .order_by(Submission.submitted_at)  # Oldest first for queue
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        submissions = list(result.scalars().all())
        
        return submissions, total

    async def review_submission(
        self,
        submission_id: str,
        reviewer_id: str,
        data: SubmissionUpdate
    ) -> Submission | None:
        """Review a submission.
        
        Args:
            submission_id: Submission ID
            reviewer_id: Reviewer user ID
            data: Review update data
            
        Returns:
            Updated submission if found, None otherwise
        """
        submission = await self.get_submission(submission_id)
        if not submission:
            return None
        
        # Update submission
        submission.status = data.status.value
        submission.reviewer_notes = data.reviewer_notes
        submission.reviewed_by = reviewer_id
        submission.reviewed_at = datetime.utcnow()
        
        if data.is_exemplary is not None:
            submission.is_exemplary = data.is_exemplary
            # Auto-set status to exemplary if marked as exemplary
            if data.is_exemplary:
                submission.status = SubmissionStatus.EXEMPLARY.value
        
        await self.session.commit()
        await self.session.refresh(submission)
        
        logger.info(
            f"Reviewed submission {submission_id} by {reviewer_id}: {data.status.value}"
        )
        
        return submission

    async def get_submission_checklist(
        self,
        files: dict[str, str],
        project_slug: str
    ) -> SubmissionChecklist:
        """Get pre-submission checklist for files.
        
        Args:
            files: Dictionary of file paths to content
            project_slug: Project slug for checking required files
            
        Returns:
            SubmissionChecklist with status
        """
        return await self._run_pre_submission_checklist(files, project_slug)

    async def add_comment(
        self,
        submission_id: str,
        user_id: str,
        file_path: str,
        line_number: int,
        content: str
    ) -> SubmissionComment:
        """Add a comment to a submission.
        
        Args:
            submission_id: Submission ID
            user_id: User ID making the comment
            file_path: File path
            line_number: Line number
            content: Comment content
            
        Returns:
            Created comment
        """
        comment = SubmissionComment(
            submission_id=submission_id,
            user_id=user_id,
            file_path=file_path,
            line_number=line_number,
            content=content,
        )
        
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        
        return comment

    async def get_comments(
        self,
        submission_id: str,
        file_path: str | None = None
    ) -> list[SubmissionComment]:
        """Get comments for a submission.
        
        Args:
            submission_id: Submission ID
            file_path: Optional file path filter
            
        Returns:
            List of comments
        """
        where_clause = SubmissionComment.submission_id == submission_id
        if file_path:
            where_clause = and_(where_clause, SubmissionComment.file_path == file_path)
        
        stmt = (
            select(SubmissionComment)
            .where(where_clause)
            .order_by(SubmissionComment.file_path, SubmissionComment.line_number)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_gamification_stats(self, user_id: str) -> GamificationStats:
        """Get gamification stats for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            GamificationStats with user's achievements
        """
        # Get all submissions
        submissions, _ = await self.get_user_submissions(user_id, limit=1000)
        
        # Calculate stats
        total_submissions = len(submissions)
        approved_count = sum(
            1 for s in submissions 
            if s.status in (SubmissionStatus.APPROVED.value, SubmissionStatus.EXEMPLARY.value)
        )
        exemplary_count = sum(1 for s in submissions if s.is_exemplary)
        
        # Calculate streak
        current_streak, longest_streak = self._calculate_streak(submissions)
        
        # Generate badges
        badges = self._generate_badges(submissions, approved_count, exemplary_count, current_streak)
        
        # Recent achievements
        recent_achievements = [
            {
                "type": "submission",
                "title": f"Submitted {s.project_slug}",
                "date": s.submitted_at.isoformat(),
            }
            for s in submissions[:5]
        ]
        
        return GamificationStats(
            total_submissions=total_submissions,
            approved_count=approved_count,
            exemplary_count=exemplary_count,
            current_streak=current_streak,
            longest_streak=longest_streak,
            badges=badges,
            recent_achievements=recent_achievements,
        )

    async def _run_pre_submission_checklist(
        self,
        files: dict[str, str],
        project_slug: str | None = None
    ) -> SubmissionChecklist:
        """Run pre-submission checks.
        
        Args:
            files: Dictionary of file paths to content
            project_slug: Optional project slug for required file checks
            
        Returns:
            SubmissionChecklist with results
        """
        warnings = []
        
        # Check for files
        has_files = len(files) > 0
        if not has_files:
            warnings.append("No files submitted")
        
        # Check for required files (basic check)
        required_files_present = True
        if project_slug:
            required_files = self._get_required_files(project_slug)
            missing_files = []
            for req in required_files:
                if not any(req in path for path in files.keys()):
                    missing_files.append(req)
                    required_files_present = False
            if missing_files:
                warnings.append(f"Missing required files: {', '.join(missing_files)}")
        
        # Check code syntax
        all_valid = True
        for path, content in files.items():
            try:
                compile(content, path, 'exec')
            except SyntaxError as e:
                all_valid = False
                warnings.append(f"Syntax error in {path}: {e}")
        
        # Check for empty files
        has_content = any(content.strip() for content in files.values())
        if not has_content:
            warnings.append("All files are empty")
        
        # Default values - will be updated with actual test results after submission
        return SubmissionChecklist(
            all_tests_pass=False,  # Will be set after test run
            required_files_present=required_files_present,
            code_reviewed=False,  # User needs to confirm
            meets_min_quality=all_valid and has_content,
            can_submit=all_valid and has_files and has_content,
            warnings=warnings,
        )

    def _get_required_files(self, project_slug: str) -> list[str]:
        """Get required files for a project.
        
        Args:
            project_slug: Project slug
            
        Returns:
            List of required file names/patterns
        """
        # Default required files for Python projects
        defaults = ["main.py", "README.md"]
        
        # Project-specific requirements
        project_requirements = {
            "oop-basics": ["main.py", "classes.py"],
            "inheritance": ["main.py", "inheritance.py"],
            "polymorphism": ["main.py", "shapes.py"],
        }
        
        return project_requirements.get(project_slug, defaults)

    def _calculate_streak(self, submissions: list[Submission]) -> tuple[int, int]:
        """Calculate current and longest streak.
        
        Args:
            submissions: List of submissions
            
        Returns:
            Tuple of (current_streak, longest_streak)
        """
        if not submissions:
            return 0, 0
        
        # Get unique submission dates (only approved/exemplary)
        approved = [
            s for s in submissions 
            if s.status in (SubmissionStatus.APPROVED.value, SubmissionStatus.EXEMPLARY.value)
        ]
        
        if not approved:
            return 0, 0
        
        # Sort by date
        dates = sorted(set(
            s.submitted_at.date() for s in approved
        ))
        
        if not dates:
            return 0, 0
        
        # Calculate current streak
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)
        
        current_streak = 0
        if dates[-1] == today or dates[-1] == yesterday:
            current_streak = 1
            for i in range(len(dates) - 2, -1, -1):
                if dates[i] == dates[i + 1] - timedelta(days=1):
                    current_streak += 1
                else:
                    break
        
        # Calculate longest streak
        longest_streak = 1
        current = 1
        
        for i in range(1, len(dates)):
            if dates[i] == dates[i - 1] + timedelta(days=1):
                current += 1
                longest_streak = max(longest_streak, current)
            elif dates[i] != dates[i - 1]:
                current = 1
        
        return current_streak, longest_streak

    def _generate_badges(
        self,
        submissions: list[Submission],
        approved_count: int,
        exemplary_count: int,
        current_streak: int
    ) -> list[dict]:
        """Generate badges based on achievements.
        
        Args:
            submissions: List of submissions
            approved_count: Number of approved submissions
            exemplary_count: Number of exemplary submissions
            current_streak: Current streak
            
        Returns:
            List of badge objects
        """
        badges = []
        
        # First submission badge
        if submissions:
            badges.append({
                "id": "first_submission",
                "name": "First Steps",
                "description": "Submitted your first project",
                "icon": "🎯",
                "earned_at": submissions[0].submitted_at.isoformat(),
            })
        
        # Approved badge
        if approved_count > 0:
            badges.append({
                "id": "first_approval",
                "name": "Project Mastered",
                "description": "First project approved",
                "icon": "⭐",
                "earned_at": submissions[0].submitted_at.isoformat(),
            })
        
        # Multiple approvals
        if approved_count >= 5:
            badges.append({
                "id": "five_approvals",
                "name": "Rising Star",
                "description": "5 projects approved",
                "icon": "🌟",
            })
        
        if approved_count >= 10:
            badges.append({
                "id": "ten_approvals",
                "name": "OOP Expert",
                "description": "10 projects approved",
                "icon": "🏆",
            })
        
        # Exemplary badge
        if exemplary_count > 0:
            badges.append({
                "id": "exemplary",
                "name": "Code Artist",
                "description": "Achieved exemplary status",
                "icon": "🎨",
            })
        
        # Streak badges
        if current_streak >= 3:
            badges.append({
                "id": "streak_3",
                "name": "On Fire",
                "description": "3 day submission streak",
                "icon": "🔥",
            })
        
        if current_streak >= 7:
            badges.append({
                "id": "streak_7",
                "name": "Week Warrior",
                "description": "7 day submission streak",
                "icon": "⚡",
            })
        
        return badges


# Service factory
def get_submission_service(session: AsyncSession) -> SubmissionService:
    """Factory function for SubmissionService.
    
    Args:
        session: Database session
        
    Returns:
        SubmissionService instance
    """
    return SubmissionService(session)
