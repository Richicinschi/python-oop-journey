"""Tests for Problem 02: Event Bus."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day06.problem_02_event_bus import (
    EventBus,
    EventLogger,
    ScoreBoard,
    HealthMonitor,
)


class TestEventBus:
    """Test event bus functionality."""
    
    def test_subscribe_and_publish(self) -> None:
        bus = EventBus()
        logger = EventLogger()
        
        bus.subscribe("test", logger.on_event)
        bus.publish("test", message="hello")
        
        assert logger.get_event_count() == 1
        assert logger.get_events()[0]["message"] == "hello"
    
    def test_multiple_subscribers(self) -> None:
        bus = EventBus()
        logger1 = EventLogger()
        logger2 = EventLogger()
        
        bus.subscribe("test", logger1.on_event)
        bus.subscribe("test", logger2.on_event)
        bus.publish("test", value=42)
        
        assert logger1.get_event_count() == 1
        assert logger2.get_event_count() == 1
    
    def test_different_event_types(self) -> None:
        bus = EventBus()
        logger = EventLogger()
        
        bus.subscribe("event_a", logger.on_event)
        bus.subscribe("event_b", logger.on_event)
        
        bus.publish("event_a", data="a")
        bus.publish("event_b", data="b")
        
        assert logger.get_event_count() == 2
    
    def test_unsubscribe(self) -> None:
        bus = EventBus()
        logger = EventLogger()
        
        bus.subscribe("test", logger.on_event)
        result = bus.unsubscribe("test", logger.on_event)
        bus.publish("test", message="hello")
        
        assert result is True
        assert logger.get_event_count() == 0
    
    def test_unsubscribe_nonexistent(self) -> None:
        bus = EventBus()
        logger = EventLogger()
        
        result = bus.unsubscribe("test", logger.on_event)
        
        assert result is False
    
    def test_priority_order(self) -> None:
        bus = EventBus()
        order: list[int] = []
        
        def handler_low(**kwargs: Any) -> None:
            order.append(1)
        
        def handler_high(**kwargs: Any) -> None:
            order.append(2)
        
        bus.subscribe("test", handler_low, priority=0)
        bus.subscribe("test", handler_high, priority=10)
        bus.publish("test")
        
        assert order == [2, 1]  # High priority called first
    
    def test_wildcard_subscription(self) -> None:
        bus = EventBus()
        logger = EventLogger()
        
        bus.subscribe("*", logger.on_event)
        bus.publish("event_a", data=1)
        bus.publish("event_b", data=2)
        
        assert logger.get_event_count() == 2
    
    def test_specific_and_wildcard(self) -> None:
        bus = EventBus()
        specific_logger = EventLogger()
        wildcard_logger = EventLogger()
        
        bus.subscribe("test", specific_logger.on_event)
        bus.subscribe("*", wildcard_logger.on_event)
        bus.publish("test", data=42)
        
        assert specific_logger.get_event_count() == 1
        assert wildcard_logger.get_event_count() == 1
    
    def test_get_subscriber_count(self) -> None:
        bus = EventBus()
        
        bus.subscribe("test", lambda **k: None)
        bus.subscribe("test", lambda **k: None)
        bus.subscribe("*", lambda **k: None)
        
        assert bus.get_subscriber_count("test") == 3  # 2 specific + 1 wildcard
        assert bus.get_subscriber_count("other") == 1  # Just wildcard
    
    def test_clear(self) -> None:
        bus = EventBus()
        logger = EventLogger()
        
        bus.subscribe("test", logger.on_event)
        bus.subscribe("*", logger.on_event)
        bus.clear()
        bus.publish("test")
        
        assert logger.get_event_count() == 0


class TestEventLogger:
    """Test event logger utility."""
    
    def test_log_event(self) -> None:
        logger = EventLogger()
        
        logger.on_event(event_type="test", data=42)
        
        events = logger.get_events()
        assert len(events) == 1
        assert events[0]["event_type"] == "test"
        assert events[0]["data"] == 42
    
    def test_clear_events(self) -> None:
        logger = EventLogger()
        logger.on_event(event_type="test")
        
        logger.clear()
        
        assert logger.get_event_count() == 0
    
    def test_get_events_returns_copy(self) -> None:
        logger = EventLogger()
        logger.on_event(event_type="test")
        
        events = logger.get_events()
        events.clear()
        
        assert logger.get_event_count() == 1  # Original unchanged


class TestScoreBoard:
    """Test score board example."""
    
    def test_score_tracking(self) -> None:
        bus = EventBus()
        scoreboard = ScoreBoard()
        
        bus.subscribe("player_score", scoreboard.on_player_score)
        bus.subscribe("player_kill", scoreboard.on_player_kill)
        
        bus.publish("player_score", points=100)
        bus.publish("player_score", points=50)
        bus.publish("player_kill")
        
        assert scoreboard.score == 150
        assert scoreboard.kills == 1
    
    def test_death_tracking(self) -> None:
        bus = EventBus()
        scoreboard = ScoreBoard()
        
        bus.subscribe("player_death", scoreboard.on_player_death)
        bus.publish("player_death")
        bus.publish("player_death")
        
        assert scoreboard.deaths == 2


class TestHealthMonitor:
    """Test health monitor example."""
    
    def test_damage_events(self) -> None:
        bus = EventBus()
        monitor = HealthMonitor()
        
        bus.subscribe("damage", monitor.on_damage)
        bus.publish("damage", amount=10, source="enemy")
        
        assert len(monitor.health_events) == 1
        assert monitor.health_events[0]["type"] == "damage"
    
    def test_heal_events(self) -> None:
        bus = EventBus()
        monitor = HealthMonitor()
        
        bus.subscribe("heal", monitor.on_heal)
        bus.publish("heal", amount=25)
        
        assert len(monitor.health_events) == 1
        assert monitor.health_events[0]["type"] == "heal"


class TestIntegration:
    """Integration tests."""
    
    def test_complex_event_flow(self) -> None:
        """Test a realistic game event scenario."""
        bus = EventBus()
        scoreboard = ScoreBoard()
        health_monitor = HealthMonitor()
        event_logger = EventLogger()
        
        # Set up subscriptions
        bus.subscribe("player_score", scoreboard.on_player_score)
        bus.subscribe("player_kill", scoreboard.on_player_kill)
        bus.subscribe("player_death", scoreboard.on_player_death)
        bus.subscribe("damage", health_monitor.on_damage)
        bus.subscribe("heal", health_monitor.on_heal)
        bus.subscribe("*", event_logger.on_event)  # Log everything
        
        # Simulate game events
        bus.publish("damage", amount=10, source="goblin")
        bus.publish("player_kill")
        bus.publish("player_score", points=100)
        bus.publish("heal", amount=5)
        
        # Verify state
        assert scoreboard.score == 100
        assert scoreboard.kills == 1
        assert len(health_monitor.health_events) == 2
        assert event_logger.get_event_count() == 4  # All events logged
