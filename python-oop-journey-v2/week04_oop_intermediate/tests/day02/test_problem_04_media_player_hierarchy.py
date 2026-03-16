"""Tests for Problem 04: Media Player Hierarchy."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day02.problem_04_media_player_hierarchy import (
    AudioPlayer,
    MediaPlayer,
    StreamingPlayer,
    VideoPlayer,
)


class TestMediaPlayer:
    """Tests for MediaPlayer base class."""

    def test_init_sets_attributes(self) -> None:
        """Test that attributes are set correctly."""
        player = MediaPlayer("My Song")
        assert player.media_name == "My Song"
        assert player.state == "stopped"
        assert player.volume == 50

    def test_default_volume_constant(self) -> None:
        """Test DEFAULT_VOLUME is 50."""
        assert MediaPlayer.DEFAULT_VOLUME == 50

    def test_play_sets_state_and_returns_string(self) -> None:
        """Test play() sets state to playing and returns correct string."""
        player = MediaPlayer("My Song")
        result = player.play()
        assert player.state == "playing"
        assert "My Song" in result
        assert "Volume: 50%" in result

    def test_pause_sets_state(self) -> None:
        """Test pause() sets state to paused."""
        player = MediaPlayer("My Song")
        player.pause()
        assert player.state == "paused"

    def test_stop_sets_state(self) -> None:
        """Test stop() sets state to stopped."""
        player = MediaPlayer("My Song")
        player.play()
        player.stop()
        assert player.state == "stopped"

    def test_set_volume_clamps_to_max(self) -> None:
        """Test set_volume() clamps to MAX_VOLUME."""
        player = MediaPlayer("My Song")
        result = player.set_volume(150)
        assert result == 100
        assert player.volume == 100

    def test_set_volume_clamps_to_min(self) -> None:
        """Test set_volume() clamps to MIN_VOLUME."""
        player = MediaPlayer("My Song")
        result = player.set_volume(-10)
        assert result == 0
        assert player.volume == 0

    def test_get_volume_returns_current(self) -> None:
        """Test get_volume() returns current volume."""
        player = MediaPlayer("My Song")
        player.set_volume(75)
        assert player.get_volume() == 75

    def test_get_status_returns_dict(self) -> None:
        """Test get_status() returns expected dict."""
        player = MediaPlayer("My Song")
        status = player.get_status()
        assert status["media_name"] == "My Song"
        assert status["state"] == "stopped"
        assert status["volume"] == 50


class TestAudioPlayer:
    """Tests for AudioPlayer class."""

    def test_supported_formats_constant(self) -> None:
        """Test SUPPORTED_FORMATS exists."""
        expected = ("MP3", "FLAC", "WAV", "AAC", "OGG")
        assert AudioPlayer.SUPPORTED_FORMATS == expected

    def test_init_validates_format(self) -> None:
        """Test that unsupported format raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported format"):
            AudioPlayer("song.xyz", "XYZ")

    def test_init_uppercases_format(self) -> None:
        """Test that format is uppercased."""
        player = AudioPlayer("song.mp3", "mp3")
        assert player.audio_format == "MP3"

    def test_init_default_eq(self) -> None:
        """Test default equalizer is Normal."""
        player = AudioPlayer("song.mp3", "MP3")
        assert player.equalizer_preset == "Normal"

    def test_play_includes_format_and_eq(self) -> None:
        """Test play() includes format and EQ info."""
        player = AudioPlayer("song.mp3", "MP3")
        result = player.play()
        assert "Playing MP3:" in result
        assert "[EQ: Normal]" in result

    def test_set_equalizer_valid_preset(self) -> None:
        """Test set_equalizer() accepts valid preset."""
        player = AudioPlayer("song.mp3", "MP3")
        result = player.set_equalizer("Rock")
        assert result == "Rock"
        assert player.equalizer_preset == "Rock"

    def test_set_equalizer_invalid_defaults_to_normal(self) -> None:
        """Test set_equalizer() defaults to Normal for invalid preset."""
        player = AudioPlayer("song.mp3", "MP3")
        result = player.set_equalizer("Invalid")
        assert result == "Normal"
        assert player.equalizer_preset == "Normal"

    def test_get_equalizer_returns_current(self) -> None:
        """Test get_equalizer() returns current preset."""
        player = AudioPlayer("song.mp3", "MP3")
        player.set_equalizer("Jazz")
        assert player.get_equalizer() == "Jazz"

    def test_get_status_extends_parent(self) -> None:
        """Test get_status() extends parent's dict."""
        player = AudioPlayer("song.mp3", "MP3")
        status = player.get_status()
        assert status["format"] == "MP3"
        assert status["equalizer"] == "Normal"
        assert status["player_type"] == "audio"

    def test_inheritance_from_media_player(self) -> None:
        """Test that AudioPlayer inherits from MediaPlayer."""
        assert issubclass(AudioPlayer, MediaPlayer)


