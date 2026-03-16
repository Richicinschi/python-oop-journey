"""Problem 04: Media Player Hierarchy

Topic: Extending behavior with super() and method overriding
Difficulty: Medium

Create a media player hierarchy where child classes extend parent behavior
for different media types while maintaining common functionality.

Classes to implement:
- MediaPlayer: Base with play(), pause(), stop(), volume controls
- AudioPlayer: Adds audio format support, equalizer settings
- VideoPlayer: Adds resolution, fullscreen support, subtitles
- StreamingPlayer: Adds buffering, quality selection, network status

Example:
    >>> player = MediaPlayer("My Song")
    >>> player.play()
    'Playing: My Song [Volume: 50%]'
    >>> player.set_volume(75)
    >>> player.get_status()
    {'state': 'playing', 'volume': 75, 'media': 'My Song'}
    
    >>> audio = AudioPlayer("Song.mp3", "MP3")
    >>> audio.play()
    'Playing MP3: Song.mp3 [Volume: 50%, EQ: Normal]'
    >>> audio.set_equalizer("Rock")
    >>> audio.play()
    'Playing MP3: Song.mp3 [Volume: 50%, EQ: Rock]'

Requirements:
    - MediaPlayer: media_name, state (stopped/playing/paused), volume (0-100)
    - AudioPlayer: audio_format (MP3, FLAC, etc.), equalizer_preset
    - VideoPlayer: resolution (1080p, 4K, etc.), fullscreen (bool)
    - StreamingPlayer: quality (auto/720p/1080p/4K), buffer_percent
    - play() should be overridden in children to add format-specific info
    - get_status() should extend parent's dict in children
    - Use super() for shared state and behavior
"""

from __future__ import annotations


class MediaPlayer:
    """Base media player class."""

    MAX_VOLUME = 100
    MIN_VOLUME = 0
    DEFAULT_VOLUME = 50

    def __init__(self, media_name: str) -> None:
        """Initialize media player.
        
        Args:
            media_name: Name of the media file/stream
        """
        raise NotImplementedError("Initialize media_name, state='stopped', volume")

    def play(self) -> str:
        """Start or resume playback.
        
        Returns:
            Status message with media name and volume
        """
        raise NotImplementedError("Set state to 'playing' and return status")

    def pause(self) -> str:
        """Pause playback.
        
        Returns:
            Status message
        """
        raise NotImplementedError("Set state to 'paused' and return status")

    def stop(self) -> str:
        """Stop playback.
        
        Returns:
            Status message
        """
        raise NotImplementedError("Set state to 'stopped' and return status")

    def set_volume(self, volume: int) -> int:
        """Set volume level.
        
        Args:
            volume: Volume level 0-100
            
        Returns:
            Actual volume set (clamped to valid range)
        """
        raise NotImplementedError("Clamp volume and set")

    def get_volume(self) -> int:
        """Get current volume."""
        raise NotImplementedError("Return current volume")

    def get_status(self) -> dict[str, object]:
        """Return player status as dictionary.
        
        Returns: state, volume, media_name
        """
        raise NotImplementedError("Return status dict")


class AudioPlayer(MediaPlayer):
    """Audio player with format support and equalizer."""

    SUPPORTED_FORMATS = ("MP3", "FLAC", "WAV", "AAC", "OGG")
    EQ_PRESETS = ("Normal", "Rock", "Pop", "Jazz", "Classical", "Bass")

    def __init__(self, media_name: str, audio_format: str) -> None:
        """Initialize audio player.
        
        Args:
            media_name: Audio file name
            audio_format: Audio format (must be in SUPPORTED_FORMATS)
            
        Raises:
            ValueError: If format not supported
        """
        raise NotImplementedError("Use super().__init__() and add format/EQ")

    def play(self) -> str:
        """Play audio with format and EQ info.
        
        Format: 'Playing {format}: {media} [Volume: X%, EQ: {preset}]'
        """
        raise NotImplementedError("Override using super().play()")

    def set_equalizer(self, preset: str) -> str:
        """Set equalizer preset.
        
        Args:
            preset: Equalizer preset name
            
        Returns:
            Actual preset set (defaults to 'Normal' if invalid)
        """
        raise NotImplementedError("Validate and set EQ preset")

    def get_equalizer(self) -> str:
        """Get current equalizer preset."""
        raise NotImplementedError("Return EQ preset")

    def get_status(self) -> dict[str, object]:
        """Return audio player status.
        
        Extends parent with: format, equalizer, player_type='audio'
        """
        raise NotImplementedError("Extend with super()")


class VideoPlayer(MediaPlayer):
    """Video player with resolution and display controls."""

    SUPPORTED_RESOLUTIONS = ("720p", "1080p", "1440p", "4K", "8K")

    def __init__(self, media_name: str, resolution: str) -> None:
        """Initialize video player.
        
        Args:
            media_name: Video file name
            resolution: Video resolution (must be in SUPPORTED_RESOLUTIONS)
            
        Raises:
            ValueError: If resolution not supported
        """
        raise NotImplementedError("Use super().__init__() and add resolution")

    def play(self) -> str:
        """Play video with resolution info.
        
        Format: 'Playing {resolution} video: {media} [Volume: X%]'
        """
        raise NotImplementedError("Override using super().play()")

    def toggle_fullscreen(self) -> bool:
        """Toggle fullscreen mode.
        
        Returns:
            New fullscreen state
        """
        raise NotImplementedError("Toggle and return fullscreen state")

    def is_fullscreen(self) -> bool:
        """Check if in fullscreen mode."""
        raise NotImplementedError("Return fullscreen state")

    def get_status(self) -> dict[str, object]:
        """Return video player status.
        
        Extends parent with: resolution, fullscreen, player_type='video'
        """
        raise NotImplementedError("Extend with super()")


class StreamingPlayer(MediaPlayer):
    """Streaming player with quality and buffering controls."""

    QUALITY_OPTIONS = ("auto", "144p", "240p", "360p", "480p", "720p", "1080p", "4K")

    def __init__(self, media_name: str, quality: str = "auto") -> None:
        """Initialize streaming player.
        
        Args:
            media_name: Stream name/URL
            quality: Stream quality (must be in QUALITY_OPTIONS)
            
        Raises:
            ValueError: If quality not valid
        """
        raise NotImplementedError("Use super().__init__() and add quality/buffer")

    def play(self) -> str:
        """Play stream with quality info.
        
        Format: 'Streaming [{quality}]: {media} [Buffer: X%, Volume: Y%]'
        """
        raise NotImplementedError("Override using super().play()")

    def set_quality(self, quality: str) -> str:
        """Set streaming quality.
        
        Args:
            quality: Quality level
            
        Returns:
            Actual quality set
        """
        raise NotImplementedError("Validate and set quality")

    def update_buffer(self, percent: int) -> int:
        """Update buffer percentage.
        
        Args:
            percent: Buffer percentage 0-100
            
        Returns:
            Actual buffer percent (clamped)
        """
        raise NotImplementedError("Clamp and set buffer percent")

    def get_buffer_percent(self) -> int:
        """Get current buffer percentage."""
        raise NotImplementedError("Return buffer percent")

    def get_status(self) -> dict[str, object]:
        """Return streaming player status.
        
        Extends parent with: quality, buffer_percent, player_type='streaming'
        """
        raise NotImplementedError("Extend with super()")
