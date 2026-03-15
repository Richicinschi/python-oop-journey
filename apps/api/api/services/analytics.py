"""Learning analytics service for tracking and analyzing user performance."""

import logging
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
from enum import Enum

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.progress import Progress, ProblemStatus
from api.models.activity import Activity, ActivityType
from api.services.curriculum import CurriculumService

logger = logging.getLogger(__name__)


class ErrorType(str, Enum):
    """Types of common errors."""
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    LOGIC = "logic"
    IMPORT = "import"
    ATTRIBUTE = "attribute"
    TYPE_ERROR = "type_error"
    INDENTATION = "indentation"
    OTHER = "other"


class AttemptPattern(str, Enum):
    """Pattern of user attempts."""
    SYSTEMATIC = "systematic"  # Thoughtful, incremental
    TRIAL_ERROR = "trial_error"  # Quick guesses
    STUCK = "stuck"  # Multiple failures without progress
    PERFECT = "perfect"  # First try success


class LearningAnalytics:
    """Analytics for learning patterns and performance."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.curriculum = CurriculumService()
    
    async def get_time_analytics(self, user_id: str) -> Dict[str, Any]:
        """Analyze time spent per difficulty level."""
        stmt = select(Progress).where(
            and_(
                Progress.user_id == user_id,
                Progress.time_spent_seconds > 0,
            )
        )
        result = await self.session.execute(stmt)
        progress_list = list(result.scalars().all())
        
        # Group by difficulty
        time_by_difficulty = defaultdict(lambda: {"total": 0, "count": 0, "times": []})
        
        for progress in progress_list:
            # Get problem difficulty from curriculum
            problem = self.curriculum.get_problem(progress.problem_slug)
            difficulty = problem["problem"].difficulty if problem else "medium"
            
            time_by_difficulty[difficulty]["total"] += progress.time_spent_seconds
            time_by_difficulty[difficulty]["count"] += 1
            time_by_difficulty[difficulty]["times"].append(progress.time_spent_seconds)
        
        # Calculate averages and format
        analytics = {}
        for difficulty, data in time_by_difficulty.items():
            times = data["times"]
            analytics[difficulty] = {
                "total_time_seconds": data["total"],
                "total_time_formatted": self._format_duration(data["total"]),
                "problem_count": data["count"],
                "average_time_seconds": round(data["total"] / data["count"], 2) if data["count"] else 0,
                "average_time_formatted": self._format_duration(data["total"] // data["count"]) if data["count"] else "0m",
                "median_time_seconds": sorted(times)[len(times) // 2] if times else 0,
                "min_time_seconds": min(times) if times else 0,
                "max_time_seconds": max(times) if times else 0,
            }
        
        return analytics
    
    def _format_duration(self, seconds: int) -> str:
        """Format seconds to readable duration."""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m"
        else:
            hours = seconds // 3600
            mins = (seconds % 3600) // 60
            return f"{hours}h {mins}m"
    
    async def get_attempt_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user's attempt patterns."""
        stmt = select(Progress).where(
            Progress.user_id == user_id
        )
        result = await self.session.execute(stmt)
        progress_list = list(result.scalars().all())
        
        patterns = {
            "systematic": 0,  # 2-5 attempts
            "trial_error": 0,  # >10 attempts or very quick retries
            "stuck": 0,  # Many failed attempts
            "perfect": 0,  # 1 attempt success
            "total": len(progress_list),
        }
        
        pattern_details = []
        
        for progress in progress_list:
            if progress.status == ProblemStatus.SOLVED:
                if progress.attempts_count == 1:
                    patterns["perfect"] += 1
                    pattern = AttemptPattern.PERFECT
                elif 2 <= progress.attempts_count <= 5:
                    patterns["systematic"] += 1
                    pattern = AttemptPattern.SYSTEMATIC
                elif progress.attempts_count > 10:
                    patterns["trial_error"] += 1
                    pattern = AttemptPattern.TRIAL_ERROR
                else:
                    patterns["systematic"] += 1
                    pattern = AttemptPattern.SYSTEMATIC
            else:
                if progress.attempts_count > 5:
                    patterns["stuck"] += 1
                    pattern = AttemptPattern.STUCK
                else:
                    pattern = AttemptPattern.TRIAL_ERROR
            
            pattern_details.append({
                "problem_slug": progress.problem_slug,
                "attempts": progress.attempts_count,
                "status": progress.status.value,
                "pattern": pattern.value,
            })
        
        # Calculate percentages
        total = patterns["total"] or 1
        return {
            "counts": patterns,
            "percentages": {
                "systematic": round(patterns["systematic"] / total * 100, 1),
                "trial_error": round(patterns["trial_error"] / total * 100, 1),
                "stuck": round(patterns["stuck"] / total * 100, 1),
                "perfect": round(patterns["perfect"] / total * 100, 1),
            },
            "dominant_pattern": max(
                ["systematic", "trial_error", "stuck", "perfect"],
                key=lambda x: patterns[x]
            ),
            "details": pattern_details[:20],  # Limit details
        }
    
    async def get_error_analytics(self, user_id: str) -> Dict[str, Any]:
        """Analyze common error types from activities."""
        # Get recent activities with error metadata
        stmt = select(Activity).where(
            and_(
                Activity.user_id == user_id,
                Activity.activity_type.in_([
                    ActivityType.ATTEMPTED_PROBLEM,
                ]),
            )
        ).order_by(Activity.created_at.desc()).limit(100)
        
        result = await self.session.execute(stmt)
        activities = list(result.scalars().all())
        
        # Count error types from metadata
        error_counts = defaultdict(int)
        error_contexts = defaultdict(list)
        
        for activity in activities:
            if activity.metadata and "error_type" in activity.metadata:
                error_type = activity.metadata["error_type"]
                error_counts[error_type] += 1
                error_contexts[error_type].append({
                    "problem_slug": activity.item_slug,
                    "timestamp": activity.created_at.isoformat(),
                    "message": activity.metadata.get("error_message", ""),
                })
        
        # Map to error types
        error_summary = {
            "counts": dict(error_counts),
            "most_common": max(error_counts.keys(), key=lambda x: error_counts[x]) if error_counts else None,
            "contexts": {k: v[:5] for k, v in error_contexts.items()},  # Limit contexts
            "total_errors": sum(error_counts.values()),
        }
        
        return error_summary
    
    async def get_topic_mastery(self, user_id: str) -> Dict[str, Any]:
        """Calculate mastery levels for each topic."""
        stmt = select(Progress).where(Progress.user_id == user_id)
        result = await self.session.execute(stmt)
        progress_list = list(result.scalars().all())
        
        # Group by week/day topics
        topic_stats = defaultdict(lambda: {
            "total": 0,
            "solved": 0,
            "in_progress": 0,
            "total_attempts": 0,
            "total_time": 0,
        })
        
        for progress in progress_list:
            topic_key = progress.week_slug or "unknown"
            
            topic_stats[topic_key]["total"] += 1
            topic_stats[topic_key]["total_attempts"] += progress.attempts_count
            topic_stats[topic_key]["total_time"] += progress.time_spent_seconds
            
            if progress.status == ProblemStatus.SOLVED:
                topic_stats[topic_key]["solved"] += 1
            elif progress.status == ProblemStatus.IN_PROGRESS:
                topic_stats[topic_key]["in_progress"] += 1
        
        # Calculate mastery scores
        mastery = {}
        for topic, stats in topic_stats.items():
            if stats["total"] == 0:
                continue
            
            # Mastery formula: solved % * 0.6 + attempt efficiency * 0.2 + time efficiency * 0.2
            solved_pct = stats["solved"] / stats["total"]
            
            # Attempt efficiency (fewer attempts per solve is better)
            avg_attempts = stats["total_attempts"] / stats["total"] if stats["total"] else 1
            attempt_efficiency = max(0, 1 - (avg_attempts - 1) / 10)
            
            # Time efficiency (not too fast, not too slow)
            avg_time = stats["total_time"] / stats["total"] if stats["total"] else 300
            # Ideal time: 5-15 minutes (300-900 seconds)
            if 300 <= avg_time <= 900:
                time_efficiency = 1.0
            elif avg_time < 300:
                time_efficiency = avg_time / 300
            else:
                time_efficiency = max(0, 1 - (avg_time - 900) / 900)
            
            mastery_score = (
                solved_pct * 0.6 +
                attempt_efficiency * 0.2 +
                time_efficiency * 0.2
            ) * 100
            
            # Get topic name
            week = self.curriculum.get_week(topic)
            topic_name = week.title if week else topic
            
            mastery[topic] = {
                "score": round(mastery_score, 1),
                "level": self._get_mastery_level(mastery_score),
                "solved": stats["solved"],
                "total": stats["total"],
                "completion_pct": round(solved_pct * 100, 1),
                "name": topic_name,
            }
        
        return mastery
    
    def _get_mastery_level(self, score: float) -> str:
        """Get mastery level from score."""
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
    
    async def get_learning_velocity(self, user_id: str) -> Dict[str, Any]:
        """Calculate learning velocity (problems per week)."""
        stmt = select(Progress).where(
            and_(
                Progress.user_id == user_id,
                Progress.solved_at != None,
            )
        ).order_by(Progress.solved_at)
        
        result = await self.session.execute(stmt)
        solved = list(result.scalars().all())
        
        if not solved:
            return {
                "velocity_per_week": 0,
                "velocity_per_day": 0,
                "trend": "flat",
                "weekly_data": [],
            }
        
        # Calculate weekly velocity
        now = datetime.now(timezone.utc)
        first_solve = solved[0].solved_at
        
        if not first_solve:
            weeks_active = 1
        else:
            weeks_active = max(1, (now - first_solve).days // 7 + 1)
        
        velocity_per_week = len(solved) / weeks_active
        velocity_per_day = len(solved) / max(1, weeks_active * 7)
        
        # Calculate trend (comparing recent vs older periods)
        recent_solves = [s for s in solved if s.solved_at and (now - s.solved_at).days <= 7]
        older_solves = [s for s in solved if s.solved_at and 7 < (now - s.solved_at).days <= 14]
        
        recent_rate = len(recent_solves) / 7 if recent_solves else 0
        older_rate = len(older_solves) / 7 if older_solves else velocity_per_day
        
        if recent_rate > older_rate * 1.2:
            trend = "accelerating"
        elif recent_rate < older_rate * 0.8:
            trend = "decelerating"
        else:
            trend = "steady"
        
        # Weekly breakdown
        weekly_data = []
        for i in range(min(8, weeks_active)):
            week_start = now - timedelta(days=(i + 1) * 7)
            week_end = now - timedelta(days=i * 7)
            
            week_solves = sum(1 for s in solved 
                            if s.solved_at and week_start <= s.solved_at <= week_end)
            
            weekly_data.append({
                "week": f"Week -{i}",
                "problems_solved": week_solves,
            })
        
        weekly_data.reverse()
        
        return {
            "velocity_per_week": round(velocity_per_week, 2),
            "velocity_per_day": round(velocity_per_day, 2),
            "trend": trend,
            "total_solved": len(solved),
            "weeks_active": weeks_active,
            "weekly_data": weekly_data,
        }
    
    async def get_success_rate_by_difficulty(self, user_id: str) -> Dict[str, Any]:
        """Calculate success rate by difficulty level."""
        stmt = select(Progress).where(Progress.user_id == user_id)
        result = await self.session.execute(stmt)
        progress_list = list(result.scalars().all())
        
        stats_by_difficulty = defaultdict(lambda: {"attempted": 0, "solved": 0, "abandoned": 0})
        
        for progress in progress_list:
            problem = self.curriculum.get_problem(progress.problem_slug)
            difficulty = problem["problem"].difficulty if problem else "medium"
            
            stats_by_difficulty[difficulty]["attempted"] += 1
            
            if progress.status == ProblemStatus.SOLVED:
                stats_by_difficulty[difficulty]["solved"] += 1
            elif progress.attempts_count > 5 and progress.status != ProblemStatus.SOLVED:
                stats_by_difficulty[difficulty]["abandoned"] += 1
        
        # Calculate rates
        result = {}
        for difficulty, stats in stats_by_difficulty.items():
            attempted = stats["attempted"]
            result[difficulty] = {
                "attempted": attempted,
                "solved": stats["solved"],
                "abandoned": stats["abandoned"],
                "success_rate": round(stats["solved"] / attempted * 100, 1) if attempted else 0,
                "abandon_rate": round(stats["abandoned"] / attempted * 100, 1) if attempted else 0,
            }
        
        return result
    
    async def get_full_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get complete analytics summary."""
        return {
            "time_analytics": await self.get_time_analytics(user_id),
            "attempt_patterns": await self.get_attempt_patterns(user_id),
            "error_analytics": await self.get_error_analytics(user_id),
            "topic_mastery": await self.get_topic_mastery(user_id),
            "learning_velocity": await self.get_learning_velocity(user_id),
            "success_rate_by_difficulty": await self.get_success_rate_by_difficulty(user_id),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }


def get_learning_analytics(session: AsyncSession) -> LearningAnalytics:
    """Factory function for LearningAnalytics."""
    return LearningAnalytics(session)
