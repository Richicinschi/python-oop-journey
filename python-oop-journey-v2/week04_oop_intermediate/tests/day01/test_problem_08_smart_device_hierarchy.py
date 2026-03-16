"""Tests for Problem 08: Smart Device Hierarchy."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day01.problem_08_smart_device_hierarchy import (
    SmartDevice, SmartLight, SmartThermostat, SmartLock
)


class TestSmartDevice:
    """Tests for the base SmartDevice class."""
    
    def test_device_init(self) -> None:
        device = SmartDevice("D001", "Living Room Light", "Living Room", 60.0)
        assert device.device_id == "D001"
        assert device.name == "Living Room Light"
        assert device.location == "Living Room"
        assert device.power_usage_watts == 60.0
        assert device.is_connected is True
        assert device.is_on is False
    
    def test_device_turn_on(self) -> None:
        device = SmartDevice("D001", "Test", "Test", 60.0)
        result = device.turn_on()
        assert result is True
        assert device.is_on is True
    
    def test_device_turn_on_already_on(self) -> None:
        device = SmartDevice("D001", "Test", "Test", 60.0)
        device.turn_on()
        result = device.turn_on()
        assert result is False
    
    def test_device_turn_on_not_connected(self) -> None:
        device = SmartDevice("D001", "Test", "Test", 60.0)
        device.disconnect()
        result = device.turn_on()
        assert result is False
    
    def test_device_turn_off(self) -> None:
        device = SmartDevice("D001", "Test", "Test", 60.0)
        device.turn_on()
        result = device.turn_off()
        assert result is True
        assert device.is_on is False
    
    def test_device_turn_off_already_off(self) -> None:
        device = SmartDevice("D001", "Test", "Test", 60.0)
        result = device.turn_off()
        assert result is False
    
    def test_device_get_status(self) -> None:
        device = SmartDevice("D001", "Living Room Light", "Living Room", 60.0)
        status = device.get_status()
        assert status["device_id"] == "D001"
        assert status["name"] == "Living Room Light"
        assert status["location"] == "Living Room"
        assert status["is_connected"] is True
        assert status["is_on"] is False
    
    def test_device_connect(self) -> None:
        device = SmartDevice("D001", "Test", "Test", 60.0)
        device.disconnect()
        result = device.connect()
        assert result is True
        assert device.is_connected is True
    
    def test_device_disconnect(self) -> None:
        device = SmartDevice("D001", "Test", "Test", 60.0)
        device.turn_on()
        result = device.disconnect()
        assert result is True
        assert device.is_connected is False
        assert device.is_on is False  # Should turn off when disconnected
    
    def test_device_get_power_usage_on(self) -> None:
        device = SmartDevice("D001", "Test", "Test", 60.0)
        device.turn_on()
        assert device.get_power_usage() == 60.0
    
    def test_device_get_power_usage_off(self) -> None:
        device = SmartDevice("D001", "Test", "Test", 60.0)
        assert device.get_power_usage() == 0.0


class TestSmartLight:
    """Tests for the SmartLight class."""
    
    def test_light_inheritance(self) -> None:
        light = SmartLight("L001", "Living Room Light", "Living Room", 60.0)
        assert isinstance(light, SmartDevice)
    
    def test_light_init(self) -> None:
        light = SmartLight("L001", "Living Room Light", "Living Room", 60.0, True)
        assert light.brightness == 100
        assert light.color_temperature == 2700
        assert light.supports_color is True
    
    def test_light_init_default(self) -> None:
        light = SmartLight("L001", "Living Room Light", "Living Room", 60.0)
        assert light.supports_color is False
    
    def test_light_get_status(self) -> None:
        light = SmartLight("L001", "Living Room Light", "Living Room", 60.0)
        status = light.get_status()
        assert status["brightness"] == 100
        assert status["color_temperature"] == 2700
    
    def test_light_set_brightness(self) -> None:
        light = SmartLight("L001", "Living Room Light", "Living Room", 60.0)
        result = light.set_brightness(50)
        assert result is True
        assert light.brightness == 50
    
    def test_light_set_brightness_invalid(self) -> None:
        light = SmartLight("L001", "Living Room Light", "Living Room", 60.0)
        result = light.set_brightness(150)
        assert result is False
    
    def test_light_set_color_temperature(self) -> None:
        light = SmartLight("L001", "Living Room Light", "Living Room", 60.0)
        result = light.set_color_temperature(4000)
        assert result is True
        assert light.color_temperature == 4000
    
    def test_light_set_color_temperature_invalid(self) -> None:
        light = SmartLight("L001", "Living Room Light", "Living Room", 60.0)
        result = light.set_color_temperature(7000)
        assert result is False
    
    def test_light_set_color_success(self) -> None:
        light = SmartLight("L001", "Living Room Light", "Living Room", 60.0, True)
        result = light.set_color(255, 0, 0)
        assert result is True
        assert light.color_rgb == (255, 0, 0)
    
    def test_light_set_color_not_supported(self) -> None:
        light = SmartLight("L001", "Living Room Light", "Living Room", 60.0, False)
        result = light.set_color(255, 0, 0)
        assert result is False
    
    def test_light_set_color_invalid(self) -> None:
        light = SmartLight("L001", "Living Room Light", "Living Room", 60.0, True)
        result = light.set_color(300, 0, 0)
        assert result is False


class TestSmartThermostat:
    """Tests for the SmartThermostat class."""
    
    def test_thermostat_inheritance(self) -> None:
        thermo = SmartThermostat("T001", "Main Thermostat", "Hallway", 50.0)
        assert isinstance(thermo, SmartDevice)
    
    def test_thermostat_init(self) -> None:
        thermo = SmartThermostat("T001", "Main Thermostat", "Hallway", 50.0, 68.0)
        assert thermo.current_temp == 68.0
        assert thermo.target_temp == 68.0
        assert thermo.mode == "off"
    
    def test_thermostat_get_status(self) -> None:
        thermo = SmartThermostat("T001", "Main Thermostat", "Hallway", 50.0)
        status = thermo.get_status()
        assert "current_temp" in status
        assert "target_temp" in status
        assert "mode" in status
    
    def test_thermostat_set_target_temperature(self) -> None:
        thermo = SmartThermostat("T001", "Main Thermostat", "Hallway", 50.0)
        result = thermo.set_target_temperature(72.0)
        assert result is True
        assert thermo.target_temp == 72.0
    
    def test_thermostat_set_target_temperature_invalid(self) -> None:
        thermo = SmartThermostat("T001", "Main Thermostat", "Hallway", 50.0)
        result = thermo.set_target_temperature(100.0)
        assert result is False
    
    def test_thermostat_set_mode(self) -> None:
        thermo = SmartThermostat("T001", "Main Thermostat", "Hallway", 50.0)
        result = thermo.set_mode("heat")
        assert result is True
        assert thermo.mode == "heat"
    
    def test_thermostat_set_mode_invalid(self) -> None:
        thermo = SmartThermostat("T001", "Main Thermostat", "Hallway", 50.0)
        result = thermo.set_mode("fan")
        assert result is False
    
    def test_thermostat_update_current_temp(self) -> None:
        thermo = SmartThermostat("T001", "Main Thermostat", "Hallway", 50.0, 68.0)
        thermo.update_current_temp(70.0)
        assert thermo.current_temp == 70.0
    
    def test_thermostat_is_heating_or_cooling(self) -> None:
        thermo = SmartThermostat("T001", "Main Thermostat", "Hallway", 50.0, 68.0)
        thermo.turn_on()
        thermo.set_target_temperature(72.0)
        assert thermo.is_heating_or_cooling() is True
    
    def test_thermostat_not_heating_when_off(self) -> None:
        thermo = SmartThermostat("T001", "Main Thermostat", "Hallway", 50.0, 68.0)
        thermo.set_target_temperature(72.0)
        assert thermo.is_heating_or_cooling() is False  # Device is off


class TestSmartLock:
    """Tests for the SmartLock class."""
    
    def test_lock_inheritance(self) -> None:
        lock = SmartLock("LK001", "Front Door", "Entrance")
        assert isinstance(lock, SmartDevice)
    
    def test_lock_init(self) -> None:
        lock = SmartLock("LK001", "Front Door", "Entrance", 2.0, 30)
        assert lock.is_locked is True
        assert lock.auto_lock_delay == 30
    
    def test_lock_get_status(self) -> None:
        lock = SmartLock("LK001", "Front Door", "Entrance")
        status = lock.get_status()
        assert status["is_locked"] is True
        assert "battery_level" in status
    
    def test_lock_lock(self) -> None:
        lock = SmartLock("LK001", "Front Door", "Entrance")
        lock.unlock(None)  # First unlock
        result = lock.lock()
        assert result is True
        assert lock.is_locked is True
    
    def test_lock_lock_already_locked(self) -> None:
        lock = SmartLock("LK001", "Front Door", "Entrance")
        result = lock.lock()
        assert result is False
    
    def test_lock_unlock(self) -> None:
        lock = SmartLock("LK001", "Front Door", "Entrance")
        result = lock.unlock(None)  # Admin override
        assert result is True
        assert lock.is_locked is False
    
    def test_lock_unlock_with_code(self) -> None:
        lock = SmartLock("LK001", "Front Door", "Entrance")
        lock.add_access_code("1234", "Family")
        result = lock.unlock("1234")
        assert result is True
        assert lock.is_locked is False
    
    def test_lock_unlock_wrong_code(self) -> None:
        lock = SmartLock("LK001", "Front Door", "Entrance")
        lock.add_access_code("1234", "Family")
        result = lock.unlock("0000")
        assert result is False
    
    def test_lock_add_access_code(self) -> None:
        lock = SmartLock("LK001", "Front Door", "Entrance")
        result = lock.add_access_code("1234", "Family")
        assert result is True
    
    def test_lock_add_access_code_duplicate(self) -> None:
        lock = SmartLock("LK001", "Front Door", "Entrance")
        lock.add_access_code("1234", "Family")
        result = lock.add_access_code("1234", "Family 2")
        assert result is False
    
    def test_lock_remove_access_code(self) -> None:
        lock = SmartLock("LK001", "Front Door", "Entrance")
        lock.add_access_code("1234", "Family")
        result = lock.remove_access_code("1234")
        assert result is True
    
    def test_lock_get_access_log(self) -> None:
        lock = SmartLock("LK001", "Front Door", "Entrance")
        lock.add_access_code("1234", "Family")
        lock.unlock("1234")
        log = lock.get_access_log()
        assert len(log) == 1
        assert log[0]["action"] == "unlock"
        assert log[0]["name"] == "Family"
    
    def test_lock_update_battery_level(self) -> None:
        lock = SmartLock("LK001", "Front Door", "Entrance")
        lock.update_battery_level(50)
        status = lock.get_status()
        assert status["battery_level"] == 50


class TestPolymorphism:
    """Tests demonstrating polymorphic behavior."""
    
    def test_polymorphic_devices(self) -> None:
        devices: list[SmartDevice] = [
            SmartDevice("D001", "Generic", "Room", 10.0),
            SmartLight("L001", "Light", "Room", 60.0),
            SmartThermostat("T001", "Thermo", "Hall", 50.0),
            SmartLock("LK001", "Door", "Entrance")
        ]
        
        # All can be turned on and off
        for device in devices:
            device.turn_on()
            assert device.is_on is True
            device.turn_off()
            assert device.is_on is False
    
    def test_polymorphic_status(self) -> None:
        devices: list[SmartDevice] = [
            SmartLight("L001", "Light", "Room", 60.0),
            SmartThermostat("T001", "Thermo", "Hall", 50.0),
            SmartLock("LK001", "Door", "Entrance")
        ]
        
        statuses = [d.get_status() for d in devices]
        assert "brightness" in statuses[0]
        assert "current_temp" in statuses[1]
        assert "is_locked" in statuses[2]
