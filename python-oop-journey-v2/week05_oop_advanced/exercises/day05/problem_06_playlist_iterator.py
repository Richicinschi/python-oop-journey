"""Problem 06: Playlist Iterator

Topic: Custom Collection with Multiple Iteration Modes
Difficulty: Medium

Create a music playlist with multiple iteration modes: sequential, shuffle,
and repeat. Demonstrates custom collections with stateful iteration.
"""

from __future__ import annotations
from typing import Iterator
from enum import Enum, auto


class PlayMode(Enum):
    """Playback modes for the playlist."""
    NORMAL = auto()
    SHUFFLE = auto()
    REPEAT_ONE = auto()
    REPEAT_ALL = auto()


class Song:
    """Represents a song in the playlist.
    
    Attributes:
        title: Song title
        artist: Artist name
        duration: Duration in seconds
    """
    
    def __init__(self, title: str, artist: str, duration: int) -> None:
        """Initialize a song.
        
        Args:
            title: The song title
            artist: The artist name
            duration: Duration in seconds (must be positive)
            
        Raises:
            ValueError: If duration is not positive
        """
        raise NotImplementedError("Implement __init__")
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on title and artist."""
        raise NotImplementedError("Implement __eq__")
    
    def __hash__(self) -> int:
        """Hash based on title and artist."""
        raise NotImplementedError("Implement __hash__")
    
    def __repr__(self) -> str:
        """String representation of the song."""
        raise NotImplementedError("Implement __repr__")


class Playlist:
    """A music playlist with multiple playback modes.
    
    Supports normal, shuffle, repeat-one, and repeat-all modes.
    
    Attributes:
        name: Playlist name
        mode: Current playback mode
        songs: List of songs in the playlist
    """
    
    def __init__(self, name: str) -> None:
        """Initialize an empty playlist.
        
        Args:
            name: The playlist name
        """
        raise NotImplementedError("Implement __init__")
    
    def add_song(self, song: Song) -> None:
        """Add a song to the playlist.
        
        Args:
            song: The song to add
        """
        raise NotImplementedError("Implement add_song")
    
    def remove_song(self, song: Song) -> bool:
        """Remove a song from the playlist.
        
        Args:
            song: The song to remove
            
        Returns:
            True if song was found and removed, False otherwise
        """
        raise NotImplementedError("Implement remove_song")
    
    def set_mode(self, mode: PlayMode) -> None:
        """Set the playback mode.
        
        Args:
            mode: The new playback mode
        """
        raise NotImplementedError("Implement set_mode")
    
    def __iter__(self) -> PlaylistIterator:
        """Return an iterator based on current mode.
        
        Returns:
            PlaylistIterator configured for the current mode
        """
        raise NotImplementedError("Implement __iter__")
    
    def __len__(self) -> int:
        """Return the number of songs.
        
        Returns:
            Count of songs in the playlist
        """
        raise NotImplementedError("Implement __len__")
    
    def shuffle_iter(self) -> Iterator[Song]:
        """Return a shuffle iterator (regardless of mode).
        
        Returns:
            Iterator that yields songs in random order
        """
        raise NotImplementedError("Implement shuffle_iter")
    
    def repeat_iter(self, count: int | None = None) -> Iterator[Song]:
        """Return a repeat iterator.
        
        Args:
            count: Number of times to repeat, None for infinite
            
        Returns:
            Iterator that repeats songs
        """
        raise NotImplementedError("Implement repeat_iter")


class PlaylistIterator:
    """Iterator that respects the playlist's playback mode.
    
    Handles different iteration behaviors based on PlayMode.
    """
    
    def __init__(self, playlist: Playlist) -> None:
        """Initialize the playlist iterator.
        
        Args:
            playlist: The playlist to iterate over
        """
        raise NotImplementedError("Implement __init__")
    
    def __iter__(self) -> PlaylistIterator:
        """Return self."""
        raise NotImplementedError("Implement __iter__")
    
    def __next__(self) -> Song:
        """Return the next song based on mode.
        
        Raises:
            StopIteration: When iteration should end (varies by mode)
            
        Returns:
            The next Song to play
        """
        raise NotImplementedError("Implement __next__")
    
    def current_index(self) -> int:
        """Get the current position in the playlist.
        
        Returns:
            Current index, or -1 if not started
        """
        raise NotImplementedError("Implement current_index")


# Hints for Playlist Iterator (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to iterate through items, supporting shuffle and repeat modes.
# Random.shuffle can shuffle a list in-place.
#
# Hint 2 - Structural plan:
# - __init__ stores items, creates a shuffled order if shuffle=True
# - Track current position and whether to repeat
# - __next__ returns item at current position, advances position
# - If at end and repeat=True, reset position to 0
# - If at end and no repeat, raise StopIteration
#
# Hint 3 - Edge-case warning:
# Shuffling should happen once at start, not on every iteration. Handle empty
# playlist (StopIteration immediately). What about repeat with shuffle - should
# it reshuffle or repeat same order?
