"""Spaced repetition service implementing SM-2 algorithm."""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.progress import Progress, ProblemStatus

logger = logging.getLogger(__name__)


@dataclass
class ReviewItem:
    """A review item for spaced repetition."""
    
    problem_slug: str
    ease_factor: float = 2.5  # EF in SM-2
    interval: int = 0  # Days between reviews
    repetitions: int = 0  # Number of successful reviews
    next_review: Optional[datetime] = None
    last_reviewed: Optional[datetime] = None
    priority: float = 0.0  # Calculated priority score
    
    def calculate_next_review(self, quality: int) -> None:
        """Calculate next review date based on SM-2 algorithm.
        
        Args:
            quality: Response quality (0-5)
                   0-2 = Incorrect response
                   3 = Correct with difficulty
                   4 = Correct with hesitation
                   5 = Perfect response
        """
        self.last_reviewed = datetime.utcnow()
        
        if quality < 3:
            # Failed review - reset repetitions
            self.repetitions = 0
            self.interval = 1
        else:
            # Successful review
            self.repetitions += 1
            
            if self.repetitions == 1:
                self.interval = 1
            elif self.repetitions == 2:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)
        
        # Update ease factor
        self.ease_factor = max(
            1.3,
            self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        )
        
        # Calculate next review date
        self.next_review = self.last_reviewed + timedelta(days=self.interval)
        
        # Update priority (lower = higher priority)
        self._update_priority()
    
    def _update_priority(self) -> None:
        """Update priority score based on due date and ease factor."""
        if not self.next_review:
            self.priority = float('inf')
            return
        
        now = datetime.utcnow()
        days_overdue = (now - self.next_review).total_seconds() / 86400
        
        # Priority formula: overdue days + ease factor weight + repetition bonus
        self.priority = max(0, days_overdue) + (3.0 - self.ease_factor) * 0.5 - self.repetitions * 0.1


@dataclass
class ReviewQueue:
    """Priority queue for review items."""
    
    items: List[ReviewItem] = field(default_factory=list)
    
    def add(self, item: ReviewItem) -> None:
        """Add item to queue."""
        self.items.append(item)
        self._sort()
    
    def _sort(self) -> None:
        """Sort by priority (lower = higher priority)."""
        self.items.sort(key=lambda x: x.priority)
    
    def get_due_items(self, now: Optional[datetime] = None) -> List[ReviewItem]:
        """Get all items due for review."""
        now = now or datetime.utcnow()
        return [
            item for item in self.items
            if item.next_review and item.next_review <= now
        ]
    
    def peek(self) -> Optional[ReviewItem]:
        """Get highest priority item without removing."""
        self._sort()
        return self.items[0] if self.items else None
    
    def pop(self) -> Optional[ReviewItem]:
        """Get and remove highest priority item."""
        self._sort()
        return self.items.pop(0) if self.items else None


