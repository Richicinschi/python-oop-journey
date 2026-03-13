"""Recommendations router for smart learning recommendations."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.middleware.auth import get_current_user, get_optional_user as get_current_user_optional
from api.services.recommendations import (
    RecommendationEngine,
    RecommendationType,
    get_recommendation_engine,
)
from api.services.spaced_repetition import (
    SpacedRepetitionService,
    get_spaced_repetition_service,
)
from api.services.analytics import LearningAnalytics, get_learning_analytics

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


# Schemas
class RecommendationResponse(BaseModel):
    """Recommendation response."""
    type: str = Field(..., description="Recommendation type")
    itemType: str = Field(..., description="Type of item: problem, day, week, theory")
    itemSlug: str = Field(..., description="Unique identifier for the item")
    itemTitle: str = Field(..., description="Human-readable title")
    reason: str = Field(..., description="Why this recommendation was made")
    priority: int = Field(..., ge=1, le=10, description="Priority 1-10 (higher = more important)")
    estimatedTimeMinutes: int = Field(..., description="Estimated time to complete")
    context: dict = Field(default_factory=dict, description="Additional context")


class ReviewItemResponse(BaseModel):
    """Spaced repetition review item."""
    problemSlug: str
    problemTitle: str
    easeFactor: float
    interval: int
    repetitions: int
    nextReview: Optional[str]
    daysOverdue: int
    priority: float


class ReviewQueueResponse(BaseModel):
    """Review queue response."""
    items: List[ReviewItemResponse]
    total: int
    dueToday: int
    dueThisWeek: int


class ReviewStatsResponse(BaseModel):
    """Spaced repetition statistics."""
    totalItems: int
    dueNow: int
    dueToday: int
    dueThisWeek: int
    averageEaseFactor: float
    completedReviews: int


class WeakAreaResponse(BaseModel):
    """Weak area response."""
    topicSlug: str
    topicName: str
    masteryScore: float
    level: str
    problemsStruggled: List[str]
    suggestedRemediation: str
    priority: int


class LearningPathStep(BaseModel):
    """A step in the learning path."""
    type: str
    weekSlug: str
    weekTitle: str
    reason: str
    estimatedDays: Optional[int] = None


class LearningPathResponse(BaseModel):
    """Personalized learning path."""
    steps: List[LearningPathStep]
    estimatedWeeks: int
    focusAreas: List[str]
    skippedTopics: List[str]
    reasoning: str


class DifficultySuggestionResponse(BaseModel):
    """Difficulty adjustment suggestion."""
    currentDifficulty: str
    suggestedDifficulty: str
    successRate: float
    message: str


class TimeAnalyticsResponse(BaseModel):
    """Time analytics by difficulty."""
    totalTimeSeconds: int
    totalTimeFormatted: str
    problemCount: int
    averageTimeSeconds: float
    averageTimeFormatted: str
    medianTimeSeconds: int
    minTimeSeconds: int
    maxTimeSeconds: int


class AttemptPatternResponse(BaseModel):
    """Attempt pattern analysis."""
    systematic: float
    trialError: float
    stuck: float
    perfect: float
    dominantPattern: str


class TopicMasteryResponse(BaseModel):
    """Topic mastery level."""
    score: float
    level: str
    solved: int
    total: int
    completionPct: float
    name: str


class LearningVelocityResponse(BaseModel):
    """Learning velocity metrics."""
    velocityPerWeek: float
    velocityPerDay: float
    trend: str
    totalSolved: int
    weeksActive: int


class SuccessRateResponse(BaseModel):
    """Success rate by difficulty."""
    attempted: int
    solved: int
    abandoned: int
    successRate: float
    abandonRate: float


class LearningStatsResponse(BaseModel):
    """Complete learning statistics."""
    problemsAttempted: int
    problemsSolved: int
    averageTimePerProblem: int
    successRateByDifficulty: dict
    topicMastery: dict
    streakDays: int
    velocity: float


class RecordReviewRequest(BaseModel):
    """Request to record a review."""
    quality: int = Field(..., ge=0, le=5, description="0-5 quality rating")


class RecordReviewResponse(BaseModel):
    """Response after recording a review."""
    problemSlug: str
    quality: int
    nextReview: str
    interval: int
    easeFactor: float


# Endpoints
@router.get("/next", response_model=RecommendationResponse)
async def get_next_recommendation(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Get the next recommended problem to attempt."""
    engine = get_recommendation_engine(session)
    recommendation = await engine.get_next_problem(user["id"])
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="No recommendations available")
    
    return RecommendationResponse(**recommendation.to_dict())


