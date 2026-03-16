"""Reference solution for Problem 06: Playlist Iterator."""

from __future__ import annotations
import random
from typing import Iterator
from enum import Enum, auto


class PlayMode(Enum):
    """Playback modes for the playlist."""
    NORMAL = auto()
    SHUFFLE = auto()
    REPEAT_ONE = auto()
    REPEAT_ALL = auto()


class Song:
    """Represents a song in the playlist."""
    
    def __init__(self, title: str, artist: str, duration: int) -> None:
        if duration <= 0:
            raise ValueError("duration must be positive")
        self.title = title
        self.artist = artist
        self.duration = duration
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Song):
            return NotImplemented
        return self.title == other.title and self.artist == other.artist
    
    def __hash__(self) -> int:
        return hash((self.title, self.artist))
    
    def __repr__(self) -> str:
        return f"Song({self.title!r}, {self.artist!r}, {self.duration})"


class Playlist:
    """A music playlist with multiple playback modes."""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self._songs: list[Song] = []
        self._mode = PlayMode.NORMAL
    
    def add_song(self, song: Song) -> None:
        self._songs.append(song)
    
    def remove_song(self, song: Song) -> bool:
        if song in self._songs:
            self._songs.remove(song)
            return True
        return False
    
    def set_mode(self, mode: PlayMode) -> None:
        self._mode = mode
    
    @property
    def mode(self) -> PlayMode:
        return self._mode
    
    def __iter__(self) -> PlaylistIterator:
        return PlaylistIterator(self)
    
    def __len__(self) -> int:
        return len(self._songs)
    
    def shuffle_iter(self) -> Iterator[Song]:
        """Return a shuffle iterator."""
        songs = self._songs.copy()
        random.shuffle(songs)
        return iter(songs)
    
    def repeat_iter(self, count: int | None = None) -> Iterator[Song]:
        """Return a repeat iterator."""
        if count is None:
            # Infinite repeat
            while True:
                for song in self._songs:
                    yield song
        else:
            for _ in range(count):
                for song in self._songs:
                    yield song


class PlaylistIterator:
    """Iterator that respects the playlist's playback mode."""
    
    def __init__(self, playlist: Playlist) -> None:
        self._playlist = playlist
        self._mode = playlist.mode
        self._index = 0
        self._current_song: Song | None = None
        self._shuffle_order: list[int] = []
        self._shuffle_index = 0
        
        if self._mode == PlayMode.SHUFFLE and playlist._songs:
            self._shuffle_order = list(range(len(playlist._songs)))
            random.shuffle(self._shuffle_order)
    
    def __iter__(self) -> PlaylistIterator:
        self._mode = self._playlist.mode
        self._index = 0
        self._shuffle_index = 0
        self._current_song = None
        if self._mode == PlayMode.SHUFFLE and self._playlist._songs:
            self._shuffle_order = list(range(len(self._playlist._songs)))
            random.shuffle(self._shuffle_order)
        return self
    
    def __next__(self) -> Song:
        if not self._playlist._songs:
            raise StopIteration
        
        if self._mode == PlayMode.NORMAL:
            if self._index >= len(self._playlist._songs):
                raise StopIteration
            song = self._playlist._songs[self._index]
            self._index += 1
            self._current_song = song
            return song
        
        elif self._mode == PlayMode.SHUFFLE:
            if self._shuffle_index >= len(self._shuffle_order):
                raise StopIteration
            idx = self._shuffle_order[self._shuffle_index]
            self._shuffle_index += 1
            song = self._playlist._songs[idx]
            self._current_song = song
            return song
        
        elif self._mode == PlayMode.REPEAT_ONE:
            if self._current_song is None:
                self._current_song = self._playlist._songs[0]
            return self._current_song
        
        elif self._mode == PlayMode.REPEAT_ALL:
            song = self._playlist._songs[self._index % len(self._playlist._songs)]
            self._index += 1
            self._current_song = song
            return song
        
        raise StopIteration
    
    def current_index(self) -> int:
        if self._mode == PlayMode.SHUFFLE:
            if self._shuffle_index == 0:
                return -1
            return self._shuffle_order[self._shuffle_index - 1]
        else:
            if self._index == 0:
                return -1
            return (self._index - 1) % len(self._playlist._songs)
