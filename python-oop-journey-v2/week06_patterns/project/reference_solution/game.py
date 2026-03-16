"""
Game Engine and State Management

This module contains the main Game class and State pattern implementation
for managing game lifecycle and states.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type
from enum import Enum, auto

from week06_patterns.project.reference_solution.entity import Entity, EntityManager
from week06_patterns.project.reference_solution.components import Component
from week06_patterns.project.reference_solution.systems import System, SystemManager
from week06_patterns.project.reference_solution.events import EventBus, get_global_event_bus


class GameState(ABC):
    """
    Abstract base class for game states using the State pattern.
    
    Each state encapsulates behavior specific to that state.
    The Game class delegates to the current state.
    """
    
    def __init__(self, name: str):
        """
        Initialize the game state.
        
        Args:
            name: The state's display name
        """
        self._name: str = name
        self._game: Optional['Game'] = None
    
    @property
    def name(self) -> str:
        """Get the state name."""
        return self._name
    
    @property
    def game(self) -> Optional['Game']:
        """Get the game instance."""
        return self._game
    
    @game.setter
    def game(self, value: 'Game') -> None:
        """Set the game instance."""
        self._game = value
    
    @abstractmethod
    def enter(self) -> None:
        """
        Called when entering this state.
        Override for initialization logic.
        """
        pass
    
    @abstractmethod
    def update(self, delta_time: float) -> None:
        """
        Called each frame while in this state.
        
        Args:
            delta_time: Time elapsed since last frame
        """
        pass
    
    @abstractmethod
    def exit(self) -> None:
        """
        Called when exiting this state.
        Override for cleanup logic.
        """
        pass
    
    def handle_input(self, event: Any) -> None:
        """
        Handle input events.
        Override for state-specific input handling.
        
        Args:
            event: Input event to process
        """
        pass


class MenuState(GameState):
    """
    The main menu state where players can start the game,
    adjust settings, or quit.
    """
    
    def __init__(self):
        """Initialize menu state."""
        super().__init__("MENU")
    
    def enter(self) -> None:
        """Called when entering menu state."""
        pass
    
    def update(self, delta_time: float) -> None:
        """Called each frame in menu state."""
        pass
    
    def exit(self) -> None:
        """Called when exiting menu state."""
        pass


class PlayingState(GameState):
    """
    The main gameplay state where the game is actively running.
    """
    
    def __init__(self):
        """Initialize playing state."""
        super().__init__("PLAYING")
    
    def enter(self) -> None:
        """Called when entering playing state."""
        pass
    
    def update(self, delta_time: float) -> None:
        """Called each frame during gameplay."""
        pass
    
    def exit(self) -> None:
        """Called when exiting playing state."""
        pass


class PausedState(GameState):
    """
    The pause menu state that overlays the game.
    """
    
    def __init__(self, previous_state: GameState):
        """
        Initialize paused state.
        
        Args:
            previous_state: The state to return to when unpaused
        """
        super().__init__("PAUSED")
        self._previous_state: GameState = previous_state
    
    @property
    def previous_state(self) -> GameState:
        """Get the state to resume to."""
        return self._previous_state
    
    def enter(self) -> None:
        """Called when entering paused state."""
        pass
    
    def update(self, delta_time: float) -> None:
        """Called each frame while paused."""
        pass
    
    def exit(self) -> None:
        """Called when exiting paused state."""
        pass


class GameOverState(GameState):
    """
    The game over state shown when the player loses.
    """
    
    def __init__(self, winner: Optional[str] = None):
        """
        Initialize game over state.
        
        Args:
            winner: Optional winner identifier
        """
        super().__init__("GAME_OVER")
        self._winner: Optional[str] = winner
    
    @property
    def winner(self) -> Optional[str]:
        """Get the winner identifier."""
        return self._winner
    
    def enter(self) -> None:
        """Called when entering game over state."""
        pass
    
    def update(self, delta_time: float) -> None:
        """Called each frame in game over state."""
        pass
    
    def exit(self) -> None:
        """Called when exiting game over state."""
        pass


class Plugin(ABC):
    """
    Abstract base class for game plugins/extensions.
    Plugins can add custom systems, entities, or behaviors.
    """
    
    def __init__(self, name: str):
        """
        Initialize plugin.
        
        Args:
            name: Plugin identifier
        """
        self._name: str = name
        self._enabled: bool = True
    
    @property
    def name(self) -> str:
        """Get plugin name."""
        return self._name
    
    @property
    def enabled(self) -> bool:
        """Get whether plugin is enabled."""
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set whether plugin is enabled."""
        self._enabled = value
    
    @abstractmethod
    def on_register(self, game: 'Game') -> None:
        """
        Called when plugin is registered with a game.
        
        Args:
            game: The game instance
        """
        pass
    
    @abstractmethod
    def on_unregister(self, game: 'Game') -> None:
        """
        Called when plugin is unregistered from a game.
        
        Args:
            game: The game instance
        """
        pass


