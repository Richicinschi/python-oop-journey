"""Tests for Problem 04: Facade Media System."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day02.problem_04_facade_media_system import (
    MediaFormat,
    VideoDecoder,
    AudioDecoder,
    VideoRenderer,
    AudioRenderer,
    MediaFileParser,
    MediaPlayerFacade,
    get_codec_for_format,
)


class TestMediaFormat:
    """Tests for the MediaFormat enum."""
    
    def test_format_values(self) -> None:
        assert MediaFormat.MP4 is not None
        assert MediaFormat.AVI is not None
        assert MediaFormat.MKV is not None
        assert MediaFormat.MP3 is not None
        assert MediaFormat.UNKNOWN is not None


class TestVideoDecoder:
    """Tests for the VideoDecoder subsystem."""
    
    def test_init_not_initialized(self) -> None:
        decoder = VideoDecoder()
        assert decoder.is_initialized is False
    
    def test_initialize(self) -> None:
        decoder = VideoDecoder()
        decoder.initialize("h264")
        assert decoder.is_initialized is True
        assert decoder._codec == "h264"
    
    def test_decode_frame_when_initialized(self) -> None:
        decoder = VideoDecoder()
        decoder.initialize("h264")
        result = decoder.decode_frame(b"frame_data")
        assert "width" in result
        assert "height" in result
    
    def test_decode_frame_when_not_initialized(self) -> None:
        decoder = VideoDecoder()
        with pytest.raises(RuntimeError):
            decoder.decode_frame(b"frame_data")


class TestAudioDecoder:
    """Tests for the AudioDecoder subsystem."""
    
    def test_init(self) -> None:
        decoder = AudioDecoder()
        assert decoder.sample_rate == 0
    
    def test_initialize(self) -> None:
        decoder = AudioDecoder()
        decoder.initialize("aac", 48000, 2)
        assert decoder.sample_rate == 48000
        assert decoder._channels == 2
    
    def test_decode_samples(self) -> None:
        decoder = AudioDecoder()
        decoder.initialize("aac", 48000, 2)
        result = decoder.decode_samples(b"audio_data")
        assert "samples" in result
        assert "duration_ms" in result


class TestVideoRenderer:
    """Tests for the VideoRenderer subsystem."""
    
    def test_init(self) -> None:
        renderer = VideoRenderer()
        assert renderer.frame_count == 0
    
    def test_set_resolution(self) -> None:
        renderer = VideoRenderer()
        renderer.set_resolution(1920, 1080)
        assert renderer._width == 1920
        assert renderer._height == 1080
    
    def test_render_frame_increments_count(self) -> None:
        renderer = VideoRenderer()
        renderer.render_frame({"data": b"frame"})
        assert renderer.frame_count == 1
        renderer.render_frame({"data": b"frame2"})
        assert renderer.frame_count == 2
    
    def test_render_frame_returns_message(self) -> None:
        renderer = VideoRenderer()
        renderer.set_resolution(1920, 1080)
        result = renderer.render_frame({"data": b"frame"})
        assert "Rendered frame 1" in result
        assert "1920x1080" in result


class TestAudioRenderer:
    """Tests for the AudioRenderer subsystem."""
    
    def test_init(self) -> None:
        renderer = AudioRenderer()
        assert renderer.volume == 1.0
    
    def test_set_volume(self) -> None:
        renderer = AudioRenderer()
        renderer.set_volume(0.5)
        assert renderer.volume == 0.5
    
    def test_set_volume_clamps_high(self) -> None:
        renderer = AudioRenderer()
        renderer.set_volume(2.0)
        assert renderer.volume == 1.0
    
    def test_set_volume_clamps_low(self) -> None:
        renderer = AudioRenderer()
        renderer.set_volume(-0.5)
        assert renderer.volume == 0.0
    
    def test_mute(self) -> None:
        renderer = AudioRenderer()
        renderer.mute()
        result = renderer.play_samples({"samples": b"audio"})
        assert "Muted" in result
    
    def test_unmute(self) -> None:
        renderer = AudioRenderer()
        renderer.mute()
        renderer.unmute()
        result = renderer.play_samples({"samples": b"audio"})
        assert "Muted" not in result


class TestMediaFileParser:
    """Tests for the MediaFileParser subsystem."""
    
    @pytest.mark.parametrize("filename,expected", [
        ("video.mp4", MediaFormat.MP4),
        ("video.MP4", MediaFormat.MP4),
        ("movie.avi", MediaFormat.AVI),
        ("movie.mkv", MediaFormat.MKV),
        ("song.mp3", MediaFormat.MP3),
        ("audio.wav", MediaFormat.WAV),
        ("music.flac", MediaFormat.FLAC),
        ("unknown.xyz", MediaFormat.UNKNOWN),
    ])
    def test_detect_format(self, filename: str, expected: MediaFormat) -> None:
        assert MediaFileParser.detect_format(filename) == expected
    
    def test_parse_metadata(self) -> None:
        metadata = MediaFileParser.parse_metadata("test.mp4")
        assert "duration" in metadata
        assert "video_codec" in metadata
        assert "audio_codec" in metadata


class TestMediaPlayerFacade:
    """Tests for the facade class."""
    
    def test_init(self) -> None:
        player = MediaPlayerFacade()
        assert player.current_file is None
        assert player.is_playing is False
    
    def test_load_media_success(self) -> None:
        player = MediaPlayerFacade()
        result = player.load_media("movie.mp4")
        
        assert result["success"] is True
        assert result["format"] == "MP4"
        assert "Loaded" in result["message"]
        assert player.current_file == "movie.mp4"
    
    def test_load_media_unknown_format(self) -> None:
        player = MediaPlayerFacade()
        result = player.load_media("file.xyz")
        
        assert result["success"] is False
        assert result["format"] == "UNKNOWN"
    
    def test_play_when_loaded(self) -> None:
        player = MediaPlayerFacade()
        player.load_media("movie.mp4")
        result = player.play()
        
        assert result["success"] is True
        assert player.is_playing is True
    
    def test_play_when_not_loaded(self) -> None:
        player = MediaPlayerFacade()
        result = player.play()
        
        assert result["success"] is False
        assert "No media loaded" in result["message"]
    
    def test_pause_when_playing(self) -> None:
        player = MediaPlayerFacade()
        player.load_media("movie.mp4")
        player.play()
        result = player.pause()
        
        assert result["success"] is True
        assert player.is_playing is False
    
    def test_pause_when_not_playing(self) -> None:
        player = MediaPlayerFacade()
        player.load_media("movie.mp4")
        result = player.pause()
        
        assert result["success"] is False
    
    def test_stop(self) -> None:
        player = MediaPlayerFacade()
        player.load_media("movie.mp4")
        player.play()
        result = player.stop()
        
        assert result["success"] is True
        assert player.is_playing is False
    
    def test_set_volume(self) -> None:
        player = MediaPlayerFacade()
        result = player.set_volume(0.5)
        
        assert result["success"] is True
        assert result["volume"] == 0.5
    
    def test_mute(self) -> None:
        player = MediaPlayerFacade()
        result = player.mute()
        
        assert result["success"] is True
        assert result["muted"] is True
    
    def test_unmute(self) -> None:
        player = MediaPlayerFacade()
        player.mute()
        result = player.unmute()
        
        assert result["success"] is True
        assert result["muted"] is False


class TestGetCodecForFormat:
    """Tests for the helper function."""
    
    def test_mp4_codecs(self) -> None:
        video, audio = get_codec_for_format(MediaFormat.MP4)
        assert video == "h264"
        assert audio == "aac"
    
    def test_mp3_codecs(self) -> None:
        video, audio = get_codec_for_format(MediaFormat.MP3)
        assert video == ""
        assert audio == "mp3"
    
    def test_unknown_format(self) -> None:
        video, audio = get_codec_for_format(MediaFormat.UNKNOWN)
        assert video == ""
        assert audio == ""


class TestFacadeSimplicity:
    """Tests demonstrating the facade simplifies the subsystem."""
    
    def test_simple_api_vs_complex_subsystem(self) -> None:
        """Facade provides simple API while hiding complex initialization."""
        player = MediaPlayerFacade()
        
        # Simple API - one call to load
        result = player.load_media("video.mp4")
        assert result["success"] is True
        
        # Without facade, we would need:
        # - Detect format
        # - Parse metadata
        # - Initialize video decoder
        # - Initialize audio decoder
        # - Set up renderers
        # All done automatically by facade
    
    def test_playback_workflow(self) -> None:
        """Common workflow is simple with facade."""
        player = MediaPlayerFacade()
        
        # Typical user workflow
        player.load_media("movie.mp4")
        player.set_volume(0.8)
        player.play()
        player.pause()
        player.stop()
        
        # All operations succeed through simple interface
        assert player.current_file == "movie.mp4"
