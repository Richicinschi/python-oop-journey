"""Problem 08: Smart Device Hierarchy

Topic: IoT Inheritance with Device-Specific Features
Difficulty: Medium

Create a SmartDevice base class with SmartLight, SmartThermostat, and SmartLock
subclasses for a home automation system.
"""

from __future__ import annotations


class SmartDevice:
    """Base class for smart home devices.
    
    Attributes:
        device_id: Unique device identifier
        name: Device name/label
        location: Room/location in home
        is_connected: Whether device is online
        is_on: Current power state
        power_usage_watts: Power consumption when on
    """
    
    def __init__(self, device_id: str, name: str, location: str, 
                 power_usage_watts: float) -> None:
        """Initialize a SmartDevice.
        
        Args:
            device_id: Unique identifier
            name: Device name
            location: Room location
            power_usage_watts: Power consumption in watts
        """
        raise NotImplementedError("Implement SmartDevice.__init__")
    
    def turn_on(self) -> bool:
        """Turn the device on.
        
        Returns:
            True if state changed to on
            False if already on or not connected
        """
        raise NotImplementedError("Implement SmartDevice.turn_on")
    
    def turn_off(self) -> bool:
        """Turn the device off.
        
        Returns:
            True if state changed to off
            False if already off
        """
        raise NotImplementedError("Implement SmartDevice.turn_off")
    
    def get_status(self) -> dict:
        """Return device status as dictionary.
        
        Returns:
            Dict with device_id, name, location, is_connected, is_on
        """
        raise NotImplementedError("Implement SmartDevice.get_status")
    
    def connect(self) -> bool:
        """Connect device to network.
        
        Returns:
            True if connected successfully
        """
        raise NotImplementedError("Implement SmartDevice.connect")
    
    def disconnect(self) -> bool:
        """Disconnect device from network.
        
        Automatically turns off device when disconnecting.
        
        Returns:
            True if disconnected
        """
        raise NotImplementedError("Implement SmartDevice.disconnect")
    
    def get_power_usage(self) -> float:
        """Return current power usage.
        
        Returns:
            Power usage if on, 0.0 if off
        """
        raise NotImplementedError("Implement SmartDevice.get_power_usage")


class SmartLight(SmartDevice):
    """A smart light bulb or fixture.
    
    Additional Attributes:
        brightness: Current brightness level (0-100)
        color_temperature: Color temp in Kelvin (2700-6500)
        color_rgb: RGB color tuple (r, g, b) each 0-255
        supports_color: Whether light supports RGB colors
    """
    
    def __init__(self, device_id: str, name: str, location: str,
                 power_usage_watts: float, supports_color: bool = False) -> None:
        """Initialize a SmartLight.
        
        Args:
            device_id: Unique identifier
            name: Device name
            location: Room location
            power_usage_watts: Power consumption
            supports_color: Whether RGB color is supported
        """
        raise NotImplementedError("Implement SmartLight.__init__")
    
    def get_status(self) -> dict:
        """Override: Include light-specific status.
        
        Returns:
            Base status + brightness, color_temperature, color_rgb
        """
        raise NotImplementedError("Implement SmartLight.get_status")
    
    def set_brightness(self, level: int) -> bool:
        """Set brightness level.
        
        Args:
            level: 0-100 brightness level
            
        Returns:
            True if set successfully
        """
        raise NotImplementedError("Implement SmartLight.set_brightness")
    
    def set_color_temperature(self, kelvin: int) -> bool:
        """Set color temperature.
        
        Args:
            kelvin: 2700-6500K
            
        Returns:
            True if valid range and set
        """
        raise NotImplementedError("Implement SmartLight.set_color_temperature")
    
    def set_color(self, r: int, g: int, b: int) -> bool:
        """Set RGB color (only if supports_color is True).
        
        Args:
            r: Red 0-255
            g: Green 0-255
            b: Blue 0-255
            
        Returns:
            True if color supported and valid
        """
        raise NotImplementedError("Implement SmartLight.set_color")


