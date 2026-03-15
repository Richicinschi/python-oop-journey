"""Curriculum endpoints."""

from fastapi import APIRouter, HTTPException, status

from api.schemas.curriculum import Curriculum, ProblemDetailResponse, Week
from api.services.curriculum import CurriculumService

router = APIRouter()

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
    return curriculum_service.get_curriculum()


@router.get(
    "/curriculum/weeks/{slug}",
    response_model=Week,
    summary="Get single week",
    description="Returns a specific week by its slug.",
    responses={
        404: {"description": "Week not found"},
    },
)
async def get_week(slug: str) -> Week:
    """Get a single week by slug."""
    week = curriculum_service.get_week(slug)
    if not week:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Week '{slug}' not found",
        )
    return week


@router.get(
    "/curriculum/problems",
    summary="List all problems",
    description="Returns a list of all problems with metadata.",
)
async def list_problems():
    """List all problems."""
    return curriculum_service.list_problems()


@router.get(
    "/curriculum/problems/{slug}",
    response_model=ProblemDetailResponse,
    summary="Get problem details",
    description="Returns a specific problem with its context.",
    responses={
        404: {"description": "Problem not found"},
    },
)
async def get_problem(slug: str) -> ProblemDetailResponse:
    """Get a problem by slug."""
    problem_data = curriculum_service.get_problem(slug)
    if not problem_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem '{slug}' not found",
        )
    return problem_data
