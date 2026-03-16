"""Tests for Problem 05: Log Parser Refactor."""

from __future__ import annotations

from datetime import datetime

import pytest

from week07_real_world.solutions.day03.problem_05_log_parser_refactor import (
    LogLevel,
    LogEntry,
    DefaultLogParser,
    LogFormatParser,
    LogAnalyzer,
    read_log_file_procedural,
    parse_log_entry_procedural,
    filter_by_level_procedural,
    count_by_level_procedural,
    search_messages_procedural,
    generate_stats_report_procedural,
)


class TestLogLevel:
    """Tests for LogLevel enum."""
    
    def test_levels_exist(self) -> None:
        assert LogLevel.DEBUG.value == "DEBUG"
        assert LogLevel.INFO.value == "INFO"
        assert LogLevel.WARNING.value == "WARNING"
        assert LogLevel.ERROR.value == "ERROR"
        assert LogLevel.CRITICAL.value == "CRITICAL"


class TestLogEntry:
    """Tests for LogEntry value object."""
    
    def test_creation(self) -> None:
        timestamp = datetime(2024, 1, 15, 10, 30, 45)
        entry = LogEntry(timestamp, LogLevel.ERROR, "Something failed")
        
        assert entry.timestamp == timestamp
        assert entry.level == LogLevel.ERROR
        assert entry.message == "Something failed"
    
    def test_from_string_valid(self) -> None:
        line = "2024-01-15 10:30:45 [ERROR] Something failed"
        entry = LogEntry.from_string(line)
        
        assert entry is not None
        assert entry.timestamp == datetime(2024, 1, 15, 10, 30, 45)
        assert entry.level == LogLevel.ERROR
        assert entry.message == "Something failed"
    
    def test_from_string_invalid_format(self) -> None:
        assert LogEntry.from_string("not a valid log line") is None
        assert LogEntry.from_string("") is None
    
    def test_from_string_invalid_level(self) -> None:
        entry = LogEntry.from_string("2024-01-15 10:30:45 [UNKNOWN] message")
        assert entry is None  # Unknown level should fail
    
    def test_from_string_invalid_date(self) -> None:
        entry = LogEntry.from_string("invalid-date [ERROR] message")
        assert entry is None
    
    def test_immutable(self) -> None:
        entry = LogEntry(datetime.now(), LogLevel.INFO, "test")
        with pytest.raises(AttributeError):
            entry.message = "changed"
    
    def test_str_formatting(self) -> None:
        timestamp = datetime(2024, 1, 15, 10, 30, 45)
        entry = LogEntry(timestamp, LogLevel.ERROR, "Something failed")
        
        result = str(entry)
        assert "2024-01-15 10:30:45" in result
        assert "[ERROR]" in result
        assert "Something failed" in result


class TestDefaultLogParser:
    """Tests for DefaultLogParser."""
    
    def test_parse_valid(self) -> None:
        parser = DefaultLogParser()
        entry = parser.parse("2024-01-15 10:30:45 [INFO] Application started")
        
        assert entry is not None
        assert entry.level == LogLevel.INFO
    
    def test_parse_invalid(self) -> None:
        parser = DefaultLogParser()
        assert parser.parse("invalid line") is None


