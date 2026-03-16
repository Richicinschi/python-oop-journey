"""Tests for Problem 10: Timer."""

from __future__ import annotations

import time

from week03_oop_basics.solutions.day01.problem_10_timer import Timer


def test_timer_creation() -> None:
    """Test creating a timer."""
    timer = Timer()
    assert timer.elapsed() == 0.0
    assert timer.is_running() is False


def test_timer_start() -> None:
    """Test starting the timer."""
    timer = Timer()
    timer.start()
    assert timer.is_running() is True


def test_timer_stop() -> None:
    """Test stopping the timer."""
    timer = Timer()
    timer.start()
    timer.stop()
    assert timer.is_running() is False


def test_timer_elapsed_basic() -> None:
    """Test that timer records elapsed time."""
    timer = Timer()
    timer.start()
    time.sleep(0.05)  # 50ms
    timer.stop()
    
    elapsed = timer.elapsed()
    assert elapsed >= 0.05
    assert elapsed < 0.5  # Should be much less than 500ms


def test_timer_elapsed_while_running() -> None:
    """Test getting elapsed time while timer is running."""
    timer = Timer()
    timer.start()
    time.sleep(0.03)  # 30ms
    
    elapsed = timer.elapsed()
    assert elapsed >= 0.03
    timer.stop()


def test_timer_pause_resume() -> None:
    """Test pausing and resuming the timer."""
    timer = Timer()
    timer.start()
    time.sleep(0.02)
    timer.stop()
    paused_time = timer.elapsed()
    
    time.sleep(0.02)  # Should not count
    assert timer.elapsed() == paused_time
    
    timer.start()  # Resume
    time.sleep(0.02)
    timer.stop()
    
    assert timer.elapsed() > paused_time


def test_timer_reset() -> None:
    """Test resetting the timer."""
    timer = Timer()
    timer.start()
    time.sleep(0.02)
    timer.stop()
    
    timer.reset()
    assert timer.elapsed() == 0.0
    assert timer.is_running() is False


def test_timer_reset_while_running() -> None:
    """Test resetting while timer is running."""
    timer = Timer()
    timer.start()
    time.sleep(0.02)
    timer.reset()
    
    assert timer.elapsed() == 0.0
    assert timer.is_running() is False


def test_timer_multiple_starts() -> None:
    """Test that multiple start calls don't reset elapsed time."""
    timer = Timer()
    timer.start()
    time.sleep(0.02)
    timer.start()  # Should not reset
    time.sleep(0.02)
    timer.stop()
    
    assert timer.elapsed() >= 0.04


def test_timer_multiple_cycles() -> None:
    """Test multiple start/stop cycles accumulate time."""
    timer = Timer()
    
    for _ in range(3):
        timer.start()
        time.sleep(0.01)
        timer.stop()
    
    assert timer.elapsed() >= 0.03


def test_timer_str() -> None:
    """Test the __str__ method."""
    timer = Timer()
    result = str(timer)
    assert "Timer" in result or "0" in result


def test_timer_repr() -> None:
    """Test the __repr__ method."""
    timer = Timer()
    result = repr(timer)
    assert "Timer" in result


def test_timer_is_running_while_running() -> None:
    """Test is_running returns True when timer is running."""
    timer = Timer()
    timer.start()
    assert timer.is_running() is True
    timer.stop()


def test_timer_is_running_when_stopped() -> None:
    """Test is_running returns False when timer is stopped."""
    timer = Timer()
    assert timer.is_running() is False
    timer.start()
    timer.stop()
    assert timer.is_running() is False
