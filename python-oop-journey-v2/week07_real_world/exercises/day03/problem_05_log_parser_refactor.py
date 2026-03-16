"""Problem 05: Log Parser Refactor

Topic: Refactoring Functions to Analyzer Class
Difficulty: Medium-Hard

Refactor a collection of log parsing functions into a cohesive LogAnalyzer class.

BEFORE (Function-Based):
    log_lines = read_log_file("app.log")
    entries = parse_log_entries(log_lines)
    errors = filter_by_level(entries, "ERROR")
    stats = calculate_stats(entries)
    report = generate_report(stats)

AFTER (OOP):
    analyzer = LogAnalyzer()
    analyzer.load_file("app.log")
    errors = analyzer.filter_by_level(LogLevel.ERROR)
    stats = analyzer.get_statistics()
    report = analyzer.generate_report()

Your task:
1. Create LogLevel enum for log levels
2. Create LogEntry as an immutable value object
3. Create LogAnalyzer class that manages log entries
4. Support filtering, analysis, and report generation
5. Support different log formats
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Protocol


# ============================================================================
# PROCEDURAL CODE (Before) - DO NOT MODIFY
# ============================================================================

def read_log_file_procedural(filepath: str) -> list[str]:
    """Read log file lines."""
    return Path(filepath).read_text().splitlines()


def parse_log_entry_procedural(line: str) -> dict | None:
    """Parse single log line into dict.
    
    Expected format: 2024-01-15 10:30:45 [ERROR] message here
    """
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
# YOUR IMPLEMENTATION (After) - TODO: Implement these classes
# ============================================================================


class LogLevel(Enum):
    """Enumeration of log levels.
    
    TODO: Define these levels:
    - DEBUG
    - INFO
    - WARNING
    - ERROR
    - CRITICAL
    """
    pass  # TODO: Implement enum values


@dataclass(frozen=True)
class LogEntry:
    """Immutable log entry value object.
    
    Attributes:
        timestamp: Entry timestamp as datetime
        level: LogLevel enum value
        message: Log message text
    
    TODO:
    1. Define fields with frozen=True
    2. Implement from_string class method to parse log lines
    """
    
    @classmethod
    def from_string(cls, line: str) -> LogEntry | None:
        """TODO: Parse log line and return LogEntry.
        
        Expected format: 2024-01-15 10:30:45 [ERROR] message here
        
        Returns None if parsing fails.
        """
        raise NotImplementedError("Implement from_string")
    
    def __str__(self) -> str:
        """TODO: Return formatted: 'YYYY-MM-DD HH:MM:SS [LEVEL] message'."""
        raise NotImplementedError("Implement __str__")


class LogFormatParser(ABC):
    """Abstract base for log format parsers.
    
    Strategy pattern for different log formats.
    
    TODO:
    1. Make ABC with abstract parse method
    2. DefaultParser implementation for standard format
    """
    
    @abstractmethod
    def parse(self, line: str) -> LogEntry | None:
        """TODO: Parse a line and return LogEntry or None."""
        raise NotImplementedError("Implement parse")


class DefaultLogParser(LogFormatParser):
    """Parser for standard log format.
    
    Format: 2024-01-15 10:30:45 [ERROR] message here
    
    TODO: Implement parse method using LogEntry.from_string
    """
    
    def parse(self, line: str) -> LogEntry | None:
        """TODO: Parse using LogEntry.from_string."""
        raise NotImplementedError("Implement parse")


class LogAnalyzer:
    """Log analyzer with encapsulated log entries.
    
    Replaces the collection of procedural functions with a cohesive class
    that maintains state and provides analysis methods.
    
    TODO:
    1. Accept parser in __init__ (default to DefaultLogParser)
    2. Initialize empty entries list
    3. Implement load_file, load_lines
    4. Implement filtering methods
    5. Implement analysis methods
    6. Implement report generation
    """
    
    def __init__(self, parser: LogFormatParser | None = None) -> None:
        """TODO: Initialize with parser and empty entries list."""
        raise NotImplementedError("Implement __init__")
    
    def load_file(self, filepath: str) -> LogAnalyzer:
        """TODO: Load and parse log file.
        
        Read file, parse each line, add valid entries.
        Returns self for chaining.
        """
        raise NotImplementedError("Implement load_file")
    
    def load_lines(self, lines: list[str]) -> LogAnalyzer:
        """TODO: Parse provided lines.
        
        Parse each line, add valid entries.
        Returns self for chaining.
        """
        raise NotImplementedError("Implement load_lines")
    
    def add_entry(self, entry: LogEntry) -> LogAnalyzer:
        """TODO: Add a single entry.
        
        Returns self for chaining.
        """
        raise NotImplementedError("Implement add_entry")
    
    @property
    def entries(self) -> tuple[LogEntry, ...]:
        """TODO: Return immutable view of all entries."""
        raise NotImplementedError("Implement entries")
    
    @property
    def count(self) -> int:
        """TODO: Return total number of entries."""
        raise NotImplementedError("Implement count")
    
    def filter_by_level(self, level: LogLevel) -> list[LogEntry]:
        """TODO: Return entries matching the specified level."""
        raise NotImplementedError("Implement filter_by_level")
    
    def filter_by_time_range(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[LogEntry]:
        """TODO: Return entries within time range [start, end].
        
        If start is None, include from beginning.
        If end is None, include to end.
        """
        raise NotImplementedError("Implement filter_by_time_range")
    
    def search(self, keyword: str) -> list[LogEntry]:
        """TODO: Search for keyword in messages (case-insensitive)."""
        raise NotImplementedError("Implement search")
    
    def count_by_level(self) -> dict[LogLevel, int]:
        """TODO: Return dict mapping LogLevel to count."""
        raise NotImplementedError("Implement count_by_level")
    
    def get_time_range(self) -> tuple[datetime, datetime] | None:
        """TODO: Return (earliest, latest) timestamps or None if empty."""
        raise NotImplementedError("Implement get_time_range")
    
    def get_statistics(self) -> dict:
        """TODO: Return statistics dict with:
        - total: total entry count
        - by_level: dict of level -> count
        - time_range: (start, end) or None
        - error_count: count of ERROR and CRITICAL
        """
        raise NotImplementedError("Implement get_statistics")
    
    def generate_report(self) -> str:
        """TODO: Generate formatted report string.
        
        Format:
        Log Analysis Report
        ========================================
        Total Entries: X
        Time Range: YYYY-MM-DD HH:MM:SS to YYYY-MM-DD HH:MM:SS
        
        Entries by Level:
          DEBUG: X
          INFO: X
          ...
        
        Errors (ERROR + CRITICAL): X
        """
        raise NotImplementedError("Implement generate_report")
    
    def clear(self) -> LogAnalyzer:
        """TODO: Clear all entries. Returns self."""
        raise NotImplementedError("Implement clear")
    
    def __len__(self) -> int:
        """TODO: Return entry count."""
        raise NotImplementedError("Implement __len__")
    
    def __bool__(self) -> bool:
        """TODO: Return True if has entries."""
        raise NotImplementedError("Implement __bool__")
