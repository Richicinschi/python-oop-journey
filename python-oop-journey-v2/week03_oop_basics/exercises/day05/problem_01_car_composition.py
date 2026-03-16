"""Problem 01: Car Composition.

Implement a Car class that is composed of Engine, Transmission, and Wheels.
This demonstrates composition where the car owns its parts.

Classes to implement:
- Engine: with attributes horsepower, is_running
- Transmission: with attributes gear_count, current_gear
- Wheel: with attributes size, position
- Car: composed of one Engine, one Transmission, and four Wheels

Methods required:
- Engine.start() / Engine.stop()
- Transmission.shift_up() / Transmission.shift_down()
- Car.start() - starts engine
- Car.drive() - requires engine running and in gear
- Car.stop() - stops engine and resets gear
"""

from __future__ import annotations


class Engine:
    """Engine component of a car."""
    
    def __init__(self, horsepower: int) -> None:
        # TODO: Initialize horsepower and is_running (False by default)
        pass
    
    def start(self) -> str:
        # TODO: Set is_running to True and return status message
        pass
    
    def stop(self) -> str:
        # TODO: Set is_running to False and return status message
        pass


class Transmission:
    """Transmission component of a car."""
    
    def __init__(self, gear_count: int) -> None:
        # TODO: Initialize gear_count and current_gear (0 for neutral)
        pass
    
    def shift_up(self) -> bool:
        # TODO: Increment gear if possible, return True if shifted
        pass
    
    def shift_down(self) -> bool:
        # TODO: Decrement gear if possible, return True if shifted
        pass


class Wheel:
    """Wheel component of a car."""
    
    def __init__(self, size: int, position: str) -> None:
        # TODO: Initialize size and position (e.g., 'front_left')
        pass


class Car:
    """A car composed of Engine, Transmission, and Wheels."""
    
    def __init__(self, make: str, model: str, horsepower: int, gear_count: int, wheel_size: int) -> None:
        # TODO: Initialize make, model, and create composed components:
        # - One Engine with given horsepower
        # - One Transmission with given gear_count
        # - Four Wheels with given size at positions: front_left, front_right, rear_left, rear_right
        pass
    
    def start(self) -> str:
        # TODO: Start the engine and return status
        pass
    
    def drive(self) -> str:
        # TODO: Return driving status if engine running and in gear, else error message
        pass
    
    def stop(self) -> str:
        # TODO: Stop engine and reset to neutral gear
        pass
    
    def shift_up(self) -> str:
        # TODO: Delegate to transmission and return status
        pass
    
    def shift_down(self) -> str:
        # TODO: Delegate to transmission and return status
        pass
