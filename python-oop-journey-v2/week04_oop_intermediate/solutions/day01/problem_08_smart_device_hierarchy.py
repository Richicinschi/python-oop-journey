"""Reference solution for Problem 08: Smart Device Hierarchy."""

from __future__ import annotations


class SmartDevice:
    """Base class for smart home devices."""
    
    def __init__(self, device_id: str, name: str, location: str, 
                 power_usage_watts: float) -> None:
        self.device_id = device_id
        self.name = name
        self.location = location
        self.power_usage_watts = power_usage_watts
        self.is_connected = True
        self.is_on = False
    
    def turn_on(self) -> bool:
        if not self.is_connected or self.is_on:
            return False
        self.is_on = True
        return True
    
    def turn_off(self) -> bool:
        if not self.is_on:
            return False
        self.is_on = False
        return True
    
    def get_status(self) -> dict:
        return {
            "device_id": self.device_id,
            "name": self.name,
            "location": self.location,
            "is_connected": self.is_connected,
            "is_on": self.is_on
        }
    
    def connect(self) -> bool:
        self.is_connected = True
        return True
    
    def disconnect(self) -> bool:
        if self.is_on:
            self.turn_off()
        self.is_connected = False
        return True
    
    def get_power_usage(self) -> float:
        return self.power_usage_watts if self.is_on else 0.0


class SmartLight(SmartDevice):
    """A smart light bulb or fixture."""
    
    def __init__(self, device_id: str, name: str, location: str,
                 power_usage_watts: float, supports_color: bool = False) -> None:
        super().__init__(device_id, name, location, power_usage_watts)
        self.brightness = 100
        self.color_temperature = 2700
        self.color_rgb = (255, 255, 255)
        self.supports_color = supports_color
    
    def get_status(self) -> dict:
        base = super().get_status()
        base.update({
            "brightness": self.brightness,
            "color_temperature": self.color_temperature,
            "color_rgb": self.color_rgb
        })
        return base
    
    def set_brightness(self, level: int) -> bool:
        if 0 <= level <= 100:
            self.brightness = level
            return True
        return False
    
    def set_color_temperature(self, kelvin: int) -> bool:
        if 2700 <= kelvin <= 6500:
            self.color_temperature = kelvin
            return True
        return False
    
    def set_color(self, r: int, g: int, b: int) -> bool:
        if not self.supports_color:
            return False
        if all(0 <= val <= 255 for val in (r, g, b)):
            self.color_rgb = (r, g, b)
            return True
        return False


class SmartThermostat(SmartDevice):
    """A smart thermostat for climate control."""
    
    def __init__(self, device_id: str, name: str, location: str,
                 power_usage_watts: float, current_temp: float = 72.0) -> None:
        super().__init__(device_id, name, location, power_usage_watts)
        self.current_temp = current_temp
        self.target_temp = current_temp
        self.mode = "off"
        self.humidity = 50.0
        self._schedule: dict = {}
    
    def get_status(self) -> dict:
        base = super().get_status()
        base.update({
            "current_temp": self.current_temp,
            "target_temp": self.target_temp,
            "mode": self.mode,
            "humidity": self.humidity
        })
        return base
    
    def set_target_temperature(self, temp: float) -> bool:
        if 50 <= temp <= 90:
            self.target_temp = temp
            return True
        return False
    
    def set_mode(self, mode: str) -> bool:
        if mode in ("heat", "cool", "auto", "off"):
            self.mode = mode
            return True
        return False
    
    def update_current_temp(self, temp: float) -> None:
        self.current_temp = temp
    
    def is_heating_or_cooling(self) -> bool:
        return self.is_on and self.current_temp != self.target_temp


class SmartLock(SmartDevice):
    """A smart door lock."""
    
    def __init__(self, device_id: str, name: str, location: str,
                 power_usage_watts: float = 2.0, auto_lock_delay: int = 0) -> None:
        super().__init__(device_id, name, location, power_usage_watts)
        self.is_locked = True
        self.auto_lock_delay = auto_lock_delay
        self._battery_level = 100
        self._access_codes: dict[str, str] = {}
        self._access_log: list[dict] = []
    
    def get_status(self) -> dict:
        base = super().get_status()
        base.update({
            "is_locked": self.is_locked,
            "battery_level": self._battery_level,
            "auto_lock_delay": self.auto_lock_delay
        })
        return base
    
    def lock(self) -> bool:
        if not self.is_connected or self.is_locked:
            return False
        self.is_locked = True
        return True
    
    def unlock(self, code: str | None = None) -> bool:
        if not self.is_connected:
            return False
        if code is None or code in self._access_codes:
            self.is_locked = False
            name = self._access_codes.get(code, "Admin")
            self._access_log.append({"action": "unlock", "name": name})
            return True
        return False
    
    def add_access_code(self, code: str, name: str) -> bool:
        if code not in self._access_codes:
            self._access_codes[code] = name
            return True
        return False
    
    def remove_access_code(self, code: str) -> bool:
        if code in self._access_codes:
            del self._access_codes[code]
            return True
        return False
    
    def get_access_log(self) -> list:
        return self._access_log.copy()
    
    def update_battery_level(self, level: int) -> None:
        self._battery_level = max(0, min(100, level))
