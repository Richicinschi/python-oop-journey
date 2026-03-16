"""Reference solution for Problem 05: Proxy Image Loader."""

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
    """Subject interface - common interface for RealImage and ImageProxy."""
    
    @property
    @abstractmethod
    def filename(self) -> str:
        """Return the image filename."""
        pass
    
    @property
    @abstractmethod
    def status(self) -> LoadingStatus:
        """Return the loading status."""
        pass
    
    @abstractmethod
    def display(self) -> str:
        """Display the image."""
        pass
    
    @abstractmethod
    def get_dimensions(self) -> tuple[int, int]:
        """Get image dimensions (width, height)."""
        pass
    
    @abstractmethod
    def get_file_size(self) -> int:
        """Get file size in KB."""
        pass


class RealImage(Image):
    """Real subject - the actual image that is expensive to load."""
    
    def __init__(self, filename: str, width: int, height: int, file_size_kb: int) -> None:
        self._filename = filename
        self._width = width
        self._height = height
        self._file_size_kb = file_size_kb
        self._pixel_data: str = ""
        self._load_from_disk()
    
    def _load_from_disk(self) -> None:
        """Simulate expensive loading operation."""
        # Simulate loading large pixel data
        self._pixel_data = f"<PixelData:{self._width}x{self._height}>"
    
    @property
    def filename(self) -> str:
        """Return the filename."""
        return self._filename
    
    @property
    def status(self) -> LoadingStatus:
        """Return the loading status."""
        return LoadingStatus.LOADED
    
    @property
    def pixel_data(self) -> str:
        """Return the loaded pixel data representation."""
        return self._pixel_data
    
    def display(self) -> str:
        """Display the loaded image."""
        return f"Displaying {self._filename}: {self._pixel_data}"
    
    def get_dimensions(self) -> tuple[int, int]:
        """Return image dimensions."""
        return (self._width, self._height)
    
    def get_file_size(self) -> int:
        """Return file size in KB."""
        return self._file_size_kb


class ImageProxy(Image):
    """Proxy - controls access to RealImage with lazy loading."""
    
    def __init__(self, filename: str, width: int, height: int, file_size_kb: int) -> None:
        # Store metadata only - don't load actual image yet
        self._metadata = ImageMetadata(filename, width, height, file_size_kb)
        self._real_image: RealImage | None = None
    
    def _ensure_loaded(self) -> None:
        """Create RealImage if not already loaded."""
        if self._real_image is None:
            self._real_image = RealImage(
                self._metadata.filename,
                self._metadata.width,
                self._metadata.height,
                self._metadata.file_size_kb
            )
    
    @property
    def filename(self) -> str:
        """Return the filename from cached metadata."""
        return self._metadata.filename
    
    @property
    def status(self) -> LoadingStatus:
        """Return current loading status."""
        if self._real_image is None:
            return LoadingStatus.NOT_LOADED
        return LoadingStatus.LOADED
    
    @property
    def real_image(self) -> RealImage | None:
        """Return the real image if loaded, None otherwise."""
        return self._real_image
    
    def display(self) -> str:
        """Display the image, loading it first if necessary."""
        self._ensure_loaded()
        assert self._real_image is not None
        return self._real_image.display()
    
    def get_dimensions(self) -> tuple[int, int]:
        """Return dimensions from cached metadata (no loading needed)."""
        return (self._metadata.width, self._metadata.height)
    
    def get_file_size(self) -> int:
        """Return file size from cached metadata (no loading needed)."""
        return self._metadata.file_size_kb


class ImageGallery:
    """Client class that works with Image interface."""
    
    def __init__(self) -> None:
        self._images: list[Image] = []
    
    def add_image(self, image: Image) -> None:
        """Add an image to the gallery."""
        self._images.append(image)
    
    def display_all(self) -> list[str]:
        """Display all images in the gallery."""
        return [img.display() for img in self._images]
    
    def get_total_size(self) -> int:
        """Get total file size of all images in KB."""
        return sum(img.get_file_size() for img in self._images)
    
    def get_loaded_count(self) -> int:
        """Count how many images have been loaded into memory."""
        return sum(1 for img in self._images if img.status == LoadingStatus.LOADED)
    
    def display_thumbnail_list(self) -> list[str]:
        """Generate a list view without loading full images."""
        results = []
        for img in self._images:
            width, height = img.get_dimensions()
            size = img.get_file_size()
            results.append(f"{img.filename}: {width}x{height}, {size}KB")
        return results


def create_image_proxy(filename: str, metadata_source: dict) -> ImageProxy:
    """Factory function to create an ImageProxy from metadata."""
    return ImageProxy(
        filename=filename,
        width=metadata_source["width"],
        height=metadata_source["height"],
        file_size_kb=metadata_source["size_kb"]
    )


class CachingImageProxy(Image):
    """Advanced proxy with result caching."""
    
    def __init__(self, filename: str, width: int, height: int, file_size_kb: int) -> None:
        self._proxy = ImageProxy(filename, width, height, file_size_kb)
        self._cached_display: str | None = None
        self._cache_hits: int = 0
    
    def display(self) -> str:
        """Display with result caching."""
        if self._cached_display is not None:
            self._cache_hits += 1
            return self._cached_display
        
        result = self._proxy.display()
        self._cached_display = result
        return result
    
    def clear_cache(self) -> None:
        """Clear the display cache."""
        self._cached_display = None
    
    @property
    def cache_hits(self) -> int:
        """Return number of times cached result was used."""
        return self._cache_hits
    
    @property
    def filename(self) -> str:
        """Return filename."""
        return self._proxy.filename
    
    @property
    def status(self) -> LoadingStatus:
        """Return status."""
        return self._proxy.status
    
    def get_dimensions(self) -> tuple[int, int]:
        """Return dimensions."""
        return self._proxy.get_dimensions()
    
    def get_file_size(self) -> int:
        """Return file size."""
        return self._proxy.get_file_size()