@router.get("/all", response_model=List[RecommendationResponse])
async def get_all_recommendations(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=20),
):
    """Get all recommendations sorted by priority."""
    engine = get_recommendation_engine(session)
    recommendations = await engine.get_all_recommendations(user["id"])
    
    return [RecommendationResponse(**r.to_dict()) for r in recommendations[:limit]]


@router.get("/review", response_model=ReviewQueueResponse)
async def get_review_queue(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50),
):
    """Get problems due for review (spaced repetition)."""
    engine = get_recommendation_engine(session)
    recommendations = await engine.get_review_suggestions(user["id"], limit)
    
    items = []
    for rec in recommendations:
        ctx = rec.context
        items.append(ReviewItemResponse(
            problemSlug=rec.item_slug,
            problemTitle=rec.item_title,
            easeFactor=ctx.get("ease_factor", 2.5),
            interval=ctx.get("interval", 1),
            repetitions=ctx.get("repetitions", 0),
            nextReview=rec.context.get("next_review"),
            daysOverdue=ctx.get("days_overdue", 0),
            priority=float(rec.priority),
        ))
    
    # Get stats
    sr_service = get_spaced_repetition_service(session)
    stats = await sr_service.get_review_stats(user["id"])
    
    return ReviewQueueResponse(
        items=items,
        total=stats["total_items"],
        dueToday=stats["due_today"],
        dueThisWeek=stats["due_this_week"],
    )


