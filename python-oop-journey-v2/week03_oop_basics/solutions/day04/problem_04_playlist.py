"""Reference solution for Problem 04: Playlist."""

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
        self.title = title
        self.artist = artist
        self.duration = duration
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on title and artist."""
        if not isinstance(other, Song):
            return NotImplemented
        return self.title == other.title and self.artist == other.artist
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        return f"Song(title={self.title!r}, artist={self.artist!r}, duration={self.duration!r})"


class Playlist:
    """A music playlist supporting container operations.
    
    Attributes:
        name: The playlist name.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize a playlist.
        
        Args:
            name: The playlist name.
        """
        self.name = name
        self._songs: list[Song] = []
    
    def add_song(self, song: Song) -> None:
        """Add a song to the playlist.
        
        Args:
            song: The song to add.
        """
        self._songs.append(song)
    
    def remove_song(self, song: Song) -> bool:
        """Remove a song from the playlist.
        
        Args:
            song: The song to remove.
        
        Returns:
            True if the song was found and removed, False otherwise.
        """
        try:
            self._songs.remove(song)
            return True
        except ValueError:
            return False
    
    def __len__(self) -> int:
        """Return the number of songs in the playlist."""
        return len(self._songs)
    
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
        return self._songs[index]
    
    def __iter__(self) -> Iterator[Song]:
        """Return an iterator over the songs."""
        return iter(self._songs)
    
    def __contains__(self, song: Song) -> bool:
        """Check if a song is in the playlist.
        
        Args:
            song: The song to check for.
        
        Returns:
            True if the song is in the playlist, False otherwise.
        """
        return song in self._songs
    
    def __repr__(self) -> str:
        """Return the official string representation."""
        return f"Playlist(name={self.name!r}, songs={self._songs!r})"
    
    def total_duration(self) -> int:
        """Calculate the total duration of all songs in seconds.
        
        Returns:
            The sum of all song durations.
        """
        return sum(song.duration for song in self._songs)
