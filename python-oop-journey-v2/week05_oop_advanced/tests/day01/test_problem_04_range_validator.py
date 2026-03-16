"""Tests for Problem 04: Range Validator."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day01.problem_04_range_validator import (
    RangeValidator, Temperature, Score, Percentage
)


class TestRangeValidator:
    """Tests for the RangeValidator descriptor."""
    
    def test_valid_value_within_range(self) -> None:
        class TestClass:
            value = RangeValidator(0, 100, int)
            
            def __init__(self, v: int) -> None:
                self.value = v
        
        obj = TestClass(50)
        assert obj.value == 50
    
    def test_value_at_boundaries(self) -> None:
        class TestClass:
            value = RangeValidator(0, 100, int)
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        obj.value = 0  # Min boundary
        assert obj.value == 0
        
        obj.value = 100  # Max boundary
        assert obj.value == 100
    
    def test_value_below_range_raises(self) -> None:
        class TestClass:
            value = RangeValidator(0, 100, int)
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        with pytest.raises(ValueError, match="between"):
            obj.value = -1
    
    def test_value_above_range_raises(self) -> None:
        class TestClass:
            value = RangeValidator(0, 100, int)
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        with pytest.raises(ValueError, match="between"):
            obj.value = 101
    
    def test_wrong_type_raises(self) -> None:
        class TestClass:
            value = RangeValidator(0, 100, int)
            
            def __init__(self) -> None:
                pass
        
        obj = TestClass()
        with pytest.raises(TypeError, match="int"):
            obj.value = "50"


class TestTemperature:
    """Tests for the Temperature class."""
    
    def test_celsius_creation(self) -> None:
        temp = Temperature(25.0)
        assert temp.celsius == 25.0
    
    def test_absolute_zero_boundary(self) -> None:
        temp = Temperature(-273.15)
        assert temp.celsius == -273.15
    
    def test_below_absolute_zero_raises(self) -> None:
        with pytest.raises(ValueError):
            _ = Temperature(-274.0)
    
    def test_fahrenheit_conversion_not_implemented(self) -> None:
        temp = Temperature(0.0)
        temp.fahrenheit = 32.0
        assert temp.fahrenheit == 32.0


class TestScore:
    """Tests for the Score class."""
    
    def test_score_creation(self) -> None:
        score = Score(85, 5)
        assert score.value == 85
        assert score.level == 5
    
    def test_score_must_be_0_to_100(self) -> None:
        with pytest.raises(ValueError):
            _ = Score(101, 5)
        
        with pytest.raises(ValueError):
            _ = Score(-1, 5)
    
    def test_level_must_be_1_to_10(self) -> None:
        with pytest.raises(ValueError):
            _ = Score(50, 0)
        
        with pytest.raises(ValueError):
            _ = Score(50, 11)


class TestPercentage:
    """Tests for the Percentage class."""
    
    def test_percentage_creation(self) -> None:
        pct = Percentage(50)
        assert pct.value == 50
    
    def test_percentage_str(self) -> None:
        pct = Percentage(75)
        assert str(pct) == "75%"
    
    def test_percentage_repr(self) -> None:
        pct = Percentage(50)
        assert repr(pct) == "Percentage(50)"
    
    def test_percentage_boundary_values(self) -> None:
        pct0 = Percentage(0)
        assert pct0.value == 0
        
        pct100 = Percentage(100)
        assert pct100.value == 100
    
    def test_percentage_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            _ = Percentage(-1)
        
        with pytest.raises(ValueError):
            _ = Percentage(101)
