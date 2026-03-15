"""AI-powered hints and code assistance endpoints.

This module provides endpoints for:
- Generating contextual hints
- Explaining errors in plain English
- Code review for project submissions
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.config import get_settings
from api.core.rate_limit import rate_limit
from api.middleware.auth import get_optional_user as get_current_user_optional
from api.schemas.ai_hints import (
    AIErrorRequest,
    AIErrorResponse,
    AIHintFeedback,
    AIHintRequest,
    AIHintResponse,
    AIReportRequest,
    CodeReviewRequest,
    CodeReviewResult,
)
from api.schemas.user import User
from api.services.ai_hints import get_ai_hint_service
from api.services.curriculum import CurriculumService

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize curriculum service for problem lookups
curriculum_service = CurriculumService()


@router.post(
    "/ai/hint",
    response_model=AIHintResponse,
    summary="Generate AI hint",
    description="Generate a contextual AI hint based on user's code and problem context.",
    responses={
        400: {"description": "Invalid request"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "AI service unavailable"},
    },
)
@rate_limit(requests=10, window_seconds=3600)
async def generate_hint(
    request: Request,
    hint_request: AIHintRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> AIHintResponse:
    """Generate an AI-powered hint for the user's code.
    
    This endpoint analyzes the user's code and generates a contextual hint
    that guides them toward the solution without giving it away.
    
    Rate limited to 10 requests per hour per user.
    
    Example request:
    ```json
    {
        "problem_slug": "w01d01-hello-object",
        "code": "def greet(name):\\n    pass",
        "hint_level": 1,
        "previous_hints": []
    }
    ```
    """
    ai_service = get_ai_hint_service()
    
    # Get problem details from curriculum
    problem_data = curriculum_service.get_problem(hint_request.problem_slug)
    if not problem_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem not found: {hint_request.problem_slug}",
        )
    
    problem = problem_data["problem"]
    
    # Generate hint
    try:
        result = await ai_service.generate_hint(
            problem_slug=hint_request.problem_slug,
            problem_title=problem.title,
            problem_description=problem.description,
            user_code=hint_request.code,
            hint_level=hint_request.hint_level,
            test_results=hint_request.test_results,
            previous_hints=hint_request.previous_hints,
        )
        
        return AIHintResponse(
            hint=result.hint,
            relevant_lines=result.relevant_lines,
            explanation=result.explanation,
            hint_level=result.hint_level,
        )
    except Exception as e:
        logger.error(f"Failed to generate hint: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI hint service temporarily unavailable",
        )


@router.post(
    "/ai/explain-error",
    response_model=AIErrorResponse,
    summary="Explain error in plain English",
    description="Take an error message and explain it in learner-friendly terms.",
    responses={
        400: {"description": "Invalid request"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "AI service unavailable"},
    },
)
@rate_limit(requests=20, window_seconds=3600)
async def explain_error(
    request: Request,
    error_request: AIErrorRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> AIErrorResponse:
    """Explain a Python error in plain English.
    
    This endpoint takes an error message and the user's code, then provides
    a learner-friendly explanation of what went wrong and how to fix it.
    
    Rate limited to 20 requests per hour per user.
    
    Example request:
    ```json
    {
        "error_message": "NameError: name 'x' is not defined",
        "code": "print(x)",
        "problem_slug": "w01d01-hello-object"
    }
    ```
    """
    ai_service = get_ai_hint_service()
    
    # Get problem description if available
    problem_description = ""
    if error_request.problem_slug:
        problem_data = curriculum_service.get_problem(error_request.problem_slug)
        if problem_data:
            problem_description = problem_data["problem"].description
    
    # Generate explanation
    try:
        result = await ai_service.explain_error(
            error_message=error_request.error_message,
            user_code=error_request.code,
            problem_slug=error_request.problem_slug,
            problem_description=problem_description,
        )
        
        return AIErrorResponse(
            explanation=result.explanation,
            suggestion=result.suggestion,
            relevant_lines=result.relevant_lines,
        )
    except Exception as e:
        logger.error(f"Failed to explain error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI error explanation service temporarily unavailable",
        )


@router.post(
    "/ai/code-review",
    response_model=CodeReviewResult,
    summary="AI code review",
    description="Perform an AI-powered code review for project submissions.",
    responses={
        400: {"description": "Invalid request"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "AI service unavailable"},
    },
)
@rate_limit(requests=5, window_seconds=3600)
async def code_review(
    request: Request,
    review_request: CodeReviewRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> CodeReviewResult:
    """Generate an AI-powered code review for a project submission.
    
    This endpoint reviews submitted code files and provides:
    - Overall feedback
    - Strengths identified
    - Suggested improvements
    - Rubric assessment (if rubric provided)
    
    Rate limited to 5 requests per hour per user (more expensive operation).
    
    Example request:
    ```json
    {
        "files": {
            "main.py": "def main():\\n    print('Hello')",
            "utils.py": "def helper():\\n    pass"
        },
        "project_slug": "w02-project-bank-account",
        "rubric": [
            {"name": "Classes", "description": "Uses classes appropriately"}
        ]
    }
    ```
    """
    ai_service = get_ai_hint_service()
    
    # Get project details from curriculum
    # Note: In production, you'd have a proper project lookup service
    project_description = f"Project: {review_request.project_slug}"
    
    # Perform review
    try:
        result = await ai_service.review_code(
            project_slug=review_request.project_slug,
            project_description=project_description,
            files=review_request.files,
            rubric=review_request.rubric,
        )
        
        return result
    except Exception as e:
        logger.error(f"Failed to perform code review: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI code review service temporarily unavailable",
        )


@router.post(
    "/ai/hint-feedback",
    summary="Submit hint feedback",
    description="Submit feedback about whether an AI hint was helpful.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def submit_hint_feedback(
    feedback: AIHintFeedback,
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> None:
    """Submit feedback about an AI hint.
    
    This helps improve the AI hint system by tracking which hints are helpful.
    
    Example request:
    ```json
    {
        "problem_slug": "w01d01-hello-object",
        "hint_level": 1,
        "was_helpful": true,
        "feedback_text": "This helped me think about the right approach"
    }
    ```
    """
    # Log feedback for analysis
    logger.info(
        "AI hint feedback received",
        extra={
            "problem_slug": feedback.problem_slug,
            "hint_level": feedback.hint_level,
            "was_helpful": feedback.was_helpful,
            "user_id": current_user.id if current_user else None,
        },
    )
    
    # In production, store this in a database for analysis
    # await store_hint_feedback(feedback)
    
    return None


@router.post(
    "/ai/report-hint",
    summary="Report problematic hint",
    description="Report an AI hint that was inappropriate or incorrect.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def report_hint(
    report: AIReportRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> None:
    """Report a problematic AI hint.
    
    Use this endpoint when an AI hint:
    - Gives away the complete solution
    - Contains inappropriate content
    - Is technically incorrect
    - Is unhelpful or confusing
    
    Example request:
    ```json
    {
        "problem_slug": "w01d01-hello-object",
        "hint_level": 1,
        "hint_text": "Just write: def add(a,b): return a+b",
        "reason": "Gave complete solution"
    }
    ```
    """
    # Log report for review
    logger.warning(
        "AI hint reported",
        extra={
            "problem_slug": report.problem_slug,
            "hint_level": report.hint_level,
            "reason": report.reason,
            "user_id": current_user.id if current_user else None,
        },
    )
    
    # In production, store this in a database for manual review
    # await store_hint_report(report)
    
    return None


@router.get(
    "/ai/health",
    summary="Check AI service health",
    description="Check if the AI hint service is available.",
)
async def ai_health_check() -> dict:
    """Check if the AI hint service is healthy.
    
    Returns the status of the AI service and which providers are configured.
    """
    ai_service = get_ai_hint_service()
    settings = get_settings()
    
    openai_configured = bool(
        getattr(settings, "openai_api_key", None) or ai_service.openai_api_key
    )
    anthropic_configured = bool(
        getattr(settings, "anthropic_api_key", None) or ai_service.anthropic_api_key
    )
    
    return {
        "status": "healthy" if openai_configured else "degraded",
        "providers": {
            "openai": openai_configured,
            "anthropic": anthropic_configured,
        },
        "models": {
            "hint": ai_service.hint_model,
            "review": ai_service.review_model,
        },
    }