class SpacedRepetitionService:
    """Service for managing spaced repetition reviews."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_review_queue(self, user_id: str) -> ReviewQueue:
        """Get user's review queue based on solved problems."""
        queue = ReviewQueue()
        
        # Get all solved problems that haven't been reviewed recently
        stmt = select(Progress).where(
            and_(
                Progress.user_id == user_id,
                Progress.status == ProblemStatus.SOLVED,
            )
        )
        result = await self.session.execute(stmt)
        solved_problems = list(result.scalars().all())
        
        for progress in solved_problems:
            # Calculate review metrics based on attempt history
            item = await self._create_review_item(progress)
            queue.add(item)
        
        return queue
    
    async def _create_review_item(self, progress: Progress) -> ReviewItem:
        """Create review item from progress record."""
        # Calculate ease factor based on attempts
        base_ef = 2.5
        if progress.attempts_count > 1:
            # Reduce EF if multiple attempts were needed
            base_ef -= min(0.5, (progress.attempts_count - 1) * 0.1)
        
        # Calculate interval based on time since solved
        interval = 1
        if progress.solved_at:
            days_since_solved = (datetime.utcnow() - progress.solved_at).days
            if days_since_solved > 0:
                interval = min(days_since_solved, 30)
        
        # Calculate repetitions based on time
        repetitions = min(3, interval // 6) if interval >= 6 else (1 if interval >= 1 else 0)
        
        item = ReviewItem(
            problem_slug=progress.problem_slug,
            ease_factor=base_ef,
            interval=interval,
            repetitions=repetitions,
            last_reviewed=progress.solved_at,
            next_review=self._calculate_initial_next_review(progress),
        )
        item._update_priority()
        return item
    
    def _calculate_initial_next_review(self, progress: Progress) -> datetime:
        """Calculate initial next review date."""
        if not progress.solved_at:
            return datetime.utcnow()
        
        # First review after 1 day
        # Second review after 6 days  
        # Then based on EF
        days = 1 if progress.attempts_count <= 2 else 6
        return progress.solved_at + timedelta(days=days)
    
    async def get_due_reviews(self, user_id: str, limit: int = 10) -> List[ReviewItem]:
        """Get problems due for review."""
        queue = await self.get_review_queue(user_id)
        due_items = queue.get_due_items()
        return due_items[:limit]
    
    async def get_review_stats(self, user_id: str) -> dict:
        """Get spaced repetition statistics."""
        queue = await self.get_review_queue(user_id)
        due_items = queue.get_due_items()
        
        # Get total items in queue
        total_items = len(queue.items)
        
        # Calculate items due today, this week
        now = datetime.utcnow()
        today_end = now + timedelta(days=1)
        week_end = now + timedelta(days=7)
        
        due_today = sum(1 for item in queue.items 
                       if item.next_review and item.next_review <= today_end)
        due_this_week = sum(1 for item in queue.items 
                           if item.next_review and item.next_review <= week_end)
        
        # Calculate average ease factor
        avg_ease_factor = sum(item.ease_factor for item in queue.items) / total_items if total_items else 2.5
        
        return {
            "total_items": total_items,
            "due_now": len(due_items),
            "due_today": due_today,
            "due_this_week": due_this_week,
            "average_ease_factor": round(avg_ease_factor, 2),
            "completed_reviews": await self._get_completed_reviews_count(user_id),
        }
    
    async def _get_completed_reviews_count(self, user_id: str) -> int:
        """Get count of completed reviews (solved problems with at least one review cycle)."""
        stmt = select(func.count()).select_from(Progress).where(
            and_(
                Progress.user_id == user_id,
                Progress.status == ProblemStatus.SOLVED,
                Progress.solved_at != None,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0
    
    async def record_review(
        self, 
        user_id: str, 
        problem_slug: str, 
        quality: int
    ) -> ReviewItem:
        """Record a review attempt and update SM-2 parameters.
        
        Args:
            user_id: User ID
            problem_slug: Problem being reviewed
            quality: 0-5 rating of recall quality
        """
        # Get progress record
        stmt = select(Progress).where(
            and_(
                Progress.user_id == user_id,
                Progress.problem_slug == problem_slug,
            )
        )
        result = await self.session.execute(stmt)
        progress = result.scalar_one_or_none()
        
        if not progress:
            raise ValueError(f"No progress found for problem {problem_slug}")
        
        # Create/update review item
        item = await self._create_review_item(progress)
        item.calculate_next_review(quality)
        
        # Log review activity
        logger.info(f"Review recorded for user {user_id}, problem {problem_slug}, quality {quality}")
        
        return item
    
    async def get_streak_info(self, user_id: str) -> dict:
        """Get review streak information."""
        stmt = select(Progress).where(
            and_(
                Progress.user_id == user_id,
                Progress.status == ProblemStatus.SOLVED,
            )
        ).order_by(Progress.solved_at.desc())
        
        result = await self.session.execute(stmt)
        solved = list(result.scalars().all())
        
        if not solved:
            return {
                "current_streak": 0,
                "longest_streak": 0,
                "last_review": None,
            }
        
        # Calculate streak based on review activity
        # For now, use solved dates as proxy
        review_dates = set()
        for p in solved:
            if p.solved_at:
                review_dates.add(p.solved_at.date())
            if p.last_attempted_at:
                review_dates.add(p.last_attempted_at.date())
        
        sorted_dates = sorted(review_dates, reverse=True)
        
        # Calculate current streak
        current_streak = 0
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)
        
        if sorted_dates and (sorted_dates[0] == today or sorted_dates[0] == yesterday):
            current_streak = 1
            for i in range(1, len(sorted_dates)):
                if sorted_dates[i] == sorted_dates[i-1] - timedelta(days=1):
                    current_streak += 1
                else:
                    break
        
        # Calculate longest streak
        longest_streak = 1
        current_count = 1
        sorted_asc = sorted(review_dates)
        
        for i in range(1, len(sorted_asc)):
            if sorted_asc[i] == sorted_asc[i-1] + timedelta(days=1):
                current_count += 1
                longest_streak = max(longest_streak, current_count)
            elif sorted_asc[i] != sorted_asc[i-1]:
                current_count = 1
        
        return {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "last_review": sorted_dates[0].isoformat() if sorted_dates else None,
        }


def get_spaced_repetition_service(session: AsyncSession) -> SpacedRepetitionService:
    """Factory function for SpacedRepetitionService."""
    return SpacedRepetitionService(session)
