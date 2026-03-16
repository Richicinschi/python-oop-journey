"""Reference solution for Problem 05: Save/Load State."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Any
from datetime import datetime


@dataclass(frozen=True)
class SaveMetadata:
    """Metadata for a save file."""
    name: str
    timestamp: str
    playtime_seconds: float = 0.0
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "timestamp": self.timestamp,
            "playtime_seconds": self.playtime_seconds,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SaveMetadata:
        return cls(
            name=data["name"],
            timestamp=data["timestamp"],
            playtime_seconds=data.get("playtime_seconds", 0.0),
        )


@dataclass(frozen=True)
class GameStateMemento:
    """Immutable state snapshot. Must be created by GameState originator."""
    player_position: tuple[float, float]
    player_health: int
    inventory: list[str]
    level: int
    experience: int
    metadata: SaveMetadata
    
    def to_dict(self) -> dict[str, Any]:
        """Convert memento to dictionary for serialization."""
        return {
            "player_position": list(self.player_position),
            "player_health": self.player_health,
            "inventory": self.inventory,
            "level": self.level,
            "experience": self.experience,
            "metadata": self.metadata.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GameStateMemento:
        """Create memento from dictionary."""
        pos = data["player_position"]
        return cls(
            player_position=(pos[0], pos[1]),
            player_health=data["player_health"],
            inventory=list(data["inventory"]),
            level=data["level"],
            experience=data["experience"],
            metadata=SaveMetadata.from_dict(data["metadata"]),
        )


class GameState:
    """Originator - the object whose state is being saved/restored."""
    
    def __init__(self) -> None:
        self.player_position: tuple[float, float] = (0.0, 0.0)
        self.player_health: int = 100
        self.inventory: list[str] = []
        self.level: int = 1
        self.experience: int = 0
        self.playtime_seconds: float = 0.0
    
    def save(self, save_name: str) -> GameStateMemento:
        """Create a memento of current state."""
        metadata = SaveMetadata(
            name=save_name,
            timestamp=datetime.now().isoformat(),
            playtime_seconds=self.playtime_seconds,
        )
        return GameStateMemento(
            player_position=self.player_position,
            player_health=self.player_health,
            inventory=self.inventory.copy(),
            level=self.level,
            experience=self.experience,
            metadata=metadata,
        )
    
    def restore(self, memento: GameStateMemento) -> None:
        """Restore state from a memento."""
        self.player_position = memento.player_position
        self.player_health = memento.player_health
        self.inventory = memento.inventory.copy()
        self.level = memento.level
        self.experience = memento.experience
        self.playtime_seconds = memento.metadata.playtime_seconds
    
    def update_playtime(self, seconds: float) -> None:
        """Add to accumulated playtime."""
        self.playtime_seconds += seconds
    
    def move_player(self, x: float, y: float) -> None:
        """Move player to new position."""
        self.player_position = (x, y)
    
    def take_damage(self, amount: int) -> None:
        """Reduce player health."""
        self.player_health = max(0, self.player_health - amount)
    
    def heal(self, amount: int) -> None:
        """Increase player health."""
        self.player_health = min(100, self.player_health + amount)
    
    def add_item(self, item: str) -> None:
        """Add item to inventory."""
        self.inventory.append(item)
    
    def gain_experience(self, amount: int) -> None:
        """Add experience and check for level up."""
        self.experience += amount
        # Simple level up formula
        while self.experience >= self.level * 100:
            self.experience -= self.level * 100
            self.level += 1
    
    def to_dict(self) -> dict[str, Any]:
        """Export state as dictionary."""
        return {
            "player_position": list(self.player_position),
            "player_health": self.player_health,
            "inventory": self.inventory,
            "level": self.level,
            "experience": self.experience,
            "playtime_seconds": self.playtime_seconds,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GameState:
        """Create GameState from dictionary."""
        state = cls()
        pos = data["player_position"]
        state.player_position = (pos[0], pos[1])
        state.player_health = data["player_health"]
        state.inventory = list(data["inventory"])
        state.level = data["level"]
        state.experience = data["experience"]
        state.playtime_seconds = data.get("playtime_seconds", 0.0)
        return state


class SaveManager:
    """Caretaker - manages memento persistence without accessing internal state."""
    
    _instance: SaveManager | None = None
    _shared_saves: dict[str, GameStateMemento] | None = None
    
    def __new__(cls) -> SaveManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._shared_saves = {}
        return cls._instance
    
    def __init__(self) -> None:
        pass  # _shared_saves is initialized in __new__
    
    @property
    def _saves(self) -> dict[str, GameStateMemento]:
        if self._shared_saves is None:
            self._shared_saves = {}
        return self._shared_saves
    
    @_saves.setter
    def _saves(self, value: dict[str, GameStateMemento]) -> None:
        SaveManager._shared_saves = value
    
    @classmethod
    def reset(cls) -> None:
        """Reset the singleton for testing."""
        cls._shared_saves = {}
    
    def save(self, slot: str, memento: GameStateMemento) -> None:
        """Save a memento to a slot."""
        self._saves[slot] = memento
    
    def load(self, slot: str) -> GameStateMemento | None:
        """Load a memento from a slot."""
        return self._saves.get(slot)
    
    def delete(self, slot: str) -> bool:
        """Delete a save slot. Returns True if deleted."""
        if slot in self._saves:
            del self._saves[slot]
            return True
        return False
    
    def list_saves(self) -> list[tuple[str, SaveMetadata]]:
        """List all saves with their metadata."""
        return [(slot, memento.metadata) for slot, memento in self._saves.items()]
    
    def has_save(self, slot: str) -> bool:
        """Check if a slot has a save."""
        return slot in self._saves
    
    def get_metadata(self, slot: str) -> SaveMetadata | None:
        """Get metadata for a save slot."""
        if memento := self._saves.get(slot):
            return memento.metadata
        return None
    
    def clear(self) -> None:
        """Delete all saves."""
        self._saves.clear()
    
    def get_save_count(self) -> int:
        """Get number of saved games."""
        return len(self._saves)


class GameSession:
    """High-level interface combining GameState and SaveManager."""
    
    def __init__(self) -> None:
        self._state = GameState()
        self._save_manager = SaveManager()
    
    def save_game(self, slot: str, save_name: str) -> bool:
        """Save current game state to slot."""
        try:
            memento = self._state.save(save_name)
            self._save_manager.save(slot, memento)
            return True
        except Exception:
            return False
    
    def load_game(self, slot: str) -> bool:
        """Load game state from slot."""
        if memento := self._save_manager.load(slot):
            self._state.restore(memento)
            return True
        return False
    
    def get_state(self) -> GameState:
        """Get current game state."""
        return self._state
    
    def list_saves(self) -> list[tuple[str, SaveMetadata]]:
        """List available saves."""
        return self._save_manager.list_saves()
    
    def has_save(self, slot: str) -> bool:
        """Check if a save exists in slot."""
        return self._save_manager.has_save(slot)
    
    def delete_save(self, slot: str) -> bool:
        """Delete save in slot."""
        return self._save_manager.delete(slot)
    
    def get_save_manager(self) -> SaveManager:
        """Get the save manager."""
        return self._save_manager


# Example: AutoSave system using the memento pattern

class AutoSaveSystem:
    """Automatically saves game at intervals."""
    
    def __init__(self, session: GameSession, interval_seconds: float = 300.0) -> None:
        self.session = session
        self.interval = interval_seconds
        self.elapsed = 0.0
        self.save_counter = 0
    
    def update(self, delta_seconds: float) -> bool:
        """Update autosave timer. Returns True if save occurred."""
        self.elapsed += delta_seconds
        self.session.get_state().update_playtime(delta_seconds)
        
        if self.elapsed >= self.interval:
            self.elapsed = 0.0
            self.save_counter += 1
            slot = f"autosave_{self.save_counter}"
            return self.session.save_game(slot, f"Auto Save {self.save_counter}")
        return False
    
    def force_save(self) -> bool:
        """Force an immediate autosave."""
        self.elapsed = 0.0
        self.save_counter += 1
        slot = f"autosave_{self.save_counter}"
        return self.session.save_game(slot, f"Auto Save {self.save_counter}")