class TestLogAnalyzer:
    """Tests for LogAnalyzer."""
    
    @pytest.fixture
    def sample_lines(self) -> list[str]:
        return [
            "2024-01-15 10:30:00 [INFO] Application started",
            "2024-01-15 10:31:00 [DEBUG] Loading configuration",
            "2024-01-15 10:32:00 [ERROR] Failed to connect to database",
            "2024-01-15 10:33:00 [INFO] Retrying connection",
            "2024-01-15 10:34:00 [ERROR] Connection failed permanently",
            "2024-01-15 10:35:00 [WARNING] Using fallback mode",
        ]
    
    @pytest.fixture
    def analyzer(self, sample_lines) -> LogAnalyzer:
        return LogAnalyzer().load_lines(sample_lines)
    
    def test_init_empty(self) -> None:
        analyzer = LogAnalyzer()
        assert analyzer.count == 0
        assert analyzer.entries == ()
    
    def test_load_lines(self, sample_lines) -> None:
        analyzer = LogAnalyzer()
        result = analyzer.load_lines(sample_lines)
        
        assert result is analyzer  # Returns self
        assert analyzer.count == 6
    
    def test_load_lines_skips_invalid(self) -> None:
        lines = [
            "2024-01-15 10:30:00 [INFO] Valid entry",
            "invalid line",
            "2024-01-15 10:31:00 [ERROR] Another valid entry",
        ]
        analyzer = LogAnalyzer()
        analyzer.load_lines(lines)
        
        assert analyzer.count == 2
    
    def test_add_entry(self) -> None:
        analyzer = LogAnalyzer()
        entry = LogEntry(datetime.now(), LogLevel.INFO, "test")
        result = analyzer.add_entry(entry)
        
        assert result is analyzer
        assert analyzer.count == 1
        assert analyzer.entries[0] == entry
    
    def test_entries_immutable(self, analyzer: LogAnalyzer) -> None:
        entries = analyzer.entries
        assert isinstance(entries, tuple)
        with pytest.raises(TypeError):
            entries[0] = None  # type: ignore
    
    def test_filter_by_level(self, analyzer: LogAnalyzer) -> None:
        errors = analyzer.filter_by_level(LogLevel.ERROR)
        
        assert len(errors) == 2
        assert all(e.level == LogLevel.ERROR for e in errors)
    
    def test_filter_by_time_range(self, analyzer: LogAnalyzer) -> None:
        start = datetime(2024, 1, 15, 10, 32, 0)
        end = datetime(2024, 1, 15, 10, 33, 30)
        
        filtered = analyzer.filter_by_time_range(start, end)
        
        assert len(filtered) == 2  # ERROR and INFO entries in range
    
    def test_filter_by_time_range_open_start(self, analyzer: LogAnalyzer) -> None:
        end = datetime(2024, 1, 15, 10, 31, 30)
        
        filtered = analyzer.filter_by_time_range(None, end)
        
        assert len(filtered) == 2  # First two entries
    
    def test_filter_by_time_range_open_end(self, analyzer: LogAnalyzer) -> None:
        start = datetime(2024, 1, 15, 10, 34, 0)
        
        filtered = analyzer.filter_by_time_range(start, None)
        
        assert len(filtered) == 2  # Last two entries
    
    def test_search(self, analyzer: LogAnalyzer) -> None:
        results = analyzer.search("connection")
        
        assert len(results) == 2  # INFO retrying connection, ERROR connection failed
    
    def test_search_case_insensitive(self, analyzer: LogAnalyzer) -> None:
        results = analyzer.search("CONNECTION")
        
        assert len(results) == 2
    
    def test_count_by_level(self, analyzer: LogAnalyzer) -> None:
        counts = analyzer.count_by_level()
        
        assert counts[LogLevel.INFO] == 2
        assert counts[LogLevel.DEBUG] == 1
        assert counts[LogLevel.ERROR] == 2
        assert counts[LogLevel.WARNING] == 1
        assert counts.get(LogLevel.CRITICAL, 0) == 0
    
    def test_get_time_range(self, analyzer: LogAnalyzer) -> None:
        time_range = analyzer.get_time_range()
        
        assert time_range is not None
        assert time_range[0] == datetime(2024, 1, 15, 10, 30, 0)
        assert time_range[1] == datetime(2024, 1, 15, 10, 35, 0)
    
    def test_get_time_range_empty(self) -> None:
        analyzer = LogAnalyzer()
        assert analyzer.get_time_range() is None
    
    def test_get_statistics(self, analyzer: LogAnalyzer) -> None:
        stats = analyzer.get_statistics()
        
        assert stats["total"] == 6
        assert stats["error_count"] == 2  # ERROR only
        assert LogLevel.ERROR in stats["by_level"]
        assert stats["time_range"] is not None
    
    def test_generate_report(self, analyzer: LogAnalyzer) -> None:
        report = analyzer.generate_report()
        
        assert "Log Analysis Report" in report
        assert "Total Entries: 6" in report
        assert "INFO: 2" in report
        assert "ERROR: 2" in report
        assert "Errors (ERROR + CRITICAL): 2" in report
    
    def test_clear(self, analyzer: LogAnalyzer) -> None:
        result = analyzer.clear()
        
        assert result is analyzer
        assert analyzer.count == 0
    
    def test_len(self, analyzer: LogAnalyzer) -> None:
        assert len(analyzer) == 6
    
    def test_bool_true(self, analyzer: LogAnalyzer) -> None:
        assert bool(analyzer) is True
    
    def test_bool_false(self) -> None:
        analyzer = LogAnalyzer()
        assert bool(analyzer) is False