@router.get("/review/stats", response_model=ReviewStatsResponse)
async def get_review_stats(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Get spaced repetition statistics."""
    sr_service = get_spaced_repetition_service(session)
    stats = await sr_service.get_review_stats(user["id"])
    
    return ReviewStatsResponse(
        totalItems=stats["total_items"],
        dueNow=stats["due_now"],
        dueToday=stats["due_today"],
        dueThisWeek=stats["due_this_week"],
        averageEaseFactor=stats["average_ease_factor"],
        completedReviews=stats["completed_reviews"],
    )


@router.post("/review/{problem_slug}", response_model=RecordReviewResponse)
async def record_review(
    problem_slug: str,
    request: RecordReviewRequest,
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Record a review attempt with quality rating (SM-2 algorithm).
    
    Quality rating:
    - 0-2: Incorrect response (will reset interval)
    - 3: Correct with difficulty
    - 4: Correct with hesitation
    - 5: Perfect response
    """
    sr_service = get_spaced_repetition_service(session)
    
    try:
        item = await sr_service.record_review(user["id"], problem_slug, request.quality)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return RecordReviewResponse(
        problemSlug=item.problem_slug,
        quality=request.quality,
        nextReview=item.next_review.isoformat() if item.next_review else None,
        interval=item.interval,
        easeFactor=item.ease_factor,
    )


@router.get("/weak-areas", response_model=List[WeakAreaResponse])
async def get_weak_areas(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
    limit: int = Query(5, ge=1, le=10),
):
    """Get topics where the user is struggling."""
    engine = get_recommendation_engine(session)
    weak_areas = await engine.get_weak_areas(user["id"])
    
    return [
        WeakAreaResponse(
            topicSlug=area.topic_slug,
            topicName=area.topic_name,
            masteryScore=area.mastery_score,
            level=area.level,
            problemsStruggled=area.problems_struggled,
            suggestedRemediation=area.suggested_remediation,
            priority=area.priority,
        )
        for area in weak_areas[:limit]
    ]


@router.get("/path", response_model=LearningPathResponse)
async def get_learning_path(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Get personalized learning path."""
    engine = get_recommendation_engine(session)
    path = await engine.get_learning_path(user["id"])
    
    return LearningPathResponse(
        steps=[
            LearningPathStep(
                type=step["type"],
                weekSlug=step["week_slug"],
                weekTitle=step["week_title"],
                reason=step["reason"],
                estimatedDays=step.get("estimated_days"),
            )
            for step in path.steps
        ],
        estimatedWeeks=path.estimated_weeks,
        focusAreas=path.focus_areas,
        skippedTopics=path.skipped_topics,
        reasoning=path.reasoning,
    )


@router.get("/difficulty", response_model=Optional[DifficultySuggestionResponse])
async def get_difficulty_suggestion(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Get difficulty adjustment suggestion based on performance."""
    engine = get_recommendation_engine(session)
    suggestion = await engine.get_difficulty_suggestion(user["id"])
    
    if not suggestion:
        return None
    
    ctx = suggestion.context
    return DifficultySuggestionResponse(
        currentDifficulty=ctx.get("current_difficulty", "easy"),
        suggestedDifficulty=ctx.get("suggested_difficulty", "medium"),
        successRate=ctx.get("success_rate", 0),
        message=suggestion.reason,
    )


@router.get("/stats/time", response_model=dict)
async def get_time_analytics(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Get time analytics by difficulty."""
    analytics = get_learning_analytics(session)
    time_data = await analytics.get_time_analytics(user["id"])
    
    return time_data


@router.get("/stats/attempts", response_model=AttemptPatternResponse)
async def get_attempt_patterns(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Get attempt pattern analysis."""
    analytics = get_learning_analytics(session)
    patterns = await analytics.get_attempt_patterns(user["id"])
    
    return AttemptPatternResponse(
        systematic=patterns["percentages"]["systematic"],
        trialError=patterns["percentages"]["trial_error"],
        stuck=patterns["percentages"]["stuck"],
        perfect=patterns["percentages"]["perfect"],
        dominantPattern=patterns["dominant_pattern"],
    )


@router.get("/stats/mastery", response_model=dict)
async def get_topic_mastery(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Get topic mastery levels."""
    analytics = get_learning_analytics(session)
    mastery = await analytics.get_topic_mastery(user["id"])
    
    return mastery


@router.get("/stats/velocity", response_model=LearningVelocityResponse)
async def get_learning_velocity(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Get learning velocity (problems per week)."""
    analytics = get_learning_analytics(session)
    velocity = await analytics.get_learning_velocity(user["id"])
    
    return LearningVelocityResponse(
        velocityPerWeek=velocity["velocity_per_week"],
        velocityPerDay=velocity["velocity_per_day"],
        trend=velocity["trend"],
        totalSolved=velocity["total_solved"],
        weeksActive=velocity["weeks_active"],
    )


@router.get("/stats/success-rate", response_model=dict)
async def get_success_rate(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Get success rate by difficulty."""
    analytics = get_learning_analytics(session)
    rates = await analytics.get_success_rate_by_difficulty(user["id"])
    
    return rates


@router.get("/stats", response_model=LearningStatsResponse)
async def get_learning_stats(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Get complete learning statistics."""
    analytics = get_learning_analytics(session)
    
    # Get all analytics
    time_data = await analytics.get_time_analytics(user["id"])
    velocity = await analytics.get_learning_velocity(user["id"])
    success_rates = await analytics.get_success_rate_by_difficulty(user["id"])
    mastery = await analytics.get_topic_mastery(user["id"])
    
    # Calculate totals
    total_time = sum(d.get("total_time_seconds", 0) for d in time_data.values())
    total_problems = sum(d.get("problem_count", 0) for d in time_data.values())
    avg_time = total_time // total_problems if total_problems else 0
    
    # Get streak
    from api.services.progress import ProgressService
    progress_service = ProgressService(session)
    streak = await progress_service.calculate_streak(user["id"])
    
    return LearningStatsResponse(
        problemsAttempted=sum(r.get("attempted", 0) for r in success_rates.values()),
        problemsSolved=velocity["total_solved"],
        averageTimePerProblem=avg_time,
        successRateByDifficulty=success_rates,
        topicMastery=mastery,
        streakDays=streak,
        velocity=velocity["velocity_per_week"],
    )


@router.get("/streak", response_model=dict)
async def get_streak_info(
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Get review streak information."""
    sr_service = get_spaced_repetition_service(session)
    streak = await sr_service.get_streak_info(user["id"])
    
    return streak
