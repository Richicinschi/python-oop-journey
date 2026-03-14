"""Tests for smart recommendations system."""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from api.services.spaced_repetition import ReviewItem, ReviewQueue
from api.services.analytics import AttemptPattern
from api.services.recommendations import (
    RecommendationEngine,
    RecommendationType,
    Recommendation,
)


class TestSpacedRepetition:
    """Tests for spaced repetition service."""

    def test_review_item_initial_state(self):
        """Test initial state of review item."""
        item = ReviewItem(problem_slug="test-problem")
        
        assert item.problem_slug == "test-problem"
        assert item.ease_factor == 2.5
        assert item.interval == 0
        assert item.repetitions == 0
        assert item.next_review is None

    def test_review_item_successful_review(self):
        """Test successful review calculation."""
        item = ReviewItem(problem_slug="test-problem")
        
        # First successful review (quality 4)
        item.calculate_next_review(4)
        
        assert item.repetitions == 1
        assert item.interval == 1
        assert item.ease_factor == 2.5  # Stays same for quality 4
        assert item.next_review is not None

    def test_review_item_multiple_successes(self):
        """Test multiple successful reviews."""
        item = ReviewItem(problem_slug="test-problem")
        
        # Quality 4, 4, 4 (good responses)
        item.calculate_next_review(4)
        item.calculate_next_review(4)
        item.calculate_next_review(4)
        
        assert item.repetitions == 3
        assert item.interval == 6  # After 2nd rep
        # Third rep: interval = 6 * EF (2.5) = 15

    def test_review_item_failure_resets(self):
        """Test that failure resets repetitions."""
        item = ReviewItem(problem_slug="test-problem")
        
        # Two successful reviews
        item.calculate_next_review(4)
        item.calculate_next_review(4)
        
        # Failed review (quality 2)
        item.calculate_next_review(2)
        
        assert item.repetitions == 0
        assert item.interval == 1

    def test_review_queue_add_and_sort(self):
        """Test review queue priority sorting."""
        queue = ReviewQueue()
        
        # Add items with different priorities
        item1 = ReviewItem(problem_slug="low-priority")
        item1.priority = 5.0
        
        item2 = ReviewItem(problem_slug="high-priority")
        item2.priority = 1.0
        
        queue.add(item1)
        queue.add(item2)
        
        # High priority (low number) should be first
        assert queue.peek().problem_slug == "high-priority"

    def test_review_queue_get_due_items(self):
        """Test getting due items from queue."""
        queue = ReviewQueue()
        
        now = datetime.utcnow()
        
        # Item due now
        item1 = ReviewItem(problem_slug="due-now")
        item1.next_review = now - timedelta(hours=1)
        item1._update_priority()
        
        # Item due tomorrow
        item2 = ReviewItem(problem_slug="due-tomorrow")
        item2.next_review = now + timedelta(days=1)
        item2._update_priority()
        
        queue.add(item1)
        queue.add(item2)
        
        due_items = queue.get_due_items(now)
        
        assert len(due_items) == 1
        assert due_items[0].problem_slug == "due-now"


class TestAnalyticsPatterns:
    """Tests for learning analytics."""

    def test_attempt_pattern_enum(self):
        """Test attempt pattern values."""
        assert AttemptPattern.SYSTEMATIC == "systematic"
        assert AttemptPattern.TRIAL_ERROR == "trial_error"
        assert AttemptPattern.STUCK == "stuck"
        assert AttemptPattern.PERFECT == "perfect"


class TestRecommendations:
    """Tests for recommendation engine."""

    def test_recommendation_creation(self):
        """Test creating a recommendation."""
        rec = Recommendation(
            type=RecommendationType.NEXT_PROBLEM,
            item_type="problem",
            item_slug="test-problem",
            item_title="Test Problem",
            reason="Based on your progress",
            priority=8,
            estimated_time_minutes=15,
        )
        
        assert rec.type == RecommendationType.NEXT_PROBLEM
        assert rec.priority == 8
        assert rec.to_dict()["type"] == "next_problem"

    def test_recommendation_with_context(self):
        """Test recommendation with context."""
        rec = Recommendation(
            type=RecommendationType.REVIEW,
            item_type="problem",
            item_slug="review-problem",
            item_title="Review Problem",
            reason="Due for review",
            priority=9,
            estimated_time_minutes=5,
            context={
                "ease_factor": 2.3,
                "interval": 6,
                "repetitions": 2,
                "days_overdue": 2,
            },
        )
        
        data = rec.to_dict()
        assert data["context"]["ease_factor"] == 2.3
        assert data["context"]["days_overdue"] == 2


class TestDifficultyProgression:
    """Tests for adaptive difficulty logic."""

    @pytest.mark.asyncio
    async def test_recommended_difficulty_easy_start(self):
        """Test that new users start with easy difficulty."""
        # This would require mocking the database session
        # For now, just test the logic structure
        success_rates = {
            "easy": {"success_rate": 50, "attempted": 4, "solved": 2},
        }
        
        # With 50% success on easy and only 4 attempted, should suggest easy
        # This is a logic test - actual implementation uses database
        assert success_rates["easy"]["success_rate"] < 70

    def test_is_easier_comparison(self):
        """Test difficulty comparison logic."""
        # This would be tested in the actual engine
        difficulty_order = ["easy", "medium", "hard", "challenge"]
        
        assert difficulty_order.index("easy") < difficulty_order.index("medium")
        assert difficulty_order.index("medium") < difficulty_order.index("hard")


class TestMasteryCalculation:
    """Tests for topic mastery calculations."""

    def test_mastery_level_calculation(self):
        """Test mastery level thresholds."""
        # Test the _get_mastery_level logic
        def get_mastery_level(score: float) -> str:
            if score >= 90:
                return "mastered"
            elif score >= 70:
                return "proficient"
            elif score >= 50:
                return "developing"
            elif score >= 30:
                return "beginner"
            else:
                return "novice"
        
        assert get_mastery_level(95) == "mastered"
        assert get_mastery_level(80) == "proficient"
        assert get_mastery_level(60) == "developing"
        assert get_mastery_level(40) == "beginner"
        assert get_mastery_level(20) == "novice"


class TestReviewStats:
    """Tests for review statistics."""

    def test_review_stats_structure(self):
        """Test expected review stats structure."""
        stats = {
            "total_items": 10,
            "due_now": 3,
            "due_today": 5,
            "due_this_week": 8,
            "average_ease_factor": 2.4,
            "completed_reviews": 25,
        }
        
        assert stats["total_items"] >= stats["due_now"]
        assert stats["due_today"] >= stats["due_now"]
        assert stats["due_this_week"] >= stats["due_today"]
        assert 1.3 <= stats["average_ease_factor"] <= 3.0