class TestLogAnalyzerChaining:
    """Tests for method chaining."""
    
    def test_chaining(self) -> None:
        lines = ["2024-01-15 10:30:00 [INFO] Test"]
        
        analyzer = LogAnalyzer().load_lines(lines).clear().load_lines(lines)
        
        assert analyzer.count == 1
    
    def test_add_entry_chaining(self) -> None:
        entry = LogEntry(datetime.now(), LogLevel.INFO, "test")
        
        analyzer = LogAnalyzer().add_entry(entry).add_entry(entry)
        
        assert analyzer.count == 2


class TestLogFormatParserIsABC:
    """Tests that LogFormatParser is properly abstract."""
    
    def test_cannot_instantiate_directly(self) -> None:
        with pytest.raises(TypeError):
            LogFormatParser()
    
    def test_subclass_must_implement_parse(self) -> None:
        class BadParser(LogFormatParser):
            pass
        
        with pytest.raises(TypeError):
            BadParser()


class TestProceduralCompatibility:
    """Tests comparing procedural and OOP results."""
    
    def test_parse_entry_behavior(self) -> None:
        line = "2024-01-15 10:30:45 [ERROR] Something failed"
        
        # Procedural
        proc_entry = parse_log_entry_procedural(line)
        
        # OOP
        oop_entry = LogEntry.from_string(line)
        
        assert proc_entry["timestamp"] == "2024-01-15 10:30:45"
        assert proc_entry["level"] == "ERROR"
        assert oop_entry is not None
        assert oop_entry.level == LogLevel.ERROR
    
    def test_filter_by_level_behavior(self) -> None:
        lines = [
            "2024-01-15 10:30:00 [INFO] test1",
            "2024-01-15 10:31:00 [ERROR] test2",
            "2024-01-15 10:32:00 [INFO] test3",
        ]
        
        # Procedural
        proc_entries = [parse_log_entry_procedural(l) for l in lines]
        proc_entries = [e for e in proc_entries if e]
        proc_filtered = filter_by_level_procedural(proc_entries, "ERROR")
        
        # OOP
        analyzer = LogAnalyzer().load_lines(lines)
        oop_filtered = analyzer.filter_by_level(LogLevel.ERROR)
        
        assert len(proc_filtered) == len(oop_filtered)
    
    def test_count_by_level_behavior(self) -> None:
        lines = [
            "2024-01-15 10:30:00 [INFO] test1",
            "2024-01-15 10:31:00 [ERROR] test2",
            "2024-01-15 10:32:00 [INFO] test3",
        ]
        
        # Procedural
        proc_entries = [parse_log_entry_procedural(l) for l in lines]
        proc_entries = [e for e in proc_entries if e]
        proc_counts = count_by_level_procedural(proc_entries)
        
        # OOP
        analyzer = LogAnalyzer().load_lines(lines)
        oop_counts = analyzer.count_by_level()
        
        assert proc_counts["INFO"] == oop_counts[LogLevel.INFO]
        assert proc_counts["ERROR"] == oop_counts[LogLevel.ERROR]
    
    def test_search_behavior(self) -> None:
        lines = [
            "2024-01-15 10:30:00 [INFO] connection established",
            "2024-01-15 10:31:00 [ERROR] connection failed",
        ]
        
        # Procedural
        proc_entries = [parse_log_entry_procedural(l) for l in lines]
        proc_entries = [e for e in proc_entries if e]
        proc_results = search_messages_procedural(proc_entries, "connection")
        
        # OOP
        analyzer = LogAnalyzer().load_lines(lines)
        oop_results = analyzer.search("connection")
        
        assert len(proc_results) == len(oop_results)
    
    def test_stats_behavior(self) -> None:
        lines = [
            "2024-01-15 10:30:00 [INFO] test1",
            "2024-01-15 10:31:00 [ERROR] test2",
        ]
        
        # Procedural
        proc_entries = [parse_log_entry_procedural(l) for l in lines]
        proc_entries = [e for e in proc_entries if e]
        proc_stats = generate_stats_report_procedural(proc_entries)
        
        # OOP
        analyzer = LogAnalyzer().load_lines(lines)
        oop_stats = analyzer.get_statistics()
        
        assert proc_stats["total"] == oop_stats["total"]
