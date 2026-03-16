"""Reference solution for Problem 04: Media Player Hierarchy."""

from __future__ import annotations


class MediaPlayer:
    """Base media player class."""

    MAX_VOLUME = 100
    MIN_VOLUME = 0
    DEFAULT_VOLUME = 50

    def __init__(self, media_name: str) -> None:
        """Initialize media player."""
        self.media_name = media_name
        self.state = "stopped"
        self.volume = self.DEFAULT_VOLUME

    def play(self) -> str:
        """Start or resume playback."""
        self.state = "playing"
        return f"Playing: {self.media_name} [Volume: {self.volume}%]"

    def pause(self) -> str:
        """Pause playback."""
        self.state = "paused"
        return f"Paused: {self.media_name}"

    def stop(self) -> str:
        """Stop playback."""
        self.state = "stopped"
        return f"Stopped: {self.media_name}"

    def set_volume(self, volume: int) -> int:
        """Set volume level."""
        self.volume = max(self.MIN_VOLUME, min(self.MAX_VOLUME, volume))
        return self.volume

    def get_volume(self) -> int:
        """Get current volume."""
        return self.volume

    def get_status(self) -> dict[str, object]:
        """Return player status as dictionary."""
        return {
            "state": self.state,
            "volume": self.volume,
            "media_name": self.media_name,
        }


class AudioPlayer(MediaPlayer):
    """Audio player with format support and equalizer."""

    SUPPORTED_FORMATS = ("MP3", "FLAC", "WAV", "AAC", "OGG")
    EQ_PRESETS = ("Normal", "Rock", "Pop", "Jazz", "Classical", "Bass")

    def __init__(self, media_name: str, audio_format: str) -> None:
        """Initialize audio player."""
        audio_upper = audio_format.upper()
        if audio_upper not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {audio_format}")
        super().__init__(media_name)
        self.audio_format = audio_upper
        self.equalizer_preset = "Normal"

    def play(self) -> str:
        """Play audio with format and EQ info."""
        base = super().play()
        base_part = base.replace("Playing:", f"Playing {self.audio_format}:")
        return f"{base_part} [EQ: {self.equalizer_preset}]"

    def set_equalizer(self, preset: str) -> str:
        """Set equalizer preset."""
        if preset in self.EQ_PRESETS:
            self.equalizer_preset = preset
        else:
            self.equalizer_preset = "Normal"
        return self.equalizer_preset

    def get_equalizer(self) -> str:
        """Get current equalizer preset."""
        return self.equalizer_preset

    def get_status(self) -> dict[str, object]:
        """Return audio player status."""
        details = super().get_status()
        details.update({
            "format": self.audio_format,
            "equalizer": self.equalizer_preset,
            "player_type": "audio",
        })
        return details


class VideoPlayer(MediaPlayer):
    """Video player with resolution and display controls."""

    SUPPORTED_RESOLUTIONS = ("720p", "1080p", "1440p", "4K", "8K")

    def __init__(self, media_name: str, resolution: str) -> None:
        """Initialize video player."""
        if resolution not in self.SUPPORTED_RESOLUTIONS:
            raise ValueError(f"Unsupported resolution: {resolution}")
        super().__init__(media_name)
        self.resolution = resolution
        self.fullscreen = False

    def play(self) -> str:
        """Play video with resolution info."""
        base = super().play()
        return base.replace("Playing:", f"Playing {self.resolution} video:")

    def toggle_fullscreen(self) -> bool:
        """Toggle fullscreen mode."""
        self.fullscreen = not self.fullscreen
        return self.fullscreen

    def is_fullscreen(self) -> bool:
        """Check if in fullscreen mode."""
        return self.fullscreen

    def get_status(self) -> dict[str, object]:
        """Return video player status."""
        details = super().get_status()
        details.update({
            "resolution": self.resolution,
            "fullscreen": self.fullscreen,
            "player_type": "video",
        })
        return details


class StreamingPlayer(MediaPlayer):
    """Streaming player with quality and buffering controls."""

    QUALITY_OPTIONS = ("auto", "144p", "240p", "360p", "480p", "720p", "1080p", "4K")

    def __init__(self, media_name: str, quality: str = "auto") -> None:
        """Initialize streaming player."""
        if quality not in self.QUALITY_OPTIONS:
            raise ValueError(f"Invalid quality: {quality}")
        super().__init__(media_name)
        self.quality = quality
        self.buffer_percent = 0

    def play(self) -> str:
        """Play stream with quality info."""
        base = super().play()
        # Extract the media name and volume part
        parts = base.split(" [Volume: ")
        media_part = parts[0].replace("Playing:", "").strip()
        volume_part = parts[1].replace("]", "") if len(parts) > 1 else "50"
        return f"Streaming [{self.quality}]: {media_part} [Buffer: {self.buffer_percent}%, Volume: {volume_part}%]"

    def set_quality(self, quality: str) -> str:
        """Set streaming quality."""
        if quality in self.QUALITY_OPTIONS:
            self.quality = quality
        return self.quality

    def update_buffer(self, percent: int) -> int:
        """Update buffer percentage."""
        self.buffer_percent = max(0, min(100, percent))
        return self.buffer_percent

    def get_buffer_percent(self) -> int:
        """Get current buffer percentage."""
        return self.buffer_percent

    def get_status(self) -> dict[str, object]:
        """Return streaming player status."""
        details = super().get_status()
        details.update({
            "quality": self.quality,
            "buffer_percent": self.buffer_percent,
            "player_type": "streaming",
        })
        return details