class Game:
    """
    The main game engine that ties together ECS, states, and plugins.
    
    Example:
        >>> game = Game()
        >>> game.add_system(PhysicsSystem())
        >>> player = game.create_entity("player")
        >>> game.change_state(PlayingState())
        >>> game.run()
    """
    
    def __init__(self):
        """
        Initialize the game engine.
        
        Initialize:
        - EntityManager
        - SystemManager
        - EventBus (use global)
        - Empty state stack
        - Empty plugin list
        - Running flag
        """
        self._entity_manager: EntityManager = EntityManager()
        self._system_manager: SystemManager = SystemManager()
        self._event_bus: EventBus = get_global_event_bus()
        self._state_stack: List[GameState] = []
        self._plugins: Dict[str, Plugin] = {}
        self._running: bool = False
        self._frame_count: int = 0
    
    @property
    def entity_manager(self) -> EntityManager:
        """Get the entity manager."""
        return self._entity_manager
    
    @property
    def system_manager(self) -> SystemManager:
        """Get the system manager."""
        return self._system_manager
    
    @property
    def event_bus(self) -> EventBus:
        """Get the event bus."""
        return self._event_bus
    
    @property
    def current_state(self) -> Optional[GameState]:
        """Get the current game state."""
        if self._state_stack:
            return self._state_stack[-1]
        return None
    
    @property
    def is_running(self) -> bool:
        """Get whether the game is running."""
        return self._running
    
    # Entity Management
    
    def create_entity(self, entity_id: Optional[str] = None) -> Entity:
        """
        Create a new entity.
        
        Args:
            entity_id: Optional unique identifier
            
        Returns:
            Entity: The new entity
        """
        return self._entity_manager.create_entity(entity_id)
    
    def add_entity(self, entity: Entity) -> 'Game':
        """
        Add an existing entity.
        
        Args:
            entity: The entity to add
            
        Returns:
            Game: Self for method chaining
        """
        self._entity_manager.add_entity(entity)
        return self
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """
        Get an entity by ID.
        
        Args:
            entity_id: The entity's unique identifier
            
        Returns:
            Entity or None
        """
        return self._entity_manager.get_entity(entity_id)
    
    def remove_entity(self, entity_id: str) -> bool:
        """
        Remove an entity.
        
        Args:
            entity_id: The entity to remove
            
        Returns:
            bool: True if entity was removed
        """
        return self._entity_manager.remove_entity(entity_id)
    
    # System Management
    
    def add_system(self, system: System) -> 'Game':
        """
        Add a system to the game.
        
        Args:
            system: The system to add
            
        Returns:
            Game: Self for method chaining
        """
        system.game = self
        self._system_manager.add_system(system)
        return self
    
    def get_system(self, system_type: Type[System]) -> Optional[System]:
        """
        Get a system by type.
        
        Args:
            system_type: The type of system to get
            
        Returns:
            System or None
        """
        return self._system_manager.get_system(system_type)
    
    # State Management
    
    def change_state(self, new_state: GameState) -> 'Game':
        """
        Change to a new state (replaces current state).
        
        Args:
            new_state: The state to switch to
            
        Returns:
            Game: Self for method chaining
        """
        if self._state_stack:
            self._state_stack[-1].exit()
        
        new_state.game = self
        if self._state_stack:
            self._state_stack[-1] = new_state
        else:
            self._state_stack.append(new_state)
        
        new_state.enter()
        return self
    
    def push_state(self, new_state: GameState) -> 'Game':
        """
        Push a new state onto the stack (pauses current).
        
        Args:
            new_state: The state to push
            
        Returns:
            Game: Self for method chaining
        """
        if self._state_stack:
            self._state_stack[-1].exit()
        
        new_state.game = self
        self._state_stack.append(new_state)
        new_state.enter()
        return self
    
    def pop_state(self) -> Optional[GameState]:
        """
        Pop the current state and return to previous.
        
        Returns:
            GameState: The popped state, or None if stack empty
        """
        if not self._state_stack:
            return None
        
        old_state = self._state_stack.pop()
        old_state.exit()
        
        if self._state_stack:
            self._state_stack[-1].enter()
        
        return old_state
    
    # Plugin Management
    
    def register_plugin(self, plugin: Plugin) -> 'Game':
        """
        Register a plugin with the game.
        
        Args:
            plugin: The plugin to register
            
        Returns:
            Game: Self for method chaining
        """
        self._plugins[plugin.name] = plugin
        plugin.on_register(self)
        return self
    
    def unregister_plugin(self, plugin_name: str) -> bool:
        """
        Unregister a plugin.
        
        Args:
            plugin_name: The name of the plugin to remove
            
        Returns:
            bool: True if plugin was found and removed
        """
        plugin = self._plugins.pop(plugin_name, None)
        if plugin:
            plugin.on_unregister(self)
            return True
        return False
    
    def get_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """
        Get a plugin by name.
        
        Args:
            plugin_name: The plugin name
            
        Returns:
            Plugin or None
        """
        return self._plugins.get(plugin_name)
    
    # Game Loop
    
    def start(self) -> 'Game':
        """
        Start the game.
        
        Returns:
            Game: Self for method chaining
        """
        self._running = True
        self._frame_count = 0
        return self
    
    def stop(self) -> 'Game':
        """
        Stop the game.
        
        Returns:
            Game: Self for method chaining
        """
        self._running = False
        return self
    
    def update(self, delta_time: float) -> None:
        """
        Update the game for one frame.
        
        This should:
        1. Update current state
        2. Update systems (if in playing state)
        
        Args:
            delta_time: Time elapsed since last frame
        """
        self._frame_count += 1
        
        # Update current state
        if self.current_state:
            self.current_state.update(delta_time)
        
        # Update systems only in playing state
        if isinstance(self.current_state, PlayingState):
            entities = self._entity_manager.get_all_entities()
            self._system_manager.update(delta_time, entities)
    
    def run(self, max_frames: Optional[int] = None) -> None:
        """
        Run the game loop.
        
        Args:
            max_frames: Optional frame limit for testing
        """
        self.start()
        delta_time = 1.0 / 60.0  # Assume 60 FPS
        
        while self._running:
            self.update(delta_time)
            
            if max_frames is not None:
                max_frames -= 1
                if max_frames <= 0:
                    self.stop()
