"""Tests for Problem 02: Flying and Swimming Animals."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day04.problem_02_flying_and_swimming_animals import (
    Animal,
    Duck,
    Flyable,
    Penguin,
    Swimmable,
    Walkable,
)


class TestFlyable:
    """Tests for the Flyable mixin."""
    
    def test_flyable_fly(self) -> None:
        """Test the fly method."""
        
        class TestBird(Flyable):
            def __init__(self) -> None:
                self.name = "TestBird"
        
        bird = TestBird()
        result = bird.fly()
        assert result == "TestBird is flying through the air!"
    
    def test_flyable_take_off(self) -> None:
        """Test the take_off method."""
        
        class TestBird(Flyable):
            def __init__(self) -> None:
                self.name = "TestBird"
        
        bird = TestBird()
        result = bird.take_off()
        assert result == "TestBird takes off into the sky!"


class TestSwimmable:
    """Tests for the Swimmable mixin."""
    
    def test_swimmable_swim(self) -> None:
        """Test the swim method."""
        
        class TestFish(Swimmable):
            def __init__(self) -> None:
                self.name = "TestFish"
        
        fish = TestFish()
        result = fish.swim()
        assert result == "TestFish is swimming gracefully!"
    
    def test_swimmable_dive(self) -> None:
        """Test the dive method."""
        
        class TestFish(Swimmable):
            def __init__(self) -> None:
                self.name = "TestFish"
        
        fish = TestFish()
        result = fish.dive()
        assert result == "TestFish dives underwater!"


class TestWalkable:
    """Tests for the Walkable mixin."""
    
    def test_walkable_walk(self) -> None:
        """Test the walk method."""
        
        class TestAnimal(Walkable):
            def __init__(self) -> None:
                self.name = "TestAnimal"
        
        animal = TestAnimal()
        result = animal.walk()
        assert result == "TestAnimal is walking around."


class TestAnimal:
    """Tests for the Animal base class."""
    
    def test_animal_init(self) -> None:
        """Test Animal initialization."""
        animal = Animal("Test", 5)
        assert animal.name == "Test"
        assert animal.age == 5
        assert animal.species == "unknown"
    
    def test_animal_describe(self) -> None:
        """Test the describe method."""
        animal = Animal("Test", 5)
        result = animal.describe()
        assert result == "Test is a 5-year-old unknown"
    
    def test_animal_speak(self) -> None:
        """Test the speak method."""
        animal = Animal("Test", 5)
        result = animal.speak()
        assert result == "Test makes a sound."


class TestDuck:
    """Tests for the Duck class."""
    
    def test_duck_init(self) -> None:
        """Test Duck initialization."""
        duck = Duck("Donald", 3)
        assert duck.name == "Donald"
        assert duck.age == 3
        assert duck.species == "duck"
    
    def test_duck_is_animal(self) -> None:
        """Test that Duck is an Animal."""
        duck = Duck("Donald", 3)
        assert isinstance(duck, Animal)
    
    def test_duck_flyable(self) -> None:
        """Test that Duck can fly."""
        duck = Duck("Donald", 3)
        assert duck.fly() == "Donald is flying through the air!"
        assert duck.take_off() == "Donald takes off into the sky!"
    
    def test_duck_swimmable(self) -> None:
        """Test that Duck can swim."""
        duck = Duck("Donald", 3)
        assert duck.swim() == "Donald is swimming gracefully!"
        assert duck.dive() == "Donald dives underwater!"
    
    def test_duck_walkable(self) -> None:
        """Test that Duck can walk."""
        duck = Duck("Donald", 3)
        assert duck.walk() == "Donald is walking around."
    
    def test_duck_speak(self) -> None:
        """Test Duck's sound."""
        duck = Duck("Donald", 3)
        assert duck.speak() == "Quack!"
    
    def test_duck_describe(self) -> None:
        """Test Duck's description."""
        duck = Duck("Donald", 3)
        assert duck.describe() == "Donald is a 3-year-old duck"
    
    def test_duck_perform_trick(self) -> None:
        """Test Duck's trick."""
        duck = Duck("Donald", 3)
        assert duck.perform_trick() == "Donald flies and dives in a loop!"
    
    def test_duck_mro(self) -> None:
        """Test Duck's MRO."""
        expected_mro = (Duck, Animal, Flyable, Swimmable, Walkable, object)
        assert Duck.__mro__ == expected_mro


class TestPenguin:
    """Tests for the Penguin class."""
    
    def test_penguin_init(self) -> None:
        """Test Penguin initialization."""
        penguin = Penguin("Skipper", 5)
        assert penguin.name == "Skipper"
        assert penguin.age == 5
        assert penguin.species == "penguin"
    
    def test_penguin_is_animal(self) -> None:
        """Test that Penguin is an Animal."""
        penguin = Penguin("Skipper", 5)
        assert isinstance(penguin, Animal)
    
    def test_penguin_swimmable(self) -> None:
        """Test that Penguin can swim."""
        penguin = Penguin("Skipper", 5)
        assert penguin.swim() == "Skipper is swimming gracefully!"
        assert penguin.dive() == "Skipper dives underwater!"
    
    def test_penguin_walkable(self) -> None:
        """Test that Penguin can walk (waddle)."""
        penguin = Penguin("Skipper", 5)
        # Penguins override walk to waddle
        assert penguin.walk() == "Skipper is waddling around."
    
    def test_penguin_no_fly(self) -> None:
        """Test that Penguin cannot fly."""
        penguin = Penguin("Skipper", 5)
        assert not hasattr(penguin, 'fly') or not callable(getattr(penguin, 'fly', None))
        with pytest.raises(AttributeError):
            penguin.fly()
    
    def test_penguin_speak(self) -> None:
        """Test Penguin's sound."""
        penguin = Penguin("Skipper", 5)
        assert penguin.speak() == "Squawk!"
    
    def test_penguin_describe(self) -> None:
        """Test Penguin's description."""
        penguin = Penguin("Skipper", 5)
        assert penguin.describe() == "Skipper is a 5-year-old penguin"
    
    def test_penguin_slide(self) -> None:
        """Test Penguin's slide."""
        penguin = Penguin("Skipper", 5)
        assert penguin.slide() == "Skipper slides on its belly! Wheee!"
    
    def test_penguin_mro(self) -> None:
        """Test Penguin's MRO."""
        expected_mro = (Penguin, Animal, Swimmable, Walkable, object)
        assert Penguin.__mro__ == expected_mro
