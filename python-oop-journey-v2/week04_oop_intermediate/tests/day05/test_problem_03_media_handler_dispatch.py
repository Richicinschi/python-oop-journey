"""Tests for Problem 03: Media Handler Dispatch."""

from __future__ import annotations

import pytest
from abc import ABC

from week04_oop_intermediate.solutions.day05.problem_03_media_handler_dispatch import (
    MediaHandler,
    AudioHandler,
    VideoHandler,
    ImageHandler,
    play_all_media,
    get_total_duration,
)


class TestMediaHandlerABC:
    """Test suite for MediaHandler abstract base class."""
    
    def test_media_handler_is_abstract(self) -> None:
        """Test that MediaHandler cannot be instantiated."""
        assert issubclass(MediaHandler, ABC)
        with pytest.raises(TypeError, match="abstract"):
            MediaHandler()


class TestAudioHandler:
    """Test suite for AudioHandler."""
    
    def test_initialization(self) -> None:
        """Test audio handler initialization."""
        handler = AudioHandler("song.mp3", 180.5, 320)
        assert handler.filename == "song.mp3"
        assert handler.bitrate == 320
    
    def test_play(self) -> None:
        """Test play method."""
        handler = AudioHandler("song.mp3", 180.5, 320)
        result = handler.play()
        assert result == "Playing audio: song.mp3"
    
    def test_get_duration(self) -> None:
        """Test get_duration method."""
        handler = AudioHandler("song.mp3", 180.5, 320)
        assert handler.get_duration() == 180.5
    
    def test_get_file_type(self) -> None:
        """Test get_file_type method."""
        handler = AudioHandler("song.mp3", 180.5, 320)
        assert handler.get_file_type() == "Audio"


class TestVideoHandler:
    """Test suite for VideoHandler."""
    
    def test_initialization(self) -> None:
        """Test video handler initialization."""
        handler = VideoHandler("movie.mp4", 7200.0, "1920x1080")
        assert handler.filename == "movie.mp4"
        assert handler.resolution == "1920x1080"
    
    def test_play(self) -> None:
        """Test play method."""
        handler = VideoHandler("movie.mp4", 7200.0, "1920x1080")
        result = handler.play()
        assert result == "Playing video: movie.mp4"
    
    def test_get_duration(self) -> None:
        """Test get_duration method."""
        handler = VideoHandler("movie.mp4", 7200.0, "1920x1080")
        assert handler.get_duration() == 7200.0
    
    def test_get_file_type(self) -> None:
        """Test get_file_type method."""
        handler = VideoHandler("movie.mp4", 7200.0, "1920x1080")
        assert handler.get_file_type() == "Video"


class TestImageHandler:
    """Test suite for ImageHandler."""
    
    def test_initialization(self) -> None:
        """Test image handler initialization."""
        handler = ImageHandler("photo.jpg", 1920, 1080)
        assert handler.filename == "photo.jpg"
        assert handler.width == 1920
        assert handler.height == 1080
    
    def test_play(self) -> None:
        """Test play method returns display message."""
        handler = ImageHandler("photo.jpg", 1920, 1080)
        result = handler.play()
        assert result == "Displaying image: photo.jpg"
    
    def test_get_duration(self) -> None:
        """Test get_duration returns 0.0 for images."""
        handler = ImageHandler("photo.jpg", 1920, 1080)
        assert handler.get_duration() == 0.0
    
    def test_get_file_type(self) -> None:
        """Test get_file_type method."""
        handler = ImageHandler("photo.jpg", 1920, 1080)
        assert handler.get_file_type() == "Image"


class TestPlayAllMedia:
    """Test suite for play_all_media function."""
    
    def test_empty_list(self) -> None:
        """Test with empty list returns empty list."""
        result = play_all_media([])
        assert result == []
    
    def test_single_handler(self) -> None:
        """Test with single handler."""
        handlers = [AudioHandler("song.mp3", 180.0, 320)]
        result = play_all_media(handlers)
        assert result == ["Playing audio: song.mp3"]
    
    def test_mixed_handlers(self) -> None:
        """Test polymorphic play with mixed handler types."""
        handlers = [
            AudioHandler("song.mp3", 180.0, 320),
            VideoHandler("movie.mp4", 7200.0, "1920x1080"),
            ImageHandler("photo.jpg", 1920, 1080),
        ]
        result = play_all_media(handlers)
        
        assert len(result) == 3
        assert "Playing audio: song.mp3" in result
        assert "Playing video: movie.mp4" in result
        assert "Displaying image: photo.jpg" in result
    
    def test_preserves_order(self) -> None:
        """Test that results are in same order as input."""
        handlers = [
            ImageHandler("photo.jpg", 1920, 1080),
            AudioHandler("song.mp3", 180.0, 320),
        ]
        result = play_all_media(handlers)
        
        assert result[0] == "Displaying image: photo.jpg"
        assert result[1] == "Playing audio: song.mp3"


class TestGetTotalDuration:
    """Test suite for get_total_duration function."""
    
    def test_empty_list(self) -> None:
        """Test with empty list returns 0."""
        result = get_total_duration([])
        assert result == 0.0
    
    def test_audio_only(self) -> None:
        """Test with audio handlers."""
        handlers = [
            AudioHandler("song1.mp3", 180.0, 320),
            AudioHandler("song2.mp3", 200.0, 256),
        ]
        result = get_total_duration(handlers)
        assert result == 380.0
    
    def test_mixed_media(self) -> None:
        """Test with mixed media types."""
        handlers = [
            AudioHandler("song.mp3", 180.0, 320),
            VideoHandler("movie.mp4", 7200.0, "1920x1080"),
            ImageHandler("photo.jpg", 1920, 1080),  # Duration 0
        ]
        result = get_total_duration(handlers)
        assert result == 7380.0  # 180 + 7200 + 0
    
    def test_images_only(self) -> None:
        """Test with only images returns 0."""
        handlers = [
            ImageHandler("photo1.jpg", 1920, 1080),
            ImageHandler("photo2.jpg", 800, 600),
        ]
        result = get_total_duration(handlers)
        assert result == 0.0
