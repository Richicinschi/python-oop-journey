"""Curriculum endpoints."""

import logging

from fastapi import APIRouter, HTTPException, status

from api.schemas.curriculum import (
    Curriculum,
    ProblemDetailResponse,
    ProblemListItem,
    Week,
)
from api.services.curriculum import CurriculumService

router = APIRouter()
logger = logging.getLogger(__name__)

# Service instance (could be dependency injected)
curriculum_service = CurriculumService()


@router.get(
    "/curriculum",
    response_model=Curriculum,
    summary="Get full curriculum",
    description="Returns the complete curriculum with all weeks, days, and problems.",
)
async def get_curriculum() -> Curriculum:
    """Get the full curriculum."""
    try:
        return curriculum_service.get_curriculum()
    except Exception as e:
        logger.error(f"Failed to get curriculum: {e}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load curriculum: {str(e)}",
        )


@router.get(
    "/curriculum/weeks/{slug}",
    response_model=Week,
    summary="Get single week",
    description="Returns a specific week by its slug.",
    responses={
        404: {"description": "Week not found"},
        500: {"description": "Server error"},
    },
)
async def get_week(slug: str) -> Week:
    """Get a single week by slug."""
    try:
        week = curriculum_service.get_week(slug)
        if not week:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Week '{slug}' not found",
            )
        return week
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get week {slug}: {e}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load week: {str(e)}",
        )


@router.get(
    "/curriculum/problems",
    response_model=list[ProblemListItem],
    summary="List all problems",
    description="Returns a list of all problems with metadata.",
    responses={
        500: {"description": "Server error"},
    },
)
async def list_problems() -> list[ProblemListItem]:
    """List all problems."""
    try:
        return curriculum_service.list_problems()
    except Exception as e:
        logger.error(f"Failed to list problems: {e}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list problems: {str(e)}",
        )


@router.get(
    "/curriculum/problems/{slug}",
    response_model=ProblemDetailResponse,
    summary="Get problem details",
    description="Returns a specific problem with its context.",
    responses={
        404: {"description": "Problem not found"},
        500: {"description": "Server error"},
    },
)
async def get_problem(slug: str) -> ProblemDetailResponse:
    """Get a problem by slug."""
    try:
        problem_data = curriculum_service.get_problem(slug)
        if not problem_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Problem '{slug}' not found",
            )
        
        # Validate the response data structure
        week = problem_data.get("week")
        day = problem_data.get("day")
        problem = problem_data.get("problem")
        
        if not all([week, day, problem]):
            logger.error(f"Incomplete problem data for {slug}: {problem_data.keys()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Problem data is incomplete",
            )
        
        return ProblemDetailResponse(
            week=week,
            day=day,
            problem=problem,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get problem {slug}: {e}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load problem: {str(e)}",
        )
