"""Problem 03: Media Handler Dispatch.

Topic: Polymorphism
Difficulty: Medium

Create media handlers for different types (Audio, Video, Image).
Demonstrate polymorphic handling through a common MediaHandler interface
with duck typing support.

TODO:
1. Create MediaHandler ABC with:
   - play(self) -> str (abstract)
   - get_duration(self) -> float (abstract)
   - get_file_type(self) -> str (abstract)

2. Create AudioHandler class:
   - __init__(self, filename: str, duration: float, bitrate: int)
   - play returns f"Playing audio: {filename}"
   - get_duration returns duration
   - get_file_type returns "Audio"

3. Create VideoHandler class:
   - __init__(self, filename: str, duration: float, resolution: str)
   - play returns f"Playing video: {filename}"
   - get_duration returns duration
   - get_file_type returns "Video"

4. Create ImageHandler class:
   - __init__(self, filename: str, width: int, height: int)
   - play returns f"Displaying image: {filename}"
   - get_duration returns 0.0 (images are static)
   - get_file_type returns "Image"

5. Implement play_all_media(handlers: list) -> list[str]
   that plays all media polymorphically.

6. Implement get_total_duration(handlers: list) -> float
   that sums durations of all media.
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
        raise NotImplementedError("play must be implemented")
    
    @abstractmethod
    def get_duration(self) -> float:
        """Get media duration in seconds.
        
        Returns:
            Duration in seconds (0.0 for static media).
        """
        raise NotImplementedError("get_duration must be implemented")
    
    @abstractmethod
    def get_file_type(self) -> str:
        """Get the file type name.
        
        Returns:
            String name of the media type.
        """
        raise NotImplementedError("get_file_type must be implemented")


class AudioHandler(MediaHandler):
    """Handler for audio files."""
    
    def __init__(self, filename: str, duration: float, bitrate: int) -> None:
        """Initialize audio handler.
        
        Args:
            filename: Name of the audio file.
            duration: Duration in seconds.
            bitrate: Audio bitrate in kbps.
        """
        # TODO: Initialize attributes
        raise NotImplementedError("Initialize audio handler")
    
    def play(self) -> str:
        """Play the audio file."""
        # TODO: Return f"Playing audio: {self.filename}"
        raise NotImplementedError("Implement play")
    
    def get_duration(self) -> float:
        """Return audio duration."""
        # TODO: Return duration
        raise NotImplementedError("Implement get_duration")
    
    def get_file_type(self) -> str:
        """Return file type."""
        # TODO: Return "Audio"
        raise NotImplementedError("Implement get_file_type")


class VideoHandler(MediaHandler):
    """Handler for video files."""
    
    def __init__(self, filename: str, duration: float, resolution: str) -> None:
        """Initialize video handler.
        
        Args:
            filename: Name of the video file.
            duration: Duration in seconds.
            resolution: Video resolution (e.g., '1920x1080').
        """
        # TODO: Initialize attributes
        raise NotImplementedError("Initialize video handler")
    
    def play(self) -> str:
        """Play the video file."""
        # TODO: Return f"Playing video: {self.filename}"
        raise NotImplementedError("Implement play")
    
    def get_duration(self) -> float:
        """Return video duration."""
        # TODO: Return duration
        raise NotImplementedError("Implement get_duration")
    
    def get_file_type(self) -> str:
        """Return file type."""
        # TODO: Return "Video"
        raise NotImplementedError("Implement get_file_type")


class ImageHandler(MediaHandler):
    """Handler for image files."""
    
    def __init__(self, filename: str, width: int, height: int) -> None:
        """Initialize image handler.
        
        Args:
            filename: Name of the image file.
            width: Image width in pixels.
            height: Image height in pixels.
        """
        # TODO: Initialize attributes
        raise NotImplementedError("Initialize image handler")
    
    def play(self) -> str:
        """Display the image file."""
        # TODO: Return f"Displaying image: {self.filename}"
        raise NotImplementedError("Implement play")
    
    def get_duration(self) -> float:
        """Return image duration (always 0.0)."""
        # TODO: Return 0.0
        raise NotImplementedError("Implement get_duration")
    
    def get_file_type(self) -> str:
        """Return file type."""
        # TODO: Return "Image"
        raise NotImplementedError("Implement get_file_type")


def play_all_media(handlers: list[MediaHandler]) -> list[str]:
    """Play all media handlers polymorphically.
    
    Args:
        handlers: List of MediaHandler instances.
    
    Returns:
        List of play result strings.
    """
    # TODO: Iterate through handlers and call play() on each
    raise NotImplementedError("Implement play_all_media")


def get_total_duration(handlers: list[MediaHandler]) -> float:
    """Calculate total duration of all media.
    
    Args:
        handlers: List of MediaHandler instances.
    
    Returns:
        Total duration in seconds.
    """
    # TODO: Sum get_duration() from all handlers
    raise NotImplementedError("Implement get_total_duration")
