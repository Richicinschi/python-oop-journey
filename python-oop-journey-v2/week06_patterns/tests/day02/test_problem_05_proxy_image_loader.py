"""Tests for Problem 05: Proxy Image Loader."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day02.problem_05_proxy_image_loader import (
    LoadingStatus,
    ImageMetadata,
    Image,
    RealImage,
    ImageProxy,
    ImageGallery,
    create_image_proxy,
    CachingImageProxy,
)


class TestLoadingStatus:
    """Tests for the LoadingStatus enum."""
    
    def test_status_values(self) -> None:
        assert LoadingStatus.NOT_LOADED is not None
        assert LoadingStatus.LOADING is not None
        assert LoadingStatus.LOADED is not None
        assert LoadingStatus.ERROR is not None


class TestImageMetadata:
    """Tests for the ImageMetadata dataclass."""
    
    def test_creation(self) -> None:
        meta = ImageMetadata("photo.jpg", 1920, 1080, 2048)
        assert meta.filename == "photo.jpg"
        assert meta.width == 1920
        assert meta.height == 1080
        assert meta.file_size_kb == 2048


class TestRealImage:
    """Tests for the RealImage (real subject)."""
    
    def test_init_loads_immediately(self) -> None:
        img = RealImage("photo.jpg", 1920, 1080, 2048)
        # RealImage loads immediately on creation
        assert img.pixel_data != ""
        assert img.status == LoadingStatus.LOADED
    
    def test_filename(self) -> None:
        img = RealImage("photo.jpg", 1920, 1080, 2048)
        assert img.filename == "photo.jpg"
    
    def test_display(self) -> None:
        img = RealImage("photo.jpg", 1920, 1080, 2048)
        result = img.display()
        assert "Displaying photo.jpg" in result
        assert "1920x1080" in result
    
    def test_get_dimensions(self) -> None:
        img = RealImage("photo.jpg", 1920, 1080, 2048)
        assert img.get_dimensions() == (1920, 1080)
    
    def test_get_file_size(self) -> None:
        img = RealImage("photo.jpg", 1920, 1080, 2048)
        assert img.get_file_size() == 2048


class TestImageProxy:
    """Tests for the ImageProxy (proxy class)."""
    
    def test_init_does_not_load(self) -> None:
        proxy = ImageProxy("photo.jpg", 1920, 1080, 2048)
        assert proxy.status == LoadingStatus.NOT_LOADED
        assert proxy.real_image is None
    
    def test_filename_no_loading(self) -> None:
        proxy = ImageProxy("photo.jpg", 1920, 1080, 2048)
        assert proxy.filename == "photo.jpg"
        assert proxy.status == LoadingStatus.NOT_LOADED
    
    def test_get_dimensions_no_loading(self) -> None:
        proxy = ImageProxy("photo.jpg", 1920, 1080, 2048)
        assert proxy.get_dimensions() == (1920, 1080)
        assert proxy.status == LoadingStatus.NOT_LOADED
    
    def test_get_file_size_no_loading(self) -> None:
        proxy = ImageProxy("photo.jpg", 1920, 1080, 2048)
        assert proxy.get_file_size() == 2048
        assert proxy.status == LoadingStatus.NOT_LOADED
    
    def test_display_triggers_loading(self) -> None:
        proxy = ImageProxy("photo.jpg", 1920, 1080, 2048)
        assert proxy.status == LoadingStatus.NOT_LOADED
        
        result = proxy.display()
        
        assert proxy.status == LoadingStatus.LOADED
        assert proxy.real_image is not None
        assert "Displaying photo.jpg" in result
    
    def test_display_after_loading_uses_cached(self) -> None:
        proxy = ImageProxy("photo.jpg", 1920, 1080, 2048)
        proxy.display()  # First call triggers loading
        
        real_img = proxy.real_image
        result = proxy.display()  # Second call uses cached RealImage
        
        assert proxy.real_image is real_img  # Same instance
        assert "Displaying photo.jpg" in result


class TestImageGallery:
    """Tests for the ImageGallery client class."""
    
    def test_init(self) -> None:
        gallery = ImageGallery()
        assert gallery.get_total_size() == 0
    
    def test_add_image(self) -> None:
        gallery = ImageGallery()
        gallery.add_image(ImageProxy("a.jpg", 100, 100, 50))
        gallery.add_image(ImageProxy("b.jpg", 200, 200, 100))
        assert gallery.get_total_size() == 150
    
    def test_display_all_triggers_loading(self) -> None:
        gallery = ImageGallery()
        gallery.add_image(ImageProxy("a.jpg", 100, 100, 50))
        gallery.add_image(ImageProxy("b.jpg", 200, 200, 100))
        
        assert gallery.get_loaded_count() == 0
        
        results = gallery.display_all()
        
        assert gallery.get_loaded_count() == 2
        assert len(results) == 2
        assert "Displaying a.jpg" in results[0]
        assert "Displaying b.jpg" in results[1]
    
    def test_thumbnail_list_no_loading(self) -> None:
        gallery = ImageGallery()
        gallery.add_image(ImageProxy("a.jpg", 100, 100, 50))
        gallery.add_image(ImageProxy("b.jpg", 200, 200, 100))
        
        thumbnails = gallery.display_thumbnail_list()
        
        # Thumbnails should not trigger loading
        assert gallery.get_loaded_count() == 0
        assert len(thumbnails) == 2
        assert "100x100" in thumbnails[0]
        assert "50KB" in thumbnails[0]
    
    def test_mixed_real_and_proxy(self) -> None:
        gallery = ImageGallery()
        gallery.add_image(RealImage("real.jpg", 100, 100, 50))
        gallery.add_image(ImageProxy("proxy.jpg", 200, 200, 100))
        
        # RealImage is already loaded, proxy is not
        assert gallery.get_loaded_count() == 1
        
        gallery.display_all()
        assert gallery.get_loaded_count() == 2


class TestCreateImageProxy:
    """Tests for the factory function."""
    
    def test_factory_creates_proxy(self) -> None:
        metadata = {"width": 1920, "height": 1080, "size_kb": 2048}
        proxy = create_image_proxy("photo.jpg", metadata)
        
        assert isinstance(proxy, ImageProxy)
        assert proxy.filename == "photo.jpg"
        assert proxy.get_dimensions() == (1920, 1080)
        assert proxy.get_file_size() == 2048


class TestCachingImageProxy:
    """Tests for the advanced caching proxy."""
    
    def test_init_not_loaded(self) -> None:
        proxy = CachingImageProxy("photo.jpg", 1920, 1080, 2048)
        assert proxy.status == LoadingStatus.NOT_LOADED
    
    def test_display_caches_result(self) -> None:
        proxy = CachingImageProxy("photo.jpg", 1920, 1080, 2048)
        
        result1 = proxy.display()
        result2 = proxy.display()
        
        assert result1 == result2
        assert proxy.cache_hits == 1
    
    def test_multiple_display_calls_count_hits(self) -> None:
        proxy = CachingImageProxy("photo.jpg", 1920, 1080, 2048)
        
        proxy.display()  # First call - no cache hit
        proxy.display()  # Cache hit
        proxy.display()  # Cache hit
        proxy.display()  # Cache hit
        
        assert proxy.cache_hits == 3
    
    def test_clear_cache(self) -> None:
        proxy = CachingImageProxy("photo.jpg", 1920, 1080, 2048)
        
        proxy.display()
        proxy.clear_cache()
        proxy.display()
        
        # After clearing, display doesn't use cache
        assert proxy.cache_hits == 0
    
    def test_metadata_methods(self) -> None:
        proxy = CachingImageProxy("photo.jpg", 1920, 1080, 2048)
        
        assert proxy.filename == "photo.jpg"
        assert proxy.get_dimensions() == (1920, 1080)
        assert proxy.get_file_size() == 2048


class TestProxyPolymorphism:
    """Tests demonstrating proxy enables polymorphic use."""
    
    def test_all_images_interchangeable(self) -> None:
        """Client code works with RealImage and ImageProxy the same way."""
        images: list[Image] = [
            RealImage("real.jpg", 100, 100, 50),
            ImageProxy("proxy1.jpg", 200, 200, 100),
            ImageProxy("proxy2.jpg", 300, 300, 150),
        ]
        
        # All support the same interface
        for img in images:
            assert isinstance(img.filename, str)
            assert isinstance(img.get_dimensions(), tuple)
            assert isinstance(img.get_file_size(), int)
            assert isinstance(img.status, LoadingStatus)
    
    def test_client_code_unaware_of_proxy(self) -> None:
        """Client code doesn't know if it's working with proxy or real."""
        def get_image_info(img: Image) -> dict:
            return {
                "name": img.filename,
                "dimensions": img.get_dimensions(),
                "size_kb": img.get_file_size(),
            }
        
        real = RealImage("real.jpg", 100, 100, 50)
        proxy = ImageProxy("proxy.jpg", 200, 200, 100)
        
        real_info = get_image_info(real)
        proxy_info = get_image_info(proxy)
        
        # Both work identically through the interface
        assert "name" in real_info
        assert "name" in proxy_info
        assert "dimensions" in real_info
        assert "dimensions" in proxy_info


class TestLazyLoadingBenefits:
    """Tests demonstrating the benefits of lazy loading."""
    
    def test_lazy_loading_saves_resources(self) -> None:
        """Proxy delays expensive loading until needed."""
        gallery = ImageGallery()
        
        # Add 100 proxies - no images loaded yet
        for i in range(100):
            gallery.add_image(ImageProxy(f"image_{i}.jpg", 1920, 1080, 2048))
        
        # Nothing loaded yet
        assert gallery.get_loaded_count() == 0
        
        # Only display first image - only that one loads
        images = gallery._images
        images[0].display()
        assert gallery.get_loaded_count() == 1
        
        # Display another - total 2 loaded
        images[1].display()
        assert gallery.get_loaded_count() == 2
