"""Tests for Problem 05: Save/Load State."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day06.problem_05_save_load_state import (
    SaveMetadata,
    GameStateMemento,
    GameState,
    SaveManager,
    GameSession,
    AutoSaveSystem,
)


@pytest.fixture(autouse=True)
def reset_save_manager() -> None:
    """Reset SaveManager singleton before each test."""
    SaveManager.reset()
    yield


class TestSaveMetadata:
    """Test save metadata."""
    
    def test_creation(self) -> None:
        meta = SaveMetadata(
            name="My Save",
            timestamp="2024-01-15T10:30:00",
            playtime_seconds=3600.0,
        )
        
        assert meta.name == "My Save"
        assert meta.timestamp == "2024-01-15T10:30:00"
        assert meta.playtime_seconds == 3600.0
    
    def test_to_dict(self) -> None:
        meta = SaveMetadata(name="Test", timestamp="2024-01-01", playtime_seconds=100.0)
        
        data = meta.to_dict()
        
        assert data["name"] == "Test"
        assert data["timestamp"] == "2024-01-01"
        assert data["playtime_seconds"] == 100.0
    
    def test_from_dict(self) -> None:
        data = {"name": "Test", "timestamp": "2024-01-01", "playtime_seconds": 100.0}
        
        meta = SaveMetadata.from_dict(data)
        
        assert meta.name == "Test"
        assert meta.playtime_seconds == 100.0


class TestGameStateMemento:
    """Test game state memento."""
    
    def test_creation(self) -> None:
        meta = SaveMetadata("Test", "2024-01-01")
        memento = GameStateMemento(
            player_position=(10.0, 20.0),
            player_health=80,
            inventory=["sword", "potion"],
            level=5,
            experience=250,
            metadata=meta,
        )
        
        assert memento.player_position == (10.0, 20.0)
        assert memento.player_health == 80
        assert memento.inventory == ["sword", "potion"]
    
    def test_immutability(self) -> None:
        meta = SaveMetadata("Test", "2024-01-01")
        memento = GameStateMemento(
            player_position=(0.0, 0.0),
            player_health=100,
            inventory=[],
            level=1,
            experience=0,
            metadata=meta,
        )
        
        # Cannot modify frozen dataclass
        with pytest.raises(Exception):
            memento.player_health = 50  # type: ignore
    
    def test_to_dict(self) -> None:
        meta = SaveMetadata("Test", "2024-01-01")
        memento = GameStateMemento(
            player_position=(10.0, 20.0),
            player_health=80,
            inventory=["sword"],
            level=5,
            experience=250,
            metadata=meta,
        )
        
        data = memento.to_dict()
        
        assert data["player_position"] == [10.0, 20.0]
        assert data["player_health"] == 80
        assert data["metadata"]["name"] == "Test"
    
    def test_from_dict(self) -> None:
        data = {
            "player_position": [10.0, 20.0],
            "player_health": 80,
            "inventory": ["sword"],
            "level": 5,
            "experience": 250,
            "metadata": {"name": "Test", "timestamp": "2024-01-01", "playtime_seconds": 0.0},
        }
        
        memento = GameStateMemento.from_dict(data)
        
        assert memento.player_position == (10.0, 20.0)
        assert memento.player_health == 80
        assert memento.level == 5


class TestGameState:
    """Test game state (originator)."""
    
    def test_initial_state(self) -> None:
        state = GameState()
        
        assert state.player_position == (0.0, 0.0)
        assert state.player_health == 100
        assert state.inventory == []
        assert state.level == 1
        assert state.experience == 0
    
    def test_save_creates_memento(self) -> None:
        state = GameState()
        state.move_player(10.0, 20.0)
        state.add_item("sword")
        
        memento = state.save("Test Save")
        
        assert isinstance(memento, GameStateMemento)
        assert memento.player_position == (10.0, 20.0)
        assert "sword" in memento.inventory
        assert memento.metadata.name == "Test Save"
    
    def test_restore_from_memento(self) -> None:
        state = GameState()
        state.move_player(10.0, 20.0)
        state.take_damage(30)
        memento = state.save("Test")
        
        # Modify state
        state.move_player(50.0, 50.0)
        state.heal(100)
        
        # Restore
        state.restore(memento)
        
        assert state.player_position == (10.0, 20.0)
        assert state.player_health == 70  # 100 - 30
    
    def test_restore_inventory_is_copied(self) -> None:
        state = GameState()
        state.add_item("sword")
        memento = state.save("Test")
        
        # Restore and modify
        state.restore(memento)
        state.inventory.append("shield")
        
        # Original memento should be unchanged
        assert "shield" not in memento.inventory
    
    def test_move_player(self) -> None:
        state = GameState()
        
        state.move_player(5.0, 10.0)
        
        assert state.player_position == (5.0, 10.0)
    
    def test_take_damage(self) -> None:
        state = GameState()
        
        state.take_damage(30)
        
        assert state.player_health == 70
    
    def test_take_damage_not_below_zero(self) -> None:
        state = GameState()
        
        state.take_damage(150)
        
        assert state.player_health == 0
    
    def test_heal(self) -> None:
        state = GameState()
        state.take_damage(50)
        
        state.heal(30)
        
        assert state.player_health == 80
    
    def test_heal_not_above_max(self) -> None:
        state = GameState()
        
        state.heal(50)
        
        assert state.player_health == 100
    
    def test_add_item(self) -> None:
        state = GameState()
        
        state.add_item("sword")
        state.add_item("shield")
        
        assert state.inventory == ["sword", "shield"]
    
    def test_gain_experience(self) -> None:
        state = GameState()
        
        state.gain_experience(50)
        
        assert state.experience == 50
        assert state.level == 1
    
    def test_gain_experience_level_up(self) -> None:
        state = GameState()
        # Need 100 XP for level 1->2
        
        state.gain_experience(150)
        
        assert state.level == 2
        assert state.experience == 50  # 150 - 100
    
    def test_update_playtime(self) -> None:
        state = GameState()
        
        state.update_playtime(60.0)
        state.update_playtime(30.0)
        
        assert state.playtime_seconds == 90.0
    
    def test_to_dict(self) -> None:
        state = GameState()
        state.move_player(5.0, 10.0)
        state.add_item("sword")
        
        data = state.to_dict()
        
        assert data["player_position"] == [5.0, 10.0]
        assert data["inventory"] == ["sword"]
    
    def test_from_dict(self) -> None:
        data = {
            "player_position": [5.0, 10.0],
            "player_health": 80,
            "inventory": ["sword", "shield"],
            "level": 3,
            "experience": 50,
            "playtime_seconds": 3600.0,
        }
        
        state = GameState.from_dict(data)
        
        assert state.player_position == (5.0, 10.0)
        assert state.player_health == 80
        assert state.inventory == ["sword", "shield"]
        assert state.level == 3
        assert state.playtime_seconds == 3600.0


class TestSaveManager:
    """Test save manager (caretaker)."""
    
    def test_save_and_load(self) -> None:
        manager = SaveManager()
        state = GameState()
        memento = state.save("Test Save")
        
        manager.save("slot1", memento)
        loaded = manager.load("slot1")
        
        assert loaded is memento
    
    def test_load_unknown_slot(self) -> None:
        manager = SaveManager()
        
        result = manager.load("unknown")
        
        assert result is None
    
    def test_delete(self) -> None:
        manager = SaveManager()
        state = GameState()
        manager.save("slot1", state.save("Test"))
        
        result = manager.delete("slot1")
        
        assert result is True
        assert manager.has_save("slot1") is False
    
    def test_delete_unknown(self) -> None:
        manager = SaveManager()
        
        result = manager.delete("unknown")
        
        assert result is False
    
    def test_list_saves(self) -> None:
        manager = SaveManager()
        state = GameState()
        manager.save("slot1", state.save("Save 1"))
        manager.save("slot2", state.save("Save 2"))
        
        saves = manager.list_saves()
        
        assert len(saves) == 2
        names = [meta.name for _, meta in saves]
        assert "Save 1" in names
        assert "Save 2" in names
    
    def test_has_save(self) -> None:
        manager = SaveManager()
        state = GameState()
        manager.save("slot1", state.save("Test"))
        
        assert manager.has_save("slot1") is True
        assert manager.has_save("slot2") is False
    
    def test_get_metadata(self) -> None:
        manager = SaveManager()
        state = GameState()
        manager.save("slot1", state.save("My Save"))
        
        meta = manager.get_metadata("slot1")
        
        assert meta is not None
        assert meta.name == "My Save"
    
    def test_get_metadata_unknown(self) -> None:
        manager = SaveManager()
        
        meta = manager.get_metadata("unknown")
        
        assert meta is None
    
    def test_clear(self) -> None:
        manager = SaveManager()
        state = GameState()
        manager.save("slot1", state.save("Test"))
        manager.save("slot2", state.save("Test"))
        
        manager.clear()
        
        assert manager.get_save_count() == 0


class TestGameSession:
    """Test game session."""
    
    def test_save_game(self) -> None:
        session = GameSession()
        session.get_state().move_player(10.0, 20.0)
        
        result = session.save_game("slot1", "My Save")
        
        assert result is True
        assert session.has_save("slot1") is True
    
    def test_load_game(self) -> None:
        session = GameSession()
        session.get_state().move_player(10.0, 20.0)
        session.save_game("slot1", "Test")
        
        # Modify state
        session.get_state().move_player(50.0, 50.0)
        
        # Load
        result = session.load_game("slot1")
        
        assert result is True
        assert session.get_state().player_position == (10.0, 20.0)
    
    def test_load_game_not_found(self) -> None:
        session = GameSession()
        
        result = session.load_game("unknown")
        
        assert result is False
    
    def test_list_saves(self) -> None:
        session = GameSession()
        session.save_game("slot1", "Save 1")
        session.save_game("slot2", "Save 2")
        
        saves = session.list_saves()
        
        assert len(saves) == 2
    
    def test_delete_save(self) -> None:
        session = GameSession()
        session.save_game("slot1", "Test")
        
        result = session.delete_save("slot1")
        
        assert result is True
        assert session.has_save("slot1") is False


class TestAutoSaveSystem:
    """Test auto-save system."""
    
    def test_update_no_save_before_interval(self) -> None:
        session = GameSession()
        auto_save = AutoSaveSystem(session, interval_seconds=300.0)
        
        result = auto_save.update(100.0)
        
        assert result is False
        assert session.has_save("autosave_1") is False
    
    def test_update_triggers_save(self) -> None:
        session = GameSession()
        auto_save = AutoSaveSystem(session, interval_seconds=100.0)
        
        result = auto_save.update(150.0)
        
        assert result is True
        assert session.has_save("autosave_1") is True
    
    def test_multiple_saves(self) -> None:
        session = GameSession()
        auto_save = AutoSaveSystem(session, interval_seconds=100.0)
        
        auto_save.update(150.0)  # autosave_1
        auto_save.update(150.0)  # autosave_2
        
        assert session.has_save("autosave_1")
        assert session.has_save("autosave_2")
    
    def test_force_save(self) -> None:
        session = GameSession()
        auto_save = AutoSaveSystem(session, interval_seconds=300.0)
        
        result = auto_save.force_save()
        
        assert result is True
        assert session.has_save("autosave_1") is True
    
    def test_playtime_tracked(self) -> None:
        session = GameSession()
        auto_save = AutoSaveSystem(session, interval_seconds=100.0)
        
        auto_save.update(50.0)
        
        assert session.get_state().playtime_seconds == 50.0


class TestIntegration:
    """Integration tests."""
    
    def test_full_save_load_cycle(self) -> None:
        """Test complete save/load workflow."""
        # Create and modify game state
        session = GameSession()
        state = session.get_state()
        state.move_player(100.0, 200.0)
        state.take_damage(25)
        state.add_item("excalibur")
        state.add_item("health_potion")
        state.gain_experience(350)  # Should level up to 3
        state.update_playtime(3600.0)
        
        # Save
        session.save_game("main", "Adventure Save")
        
        # Create new session and load
        new_session = GameSession()
        loaded = new_session.load_game("main")
        new_state = new_session.get_state()
        
        # Verify
        assert loaded is True
        assert new_state.player_position == (100.0, 200.0)
        assert new_state.player_health == 75
        assert "excalibur" in new_state.inventory
        assert new_state.level == 3
        assert new_state.playtime_seconds == 3600.0
        
        # Check metadata
        meta = new_session.get_save_manager().get_metadata("main")
        assert meta is not None
        assert meta.name == "Adventure Save"
    
    def test_multiple_save_slots(self) -> None:
        """Test managing multiple saves."""
        session = GameSession()
        
        # Create different saves
        session.get_state().move_player(10.0, 10.0)
        session.save_game("early", "Early Game")
        
        session.get_state().move_player(50.0, 50.0)
        session.get_state().gain_experience(200)
        session.save_game("mid", "Mid Game")
        
        session.get_state().move_player(100.0, 100.0)
        session.get_state().level = 10
        session.save_game("late", "Late Game")
        
        # List saves
        saves = session.list_saves()
        assert len(saves) == 3
        
        # Load early save
        session.load_game("early")
        assert session.get_state().player_position == (10.0, 10.0)
        
        # Load late save
        session.load_game("late")
        assert session.get_state().level == 10
