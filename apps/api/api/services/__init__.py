"""Services module."""

from api.services.activity import ActivityService, get_activity_service
from api.services.analytics import LearningAnalytics, get_learning_analytics
from api.services.auth import AuthService, get_auth_service
from api.services.bookmark import BookmarkService, get_bookmark_service
from api.services.curriculum import CurriculumService, get_curriculum_service
from api.services.docker_runner import DockerRunner, get_docker_runner
from api.services.draft import DraftService, get_draft_service
from api.services.execution import ExecutionService, get_execution_service
from api.services.monitoring import ExecutionMonitor, get_monitor
from api.services.progress import ProgressService, get_progress_service
from api.services.project_execution import (
    ProjectExecutionService,
    get_project_execution_service,
    reset_project_execution_service,
)
from api.services.recommendations import (
    RecommendationEngine,
    get_recommendation_engine,
)
from api.services.spaced_repetition import (
    SpacedRepetitionService,
    get_spaced_repetition_service,
)
from api.services.verification import VerificationService, get_verification_service

__all__ = [
    "ActivityService",
    "get_activity_service",
    "AuthService",
    "get_auth_service",
    "BookmarkService",
    "get_bookmark_service",
    "CurriculumService",
    "get_curriculum_service",
    "DockerRunner",
    "get_docker_runner",
    "DraftService",
    "get_draft_service",
    "ExecutionService",
    "get_execution_service",
    "ExecutionMonitor",
    "get_monitor",
    "LearningAnalytics",
    "get_learning_analytics",
    "ProgressService",
    "get_progress_service",
    "ProjectExecutionService",
    "get_project_execution_service",
    "reset_project_execution_service",
    "RecommendationEngine",
    "get_recommendation_engine",
    "SpacedRepetitionService",
    "get_spaced_repetition_service",
    "VerificationService",
    "get_verification_service",
]
