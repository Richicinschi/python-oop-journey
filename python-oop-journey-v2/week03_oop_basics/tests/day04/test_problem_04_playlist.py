"""Tests for Problem 04: Playlist."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day04.problem_04_playlist import Playlist, Song


class TestSongInit:
    """Test Song initialization."""
    
    def test_init_basic(self) -> None:
        song = Song("Title", "Artist", 180)
        assert song.title == "Title"
        assert song.artist == "Artist"
        assert song.duration == 180


class TestSongEquality:
    """Test Song equality."""
    
    def test_equal_same_title_and_artist(self) -> None:
        s1 = Song("Title", "Artist", 180)
        s2 = Song("Title", "Artist", 200)
        assert s1 == s2  # Duration doesn't matter for equality
    
    def test_not_equal_different_title(self) -> None:
        s1 = Song("Title1", "Artist", 180)
        s2 = Song("Title2", "Artist", 180)
        assert s1 != s2
    
    def test_not_equal_different_artist(self) -> None:
        s1 = Song("Title", "Artist1", 180)
        s2 = Song("Title", "Artist2", 180)
        assert s1 != s2


class TestPlaylistInit:
    """Test Playlist initialization."""
    
    def test_init_empty(self) -> None:
        playlist = Playlist("My Playlist")
        assert playlist.name == "My Playlist"
        assert len(playlist) == 0


class TestPlaylistAddSong:
    """Test adding songs to playlist."""
    
    def test_add_song(self) -> None:
        playlist = Playlist("My Playlist")
        song = Song("Title", "Artist", 180)
        playlist.add_song(song)
        assert len(playlist) == 1
    
    def test_add_multiple_songs(self) -> None:
        playlist = Playlist("My Playlist")
        playlist.add_song(Song("Song1", "Artist1", 180))
        playlist.add_song(Song("Song2", "Artist2", 200))
        assert len(playlist) == 2


class TestPlaylistRemoveSong:
    """Test removing songs from playlist."""
    
    def test_remove_existing_song(self) -> None:
        playlist = Playlist("My Playlist")
        song = Song("Title", "Artist", 180)
        playlist.add_song(song)
        result = playlist.remove_song(song)
        assert result is True
        assert len(playlist) == 0
    
    def test_remove_nonexistent_song(self) -> None:
        playlist = Playlist("My Playlist")
        song = Song("Title", "Artist", 180)
        result = playlist.remove_song(song)
        assert result is False


class TestPlaylistLen:
    """Test Playlist length."""
    
    def test_len_empty(self) -> None:
        playlist = Playlist("My Playlist")
        assert len(playlist) == 0
    
    def test_len_with_songs(self) -> None:
        playlist = Playlist("My Playlist")
        playlist.add_song(Song("Song1", "Artist1", 180))
        playlist.add_song(Song("Song2", "Artist2", 200))
        assert len(playlist) == 2


class TestPlaylistGetItem:
    """Test Playlist indexing."""
    
    def test_get_item_by_index(self) -> None:
        playlist = Playlist("My Playlist")
        song = Song("Title", "Artist", 180)
        playlist.add_song(song)
        assert playlist[0] == song
    
    def test_get_item_slice(self) -> None:
        playlist = Playlist("My Playlist")
        s1 = Song("Song1", "Artist", 180)
        s2 = Song("Song2", "Artist", 200)
        s3 = Song("Song3", "Artist", 220)
        playlist.add_song(s1)
        playlist.add_song(s2)
        playlist.add_song(s3)
        result = playlist[0:2]
        assert len(result) == 2
        assert result[0] == s1
        assert result[1] == s2
    
    def test_get_item_index_error(self) -> None:
        playlist = Playlist("My Playlist")
        with pytest.raises(IndexError):
            playlist[0]


class TestPlaylistIteration:
    """Test Playlist iteration."""
    
    def test_iteration(self) -> None:
        playlist = Playlist("My Playlist")
        s1 = Song("Song1", "Artist", 180)
        s2 = Song("Song2", "Artist", 200)
        playlist.add_song(s1)
        playlist.add_song(s2)
        songs = list(playlist)
        assert songs == [s1, s2]
    
    def test_iteration_empty(self) -> None:
        playlist = Playlist("My Playlist")
        songs = list(playlist)
        assert songs == []


class TestPlaylistContains:
    """Test Playlist membership testing."""
    
    def test_contains_true(self) -> None:
        playlist = Playlist("My Playlist")
        song = Song("Title", "Artist", 180)
        playlist.add_song(song)
        assert song in playlist
    
    def test_contains_false(self) -> None:
        playlist = Playlist("My Playlist")
        song1 = Song("Title1", "Artist", 180)
        song2 = Song("Title2", "Artist", 200)
        playlist.add_song(song1)
        assert song2 not in playlist


class TestPlaylistTotalDuration:
    """Test Playlist total duration."""
    
    def test_total_duration_empty(self) -> None:
        playlist = Playlist("My Playlist")
        assert playlist.total_duration() == 0
    
    def test_total_duration_with_songs(self) -> None:
        playlist = Playlist("My Playlist")
        playlist.add_song(Song("Song1", "Artist", 180))
        playlist.add_song(Song("Song2", "Artist", 200))
        assert playlist.total_duration() == 380


class TestPlaylistRepr:
    """Test Playlist representation."""
    
    def test_repr(self) -> None:
        playlist = Playlist("My Playlist")
        song = Song("Title", "Artist", 180)
        playlist.add_song(song)
        repr_str = repr(playlist)
        assert "My Playlist" in repr_str
        assert "Title" in repr_str
