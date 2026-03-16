"""Tests for Problem 01: Plugin-Driven Game Loop."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day06.problem_01_plugin_driven_game_loop import (
    GameLoop,
    PluginManager,
    PhysicsPlugin,
    RenderPlugin,
    InputPlugin,
)


class TestPluginManager:
    """Test plugin manager functionality."""
    
    def test_register_plugin(self) -> None:
        manager = PluginManager()
        plugin = PhysicsPlugin()
        
        manager.register(plugin)
        
        assert "physics" in manager.get_all_names()
        assert manager.get_plugin("physics") is plugin
        assert plugin._initialized is True
    
    def test_unregister_plugin(self) -> None:
        manager = PluginManager()
        plugin = PhysicsPlugin()
        manager.register(plugin)
        
        result = manager.unregister("physics")
        
        assert result is True
        assert "physics" not in manager.get_all_names()
        assert plugin._initialized is False
    
    def test_unregister_nonexistent(self) -> None:
        manager = PluginManager()
        
        result = manager.unregister("nonexistent")
        
        assert result is False
    
    def test_update_all_calls_update(self) -> None:
        manager = PluginManager()
        physics = PhysicsPlugin()
        render = RenderPlugin()
        manager.register(physics)
        manager.register(render)
        
        manager.update_all(0.016)
        manager.update_all(0.016)
        
        assert physics.update_count == 2
        assert render.frame_count == 2
    
    def test_disable_plugin(self) -> None:
        manager = PluginManager()
        plugin = PhysicsPlugin()
        manager.register(plugin)
        
        manager.disable("physics")
        manager.update_all(0.016)
        
        assert plugin.update_count == 0
        assert manager.is_enabled("physics") is False
    
    def test_enable_plugin(self) -> None:
        manager = PluginManager()
        plugin = PhysicsPlugin()
        manager.register(plugin)
        manager.disable("physics")
        
        manager.enable("physics")
        manager.update_all(0.016)
        
        assert plugin.update_count == 1
        assert manager.is_enabled("physics") is True
    
    def test_shutdown_all(self) -> None:
        manager = PluginManager()
        physics = PhysicsPlugin()
        render = RenderPlugin()
        manager.register(physics)
        manager.register(render)
        
        manager.shutdown_all()
        
        assert physics._initialized is False
        assert render._initialized is False
        assert manager.get_all_names() == []


class TestGameLoop:
    """Test game loop functionality."""
    
    def test_initial_state(self) -> None:
        loop = GameLoop(tick_rate=30.0)
        
        assert loop.is_running is False
        assert loop.tick_rate == 30.0
        assert loop.tick_count == 0
    
    def test_start_loop(self) -> None:
        loop = GameLoop()
        
        loop.start()
        
        assert loop.is_running is True
    
    def test_stop_loop(self) -> None:
        loop = GameLoop()
        loop.start()
        
        loop.stop()
        
        assert loop.is_running is False
    
    def test_tick_increments_counter(self) -> None:
        loop = GameLoop()
        loop.start()
        
        loop.tick(0.016)
        loop.tick(0.016)
        
        assert loop.tick_count == 2
    
    def test_tick_only_when_running(self) -> None:
        loop = GameLoop()
        # Don't start the loop
        
        loop.tick(0.016)
        
        assert loop.tick_count == 0
    
    def test_tick_updates_plugins(self) -> None:
        loop = GameLoop()
        plugin = PhysicsPlugin()
        loop.plugin_manager.register(plugin)
        loop.start()
        
        loop.tick(0.016)
        
        assert plugin.update_count == 1
    
    def test_plugin_manager_accessible(self) -> None:
        loop = GameLoop()
        
        manager = loop.plugin_manager
        
        assert isinstance(manager, PluginManager)


class TestExamplePlugins:
    """Test example plugin implementations."""
    
    def test_physics_plugin_lifecycle(self) -> None:
        plugin = PhysicsPlugin()
        
        assert plugin.name == "physics"
        assert plugin._initialized is False
        
        plugin.initialize()
        assert plugin._initialized is True
        
        plugin.update(0.016)
        assert plugin.update_count == 1
        
        plugin.shutdown()
        assert plugin._initialized is False
    
    def test_render_plugin_lifecycle(self) -> None:
        plugin = RenderPlugin()
        
        assert plugin.name == "render"
        
        plugin.initialize()
        plugin.update(0.016)
        plugin.update(0.016)
        
        assert plugin.frame_count == 2
    
    def test_input_plugin_records_events(self) -> None:
        plugin = InputPlugin()
        
        assert plugin.name == "input"
        
        plugin.record_input("KEY_UP")
        plugin.record_input("KEY_DOWN")
        
        assert len(plugin._input_events) == 2
    
    def test_multiple_plugins_independent(self) -> None:
        physics = PhysicsPlugin()
        render = RenderPlugin()
        
        physics.initialize()
        physics.update(0.016)
        
        assert physics.update_count == 1
        assert render.frame_count == 0  # Not updated
