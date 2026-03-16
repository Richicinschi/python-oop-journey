"""Problem 05: Proxy Image Loader

Topic: Proxy Pattern
Difficulty: Medium

Implement a lazy-loading proxy for expensive image loading operations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto


class LoadingStatus(Enum):
    """Status of image loading."""
    NOT_LOADED = auto()
    LOADING = auto()
    LOADED = auto()
    ERROR = auto()


@dataclass
class ImageMetadata:
    """Metadata about an image without loading the actual data."""
    filename: str
    width: int
    height: int
    file_size_kb: int


class Image(ABC):
    """Subject interface - common interface for RealImage and ImageProxy.
    
    Clients use this interface, unaware whether they're working with
    the real image or a proxy.
    """
    
    @property
    @abstractmethod
    def filename(self) -> str:
        """Return the image filename."""
        raise NotImplementedError("Implement filename")
    
    @property
    @abstractmethod
    def status(self) -> LoadingStatus:
        """Return the loading status."""
        raise NotImplementedError("Implement status")
    
    @abstractmethod
    def display(self) -> str:
        """Display the image.
        
        For RealImage: returns the actual image data display.
        For ImageProxy: may trigger lazy loading.
        
        Returns:
            String describing the displayed image
        """
        raise NotImplementedError("Implement display")
    
    @abstractmethod
    def get_dimensions(self) -> tuple[int, int]:
        """Get image dimensions (width, height).
        
        For RealImage: returns actual dimensions.
        For ImageProxy: may use cached metadata.
        
        Returns:
            Tuple of (width, height)
        """
        raise NotImplementedError("Implement get_dimensions")
    
    @abstractmethod
    def get_file_size(self) -> int:
        """Get file size in KB.
        
        Returns:
            File size in kilobytes
        """
        raise NotImplementedError("Implement get_file_size")


class RealImage(Image):
    """Real subject - the actual image that is expensive to load.
    
    This class represents the heavyweight object that the proxy
    delays creating until absolutely necessary.
    """
    
    def __init__(self, filename: str, width: int, height: int, file_size_kb: int) -> None:
        """Initialize and immediately load the image.
        
        Args:
            filename: Path to the image file
            width: Image width in pixels
            height: Image height in pixels
            file_size_kb: File size in kilobytes
        """
        raise NotImplementedError("Implement __init__")
    
    def _load_from_disk(self) -> None:
        """Simulate expensive loading operation.
        
        This would typically involve:
        - Reading large file from disk
        - Decompressing image data
        - Allocating memory for pixel buffer
        """
        raise NotImplementedError("Implement _load_from_disk")
    
    @property
    def filename(self) -> str:
        """Return the filename."""
        raise NotImplementedError("Implement filename")
    
    @property
    def status(self) -> LoadingStatus:
        """Return the loading status."""
        raise NotImplementedError("Implement status")
    
    @property
    def pixel_data(self) -> str:
        """Return the loaded pixel data representation."""
        raise NotImplementedError("Implement pixel_data")
    
    def display(self) -> str:
        """Display the loaded image."""
        raise NotImplementedError("Implement display")
    
    def get_dimensions(self) -> tuple[int, int]:
        """Return image dimensions."""
        raise NotImplementedError("Implement get_dimensions")
    
    def get_file_size(self) -> int:
        """Return file size in KB."""
        raise NotImplementedError("Implement get_file_size")


class ImageProxy(Image):
    """Proxy - controls access to RealImage with lazy loading.
    
    The proxy delays creating the RealImage until display() is called.
    Metadata (dimensions, file size) is cached to avoid loading.
    """
    
    def __init__(self, filename: str, width: int, height: int, file_size_kb: int) -> None:
        """Initialize proxy with metadata only - doesn't load actual image.
        
        Args:
            filename: Path to the image file
            width: Image width in pixels (from metadata)
            height: Image height in pixels (from metadata)
            file_size_kb: File size in kilobytes (from metadata)
        """
        raise NotImplementedError("Implement __init__")
    
    def _ensure_loaded(self) -> None:
        """Create RealImage if not already loaded.
        
        This is the key method that implements lazy loading.
        """
        raise NotImplementedError("Implement _ensure_loaded")
    
    @property
    def filename(self) -> str:
        """Return the filename from cached metadata."""
        raise NotImplementedError("Implement filename")
    
    @property
    def status(self) -> LoadingStatus:
        """Return current loading status."""
        raise NotImplementedError("Implement status")
    
    @property
    def real_image(self) -> RealImage | None:
        """Return the real image if loaded, None otherwise."""
        raise NotImplementedError("Implement real_image")
    
    def display(self) -> str:
        """Display the image, loading it first if necessary."""
        raise NotImplementedError("Implement display")
    
    def get_dimensions(self) -> tuple[int, int]:
        """Return dimensions from cached metadata (no loading needed)."""
        raise NotImplementedError("Implement get_dimensions")
    
    def get_file_size(self) -> int:
        """Return file size from cached metadata (no loading needed)."""
        raise NotImplementedError("Implement get_file_size")


class ImageGallery:
    """Client class that works with Image interface.
    
    Demonstrates how client code works with both RealImage and ImageProxy
    interchangeably through the common Image interface.
    """
    
    def __init__(self) -> None:
        """Initialize empty gallery."""
        raise NotImplementedError("Implement __init__")
    
    def add_image(self, image: Image) -> None:
        """Add an image to the gallery.
        
        Args:
            image: The Image (RealImage or ImageProxy) to add
        """
        raise NotImplementedError("Implement add_image")
    
    def display_all(self) -> list[str]:
        """Display all images in the gallery.
        
        Returns:
            List of display results for each image
        """
        raise NotImplementedError("Implement display_all")
    
    def get_total_size(self) -> int:
        """Get total file size of all images in KB.
        
        Returns:
            Total size in kilobytes
        """
        raise NotImplementedError("Implement get_total_size")
    
    def get_loaded_count(self) -> int:
        """Count how many images have been loaded into memory.
        
        Returns:
            Number of images with status LOADED
        """
        raise NotImplementedError("Implement get_loaded_count")
    
    def display_thumbnail_list(self) -> list[str]:
        """Generate a list view without loading full images.
        
        Uses metadata only to show image information.
        
        Returns:
            List of formatted strings showing image info
        """
        raise NotImplementedError("Implement display_thumbnail_list")


def create_image_proxy(filename: str, metadata_source: dict) -> ImageProxy:
    """Factory function to create an ImageProxy from metadata.
    
    Args:
        filename: The image filename
        metadata_source: Dict with 'width', 'height', 'size_kb'
        
    Returns:
        Configured ImageProxy instance
    """
    raise NotImplementedError("Implement create_image_proxy")


class CachingImageProxy(Image):
    """Advanced proxy with result caching.
    
    Extends the basic proxy pattern with caching of display results
    to avoid re-processing the same image data.
    """
    
    def __init__(self, filename: str, width: int, height: int, file_size_kb: int) -> None:
        """Initialize caching proxy."""
        raise NotImplementedError("Implement __init__")
    
    def display(self) -> str:
        """Display with result caching."""
        raise NotImplementedError("Implement display")
    
    def clear_cache(self) -> None:
        """Clear the display cache."""
        raise NotImplementedError("Implement clear_cache")
    
    @property
    def cache_hits(self) -> int:
        """Return number of times cached result was used."""
        raise NotImplementedError("Implement cache_hits")
    
    @property
    def filename(self) -> str:
        """Return filename."""
        raise NotImplementedError("Implement filename")
    
    @property
    def status(self) -> LoadingStatus:
        """Return status."""
        raise NotImplementedError("Implement status")
    
    def get_dimensions(self) -> tuple[int, int]:
        """Return dimensions."""
        raise NotImplementedError("Implement get_dimensions")
    
    def get_file_size(self) -> int:
        """Return file size."""
        raise NotImplementedError("Implement get_file_size")
