"""Reference solution for Problem 05: Log Parser Refactor."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Protocol


# ============================================================================
# PROCEDURAL CODE (Before) - Kept for reference
# ============================================================================

def read_log_file_procedural(filepath: str) -> list[str]:
    """Read log file lines."""
    return Path(filepath).read_text().splitlines()


def parse_log_entry_procedural(line: str) -> dict | None:
    """Parse single log line into dict."""
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.+)"
    match = re.match(pattern, line)
    if match:
        return {
            "timestamp": match.group(1),
            "level": match.group(2),
            "message": match.group(3),
        }
    return None


def parse_log_entries_procedural(lines: list[str]) -> list[dict]:
    """Parse multiple log lines."""
    entries = []
    for line in lines:
        entry = parse_log_entry_procedural(line)
        if entry:
            entries.append(entry)
    return entries


def filter_by_level_procedural(entries: list[dict], level: str) -> list[dict]:
    """Filter entries by log level."""
    return [e for e in entries if e["level"] == level]


def count_by_level_procedural(entries: list[dict]) -> dict[str, int]:
    """Count entries per level."""
    counts: dict[str, int] = {}
    for entry in entries:
        level = entry["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts


def get_time_range_procedural(entries: list[dict]) -> tuple[str, str] | None:
    """Get first and last timestamp."""
    if not entries:
        return None
    timestamps = [e["timestamp"] for e in entries]
    return (min(timestamps), max(timestamps))


def search_messages_procedural(entries: list[dict], keyword: str) -> list[dict]:
    """Search for keyword in messages."""
    return [e for e in entries if keyword.lower() in e["message"].lower()]


def generate_stats_report_procedural(entries: list[dict]) -> dict:
    """Generate statistics report."""
    if not entries:
        return {"total": 0, "by_level": {}, "time_range": None}
    
    return {
        "total": len(entries),
        "by_level": count_by_level_procedural(entries),
        "time_range": get_time_range_procedural(entries),
    }


def format_report_procedural(stats: dict) -> str:
    """Format statistics as report."""
    lines = ["Log Analysis Report", "=" * 40]
    lines.append(f"Total Entries: {stats['total']}")
    
    if stats["time_range"]:
        lines.append(f"Time Range: {stats['time_range'][0]} to {stats['time_range'][1]}")
    
    lines.append("\nEntries by Level:")
    for level, count in sorted(stats["by_level"].items()):
        lines.append(f"  {level}: {count}")
    
    return "\n".join(lines)


# ============================================================================
# OOP IMPLEMENTATION (After)
# ============================================================================


class LogLevel(Enum):
    """Enumeration of log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class LogEntry:
    """Immutable log entry value object."""
    
    timestamp: datetime
    level: LogLevel
    message: str
    
    @classmethod
    def from_string(cls, line: str) -> LogEntry | None:
        """Parse log line and return LogEntry."""
        pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.+)"
        match = re.match(pattern, line)
        if not match:
            return None
        
        timestamp_str = match.group(1)
        level_str = match.group(2)
        message = match.group(3)
        
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            level = LogLevel(level_str)
        except (ValueError, KeyError):
            return None
        
        return cls(timestamp, level, message)
    
    def __str__(self) -> str:
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} [{self.level.value}] {self.message}"


class LogFormatParser(ABC):
    """Abstract base for log format parsers."""
    
    @abstractmethod
    def parse(self, line: str) -> LogEntry | None:
        """Parse a line and return LogEntry or None."""
        pass


class DefaultLogParser(LogFormatParser):
    """Parser for standard log format."""
    
    def parse(self, line: str) -> LogEntry | None:
        return LogEntry.from_string(line)


class LogAnalyzer:
    """Log analyzer with encapsulated log entries."""
    
    def __init__(self, parser: LogFormatParser | None = None) -> None:
        self._parser = parser if parser is not None else DefaultLogParser()
        self._entries: list[LogEntry] = []
    
    def load_file(self, filepath: str) -> LogAnalyzer:
        """Load and parse log file."""
        lines = Path(filepath).read_text().splitlines()
        return self.load_lines(lines)
    
    def load_lines(self, lines: list[str]) -> LogAnalyzer:
        """Parse provided lines."""
        for line in lines:
            entry = self._parser.parse(line)
            if entry:
                self._entries.append(entry)
        return self
    
    def add_entry(self, entry: LogEntry) -> LogAnalyzer:
        """Add a single entry."""
        self._entries.append(entry)
        return self
    
    @property
    def entries(self) -> tuple[LogEntry, ...]:
        """Return immutable view of all entries."""
        return tuple(self._entries)
    
    @property
    def count(self) -> int:
        """Return total number of entries."""
        return len(self._entries)
    
    def filter_by_level(self, level: LogLevel) -> list[LogEntry]:
        """Return entries matching the specified level."""
        return [e for e in self._entries if e.level == level]
    
    def filter_by_time_range(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[LogEntry]:
        """Return entries within time range [start, end]."""
        result = self._entries
        if start is not None:
            result = [e for e in result if e.timestamp >= start]
        if end is not None:
            result = [e for e in result if e.timestamp <= end]
        return result
    
    def search(self, keyword: str) -> list[LogEntry]:
        """Search for keyword in messages (case-insensitive)."""
        return [e for e in self._entries if keyword.lower() in e.message.lower()]
    
    def count_by_level(self) -> dict[LogLevel, int]:
        """Return dict mapping LogLevel to count."""
        counts: dict[LogLevel, int] = {}
        for entry in self._entries:
            counts[entry.level] = counts.get(entry.level, 0) + 1
        return counts
    
    def get_time_range(self) -> tuple[datetime, datetime] | None:
        """Return (earliest, latest) timestamps or None if empty."""
        if not self._entries:
            return None
        timestamps = [e.timestamp for e in self._entries]
        return (min(timestamps), max(timestamps))
    
    def get_statistics(self) -> dict:
        """Return statistics dict."""
        by_level = self.count_by_level()
        error_count = by_level.get(LogLevel.ERROR, 0) + by_level.get(LogLevel.CRITICAL, 0)
        
        return {
            "total": self.count,
            "by_level": by_level,
            "time_range": self.get_time_range(),
            "error_count": error_count,
        }
    
    def generate_report(self) -> str:
        """Generate formatted report string."""
        stats = self.get_statistics()
        
        lines = ["Log Analysis Report", "=" * 40]
        lines.append(f"Total Entries: {stats['total']}")
        
        if stats["time_range"]:
            start, end = stats["time_range"]
            lines.append(f"Time Range: {start.strftime('%Y-%m-%d %H:%M:%S')} to {end.strftime('%Y-%m-%d %H:%M:%S')}")
        
        lines.append("\nEntries by Level:")
        for level in LogLevel:
            count = stats["by_level"].get(level, 0)
            lines.append(f"  {level.value}: {count}")
        
        lines.append(f"\nErrors (ERROR + CRITICAL): {stats['error_count']}")
        
        return "\n".join(lines)
    
    def clear(self) -> LogAnalyzer:
        """Clear all entries."""
        self._entries.clear()
        return self
    
    def __len__(self) -> int:
        return len(self._entries)
    
    def __bool__(self) -> bool:
        return len(self._entries) > 0
