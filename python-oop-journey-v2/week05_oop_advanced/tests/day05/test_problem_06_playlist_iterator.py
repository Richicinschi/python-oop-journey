"""Tests for Problem 06: Playlist Iterator."""

from __future__ import annotations

import pytest
from itertools import islice

from week05_oop_advanced.solutions.day05.problem_06_playlist_iterator import (
    PlayMode, Song, Playlist, PlaylistIterator
)


class TestSong:
    """Tests for Song class."""
    
    def test_song_creation(self) -> None:
        song = Song("Bohemian Rhapsody", "Queen", 354)
        assert song.title == "Bohemian Rhapsody"
        assert song.artist == "Queen"
        assert song.duration == 354
    
    def test_song_invalid_duration(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            Song("Test", "Artist", 0)
        with pytest.raises(ValueError, match="positive"):
            Song("Test", "Artist", -1)
    
    def test_song_equality(self) -> None:
        song1 = Song("Song", "Artist", 180)
        song2 = Song("Song", "Artist", 240)  # Different duration
        song3 = Song("Other", "Artist", 180)
        
        assert song1 == song2  # Same title and artist
        assert song1 != song3
    
    def test_song_hash(self) -> None:
        song1 = Song("Song", "Artist", 180)
        song2 = Song("Song", "Artist", 240)
        assert hash(song1) == hash(song2)
    
    def test_song_repr(self) -> None:
        song = Song("Test", "Artist", 180)
        assert "Test" in repr(song)
        assert "Artist" in repr(song)


class TestPlaylistInit:
    """Tests for Playlist initialization."""
    
    def test_init_empty(self) -> None:
        pl = Playlist("My Playlist")
        assert pl.name == "My Playlist"
        assert len(pl) == 0
    
    def test_default_mode_is_normal(self) -> None:
        pl = Playlist("Test")
        assert pl.mode == PlayMode.NORMAL


class TestPlaylistAddRemove:
    """Tests for adding and removing songs."""
    
    def test_add_song(self) -> None:
        pl = Playlist("Test")
        song = Song("Song", "Artist", 180)
        pl.add_song(song)
        assert len(pl) == 1
    
    def test_add_multiple_songs(self) -> None:
        pl = Playlist("Test")
        pl.add_song(Song("Song1", "A", 180))
        pl.add_song(Song("Song2", "B", 200))
        assert len(pl) == 2
    
    def test_remove_song_success(self) -> None:
        pl = Playlist("Test")
        song = Song("Song", "Artist", 180)
        pl.add_song(song)
        assert pl.remove_song(song) is True
        assert len(pl) == 0
    
    def test_remove_song_not_found(self) -> None:
        pl = Playlist("Test")
        song = Song("Song", "Artist", 180)
        assert pl.remove_song(song) is False


class TestPlaylistSetMode:
    """Tests for setting playback mode."""
    
    def test_set_mode_shuffle(self) -> None:
        pl = Playlist("Test")
        pl.set_mode(PlayMode.SHUFFLE)
        assert pl.mode == PlayMode.SHUFFLE
    
    def test_set_mode_repeat_one(self) -> None:
        pl = Playlist("Test")
        pl.set_mode(PlayMode.REPEAT_ONE)
        assert pl.mode == PlayMode.REPEAT_ONE


class TestPlaylistNormalMode:
    """Tests for NORMAL mode iteration."""
    
    def test_normal_mode_iteration(self) -> None:
        pl = Playlist("Test")
        songs = [Song(f"Song{i}", "Artist", 180) for i in range(3)]
        for song in songs:
            pl.add_song(song)
        
        result = list(pl)
        assert result == songs
    
    def test_normal_mode_stop_at_end(self) -> None:
        pl = Playlist("Test")
        pl.add_song(Song("Song", "Artist", 180))
        
        iterator = iter(pl)
        next(iterator)  # First song
        
        with pytest.raises(StopIteration):
            next(iterator)  # Should stop


class TestPlaylistShuffleMode:
    """Tests for SHUFFLE mode."""
    
    def test_shuffle_mode_yields_all_songs(self) -> None:
        pl = Playlist("Test")
        songs = [Song(f"Song{i}", "Artist", 180) for i in range(5)]
        for song in songs:
            pl.add_song(song)
        
        pl.set_mode(PlayMode.SHUFFLE)
        result = list(pl)
        
        assert len(result) == 5
        assert set(s.title for s in result) == set(s.title for s in songs)
    
    def test_shuffle_mode_stop_at_end(self) -> None:
        pl = Playlist("Test")
        pl.add_song(Song("Song1", "A", 180))
        pl.add_song(Song("Song2", "B", 200))
        pl.set_mode(PlayMode.SHUFFLE)
        
        iterator = iter(pl)
        next(iterator)
        next(iterator)
        
        with pytest.raises(StopIteration):
            next(iterator)


class TestPlaylistRepeatOneMode:
    """Tests for REPEAT_ONE mode."""
    
    def test_repeat_one_infinite(self) -> None:
        pl = Playlist("Test")
        song = Song("Song", "Artist", 180)
        pl.add_song(song)
        pl.set_mode(PlayMode.REPEAT_ONE)
        
        iterator = iter(pl)
        # Can get many values without StopIteration
        for _ in range(100):
            assert next(iterator) == song


class TestPlaylistRepeatAllMode:
    """Tests for REPEAT_ALL mode."""
    
    def test_repeat_all_cycles(self) -> None:
        pl = Playlist("Test")
        songs = [Song(f"Song{i}", "Artist", 180) for i in range(3)]
        for song in songs:
            pl.add_song(song)
        pl.set_mode(PlayMode.REPEAT_ALL)
        
        iterator = iter(pl)
        first_cycle = [next(iterator) for _ in range(3)]
        second_cycle = [next(iterator) for _ in range(3)]
        
        assert first_cycle == songs
        assert second_cycle == songs


class TestPlaylistShuffleIter:
    """Tests for shuffle_iter method."""
    
    def test_shuffle_iter_yields_all_songs(self) -> None:
        pl = Playlist("Test")
        songs = [Song(f"Song{i}", "Artist", 180) for i in range(5)]
        for song in songs:
            pl.add_song(song)
        
        result = list(pl.shuffle_iter())
        assert len(result) == 5
        assert set(s.title for s in result) == set(s.title for s in songs)


class TestPlaylistRepeatIter:
    """Tests for repeat_iter method."""
    
    def test_repeat_iter_with_count(self) -> None:
        pl = Playlist("Test")
        songs = [Song(f"Song{i}", "Artist", 180) for i in range(3)]
        for song in songs:
            pl.add_song(song)
        
        result = list(pl.repeat_iter(2))
        assert result == songs + songs
    
    def test_repeat_iter_infinite(self) -> None:
        pl = Playlist("Test")
        pl.add_song(Song("Song", "Artist", 180))
        
        gen = pl.repeat_iter()
        first_5 = list(islice(gen, 5))
        assert len(first_5) == 5
        assert all(s.title == "Song" for s in first_5)


class TestPlaylistIterator:
    """Tests for PlaylistIterator class."""
    
    def test_iterator_current_index(self) -> None:
        pl = Playlist("Test")
        pl.add_song(Song("Song0", "A", 180))
        pl.add_song(Song("Song1", "B", 200))
        
        iterator = PlaylistIterator(pl)
        assert iterator.current_index() == -1
        
        next(iterator)
        assert iterator.current_index() == 0
        
        next(iterator)
        assert iterator.current_index() == 1


class TestPlaylistEmpty:
    """Tests for empty playlist behavior."""
    
    def test_empty_playlist_iteration(self) -> None:
        pl = Playlist("Empty")
        result = list(pl)
        assert result == []
    
    def test_empty_playlist_raises_stop_iteration_immediately(self) -> None:
        pl = Playlist("Empty")
        iterator = iter(pl)
        with pytest.raises(StopIteration):
            next(iterator)


class TestPlaylistIntegration:
    """Integration tests."""
    
    def test_full_playlist_workflow(self) -> None:
        pl = Playlist("My Favorites")
        
        # Add songs
        pl.add_song(Song("Song A", "Artist 1", 180))
        pl.add_song(Song("Song B", "Artist 2", 200))
        pl.add_song(Song("Song C", "Artist 1", 220))
        
        # Normal playthrough
        pl.set_mode(PlayMode.NORMAL)
        normal_play = list(pl)
        assert len(normal_play) == 3
        
        # Switch to shuffle
        pl.set_mode(PlayMode.SHUFFLE)
        shuffle_play = list(pl)
        assert len(shuffle_play) == 3
        
        # Remove a song
        removed = pl.remove_song(Song("Song B", "Artist 2", 200))
        assert removed is True
        assert len(pl) == 2
        
        # Repeat all mode
        pl.set_mode(PlayMode.REPEAT_ALL)
        iterator = iter(pl)
        first_4 = [next(iterator) for _ in range(4)]
        assert len(first_4) == 4  # Should cycle
