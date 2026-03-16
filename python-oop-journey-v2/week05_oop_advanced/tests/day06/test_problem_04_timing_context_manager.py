"""Tests for Problem 04: Timing Context Manager."""

from __future__ import annotations

import time

import pytest

from week05_oop_advanced.solutions.day06.problem_04_timing_context_manager import (
    Timer,
    TimerGroup,
    TimedBlock,
)


class TestTimer:
    """Tests for the Timer context manager."""
    
    def test_timer_measures_elapsed(self) -> None:
        """Test that timer measures elapsed time correctly."""
        with Timer() as timer:
            time.sleep(0.05)
        
        assert timer.elapsed >= 0.05
        assert timer.elapsed < 0.5  # Sanity check
    
    def test_timer_with_name(self) -> None:
        """Test timer with custom name."""
        timer = Timer(name="test_operation")
        assert timer.name == "test_operation"
    
    def test_timer_default_name(self) -> None:
        """Test timer has default name."""
        timer = Timer()
        assert timer.name == "Timer"
    
    def test_timer_str_representation(self) -> None:
        """Test timer string representation."""
        with Timer(name="test") as timer:
            pass
        
        result = str(timer)
        assert "test:" in result
        assert "s" in result
    
    def test_timer_threshold_callback(self) -> None:
        """Test threshold callback is called when exceeded."""
        callback_calls = []
        
        def callback(name: str, elapsed: float) -> None:
            callback_calls.append((name, elapsed))
        
        with Timer(threshold=0.01, callback=callback) as timer:
            time.sleep(0.05)
        
        assert len(callback_calls) == 1
        assert callback_calls[0][0] == "Timer"
        assert callback_calls[0][1] >= 0.05
    
    def test_timer_threshold_not_exceeded(self) -> None:
        """Test callback not called when threshold not exceeded."""
        callback_calls = []
        
        def callback(name: str, elapsed: float) -> None:
            callback_calls.append((name, elapsed))
        
        with Timer(threshold=1.0, callback=callback) as timer:
            pass
        
        assert len(callback_calls) == 0
    
    def test_timer_elapsed_accessible_in_context(self) -> None:
        """Test that timer can be accessed within the context."""
        with Timer() as timer:
            # Elapsed should be 0 or very small while in context
            assert timer._start_time is not None


class TestTimedBlock:
    """Tests for the TimedBlock context manager."""
    
    def test_block_initial_state(self) -> None:
        """Test block starts with zero stats."""
        block = TimedBlock("test")
        
        assert block.total == 0.0
        assert block.count == 0
        assert block.average == 0.0
    
    def test_block_single_use(self) -> None:
        """Test block with single use."""
        block = TimedBlock("test")
        
        with block:
            time.sleep(0.05)
        
        assert block.count == 1
        assert block.total >= 0.05
        assert block.average >= 0.05
        assert block.last >= 0.05
    
    def test_block_multiple_uses(self) -> None:
        """Test block with multiple uses accumulates stats."""
        block = TimedBlock("test")
        
        with block:
            time.sleep(0.02)
        
        with block:
            time.sleep(0.03)
        
        assert block.count == 2
        assert block.total >= 0.05
        assert block.average >= 0.025
    
    def test_block_reset(self) -> None:
        """Test block reset clears stats."""
        block = TimedBlock("test")
        
        with block:
            time.sleep(0.01)
        
        block.reset()
        
        assert block.total == 0.0
        assert block.count == 0
        assert block.average == 0.0
    
    def test_block_report(self) -> None:
        """Test block report format."""
        block = TimedBlock("test_block")
        
        with block:
            time.sleep(0.01)
        
        report = block.report()
        
        assert "TimedBlock: test_block" in report
        assert "Count:" in report
        assert "Total:" in report
        assert "Average:" in report
    
    def test_block_with_name(self) -> None:
        """Test block name is used in output."""
        block = TimedBlock("my_block")
        assert block.name == "my_block"
    
    def test_block_str(self) -> None:
        """Test block string representation."""
        block = TimedBlock("test")
        
        with block:
            time.sleep(0.01)
        
        result = str(block)
        assert "test:" in result
        assert "1 calls" in result


class TestTimerGroup:
    """Tests for the TimerGroup class."""
    
    def test_group_init(self) -> None:
        """Test group initialization."""
        group = TimerGroup()
        assert group.report() == {}
    
    def test_group_single_timer(self) -> None:
        """Test group with single timer."""
        group = TimerGroup()
        
        with group.timer("database"):
            time.sleep(0.02)
        
        report = group.report()
        
        assert "database" in report
        assert report["database"]["count"] == 1.0
        assert report["database"]["total"] >= 0.02
    
    def test_group_multiple_timers(self) -> None:
        """Test group with multiple named timers."""
        group = TimerGroup()
        
        with group.timer("db"):
            time.sleep(0.02)
        
        with group.timer("api"):
            time.sleep(0.03)
        
        report = group.report()
        
        assert "db" in report
        assert "api" in report
        assert report["db"]["total"] >= 0.02
        assert report["api"]["total"] >= 0.03
    
    def test_group_same_timer_multiple_times(self) -> None:
        """Test using same timer name multiple times."""
        group = TimerGroup()
        
        with group.timer("db"):
            time.sleep(0.02)
        
        with group.timer("db"):
            time.sleep(0.03)
        
        report = group.report()
        
        assert report["db"]["count"] == 2.0
        assert report["db"]["total"] >= 0.05
    
    def test_group_reset(self) -> None:
        """Test group reset clears all timers."""
        group = TimerGroup()
        
        with group.timer("db"):
            time.sleep(0.02)
        
        group.reset()
        
        report = group.report()
        
        # Stats should be reset
        assert report["db"]["count"] == 0.0
        assert report["db"]["total"] == 0.0
    
    def test_group_elapsed_accessible(self) -> None:
        """Test that elapsed time is accessible during/after context."""
        group = TimerGroup()
        
        with group.timer("test") as t:
            time.sleep(0.02)
        
        assert t.elapsed >= 0.02
    
    def test_group_str(self) -> None:
        """Test group string representation."""
        group = TimerGroup()
        
        with group.timer("db"):
            time.sleep(0.01)
        
        result = str(group)
        
        assert "TimerGroup Report:" in result
        assert "db:" in result
