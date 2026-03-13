"""Curriculum service."""

import json
import logging
from pathlib import Path
from typing import Any

from api.schemas.curriculum import Curriculum, Week

logger = logging.getLogger(__name__)

# Default curriculum path - can be overridden
CURRICULUM_PATH = Path(__file__).parent.parent.parent / "data" / "curriculum.json"


class CurriculumService:
    """Service for curriculum operations."""

    def __init__(self, curriculum_path: Path | None = None):
        self.curriculum_path = curriculum_path or CURRICULUM_PATH
        self._cache: Curriculum | None = None

    def _load_curriculum(self) -> Curriculum:
        """Load curriculum from JSON file."""
        if not self.curriculum_path.exists():
            logger.warning(f"Curriculum file not found: {self.curriculum_path}")
            return self._create_default_curriculum()

        try:
            with open(self.curriculum_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Curriculum(**data)
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to load curriculum: {e}")
            return self._create_default_curriculum()

    def _create_default_curriculum(self) -> Curriculum:
        """Create minimal default curriculum."""
        return Curriculum(
            version="1.0.0",
            weeks=[
                Week(
                    slug="week-01",
                    title="Week 1: Foundations",
                    description="Object basics and classes",
                    theme="foundations",
                    days=[],
                )
            ],
        )

    def get_curriculum(self) -> Curriculum:
        """Get full curriculum."""
        if self._cache is None:
            self._cache = self._load_curriculum()
        return self._cache

    def get_week(self, slug: str) -> Week | None:
        """Get single week by slug."""
        curriculum = self.get_curriculum()
        for week in curriculum.weeks:
            if week.slug == slug:
                return week
        return None

    def get_problem(self, slug: str) -> dict[str, Any] | None:
        """Get problem by slug."""
        curriculum = self.get_curriculum()
        for week in curriculum.weeks:
            for day in week.days:
                for problem in day.problems:
                    if problem.slug == slug:
                        return {
                            "week": week,
                            "day": day,
                            "problem": problem,
                        }
        return None

    def list_problems(self) -> list[dict[str, Any]]:
        """List all problems with metadata."""
        problems = []
        curriculum = self.get_curriculum()
        for week in curriculum.weeks:
            for day in week.days:
                for problem in day.problems:
                    problems.append({
                        "slug": problem.slug,
                        "title": problem.title,
                        "difficulty": problem.difficulty,
                        "week_slug": week.slug,
                        "week_title": week.title,
                        "day_slug": day.slug,
                        "day_title": day.title,
                    })
        return problems

    def invalidate_cache(self) -> None:
        """Invalidate curriculum cache."""
        self._cache = None


# Singleton instance
_curriculum_service: CurriculumService | None = None


def get_curriculum_service() -> CurriculumService:
    """Get singleton CurriculumService instance."""
    global _curriculum_service
    if _curriculum_service is None:
        _curriculum_service = CurriculumService()
    return _curriculum_service
