"""Smart recommendations service for personalized learning."""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import List, Optional, Dict, Any, Union
from uuid import uuid4

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.progress import Progress, ProblemStatus
from api.models.activity import Activity, ActivityType
from api.services.curriculum import CurriculumService
from api.services.spaced_repetition import SpacedRepetitionService
from api.services.analytics import LearningAnalytics

logger = logging.getLogger(__name__)


class RecommendationType(str, Enum):
    """Types of recommendations."""
    NEXT_PROBLEM = "next_problem"
    REVIEW = "review"
    THEORY = "theory"
    PRACTICE = "practice"
    DIFFICULTY_ADJUSTMENT = "difficulty_adjustment"
    REMEDIAL = "remedial"
    CHALLENGE = "challenge"


class DifficultyLevel(str, Enum):
    """Problem difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    CHALLENGE = "challenge"


@dataclass
class Recommendation:
    """A learning recommendation."""
    
    type: RecommendationType
    item_type: str  # "problem", "day", "week", "theory"
    item_slug: str
    item_title: str
    reason: str
    priority: int  # 1-10
    estimated_time_minutes: int
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "type": self.type.value,
            "itemType": self.item_type,
            "itemSlug": self.item_slug,
            "itemTitle": self.item_title,
            "reason": self.reason,
            "priority": self.priority,
            "estimatedTimeMinutes": self.estimated_time_minutes,
            "context": self.context,
        }


@dataclass
class WeakArea:
    """A topic area where the user is struggling."""
    
    topic_slug: str
    topic_name: str
    mastery_score: float
    level: str
    problems_struggled: List[str]
    suggested_remediation: str
    priority: int


@dataclass
class LearningPath:
    """Personalized learning path."""
    
    steps: List[Dict[str, Any]]
    estimated_weeks: int
    focus_areas: List[str]
    skipped_topics: List[str]
    reasoning: str


class RecommendationEngine:
    """Engine for generating smart learning recommendations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.curriculum = CurriculumService()
        self.spaced_rep = SpacedRepetitionService(session)
        self.analytics = LearningAnalytics(session)
        
        # Difficulty progression thresholds
        self.DIFFICULTY_THRESHOLDS = {
            DifficultyLevel.EASY: {"success_rate": 0.7, "min_solved": 5},
            DifficultyLevel.MEDIUM: {"success_rate": 0.6, "min_solved": 10},
            DifficultyLevel.HARD: {"success_rate": 0.5, "min_solved": 15},
            DifficultyLevel.CHALLENGE: {"success_rate": 0.8, "min_solved": 20},  # Requires strong medium performance
        }
    
    async def get_next_problem(self, user_id: str) -> Optional[Recommendation]:
        """Get the next recommended problem for the user.
        
        Considers:
        - Current progress
        - Performance on similar problems
        - Time spent per difficulty
        - Learning path gaps
        """
        # Get user's progress
        stmt = select(Progress).where(Progress.user_id == user_id)
        result = await self.session.execute(stmt)
        progress_list = list(result.scalars().all())
        
        # Build progress lookup
        progress_map = {p.problem_slug: p for p in progress_list}
        
        # Get all problems from curriculum
        all_problems = self.curriculum.list_problems()
        
        # Determine recommended difficulty
        recommended_difficulty = await self._get_recommended_difficulty(user_id)
        
        # Filter to unsolved problems of appropriate difficulty
        candidates = []
        for prob in all_problems:
            slug = prob["slug"]
            if slug not in progress_map:
                # Not started - high priority
                if prob["difficulty"] == recommended_difficulty:
                    candidates.append((prob, 10))
                elif self._is_easier(prob["difficulty"], recommended_difficulty):
                    candidates.append((prob, 7))
            elif progress_map[slug].status == ProblemStatus.IN_PROGRESS:
                # Started but not solved - medium priority
                candidates.append((prob, 8))
        
        if not candidates:
            # All problems done - suggest review or challenge
            return await self._get_challenge_recommendation(user_id)
        
        # Sort by priority and curriculum order
        candidates.sort(key=lambda x: (-x[1], x[0].get("week_slug", "")))
        
        # Pick the best candidate
        chosen = candidates[0][0]
        
        # Build recommendation reason
        reason = self._build_next_problem_reason(chosen, progress_map.get(chosen["slug"]))
        
        return Recommendation(
            type=RecommendationType.NEXT_PROBLEM,
            item_type="problem",
            item_slug=chosen["slug"],
            item_title=chosen["title"],
            reason=reason,
            priority=9,
            estimated_time_minutes=self._estimate_time(chosen["difficulty"]),
            context={
                "difficulty": chosen["difficulty"],
                "week_slug": chosen.get("week_slug"),
                "day_slug": chosen.get("day_slug"),
            },
        )
    
    def _is_easier(self, difficulty1: str, difficulty2: str) -> bool:
        """Check if difficulty1 is easier than difficulty2."""
        order = ["easy", "medium", "hard", "challenge"]
        try:
            return order.index(difficulty1) < order.index(difficulty2)
        except ValueError:
            return False
    
    async def _get_recommended_difficulty(self, user_id: str) -> str:
        """Determine the recommended difficulty level for the user."""
        # Get success rates by difficulty
        success_rates = await self.analytics.get_success_rate_by_difficulty(user_id)
        
        # Count problems solved per difficulty
        stmt = select(Progress).where(
            and_(
                Progress.user_id == user_id,
                Progress.status == ProblemStatus.SOLVED,
            )
        )
        result = await self.session.execute(stmt)
        solved = list(result.scalars().all())
        
        # Get difficulty of solved problems
        solved_by_difficulty = {"easy": 0, "medium": 0, "hard": 0, "challenge": 0}
        for progress in solved:
            prob = self.curriculum.get_problem(progress.problem_slug)
            if prob:
                diff = prob["problem"].difficulty
                solved_by_difficulty[diff] = solved_by_difficulty.get(diff, 0) + 1
        
        # Decision logic based on success rates and solved counts
        easy_rate = success_rates.get("easy", {}).get("success_rate", 0)
        medium_rate = success_rates.get("medium", {}).get("success_rate", 0)
        hard_rate = success_rates.get("hard", {}).get("success_rate", 0)
        
        # Don't suggest challenge until medium success rate > 80%
        if solved_by_difficulty["medium"] >= 10 and medium_rate >= 80:
            if hard_rate >= 50 and solved_by_difficulty["hard"] >= 5:
                return "challenge"
            return "hard"
        
        if easy_rate >= 70 or solved_by_difficulty["easy"] >= 5:
            return "medium"
        
        return "easy"
    
    def _estimate_time(self, difficulty: str) -> int:
        """Estimate time in minutes for a problem based on difficulty."""
        estimates = {
            "easy": 10,
            "medium": 20,
            "hard": 35,
            "challenge": 60,
        }
        return estimates.get(difficulty, 20)
    
    def _build_next_problem_reason(self, problem: Dict, progress: Optional[Progress]) -> str:
        """Build a personalized reason for the recommendation."""
        if not progress:
            return f"This {problem['difficulty']} problem introduces key concepts in {problem.get('day_title', 'this topic')}."
        
        if progress.status == ProblemStatus.IN_PROGRESS:
            if progress.attempts_count > 3:
                return f"You've attempted this {problem['difficulty']} problem {progress.attempts_count} times. Take a fresh approach!"
            return f"You started this problem but haven't solved it yet. Continue where you left off."
        
        return f"Based on your progress, this {problem['difficulty']} problem is a good next step."
    
    async def get_review_suggestions(self, user_id: str, limit: int = 5) -> List[Recommendation]:
        """Get problems due for review using spaced repetition."""
        due_items = await self.spaced_rep.get_due_reviews(user_id, limit)
        
        recommendations = []
        for item in due_items:
            problem = self.curriculum.get_problem(item.problem_slug)
            if not problem:
                continue
            
            days_overdue = (datetime.now(timezone.utc) - item.next_review).days if item.next_review else 0
            
            reason = f"Due for review"
            if days_overdue > 0:
                reason += f" ({days_overdue} days overdue)"
            reason += ". Spaced repetition helps solidify your knowledge."
            
            recommendations.append(Recommendation(
                type=RecommendationType.REVIEW,
                item_type="problem",
                item_slug=item.problem_slug,
                item_title=problem["problem"].title,
                reason=reason,
                priority=min(10, 7 + days_overdue),
                estimated_time_minutes=5,
                context={
                    "ease_factor": round(item.ease_factor, 2),
                    "interval": item.interval,
                    "repetitions": item.repetitions,
                    "days_overdue": days_overdue,
                },
            ))
        
        return recommendations
    
    async def get_weak_areas(self, user_id: str) -> List[WeakArea]:
        """Identify topics where the user is struggling.
        
        Analyzes:
        - Failed attempts
        - Multiple attempts before success
        - Abandoned problems
        - Low mastery scores
        """
        topic_mastery = await self.analytics.get_topic_mastery(user_id)
        
        # Get attempt patterns
        patterns = await self.analytics.get_attempt_patterns(user_id)
        
        weak_areas = []
        
        # Find topics with low mastery
        for topic_slug, data in topic_mastery.items():
            if data["score"] < 50:
                # Get struggling problems in this topic
                problems = await self._get_struggling_problems(user_id, topic_slug)
                
                if problems:
                    weak_areas.append(WeakArea(
                        topic_slug=topic_slug,
                        topic_name=data["name"],
                        mastery_score=data["score"],
                        level=data["level"],
                        problems_struggled=[p["slug"] for p in problems],
                        suggested_remediation=self._get_remediation_suggestion(topic_slug, problems),
                        priority=self._calculate_weak_area_priority(data, problems),
                    ))
        
        # Sort by priority (higher = more urgent)
        weak_areas.sort(key=lambda x: -x.priority)
        
        return weak_areas
    
    async def _get_struggling_problems(self, user_id: str, week_slug: str) -> List[Dict]:
        """Get problems the user is struggling with in a topic."""
        stmt = select(Progress).where(
            and_(
                Progress.user_id == user_id,
                Progress.week_slug == week_slug,
            )
        )
        result = await self.session.execute(stmt)
        progress_list = list(result.scalars().all())
        
        struggling = []
        for progress in progress_list:
            # Criteria for struggling:
            # - Many attempts without solving
            # - Solved but took many attempts
            is_struggling = (
                (progress.status != ProblemStatus.SOLVED and progress.attempts_count > 3) or
                (progress.status == ProblemStatus.SOLVED and progress.attempts_count > 5)
            )
            
            if is_struggling:
                problem = self.curriculum.get_problem(progress.problem_slug)
                if problem:
                    struggling.append({
                        "slug": progress.problem_slug,
                        "attempts": progress.attempts_count,
                        "status": progress.status.value,
                    })
        
        return struggling
    
    def _get_remediation_suggestion(self, topic_slug: str, problems: List[Dict]) -> str:
        """Generate a remediation suggestion for a weak area."""
        # Get topic info
        week = self.curriculum.get_week(topic_slug)
        if not week:
            return "Review the fundamentals and practice more problems."
        
        suggestions = [
            f"Review the theory section for {week.title}",
            "Try the guided exercises before attempting problems",
            "Use the hint system when you get stuck",
        ]
        
        return " • ".join(suggestions)
    
    def _calculate_weak_area_priority(self, mastery_data: Dict, problems: List[Dict]) -> int:
        """Calculate priority score for a weak area."""
        base_score = 10 - int(mastery_data["score"] / 10)  # Lower score = higher priority
        problem_bonus = min(5, len(problems))  # More problems = higher priority
        return min(10, base_score + problem_bonus)
    
    async def get_learning_path(self, user_id: str) -> LearningPath:
        """Generate a personalized learning path.
        
        - Skip mastered topics
        - Spend more time on weak areas
        - Suggest theory review before problems
        """
        topic_mastery = await self.analytics.get_topic_mastery(user_id)
        weak_areas = await self.get_weak_areas(user_id)
        
        # Get curriculum weeks
        curriculum = self.curriculum.get_curriculum()
        
        steps = []
        skipped = []
        focus_areas = []
        
        for week in curriculum.weeks:
            mastery = topic_mastery.get(week.slug, {})
            score = mastery.get("score", 0)
            
            if score >= 90:
                # Mastered - can be skipped
                skipped.append(week.title)
                steps.append({
                    "type": "skipped",
                    "week_slug": week.slug,
                    "week_title": week.title,
                    "reason": "Already mastered",
                })
            elif score >= 70:
                # Proficient - quick review
                steps.append({
                    "type": "review",
                    "week_slug": week.slug,
                    "week_title": week.title,
                    "reason": "Quick review to reinforce",
                    "estimated_days": 1,
                })
            elif score >= 40:
                # Developing - standard path
                steps.append({
                    "type": "theory",
                    "week_slug": week.slug,
                    "week_title": week.title,
                    "reason": "Study theory first",
                    "estimated_days": 1,
                })
                steps.append({
                    "type": "practice",
                    "week_slug": week.slug,
                    "week_title": week.title,
                    "reason": "Complete all problems",
                    "estimated_days": 3,
                })
            else:
                # Novice/Beginner - intensive focus
                focus_areas.append(week.title)
                steps.append({
                    "type": "theory",
                    "week_slug": week.slug,
                    "week_title": week.title,
                    "reason": "Careful study required",
                    "estimated_days": 2,
                })
                steps.append({
                    "type": "guided",
                    "week_slug": week.slug,
                    "week_title": week.title,
                    "reason": "Start with guided exercises",
                    "estimated_days": 2,
                })
                steps.append({
                    "type": "practice",
                    "week_slug": week.slug,
                    "week_title": week.title,
                    "reason": "Practice with hints",
                    "estimated_days": 4,
                })
        
        # Estimate total weeks
        total_days = sum(s.get("estimated_days", 0) for s in steps)
        estimated_weeks = max(1, total_days // 5)
        
        return LearningPath(
            steps=steps,
            estimated_weeks=estimated_weeks,
            focus_areas=focus_areas,
            skipped_topics=skipped,
            reasoning=self._build_path_reasoning(focus_areas, skipped),
        )
    
    def _build_path_reasoning(self, focus_areas: List[str], skipped: List[str]) -> str:
        """Build reasoning text for the learning path."""
        parts = []
        
        if focus_areas:
            parts.append(f"Focus on: {', '.join(focus_areas[:3])}")
        
        if skipped:
            parts.append(f"Skipping {len(skipped)} mastered topics")
        
        if not parts:
            return "Following the standard curriculum path"
        
        return " • ".join(parts)
    
    async def get_difficulty_suggestion(self, user_id: str) -> Optional[Recommendation]:
        """Suggest difficulty adjustment based on performance."""
        success_rates = await self.analytics.get_success_rate_by_difficulty(user_id)
        current_difficulty = await self._get_recommended_difficulty(user_id)
        
        # Check if ready for harder difficulty
        if current_difficulty == "easy":
            easy_rate = success_rates.get("easy", {}).get("success_rate", 0)
            if easy_rate >= 80:
                return Recommendation(
                    type=RecommendationType.DIFFICULTY_ADJUSTMENT,
                    item_type="suggestion",
                    item_slug="ready-for-medium",
                    item_title="Ready for Medium Problems!",
                    reason=f"Great job! You've achieved {easy_rate}% success on easy problems. Time to try medium difficulty!",
                    priority=8,
                    estimated_time_minutes=0,
                    context={
                        "current_difficulty": "easy",
                        "suggested_difficulty": "medium",
                        "success_rate": easy_rate,
                    },
                )
        
        elif current_difficulty == "medium":
            medium_rate = success_rates.get("medium", {}).get("success_rate", 0)
            if medium_rate >= 80:
                return Recommendation(
                    type=RecommendationType.DIFFICULTY_ADJUSTMENT,
                    item_type="suggestion",
                    item_slug="ready-for-hard",
                    item_title="Ready for Hard Problems!",
                    reason=f"Excellent progress! {medium_rate}% success on medium problems. Challenge yourself with hard problems!",
                    priority=8,
                    estimated_time_minutes=0,
                    context={
                        "current_difficulty": "medium",
                        "suggested_difficulty": "hard",
                        "success_rate": medium_rate,
                    },
                )
        
        # Check if struggling and should try easier
        for diff in ["medium", "hard"]:
            rate = success_rates.get(diff, {}).get("success_rate", 0)
            if rate < 30 and success_rates.get(diff, {}).get("attempted", 0) > 5:
                easier = "easy" if diff == "medium" else "medium"
                return Recommendation(
                    type=RecommendationType.DIFFICULTY_ADJUSTMENT,
                    item_type="suggestion",
                    item_slug=f"consider-{easier}",
                    item_title=f"Try {easier.title()} Problems First",
                    reason=f"Having trouble with {diff} problems? Build confidence with {easier} problems first.",
                    priority=7,
                    estimated_time_minutes=0,
                    context={
                        "current_difficulty": diff,
                        "suggested_difficulty": easier,
                        "success_rate": rate,
                    },
                )
        
        return None
    
    async def _get_challenge_recommendation(self, user_id: str) -> Optional[Recommendation]:
        """Get a challenge recommendation when user has solved many problems."""
        all_problems = self.curriculum.list_problems()
        
        # Find a hard or challenge problem not yet solved
        stmt = select(Progress).where(
            and_(
                Progress.user_id == user_id,
                Progress.status == ProblemStatus.SOLVED,
            )
        )
        result = await self.session.execute(stmt)
        solved_slugs = {p.problem_slug for p in result.scalars().all()}
        
        challenges = [p for p in all_problems 
                     if p["slug"] not in solved_slugs and p["difficulty"] in ["hard", "challenge"]]
        
        if challenges:
            challenge = challenges[0]
            return Recommendation(
                type=RecommendationType.CHALLENGE,
                item_type="problem",
                item_slug=challenge["slug"],
                item_title=challenge["title"],
                reason="You've solved many problems! Ready for a challenge?",
                priority=7,
                estimated_time_minutes=self._estimate_time(challenge["difficulty"]),
                context={
                    "difficulty": challenge["difficulty"],
                    "is_challenge": True,
                },
            )
        
        return None
    
    async def get_all_recommendations(self, user_id: str) -> List[Recommendation]:
        """Get all recommendations sorted by priority."""
        recommendations = []
        
        # 1. Reviews (highest priority for learning retention)
        reviews = await self.get_review_suggestions(user_id, limit=3)
        recommendations.extend(reviews)
        
        # 2. Next problem
        next_prob = await self.get_next_problem(user_id)
        if next_prob:
            recommendations.append(next_prob)
        
        # 3. Difficulty suggestion
        difficulty_rec = await self.get_difficulty_suggestion(user_id)
        if difficulty_rec:
            recommendations.append(difficulty_rec)
        
        # 4. Weak areas remedial
        weak_areas = await self.get_weak_areas(user_id)
        if weak_areas:
            top_weak = weak_areas[0]
            recommendations.append(Recommendation(
                type=RecommendationType.REMEDIAL,
                item_type="week",
                item_slug=top_weak.topic_slug,
                item_title=top_weak.topic_name,
                reason=f"Focus area: Your mastery score is {top_weak.mastery_score}%. {top_weak.suggested_remediation}",
                priority=8,
                estimated_time_minutes=30,
                context={
                    "mastery_score": top_weak.mastery_score,
                    "problems_struggled": top_weak.problems_struggled,
                },
            ))
        
        # Sort by priority (higher first)
        recommendations.sort(key=lambda r: -r.priority)
        
        return recommendations[:10]  # Limit to top 10


def get_recommendation_engine(session: AsyncSession) -> RecommendationEngine:
    """Factory function for RecommendationEngine."""
    return RecommendationEngine(session)
