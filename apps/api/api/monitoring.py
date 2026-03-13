"""
Monitoring and observability utilities for the API.

This module provides structured logging, metrics collection, and Sentry integration.
"""

import json
import logging
import time
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Optional

import sentry_sdk
from fastapi import Request
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from api.config import get_settings

settings = get_settings()

# Structured JSON logger for production
class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add extra fields
        if hasattr(record, "request_id"):
            log_obj["request_id"] = record.request_id
        if hasattr(record, "user_id"):
            log_obj["user_id"] = record.user_id
        if hasattr(record, "duration_ms"):
            log_obj["duration_ms"] = record.duration_ms
        if hasattr(record, "path"):
            log_obj["path"] = record.path
        if hasattr(record, "method"):
            log_obj["method"] = record.method
        if hasattr(record, "status_code"):
            log_obj["status_code"] = record.status_code
        
        # Add exception info if present
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_obj)


def setup_logging() -> None:
    """Configure structured logging for production."""
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    
    # Use JSON formatter in production, standard in development
    if settings.is_production:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)


def init_sentry() -> None:
    """Initialize Sentry for error tracking."""
    if not settings.sentry_dsn:
        logging.info("Sentry DSN not configured - error tracking disabled")
        return
    
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        release=settings.app_version,
        
        # Sample rates
        traces_sample_rate=0.1 if settings.is_production else 1.0,
        profiles_sample_rate=0.01 if settings.is_production else 1.0,
        
        # Integrations
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
        ],
        
        # Don't send PII
        send_default_pii=False,
        
        # Before send hook
        before_send=before_send_event,
    )


def before_send_event(event: dict, hint: dict) -> Optional[dict]:
    """Filter events before sending to Sentry."""
    # Skip events in development
    if settings.is_development:
        return None
    
    # Filter out certain errors
    if "exception" in event:
        exception = event["exception"]
        if "values" in exception:
            for value in exception["values"]:
                if "type" in value:
                    error_type = value["type"]
                    # Skip common non-actionable errors
                    if error_type in [
                        "HTTPException",  # FastAPI HTTP exceptions
                        "ValidationError",  # Pydantic validation errors
                        "StarletteHTTPException",
                    ]:
                        return None
    
    return event


class MetricsCollector:
    """Simple metrics collector for API operations."""
    
    def __init__(self):
        self.counters: dict[str, int] = {}
        self.timers: dict[str, list[float]] = {}
    
    def increment(self, name: str, value: int = 1) -> None:
        """Increment a counter metric."""
        self.counters[name] = self.counters.get(name, 0) + value
    
    def record_time(self, name: str, duration_ms: float) -> None:
        """Record a timing metric."""
        if name not in self.timers:
            self.timers[name] = []
        self.timers[name].append(duration_ms)
    
    @contextmanager
    def time(self, name: str):
        """Context manager for timing operations."""
        start = time.time()
        try:
            yield
        finally:
            duration_ms = (time.time() - start) * 1000
            self.record_time(name, duration_ms)
    
    def get_summary(self) -> dict:
        """Get a summary of all metrics."""
        summary = {
            "counters": self.counters.copy(),
            "timers": {},
        }
        
        for name, times in self.timers.items():
            if times:
                summary["timers"][name] = {
                    "count": len(times),
                    "avg_ms": sum(times) / len(times),
                    "min_ms": min(times),
                    "max_ms": max(times),
                }
        
        return summary


# Global metrics instance
metrics = MetricsCollector()


def log_request(request: Request, duration_ms: float, status_code: int) -> None:
    """Log an HTTP request with structured data."""
    logger = logging.getLogger("api.request")
    
    extra = {
        "path": request.url.path,
        "method": request.method,
        "status_code": status_code,
        "duration_ms": round(duration_ms, 2),
    }
    
    # Add request ID if present
    if hasattr(request.state, "request_id"):
        extra["request_id"] = request.state.request_id
    
    # Log based on status code
    if status_code >= 500:
        logger.error("Request failed", extra=extra)
    elif status_code >= 400:
        logger.warning("Request error", extra=extra)
    else:
        logger.info("Request completed", extra=extra)


def timed(func: Callable) -> Callable:
    """Decorator to time function execution."""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.time()
        try:
            return await func(*args, **kwargs)
        finally:
            duration = (time.time() - start) * 1000
            metrics.record_time(func.__name__, duration)
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            duration = (time.time() - start) * 1000
            metrics.record_time(func.__name__, duration)
    
    # Return appropriate wrapper based on function type
    import inspect
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


def set_user_context(user_id: str, email: Optional[str] = None) -> None:
    """Set user context for Sentry."""
    sentry_sdk.set_user({
        "id": user_id,
        "email": email,
    })


def clear_user_context() -> None:
    """Clear user context from Sentry."""
    sentry_sdk.set_user(None)
