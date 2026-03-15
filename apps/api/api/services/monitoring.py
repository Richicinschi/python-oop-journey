"""Execution monitoring and metrics tracking."""

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any

from api.schemas.execution import ExecutionMetrics, ExecutionStatus

logger = logging.getLogger(__name__)


class ExecutionErrorType(str, Enum):
    """Types of execution errors."""
    TIMEOUT = "timeout"
    MEMORY_LIMIT = "memory_limit"
    SYNTAX_ERROR = "syntax_error"
    RUNTIME_ERROR = "runtime_error"
    CONTAINER_ERROR = "container_error"
    SECURITY_VIOLATION = "security_violation"
    UNKNOWN = "unknown"


@dataclass
class ExecutionRecord:
    """Record of a single execution."""
    id: str
    user_id: str | None
    code_length: int
    status: ExecutionStatus
    duration_ms: int
    exit_code: int | None
    error_type: ExecutionErrorType | None
    memory_usage_mb: float | None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    ip_address: str | None = None
    user_agent: str | None = None


class ExecutionMonitor:
    """Monitor and track code executions."""
    
    # Rate limiting configuration
    RATE_LIMIT_WINDOW_SECONDS = 60
    MAX_EXECUTIONS_PER_WINDOW = 10
    ALERT_THRESHOLD_FAILURE_RATE = 0.3  # 30% failure rate triggers alert
    
    def __init__(self):
        """Initialize execution monitor."""
        self._execution_history: list[ExecutionRecord] = []
        self._user_execution_counts: dict[str, list[datetime]] = {}
        self._max_history_size = 10000
        
    def log_execution(self,
                     execution_id: str,
                     user_id: str | None,
                     code: str,
                     status: ExecutionStatus,
                     duration_ms: int,
                     exit_code: int | None = None,
                     error: str | None = None,
                     memory_usage_mb: float | None = None,
                     ip_address: str | None = None,
                     user_agent: str | None = None) -> ExecutionRecord:
        """Log an execution event.
        
        Args:
            execution_id: Unique execution identifier
            user_id: User identifier (if authenticated)
            code: Executed code
            status: Execution status
            duration_ms: Execution duration in milliseconds
            exit_code: Process exit code
            error: Error message if failed
            memory_usage_mb: Memory usage in MB
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            ExecutionRecord that was created
        """
        # Determine error type
        error_type = self._classify_error(status, exit_code, error)
        
        record = ExecutionRecord(
            id=execution_id,
            user_id=user_id,
            code_length=len(code),
            status=status,
            duration_ms=duration_ms,
            exit_code=exit_code,
            error_type=error_type,
            memory_usage_mb=memory_usage_mb,
            timestamp=datetime.now(timezone.utc),
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Add to history
        self._execution_history.append(record)
        
        # Trim history if too large
        if len(self._execution_history) > self._max_history_size:
            self._execution_history = self._execution_history[-self._max_history_size:]
        
        # Update user rate limit tracking
        if user_id:
            self._track_user_execution(user_id)
        
        # Log the execution
        self._log_execution(record)
        
        # Check for alerts
        self._check_alerts(record)
        
        return record
    
    def _classify_error(self, 
                       status: ExecutionStatus, 
                       exit_code: int | None,
                       error: str | None) -> ExecutionErrorType | None:
        """Classify the type of error."""
        if status == ExecutionStatus.COMPLETED:
            return None
            
        if status == ExecutionStatus.TIMEOUT:
            return ExecutionErrorType.TIMEOUT
            
        if error:
            error_lower = error.lower()
            if "syntax" in error_lower or "indent" in error_lower:
                return ExecutionErrorType.SYNTAX_ERROR
            if "memory" in error_lower or "killed" in error_lower:
                return ExecutionErrorType.MEMORY_LIMIT
            if "security" in error_lower or "permission" in error_lower:
                return ExecutionErrorType.SECURITY_VIOLATION
            if "container" in error_lower:
                return ExecutionErrorType.CONTAINER_ERROR
                
        if exit_code is not None and exit_code != 0:
            return ExecutionErrorType.RUNTIME_ERROR
            
        return ExecutionErrorType.UNKNOWN
    
    def _track_user_execution(self, user_id: str) -> None:
        """Track execution for rate limiting."""
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(seconds=self.RATE_LIMIT_WINDOW_SECONDS)
        
        if user_id not in self._user_execution_counts:
            self._user_execution_counts[user_id] = []
        
        # Filter to recent executions and add new one
        self._user_execution_counts[user_id] = [
            t for t in self._user_execution_counts[user_id] if t > window_start
        ]
        self._user_execution_counts[user_id].append(now)
    
    def _log_execution(self, record: ExecutionRecord) -> None:
        """Log execution details."""
        log_data = {
            "execution_id": record.id,
            "user_id": record.user_id,
            "code_length": record.code_length,
            "status": record.status.value,
            "duration_ms": record.duration_ms,
            "error_type": record.error_type.value if record.error_type else None,
        }
        
        if record.status == ExecutionStatus.COMPLETED:
            logger.info(f"Execution completed: {log_data}")
        else:
            logger.warning(f"Execution failed: {log_data}")
    
    def _check_alerts(self, record: ExecutionRecord) -> None:
        """Check for conditions that should trigger alerts."""
        # Check for high failure rate
        recent_executions = self._get_recent_executions(minutes=5)
        if len(recent_executions) >= 10:
            failed = sum(1 for e in recent_executions if e.status != ExecutionStatus.COMPLETED)
            failure_rate = failed / len(recent_executions)
            
            if failure_rate > self.ALERT_THRESHOLD_FAILURE_RATE:
                logger.error(
                    f"ALERT: High failure rate detected: {failure_rate:.1%} "
                    f"({failed}/{len(recent_executions)} executions failed in last 5 minutes)"
                )
        
        # Check for suspicious patterns (e.g., many rapid executions from same IP)
        if record.ip_address:
            recent_from_ip = sum(
                1 for e in self._execution_history
                if e.ip_address == record.ip_address 
                and e.timestamp > datetime.now(timezone.utc) - timedelta(minutes=1)
            )
            if recent_from_ip > 20:
                logger.warning(
                    f"ALERT: Suspicious activity from IP {record.ip_address}: "
                    f"{recent_from_ip} executions in last minute"
                )
    
    def check_rate_limit(self, user_id: str | None, ip_address: str | None) -> tuple[bool, int, int]:
        """Check if user/IP has exceeded rate limit.
        
        Args:
            user_id: User identifier
            ip_address: IP address
            
        Returns:
            Tuple of (allowed, current_count, limit)
        """
        # Check by user ID first, then by IP
        identifier = user_id or ip_address or "anonymous"
        
        if identifier not in self._user_execution_counts:
            return True, 0, self.MAX_EXECUTIONS_PER_WINDOW
        
        recent_count = len(self._user_execution_counts[identifier])
        allowed = recent_count < self.MAX_EXECUTIONS_PER_WINDOW
        
        return allowed, recent_count, self.MAX_EXECUTIONS_PER_WINDOW
    
    def _get_recent_executions(self, minutes: int = 60) -> list[ExecutionRecord]:
        """Get executions from the last N minutes."""
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
        return [e for e in self._execution_history if e.timestamp > cutoff]
    
    def get_metrics(self, hours: int = 24) -> ExecutionMetrics:
        """Get execution metrics for the specified time period.
        
        Args:
            hours: Number of hours to include in metrics
            
        Returns:
            ExecutionMetrics for the period
        """
        executions = [
            e for e in self._execution_history
            if e.timestamp > datetime.now(timezone.utc) - timedelta(hours=hours)
        ]
        
        if not executions:
            return ExecutionMetrics(
                total_executions=0,
                successful_executions=0,
                failed_executions=0,
                timeout_executions=0,
                average_execution_time_ms=0.0,
                average_memory_usage_mb=None,
                peak_memory_usage_mb=None,
                failure_rate=0.0,
                time_period=f"{hours}h"
            )
        
        total = len(executions)
        successful = sum(1 for e in executions if e.status == ExecutionStatus.COMPLETED)
        timeouts = sum(1 for e in executions if e.status == ExecutionStatus.TIMEOUT)
        failed = total - successful
        
        avg_duration = sum(e.duration_ms for e in executions) / total
        
        # Memory stats
        memory_usages = [e.memory_usage_mb for e in executions if e.memory_usage_mb is not None]
        avg_memory = sum(memory_usages) / len(memory_usages) if memory_usages else None
        peak_memory = max(memory_usages) if memory_usages else None
        
        failure_rate = (failed / total) * 100
        
        return ExecutionMetrics(
            total_executions=total,
            successful_executions=successful,
            failed_executions=failed,
            timeout_executions=timeouts,
            average_execution_time_ms=round(avg_duration, 2),
            average_memory_usage_mb=round(avg_memory, 2) if avg_memory else None,
            peak_memory_usage_mb=round(peak_memory, 2) if peak_memory else None,
            failure_rate=round(failure_rate, 2),
            time_period=f"{hours}h"
        )
    
    def get_error_breakdown(self, hours: int = 24) -> dict[str, int]:
        """Get breakdown of error types.
        
        Args:
            hours: Number of hours to include
            
        Returns:
            Dictionary mapping error types to counts
        """
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        errors: dict[str, int] = {}
        
        for e in self._execution_history:
            if e.timestamp > cutoff and e.error_type:
                error_type = e.error_type.value
                errors[error_type] = errors.get(error_type, 0) + 1
        
        return errors


# Singleton instance
_monitor: ExecutionMonitor | None = None


def get_monitor() -> ExecutionMonitor:
    """Get or create execution monitor singleton."""
    global _monitor
    if _monitor is None:
        _monitor = ExecutionMonitor()
    return _monitor


def reset_monitor() -> None:
    """Reset execution monitor (for testing)."""
    global _monitor
    _monitor = None
