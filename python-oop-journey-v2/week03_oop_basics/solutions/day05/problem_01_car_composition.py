"""Solution for Problem 01: Car Composition.

Car with Engine, Transmission, Wheels - demonstrates composition pattern
where the car owns its parts and manages their lifetime.
"""

from __future__ import annotations


class Engine:
    """Engine component of a car.
    
    The engine is created with the car and destroyed when the car is destroyed.
    """
    
    def __init__(self, horsepower: int) -> None:
        """Initialize the engine.
        
        Args:
            horsepower: The engine's power output.
        """
        self.horsepower = horsepower
        self.is_running = False
    
    def start(self) -> str:
        """Start the engine.
        
        Returns:
            Status message indicating engine state.
        """
        if self.is_running:
            return "Engine is already running"
        self.is_running = True
        return f"Engine started ({self.horsepower} HP)"
    
    def stop(self) -> str:
        """Stop the engine.
        
        Returns:
            Status message indicating engine state.
        """
        if not self.is_running:
            return "Engine is already stopped"
        self.is_running = False
        return "Engine stopped"


class Transmission:
    """Transmission component of a car.
    
    The transmission is created with the car and manages gear selection.
    """
    
    def __init__(self, gear_count: int) -> None:
        """Initialize the transmission.
        
        Args:
            gear_count: Number of gears (excluding neutral/reverse).
        """
        self.gear_count = gear_count
        self.current_gear = 0  # 0 is neutral
    
    def shift_up(self) -> bool:
        """Shift to a higher gear.
        
        Returns:
            True if shift was successful, False if at max gear.
        """
        if self.current_gear < self.gear_count:
            self.current_gear += 1
            return True
        return False
    
    def shift_down(self) -> bool:
        """Shift to a lower gear.
        
        Returns:
            True if shift was successful, False if at neutral.
        """
        if self.current_gear > 0:
            self.current_gear -= 1
            return True
        return False
    
    def is_in_gear(self) -> bool:
        """Check if transmission is in gear (not neutral).
        
        Returns:
            True if in gear, False if in neutral.
        """
        return self.current_gear > 0


class Wheel:
    """Wheel component of a car.
    
    Each wheel is created with the car and positioned at a specific corner.
    """
    
    def __init__(self, size: int, position: str) -> None:
        """Initialize the wheel.
        
        Args:
            size: Wheel diameter in inches.
            position: Position on car ('front_left', 'front_right', etc.).
        """
        self.size = size
        self.position = position
    
    def __repr__(self) -> str:
        """Return string representation of the wheel."""
        return f"Wheel({self.size}\" at {self.position})"


class Car:
    """A car composed of Engine, Transmission, and Wheels.
    
    This class demonstrates composition - the car creates and owns all its
    components. When a Car is destroyed, its parts are destroyed too.
    
    Attributes:
        make: Car manufacturer.
        model: Car model name.
        engine: The car's engine (composition).
        transmission: The car's transmission (composition).
        wheels: List of four wheels (composition).
    """
    
    def __init__(self, make: str, model: str, horsepower: int, gear_count: int, wheel_size: int) -> None:
        """Initialize the car with all its components.
        
        Args:
            make: Car manufacturer.
            model: Car model name.
            horsepower: Engine horsepower.
            gear_count: Number of transmission gears.
            wheel_size: Wheel diameter in inches.
        """
        self.make = make
        self.model = model
        
        # Composition: Car creates and owns these components
        self.engine = Engine(horsepower)
        self.transmission = Transmission(gear_count)
        self.wheels = [
            Wheel(wheel_size, "front_left"),
            Wheel(wheel_size, "front_right"),
            Wheel(wheel_size, "rear_left"),
            Wheel(wheel_size, "rear_right"),
        ]
    
    def start(self) -> str:
        """Start the car's engine.
        
        Returns:
            Status message from the engine.
        """
        return self.engine.start()
    
    def drive(self) -> str:
        """Attempt to drive the car.
        
        Returns:
            Driving status or error message.
        """
        if not self.engine.is_running:
            return "Cannot drive: engine is not running"
        if not self.transmission.is_in_gear():
            return "Cannot drive: transmission is in neutral"
        return f"{self.make} {self.model} is driving in gear {self.transmission.current_gear}"
    
    def stop(self) -> str:
        """Stop the car.
        
        Stops the engine and resets transmission to neutral.
        
        Returns:
            Status message.
        """
        engine_status = self.engine.stop()
        self.transmission.current_gear = 0
        return f"{engine_status}, transmission in neutral"
    
    def shift_up(self) -> str:
        """Shift transmission to higher gear.
        
        Returns:
            Status message.
        """
        if self.transmission.shift_up():
            return f"Shifted up to gear {self.transmission.current_gear}"
        return "Already at highest gear"
    
    def shift_down(self) -> str:
        """Shift transmission to lower gear.
        
        Returns:
            Status message.
        """
        if self.transmission.shift_down():
            return f"Shifted down to gear {self.transmission.current_gear}"
        return "Already in neutral"
    
    def get_wheel_count(self) -> int:
        """Return number of wheels.
        
        Returns:
            Number of wheels (always 4).
        """
        return len(self.wheels)
