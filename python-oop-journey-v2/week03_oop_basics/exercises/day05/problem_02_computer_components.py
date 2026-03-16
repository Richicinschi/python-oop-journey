"""Problem 02: Computer Components.

Implement a Computer class composed of CPU, RAM modules, and Storage devices.
This demonstrates composition where the computer owns its components.

Classes to implement:
- CPU: with attributes cores, clock_speed_ghz
- RAM: with attributes capacity_gb, speed_mhz
- Storage: with attributes capacity_gb, storage_type (SSD/HDD)
- Computer: composed of one CPU, multiple RAM modules, and multiple Storage devices

Methods required:
- CPU.process(task: str) -> str: returns processing status
- RAM.load(data_size: int) -> bool: returns True if data fits
- Storage.write(data: str) -> str: returns write confirmation
- Computer.get_total_ram() -> int: sum of all RAM capacities
- Computer.get_total_storage() -> int: sum of all storage capacities
- Computer.boot() -> str: checks all components and returns boot status
"""

from __future__ import annotations


class CPU:
    """CPU component of a computer."""
    
    def __init__(self, cores: int, clock_speed_ghz: float) -> None:
        # TODO: Initialize cores and clock_speed_ghz
        pass
    
    def process(self, task: str) -> str:
        # TODO: Return processing message with task and CPU specs
        pass


class RAM:
    """RAM module component of a computer."""
    
    def __init__(self, capacity_gb: int, speed_mhz: int) -> None:
        # TODO: Initialize capacity_gb and speed_mhz
        pass
    
    def load(self, data_size: int) -> bool:
        # TODO: Return True if data_size <= capacity_gb
        pass


class Storage:
    """Storage device component of a computer."""
    
    def __init__(self, capacity_gb: int, storage_type: str) -> None:
        # TODO: Initialize capacity_gb and storage_type (SSD or HDD)
        pass
    
    def write(self, data: str) -> str:
        # TODO: Return write confirmation message with storage type
        pass


class Computer:
    """A computer composed of CPU, RAM modules, and Storage devices."""
    
    def __init__(self, name: str) -> None:
        # TODO: Initialize name, cpu (None), ram_modules (empty list), storage_devices (empty list)
        pass
    
    def install_cpu(self, cores: int, clock_speed_ghz: float) -> None:
        # TODO: Create and assign CPU
        pass
    
    def add_ram(self, capacity_gb: int, speed_mhz: int) -> None:
        # TODO: Add RAM module to list
        pass
    
    def add_storage(self, capacity_gb: int, storage_type: str) -> None:
        # TODO: Add Storage device to list
        pass
    
    def get_total_ram(self) -> int:
        # TODO: Return sum of all RAM capacities
        pass
    
    def get_total_storage(self) -> int:
        # TODO: Return sum of all storage capacities
        pass
    
    def boot(self) -> str:
        # TODO: Check all components present and return boot status message
        pass
    
    def process_task(self, task: str) -> str:
        # TODO: Delegate to CPU if installed
        pass
