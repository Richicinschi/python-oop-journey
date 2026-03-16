"""Problem 04: Playlist

Topic: Magic Methods - Container Protocol
Difficulty: Medium

Implement a playlist class that behaves like a container.

Hints:
    - Hint 1: Store songs in a list: self._songs = []
    - Hint 2: __getitem__ handles both index (returns Song) and slice (returns list)
    - Hint 3: __iter__ can simply return iter(self._songs) - delegation pattern
"""

from __future__ import annotations

from typing import Iterator


class Song:
    """Represents a song with title and artist.
    
    Attributes:
        title: The song title.
        artist: The song artist.
        duration: The song duration in seconds.
    """
    
    def __init__(self, title: str, artist: str, duration: int) -> None:
        """Initialize a song.
        
        Args:
            title: The song title.
            artist: The song artist.
            duration: The song duration in seconds.
        """
        raise NotImplementedError("Implement __init__")
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on title and artist."""
        raise NotImplementedError("Implement __eq__")
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        raise NotImplementedError("Implement __repr__")


class Playlist:
    """A music playlist supporting container operations.
    
    Attributes:
        name: The playlist name.
    
    Example:
        >>> playlist = Playlist("My Favorites")
        >>> playlist.add_song(Song("Song A", "Artist 1", 180))
        >>> len(playlist)
        1
        >>> playlist[0]
        Song(title='Song A', artist='Artist 1', duration=180)
        >>> for song in playlist:
        ...     print(song.title)
        Song A
    """
    
    def __init__(self, name: str) -> None:
        """Initialize a playlist.
        
        Args:
            name: The playlist name.
        """
        raise NotImplementedError("Implement __init__")
    
    def add_song(self, song: Song) -> None:
        """Add a song to the playlist.
        
        Args:
            song: The song to add.
        """
        raise NotImplementedError("Implement add_song")
    
    def remove_song(self, song: Song) -> bool:
        """Remove a song from the playlist.
        
        Args:
            song: The song to remove.
        
        Returns:
            True if the song was found and removed, False otherwise.
        """
        raise NotImplementedError("Implement remove_song")
    
    def __len__(self) -> int:
        """Return the number of songs in the playlist."""
        raise NotImplementedError("Implement __len__")
    
    def __getitem__(self, index: int | slice) -> Song | list[Song]:
        """Get a song or slice of songs by index.
        
        Args:
            index: The index or slice.
        
        Returns:
            A single Song or list of Songs.
        
        Raises:
            IndexError: If index is out of range.
            TypeError: If index is not int or slice.
        """
        raise NotImplementedError("Implement __getitem__")
    
    def __iter__(self) -> Iterator[Song]:
        """Return an iterator over the songs."""
        raise NotImplementedError("Implement __iter__")
    
    def __contains__(self, song: Song) -> bool:
        """Check if a song is in the playlist.
        
        Args:
            song: The song to check for.
        
        Returns:
            True if the song is in the playlist, False otherwise.
        """
        raise NotImplementedError("Implement __contains__")
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        raise NotImplementedError("Implement __repr__")
    
    def total_duration(self) -> int:
        """Calculate the total duration of all songs in seconds.
        
        Returns:
            The sum of all song durations.
        """
        raise NotImplementedError("Implement total_duration")