class TestVideoPlayer:
    """Tests for VideoPlayer class."""

    def test_supported_resolutions_constant(self) -> None:
        """Test SUPPORTED_RESOLUTIONS exists."""
        expected = ("720p", "1080p", "1440p", "4K", "8K")
        assert VideoPlayer.SUPPORTED_RESOLUTIONS == expected

    def test_init_validates_resolution(self) -> None:
        """Test that unsupported resolution raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported resolution"):
            VideoPlayer("movie.mp4", "480p")

    def test_init_default_fullscreen_false(self) -> None:
        """Test default fullscreen is False."""
        player = VideoPlayer("movie.mp4", "1080p")
        assert player.fullscreen is False

    def test_play_includes_resolution(self) -> None:
        """Test play() includes resolution info."""
        player = VideoPlayer("movie.mp4", "1080p")
        result = player.play()
        assert "Playing 1080p video:" in result

    def test_toggle_fullscreen_toggles_state(self) -> None:
        """Test toggle_fullscreen() toggles state."""
        player = VideoPlayer("movie.mp4", "1080p")
        result = player.toggle_fullscreen()
        assert result is True
        assert player.fullscreen is True
        result = player.toggle_fullscreen()
        assert result is False
        assert player.fullscreen is False

    def test_is_fullscreen_returns_state(self) -> None:
        """Test is_fullscreen() returns current state."""
        player = VideoPlayer("movie.mp4", "1080p")
        assert player.is_fullscreen() is False
        player.toggle_fullscreen()
        assert player.is_fullscreen() is True

    def test_get_status_extends_parent(self) -> None:
        """Test get_status() extends parent's dict."""
        player = VideoPlayer("movie.mp4", "1080p")
        status = player.get_status()
        assert status["resolution"] == "1080p"
        assert status["fullscreen"] is False
        assert status["player_type"] == "video"

    def test_inheritance_from_media_player(self) -> None:
        """Test that VideoPlayer inherits from MediaPlayer."""
        assert issubclass(VideoPlayer, MediaPlayer)


class TestStreamingPlayer:
    """Tests for StreamingPlayer class."""

    def test_quality_options_constant(self) -> None:
        """Test QUALITY_OPTIONS exists."""
        expected = ("auto", "144p", "240p", "360p", "480p", "720p", "1080p", "4K")
        assert StreamingPlayer.QUALITY_OPTIONS == expected

    def test_init_default_quality(self) -> None:
        """Test default quality is 'auto'."""
        player = StreamingPlayer("stream")
        assert player.quality == "auto"

    def test_init_validates_quality(self) -> None:
        """Test that invalid quality raises ValueError."""
        with pytest.raises(ValueError, match="Invalid quality"):
            StreamingPlayer("stream", "8K")

    def test_init_default_buffer_zero(self) -> None:
        """Test default buffer_percent is 0."""
        player = StreamingPlayer("stream")
        assert player.buffer_percent == 0

    def test_play_includes_quality_and_buffer(self) -> None:
        """Test play() includes quality and buffer info."""
        player = StreamingPlayer("stream", "720p")
        result = player.play()
        assert "Streaming [720p]:" in result
        assert "Buffer: 0%" in result

    def test_set_quality_valid_quality(self) -> None:
        """Test set_quality() accepts valid quality."""
        player = StreamingPlayer("stream", "auto")
        result = player.set_quality("1080p")
        assert result == "1080p"
        assert player.quality == "1080p"

    def test_update_buffer_clamps_to_range(self) -> None:
        """Test update_buffer() clamps to 0-100."""
        player = StreamingPlayer("stream")
        assert player.update_buffer(150) == 100
        assert player.update_buffer(-10) == 0
        assert player.update_buffer(50) == 50

    def test_get_buffer_percent_returns_current(self) -> None:
        """Test get_buffer_percent() returns current buffer."""
        player = StreamingPlayer("stream")
        player.update_buffer(75)
        assert player.get_buffer_percent() == 75

    def test_get_status_extends_parent(self) -> None:
        """Test get_status() extends parent's dict."""
        player = StreamingPlayer("stream", "720p")
        player.update_buffer(50)
        status = player.get_status()
        assert status["quality"] == "720p"
        assert status["buffer_percent"] == 50
        assert status["player_type"] == "streaming"

    def test_inheritance_from_media_player(self) -> None:
        """Test that StreamingPlayer inherits from MediaPlayer."""
        assert issubclass(StreamingPlayer, MediaPlayer)
