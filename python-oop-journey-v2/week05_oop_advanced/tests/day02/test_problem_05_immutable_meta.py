"""Tests for Problem 05: Immutable Instance Metaclass."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day02.problem_05_immutable_meta import (
    ImmutableConfig,
    ImmutableMeta,
    Point,
)


class TestImmutableMeta:
    """Tests for the ImmutableMeta metaclass."""
    
    def test_metaclass_exists(self) -> None:
        """Test that ImmutableMeta is defined."""
        assert isinstance(ImmutableMeta, type)
    
    def test_init_allows_setting(self) -> None:
        """Test that attributes can be set during __init__."""
        p = Point(1, 2)
        assert p.x == 1
        assert p.y == 2
    
    def test_modification_raises_error(self) -> None:
        """Test that modification after init raises AttributeError."""
        p = Point(1, 2)
        
        with pytest.raises(AttributeError):
            p.x = 3
        
        with pytest.raises(AttributeError):
            p.new_attr = "value"
    
    def test_deletion_raises_error(self) -> None:
        """Test that attribute deletion raises AttributeError."""
        p = Point(1, 2)
        
        with pytest.raises(AttributeError):
            del p.x


class TestPoint:
    """Tests for the Point class."""
    
    def test_point_init(self) -> None:
        """Test Point initialization."""
        p = Point(3, 4)
        assert p.x == 3
        assert p.y == 4
    
    def test_point_properties_readonly(self) -> None:
        """Test that Point properties are read-only."""
        p = Point(1, 2)
        
        with pytest.raises(AttributeError):
            p.x = 10
    
    def test_point_replace(self) -> None:
        """Test Point replace method."""
        p1 = Point(1, 2)
        p2 = p1.replace(x=10)
        
        # Original unchanged
        assert p1.x == 1
        assert p1.y == 2
        
        # New point has new x, same y
        assert p2.x == 10
        assert p2.y == 2
    
    def test_point_replace_y(self) -> None:
        """Test Point replace for y coordinate."""
        p1 = Point(1, 2)
        p2 = p1.replace(y=20)
        
        assert p2.x == 1
        assert p2.y == 20
    
    def test_point_replace_both(self) -> None:
        """Test Point replace for both coordinates."""
        p1 = Point(1, 2)
        p2 = p1.replace(x=10, y=20)
        
        assert p2.x == 10
        assert p2.y == 20
    
    def test_point_equality(self) -> None:
        """Test Point equality."""
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        p3 = Point(2, 1)
        
        assert p1 == p2
        assert p1 != p3
    
    def test_point_hash(self) -> None:
        """Test Point hashability."""
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        
        # Same points should have same hash
        assert hash(p1) == hash(p2)
        
        # Can be used as dict key
        d = {p1: "value"}
        assert d[p2] == "value"
    
    def test_point_repr(self) -> None:
        """Test Point representation."""
        p = Point(3, 4)
        assert repr(p) == "Point(3, 4)"


class TestImmutableConfig:
    """Tests for the ImmutableConfig class."""
    
    def test_config_init(self) -> None:
        """Test Config initialization."""
        c = ImmutableConfig(debug=True, timeout=60, retries=5)
        assert c.debug is True
        assert c.timeout == 60
        assert c.retries == 5
    
    def test_config_defaults(self) -> None:
        """Test Config default values."""
        c = ImmutableConfig()
        assert c.debug is False
        assert c.timeout == 30
        assert c.retries == 3
    
    def test_config_immutability(self) -> None:
        """Test that Config is immutable."""
        c = ImmutableConfig()
        
        with pytest.raises(AttributeError):
            c.debug = True
        
        with pytest.raises(AttributeError):
            c.timeout = 60
    
    def test_config_replace(self) -> None:
        """Test Config replace method."""
        c1 = ImmutableConfig(debug=False, timeout=30)
        c2 = c1.replace(debug=True)
        
        # Original unchanged
        assert c1.debug is False
        assert c1.timeout == 30
        
        # New config has new value
        assert c2.debug is True
        assert c2.timeout == 30
    
    def test_config_equality(self) -> None:
        """Test Config equality."""
        c1 = ImmutableConfig(debug=True, timeout=45)
        c2 = ImmutableConfig(debug=True, timeout=45)
        c3 = ImmutableConfig(debug=False, timeout=45)
        
        assert c1 == c2
        assert c1 != c3
    
    def test_config_hash(self) -> None:
        """Test Config hashability."""
        c1 = ImmutableConfig(debug=True, timeout=45)
        c2 = ImmutableConfig(debug=True, timeout=45)
        
        assert hash(c1) == hash(c2)
        
        d = {c1: "config"}
        assert d[c2] == "config"
