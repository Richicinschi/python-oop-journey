"""Tests for Problem 03: Animal Kingdom."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day01.problem_03_animal_kingdom import (
    Animal, Mammal, Bird, Fish
)


class TestAnimal:
    """Tests for the base Animal class."""
    
    def test_animal_init(self) -> None:
        animal = Animal("Test", "Testicus", 5)
        assert animal.name == "Test"
        assert animal.species == "Testicus"
        assert animal.age == 5
    
    def test_animal_speak(self) -> None:
        animal = Animal("Test", "Testicus", 5)
        assert animal.speak() == "Some generic animal sound"
    
    def test_animal_move(self) -> None:
        animal = Animal("Test", "Testicus", 5)
        assert animal.move() == "moving"
    
    def test_animal_describe(self) -> None:
        animal = Animal("Leo", "Lion", 8)
        assert animal.describe() == "Leo (Lion), 8 years old"
    
    def test_animal_get_animal_type(self) -> None:
        animal = Animal("Test", "Testicus", 5)
        assert animal.get_animal_type() == "Unknown"


class TestMammal:
    """Tests for the Mammal class."""
    
    def test_mammal_inheritance(self) -> None:
        mammal = Mammal("Leo", "Lion", 8, "Golden", False)
        assert isinstance(mammal, Animal)
    
    def test_mammal_init(self) -> None:
        mammal = Mammal("Leo", "Lion", 8, "Golden", False)
        assert mammal.name == "Leo"
        assert mammal.fur_color == "Golden"
        assert mammal.is_domesticated is False
    
    def test_mammal_speak_override(self) -> None:
        mammal = Mammal("Leo", "Lion", 8, "Golden", False)
        assert mammal.speak() == "Grunt!"
    
    def test_mammal_move_override(self) -> None:
        mammal = Mammal("Leo", "Lion", 8, "Golden", False)
        assert mammal.move() == "walking on four legs"
    
    def test_mammal_get_animal_type(self) -> None:
        mammal = Mammal("Leo", "Lion", 8, "Golden", False)
        assert mammal.get_animal_type() == "Mammal"
    
    def test_mammal_nurse(self) -> None:
        mammal = Mammal("Leo", "Lion", 8, "Golden", False)
        assert mammal.nurse() == "Nursing young with milk"
    
    def test_mammal_describe_inherits(self) -> None:
        mammal = Mammal("Leo", "Lion", 8, "Golden", False)
        assert mammal.describe() == "Leo (Lion), 8 years old"


class TestBird:
    """Tests for the Bird class."""
    
    def test_bird_inheritance(self) -> None:
        bird = Bird("Tweety", "Canary", 2, 15.0, True, "Yellow")
        assert isinstance(bird, Animal)
    
    def test_bird_init(self) -> None:
        bird = Bird("Tweety", "Canary", 2, 15.0, True, "Yellow")
        assert bird.name == "Tweety"
        assert bird.wingspan == 15.0
        assert bird.can_fly is True
        assert bird.feather_color == "Yellow"
    
    def test_bird_speak_override(self) -> None:
        bird = Bird("Tweety", "Canary", 2, 15.0, True, "Yellow")
        assert bird.speak() == "Chirp!"
    
    def test_bird_move_can_fly(self) -> None:
        bird = Bird("Tweety", "Canary", 2, 15.0, True, "Yellow")
        assert bird.move() == "flying through the air"
    
    def test_bird_move_cannot_fly(self) -> None:
        bird = Bird("Penguin", "Emperor Penguin", 5, 0.0, False, "Black/White")
        assert bird.move() == "walking on two legs"
    
    def test_bird_get_animal_type(self) -> None:
        bird = Bird("Tweety", "Canary", 2, 15.0, True, "Yellow")
        assert bird.get_animal_type() == "Bird"
    
    def test_bird_lay_egg(self) -> None:
        bird = Bird("Tweety", "Canary", 2, 15.0, True, "Yellow")
        assert bird.lay_egg() == "Laying an egg"


class TestFish:
    """Tests for the Fish class."""
    
    def test_fish_inheritance(self) -> None:
        fish = Fish("Nemo", "Clownfish", 1, "saltwater", 5, 50.0)
        assert isinstance(fish, Animal)
    
    def test_fish_init(self) -> None:
        fish = Fish("Nemo", "Clownfish", 1, "saltwater", 5, 50.0)
        assert fish.name == "Nemo"
        assert fish.water_type == "saltwater"
        assert fish.fin_count == 5
        assert fish.max_depth == 50.0
    
    def test_fish_speak_override(self) -> None:
        fish = Fish("Nemo", "Clownfish", 1, "saltwater", 5, 50.0)
        assert fish.speak() == "Blub blub!"
    
    def test_fish_move_override(self) -> None:
        fish = Fish("Nemo", "Clownfish", 1, "saltwater", 5, 50.0)
        assert fish.move() == "swimming with 5 fins"
    
    def test_fish_get_animal_type(self) -> None:
        fish = Fish("Nemo", "Clownfish", 1, "saltwater", 5, 50.0)
        assert fish.get_animal_type() == "Fish"
    
    def test_fish_dive_success(self) -> None:
        fish = Fish("Nemo", "Clownfish", 1, "saltwater", 5, 50.0)
        assert fish.dive(30.0) == "Dived to 30.0 meters"
    
    def test_fish_dive_failure(self) -> None:
        fish = Fish("Nemo", "Clownfish", 1, "saltwater", 5, 50.0)
        assert fish.dive(60.0) == "Cannot dive to 60.0m. Max depth: 50.0m"


class TestPolymorphism:
    """Tests demonstrating polymorphic behavior."""
    
    def test_polymorphic_speak(self) -> None:
        animals: list[Animal] = [
            Mammal("Leo", "Lion", 8, "Golden", False),
            Bird("Tweety", "Canary", 2, 15.0, True, "Yellow"),
            Fish("Nemo", "Clownfish", 1, "saltwater", 5, 50.0)
        ]
        
        sounds = [a.speak() for a in animals]
        assert sounds == ["Grunt!", "Chirp!", "Blub blub!"]
    
    def test_polymorphic_move(self) -> None:
        animals: list[Animal] = [
            Mammal("Leo", "Lion", 8, "Golden", False),
            Bird("Tweety", "Canary", 2, 15.0, True, "Yellow"),
            Fish("Nemo", "Clownfish", 1, "saltwater", 5, 50.0)
        ]
        
        movements = [a.move() for a in animals]
        assert movements[0] == "walking on four legs"
        assert movements[1] == "flying through the air"
        assert movements[2] == "swimming with 5 fins"
    
    def test_polymorphic_types(self) -> None:
        animals: list[Animal] = [
            Mammal("Leo", "Lion", 8, "Golden", False),
            Bird("Tweety", "Canary", 2, 15.0, True, "Yellow"),
            Fish("Nemo", "Clownfish", 1, "saltwater", 5, 50.0)
        ]
        
        types = [a.get_animal_type() for a in animals]
        assert types == ["Mammal", "Bird", "Fish"]


class TestIsinstance:
    """Tests for isinstance checks."""
    
    def test_mammal_isinstance_animal(self) -> None:
        mammal = Mammal("Leo", "Lion", 8, "Golden", False)
        assert isinstance(mammal, Animal)
        assert isinstance(mammal, Mammal)
    
    def test_bird_isinstance_animal(self) -> None:
        bird = Bird("Tweety", "Canary", 2, 15.0, True, "Yellow")
        assert isinstance(bird, Animal)
        assert isinstance(bird, Bird)
    
    def test_fish_isinstance_animal(self) -> None:
        fish = Fish("Nemo", "Clownfish", 1, "saltwater", 5, 50.0)
        assert isinstance(fish, Animal)
        assert isinstance(fish, Fish)


class TestIssubclass:
    """Tests for issubclass checks."""
    
    def test_mammal_subclass_animal(self) -> None:
        assert issubclass(Mammal, Animal)
    
    def test_bird_subclass_animal(self) -> None:
        assert issubclass(Bird, Animal)
    
    def test_fish_subclass_animal(self) -> None:
        assert issubclass(Fish, Animal)
