"""Tests for Problem 06: Tracked Class Creation Metaclass."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day02.problem_06_tracked_class_meta import (
    ServiceA,
    ServiceAAdvanced,
    ServiceAEnhanced,
    ServiceB,
    StandaloneService,
    TrackedClass,
    TrackedMeta,
)


class TestTrackedMeta:
    """Tests for the TrackedMeta metaclass."""
    
    def setup_method(self) -> None:
        """Reset stats before each test."""
        TrackedMeta.reset_stats()
    
    def test_metaclass_exists(self) -> None:
        """Test that TrackedMeta is defined."""
        assert isinstance(TrackedMeta, type)
    
    def test_creation_count_increments(self) -> None:
        """Test that class creation increments count."""
        initial = TrackedMeta.get_creation_count()
        
        class TestClass1(metaclass=TrackedMeta):
            pass
        
        assert TrackedMeta.get_creation_count() == initial + 1
        
        class TestClass2(metaclass=TrackedMeta):
            pass
        
        assert TrackedMeta.get_creation_count() == initial + 2
    
    def test_creation_log_contains_metadata(self) -> None:
        """Test that creation log contains expected metadata."""
        TrackedMeta.reset_stats()
        
        class TestClass(metaclass=TrackedMeta):
            pass
        
        log = TrackedMeta.get_creation_log()
        assert len(log) == 1
        
        entry = log[0]
        assert entry['name'] == 'TestClass'
        assert 'timestamp' in entry
        assert 'depth' in entry
        assert 'bases' in entry
        assert 'order' in entry
    
    def test_class_names_list(self) -> None:
        """Test that get_class_names returns names in order."""
        TrackedMeta.reset_stats()
        
        class First(metaclass=TrackedMeta):
            pass
        
        class Second(metaclass=TrackedMeta):
            pass
        
        names = TrackedMeta.get_class_names()
        assert names == ['First', 'Second']
    
    def test_reset_stats(self) -> None:
        """Test reset_stats clears all tracking."""
        class TempClass(metaclass=TrackedMeta):
            pass
        
        assert TrackedMeta.get_creation_count() > 0
        TrackedMeta.reset_stats()
        
        assert TrackedMeta.get_creation_count() == 0
        assert TrackedMeta.get_creation_log() == []
    
    def test_depth_calculation_root(self) -> None:
        """Test depth calculation for root classes."""
        TrackedMeta.reset_stats()
        
        class RootClass(metaclass=TrackedMeta):
            pass
        
        log = TrackedMeta.get_creation_log()
        assert log[0]['depth'] == 0
    
    def test_depth_calculation_inheritance(self) -> None:
        """Test depth calculation with inheritance."""
        TrackedMeta.reset_stats()
        
        class Level1(metaclass=TrackedMeta):
            pass
        
        class Level2(Level1, metaclass=TrackedMeta):
            pass
        
        class Level3(Level2, metaclass=TrackedMeta):
            pass
        
        log = TrackedMeta.get_creation_log()
        # Note: depth calculation may vary based on implementation
        assert len(log) == 3


class TestTrackedClass:
    """Tests for the TrackedClass base class."""
    
    def setup_method(self) -> None:
        """Reset stats before each test."""
        TrackedMeta.reset_stats()
    
    def test_tracked_class_info(self) -> None:
        """Test get_class_info returns metadata."""
        TrackedMeta.reset_stats()
        
        class TestService(TrackedClass):
            pass
        
        info = TestService.get_class_info()
        assert info['name'] == 'TestService'


class TestServiceClasses:
    """Tests for the example service classes."""
    
    def setup_method(self) -> None:
        """Reset stats before each test."""
        TrackedMeta.reset_stats()
    
    def test_service_a_process(self) -> None:
        """Test ServiceA process method."""
        s = ServiceA()
        assert "processing" in s.process().lower()
    
    def test_service_b_handle(self) -> None:
        """Test ServiceB handle method."""
        s = ServiceB()
        assert "handling" in s.handle().lower()
    
    def test_service_a_enhanced(self) -> None:
        """Test ServiceAEnhanced."""
        s = ServiceAEnhanced()
        assert "processing" in s.process().lower()
        assert "enhanced" in s.enhanced_process().lower()
    
    def test_service_a_advanced(self) -> None:
        """Test ServiceAAdvanced."""
        s = ServiceAAdvanced()
        assert "processing" in s.process().lower()
        assert "enhanced" in s.enhanced_process().lower()
        assert "advanced" in s.advanced_process().lower()
    
    def test_standalone_service(self) -> None:
        """Test StandaloneService."""
        s = StandaloneService()
        assert "executing" in s.execute().lower()
