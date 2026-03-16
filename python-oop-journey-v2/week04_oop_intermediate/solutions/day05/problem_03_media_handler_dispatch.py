"""Solution for Problem 03: Media Handler Dispatch.

Demonstrates polymorphic handling of different media types.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class MediaHandler(ABC):
    """Abstract base class for media handlers."""
    
    @abstractmethod
    def play(self) -> str:
        """Play or display the media.
        
        Returns:
            String describing the play action.
        """
        pass
    
    @abstractmethod
    def get_duration(self) -> float:
        """Get media duration in seconds.
        
        Returns:
            Duration in seconds (0.0 for static media).
        """
        pass
    
    @abstractmethod
    def get_file_type(self) -> str:
        """Get the file type name.
        
        Returns:
            String name of the media type.
        """
        pass


class AudioHandler(MediaHandler):
    """Handler for audio files.
    
    Attributes:
        filename: Name of the audio file.
        duration: Duration in seconds.
        bitrate: Audio bitrate in kbps.
    """
    
    def __init__(self, filename: str, duration: float, bitrate: int) -> None:
        """Initialize audio handler.
        
        Args:
            filename: Name of the audio file.
            duration: Duration in seconds.
            bitrate: Audio bitrate in kbps.
        """
        self.filename = filename
        self._duration = duration
        self.bitrate = bitrate
    
    def play(self) -> str:
        """Play the audio file.
        
        Returns:
            String describing the play action.
        """
        return f"Playing audio: {self.filename}"
    
    def get_duration(self) -> float:
        """Return audio duration.
        
        Returns:
            Duration in seconds.
        """
        return self._duration
    
    def get_file_type(self) -> str:
        """Return file type."""
        return "Audio"


class VideoHandler(MediaHandler):
    """Handler for video files.
    
    Attributes:
        filename: Name of the video file.
        duration: Duration in seconds.
        resolution: Video resolution (e.g., '1920x1080').
    """
    
    def __init__(self, filename: str, duration: float, resolution: str) -> None:
        """Initialize video handler.
        
        Args:
            filename: Name of the video file.
            duration: Duration in seconds.
            resolution: Video resolution (e.g., '1920x1080').
        """
        self.filename = filename
        self._duration = duration
        self.resolution = resolution
    
    def play(self) -> str:
        """Play the video file.
        
        Returns:
            String describing the play action.
        """
        return f"Playing video: {self.filename}"
    
    def get_duration(self) -> float:
        """Return video duration.
        
        Returns:
            Duration in seconds.
        """
        return self._duration
    
    def get_file_type(self) -> str:
        """Return file type."""
        return "Video"


class ImageHandler(MediaHandler):
    """Handler for image files.
    
    Attributes:
        filename: Name of the image file.
        width: Image width in pixels.
        height: Image height in pixels.
    """
    
    def __init__(self, filename: str, width: int, height: int) -> None:
        """Initialize image handler.
        
        Args:
            filename: Name of the image file.
            width: Image width in pixels.
            height: Image height in pixels.
        """
        self.filename = filename
        self.width = width
        self.height = height
    
    def play(self) -> str:
        """Display the image file.
        
        Returns:
            String describing the display action.
        """
        return f"Displaying image: {self.filename}"
    
    def get_duration(self) -> float:
        """Return image duration (always 0.0).
        
        Returns:
            0.0 since images are static.
        """
        return 0.0
    
    def get_file_type(self) -> str:
        """Return file type."""
        return "Image"


def play_all_media(handlers: list[MediaHandler]) -> list[str]:
    """Play all media handlers polymorphically.
    
    This function demonstrates polymorphism - it works with any
    MediaHandler subclass without knowing the specific type.
    
    Args:
        handlers: List of MediaHandler instances.
    
    Returns:
        List of play result strings.
    """
    return [handler.play() for handler in handlers]


def get_total_duration(handlers: list[MediaHandler]) -> float:
    """Calculate total duration of all media.
    
    Args:
        handlers: List of MediaHandler instances.
    
    Returns:
        Total duration in seconds.
    """
    return sum(handler.get_duration() for handler in handlers)
