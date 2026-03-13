"""Celery application configuration."""

import logging
import os

from celery import Celery
from celery.signals import task_failure, task_postrun, task_prerun

from api.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Configure Celery
redis_url = settings.redis_url

app = Celery(
    "api",
    broker=redis_url,
    backend=redis_url,
    include=["api.tasks"]
)

# Celery configuration
app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Result backend settings
    result_expires=3600,  # Results expire after 1 hour
    result_extended=True,
    
    # Task execution settings
    task_track_started=True,
    task_time_limit=70,  # Hard time limit (slightly above max timeout)
    task_soft_time_limit=65,  # Soft time limit
    
    # Worker settings
    worker_prefetch_multiplier=1,  # Don't prefetch tasks
    worker_max_tasks_per_child=1000,  # Restart worker after 1000 tasks
    
    # Rate limiting
    task_default_rate_limit="100/m",  # Default rate limit per task type
    
    # Retry settings
    task_default_retry_delay=60,
    task_max_retries=3,
)


@task_prerun.connect
def task_prerun_handler(task_id, task, args, kwargs, **extras):
    """Handle task pre-run events."""
    logger.info(f"Task {task.name}[{task_id}] started")


@task_postrun.connect
def task_postrun_handler(task_id, task, args, kwargs, retval, state, **extras):
    """Handle task post-run events."""
    logger.info(f"Task {task.name}[{task_id}] finished with state: {state}")


@task_failure.connect
def task_failure_handler(task_id, exception, args, kwargs, traceback, einfo, **extras):
    """Handle task failure events."""
    logger.error(f"Task failed [{task_id}]: {exception}")


def start_worker():
    """Start Celery worker (for development)."""
    argv = [
        "worker",
        "--loglevel=info",
        "--concurrency=4",
        "--queues=celery,execution",
    ]
    app.start(argv=argv)


def start_beat():
    """Start Celery beat scheduler."""
    argv = [
        "beat",
        "--loglevel=info",
    ]
    app.start(argv=argv)


def start_flower():
    """Start Flower monitoring."""
    argv = [
        "flower",
        "--port=5555",
    ]
    app.start(argv=argv)


if __name__ == "__main__":
    start_worker()