class SmartThermostat(SmartDevice):
    """A smart thermostat for climate control.
    
    Additional Attributes:
        current_temp: Current room temperature
        target_temp: Target temperature setting
        mode: "heat", "cool", "auto", or "off"
        humidity: Current humidity percentage
        schedule: Temperature schedule dict {time: temp}
    """
    
    def __init__(self, device_id: str, name: str, location: str,
                 power_usage_watts: float, current_temp: float = 72.0) -> None:
        """Initialize a SmartThermostat.
        
        Args:
            device_id: Unique identifier
            name: Device name
            location: Room location
            power_usage_watts: Power consumption
            current_temp: Initial temperature (default 72F)
        """
        raise NotImplementedError("Implement SmartThermostat.__init__")
    
    def get_status(self) -> dict:
        """Override: Include thermostat-specific status.
        
        Returns:
            Base status + current_temp, target_temp, mode, humidity
        """
        raise NotImplementedError("Implement SmartThermostat.get_status")
    
    def set_target_temperature(self, temp: float) -> bool:
        """Set target temperature.
        
        Args:
            temp: Target temperature in Fahrenheit (50-90)
            
        Returns:
            True if valid range
        """
        raise NotImplementedError("Implement SmartThermostat.set_target_temperature")
    
    def set_mode(self, mode: str) -> bool:
        """Set thermostat mode.
        
        Args:
            mode: "heat", "cool", "auto", or "off"
            
        Returns:
            True if valid mode
        """
        raise NotImplementedError("Implement SmartThermostat.set_mode")
    
    def update_current_temp(self, temp: float) -> None:
        """Update current room temperature reading.
        
        Args:
            temp: Current temperature
        """
        raise NotImplementedError("Implement SmartThermostat.update_current_temp")
    
    def is_heating_or_cooling(self) -> bool:
        """Check if actively heating or cooling.
        
        Returns:
            True if on and current_temp != target_temp
        """
        raise NotImplementedError("Implement SmartThermostat.is_heating_or_cooling")


class SmartLock(SmartDevice):
    """A smart door lock.
    
    Additional Attributes:
        is_locked: Current lock state
        access_codes: Dictionary of {code: name} pairs
        access_log: List of access events
        auto_lock_delay: Seconds before auto-lock (0 = disabled)
        battery_level: Battery percentage (0-100)
    """
    
    def __init__(self, device_id: str, name: str, location: str,
                 power_usage_watts: float = 2.0, auto_lock_delay: int = 0) -> None:
        """Initialize a SmartLock.
        
        Args:
            device_id: Unique identifier
            name: Device name
            location: Door location
            power_usage_watts: Power consumption (low default)
            auto_lock_delay: Seconds before auto-lock (0 = off)
        """
        raise NotImplementedError("Implement SmartLock.__init__")
    
    def get_status(self) -> dict:
        """Override: Include lock-specific status.
        
        Returns:
            Base status + is_locked, battery_level, auto_lock_delay
        """
        raise NotImplementedError("Implement SmartLock.get_status")
    
    def lock(self) -> bool:
        """Lock the door.
        
        Returns:
            True if successfully locked
            False if already locked or not connected
        """
        raise NotImplementedError("Implement SmartLock.lock")
    
    def unlock(self, code: str | None = None) -> bool:
        """Unlock the door.
        
        Args:
            code: Access code (optional, can be admin override)
            
        Returns:
            True if successfully unlocked
        """
        raise NotImplementedError("Implement SmartLock.unlock")
    
    def add_access_code(self, code: str, name: str) -> bool:
        """Add a new access code.
        
        Args:
            code: The access code string
            name: Name of person who gets this code
            
        Returns:
            True if added successfully
        """
        raise NotImplementedError("Implement SmartLock.add_access_code")
    
    def remove_access_code(self, code: str) -> bool:
        """Remove an access code.
        
        Args:
            code: Code to remove
            
        Returns:
            True if removed, False if code didn't exist
        """
        raise NotImplementedError("Implement SmartLock.remove_access_code")
    
    def get_access_log(self) -> list:
        """Return the access log.
        
        Returns:
            List of access events (dict with time, action, code_name)
        """
        raise NotImplementedError("Implement SmartLock.get_access_log")
    
    def update_battery_level(self, level: int) -> None:
        """Update battery level.
        
        Args:
            level: Battery percentage 0-100
        """
        raise NotImplementedError("Implement SmartLock.update_battery_level")
