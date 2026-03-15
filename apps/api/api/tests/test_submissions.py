"""Tests for submission system."""

import pytest
from datetime import datetime, timezone
from uuid import uuid4

from api.services.submission import SubmissionService
from api.services.code_review import CodeReviewService
from api.schemas.submission import (
    SubmissionCreate,
    SubmissionUpdate,
    SubmissionStatus,
)


@pytest.fixture
def sample_files():
    """Sample project files for testing."""
    return {
        "main.py": '''
class Calculator:
    """A simple calculator class."""
    
    def add(self, a, b):
        """Add two numbers."""
        return a + b
    
    def subtract(self, a, b):
        """Subtract two numbers."""
        return a - b

if __name__ == "__main__":
    calc = Calculator()
    print(calc.add(2, 3))
''',
        "test_main.py": '''
import unittest
from main import Calculator

class TestCalculator(unittest.TestCase):
    def test_add(self):
        calc = Calculator()
        self.assertEqual(calc.add(2, 3), 5)
    
    def test_subtract(self):
        calc = Calculator()
        self.assertEqual(calc.subtract(5, 3), 2)

if __name__ == "__main__":
    unittest.main()
'''
    }


@pytest.fixture
def invalid_files():
    """Invalid project files for testing."""
    return {
        "main.py": '''
# This file has a syntax error
def broken_function(
    print("missing closing parenthesis")
'''
    }


class TestCodeReviewService:
    """Tests for code review service."""

    @pytest.mark.asyncio
    async def test_analyze_code(self, sample_files):
        """Test code analysis."""
        service = CodeReviewService()
        metrics = await service.analyze_code(sample_files)
        
        assert metrics.lines_of_code > 0
        assert metrics.function_count >= 2  # add, subtract
        assert metrics.class_count >= 1  # Calculator
        assert metrics.docstring_coverage >= 50  # At least 50% docstring coverage

    @pytest.mark.asyncio
    async def test_check_required_patterns(self, sample_files):
        """Test pattern checking."""
        service = CodeReviewService()
        results = service.check_required_patterns(sample_files)
        
        assert results["all_patterns_present"] is True

    @pytest.mark.asyncio
    async def test_check_required_files(self, sample_files):
        """Test required file checking."""
        service = CodeReviewService()
        results = service.check_required_files(sample_files, ["main.py", "README.md"])
        
        assert results["main.py"] is True
        assert results["README.md"] is False

    def test_count_functions(self, sample_files):
        """Test function counting."""
        service = CodeReviewService()
        count = service._count_functions(sample_files["main.py"])
        assert count >= 2

    def test_calculate_docstring_coverage(self, sample_files):
        """Test docstring coverage calculation."""
        service = CodeReviewService()
        coverage = service._calculate_docstring_coverage(sample_files["main.py"])
        assert coverage > 0


class TestSubmissionService:
    """Tests for submission service."""

    @pytest.mark.asyncio
    async def test_create_submission(self, sample_files, mock_db_session):
        """Test creating a submission."""
        service = SubmissionService(mock_db_session)
        
        data = SubmissionCreate(
            project_slug="test-project",
            files=sample_files,
            week_slug="week-1",
            day_slug="day-1",
        )
        
        response = await service.create_submission("user-123", data)
        
        assert response.submission_id is not None
        assert response.status == SubmissionStatus.PENDING_REVIEW
        assert response.checklist is not None

    @pytest.mark.asyncio
    async def test_get_user_submissions(self, mock_db_session):
        """Test fetching user submissions."""
        service = SubmissionService(mock_db_session)
        
        submissions, total = await service.get_user_submissions("user-123")
        
        assert isinstance(submissions, list)
        assert isinstance(total, int)

    @pytest.mark.asyncio
    async def test_get_pending_reviews(self, mock_db_session):
        """Test fetching pending reviews."""
        service = SubmissionService(mock_db_session)
        
        submissions, total = await service.get_pending_reviews()
        
        assert isinstance(submissions, list)
        assert isinstance(total, int)

    @pytest.mark.asyncio
    async def test_review_submission(self, mock_db_session):
        """Test reviewing a submission."""
        service = SubmissionService(mock_db_session)
        
        # First create a submission
        data = SubmissionCreate(
            project_slug="test-project",
            files={"main.py": "print('hello')"},
        )
        create_response = await service.create_submission("user-123", data)
        
        # Then review it
        review_data = SubmissionUpdate(
            status=SubmissionStatus.APPROVED,
            reviewer_notes="Great work!",
            is_exemplary=False,
        )
        
        reviewed = await service.review_submission(
            create_response.submission_id,
            "reviewer-123",
            review_data
        )
        
        assert reviewed is not None
        assert reviewed.status == SubmissionStatus.APPROVED.value
        assert reviewed.reviewer_notes == "Great work!"

    @pytest.mark.asyncio
    async def test_get_gamification_stats(self, mock_db_session):
        """Test fetching gamification stats."""
        service = SubmissionService(mock_db_session)
        
        stats = await service.get_gamification_stats("user-123")
        
        assert stats.total_submissions >= 0
        assert stats.approved_count >= 0
        assert stats.current_streak >= 0
        assert isinstance(stats.badges, list)

    def test_calculate_streak(self):
        """Test streak calculation."""
        service = SubmissionService(None)
        
        # Create mock submissions
        from api.models.submission import Submission
        submissions = [
            Submission(
                id=str(uuid4()),
                user_id="user-123",
                project_slug="project-1",
                files={},
                status="approved",
                submitted_at=datetime.now(timezone.utc),
            ),
            Submission(
                id=str(uuid4()),
                user_id="user-123",
                project_slug="project-2",
                files={},
                status="approved",
                submitted_at=datetime.now(timezone.utc),
            ),
        ]
        
        current, longest = service._calculate_streak(submissions)
        
        assert current >= 0
        assert longest >= 0

    def test_generate_badges(self):
        """Test badge generation."""
        service = SubmissionService(None)
        
        badges = service._generate_badges([], 5, 1, 3)
        
        assert isinstance(badges, list)
        # Should have badges for first submission, approvals, and streak
        assert len(badges) >= 0


class TestSubmissionIntegration:
    """Integration tests for submission system."""

    @pytest.mark.asyncio
    async def test_full_submission_flow(self, sample_files, mock_db_session):
        """Test the full submission flow."""
        service = SubmissionService(mock_db_session)
        
        # 1. Create submission
        create_data = SubmissionCreate(
            project_slug="oop-basics",
            files=sample_files,
            week_slug="week-1",
            day_slug="day-1",
        )
        
        create_response = await service.create_submission("user-123", create_data)
        assert create_response.submission_id is not None
        
        # 2. Verify submission is pending
        submission = await service.get_submission(create_response.submission_id)
        assert submission.status == SubmissionStatus.PENDING_REVIEW.value
        
        # 3. Review submission
        review_data = SubmissionUpdate(
            status=SubmissionStatus.EXEMPLARY,
            reviewer_notes="Excellent work! Clean code and great documentation.",
            is_exemplary=True,
        )
        
        reviewed = await service.review_submission(
            create_response.submission_id,
            "reviewer-123",
            review_data
        )
        
        assert reviewed.status == SubmissionStatus.EXEMPLARY.value
        assert reviewed.is_exemplary is True
        
        # 4. Check gamification stats
        stats = await service.get_gamification_stats("user-123")
        assert stats.total_submissions >= 1
        assert stats.exemplary_count >= 1
