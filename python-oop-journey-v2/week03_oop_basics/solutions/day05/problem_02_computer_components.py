"""Solution for Problem 02: Computer Components.

Computer with CPU, RAM, Storage - demonstrates composition with
collections of components.
"""

from __future__ import annotations


class CPU:
    """CPU component of a computer."""
    
    def __init__(self, cores: int, clock_speed_ghz: float) -> None:
        """Initialize the CPU.
        
        Args:
            cores: Number of CPU cores.
            clock_speed_ghz: Clock speed in gigahertz.
        """
        self.cores = cores
        self.clock_speed_ghz = clock_speed_ghz
    
    def process(self, task: str) -> str:
        """Process a task.
        
        Args:
            task: Description of the task to process.
            
        Returns:
            Processing confirmation message.
        """
        return f"Processing '{task}' on {self.cores}-core CPU @ {self.clock_speed_ghz} GHz"


class RAM:
    """RAM module component of a computer."""
    
    def __init__(self, capacity_gb: int, speed_mhz: int) -> None:
        """Initialize the RAM module.
        
        Args:
            capacity_gb: Memory capacity in gigabytes.
            speed_mhz: Memory speed in megahertz.
        """
        self.capacity_gb = capacity_gb
        self.speed_mhz = speed_mhz
    
    def load(self, data_size: int) -> bool:
        """Check if data can fit in RAM.
        
        Args:
            data_size: Size of data to load in GB.
            
        Returns:
            True if data fits, False otherwise.
        """
        return data_size <= self.capacity_gb


class Storage:
    """Storage device component of a computer."""
    
    def __init__(self, capacity_gb: int, storage_type: str) -> None:
        """Initialize the storage device.
        
        Args:
            capacity_gb: Storage capacity in gigabytes.
            storage_type: Type of storage ('SSD' or 'HDD').
        """
        self.capacity_gb = capacity_gb
        self.storage_type = storage_type
    
    def write(self, data: str) -> str:
        """Write data to storage.
        
        Args:
            data: Data to write.
            
        Returns:
            Write confirmation message.
        """
        return f"Wrote '{data}' to {self.storage_type}"


class Computer:
    """A computer composed of CPU, RAM modules, and Storage devices.
    
    This demonstrates composition where the computer creates and manages
    multiple components of different types.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize the computer.
        
        Args:
            name: Computer name/identifier.
        """
        self.name = name
        self.cpu: CPU | None = None
        self.ram_modules: list[RAM] = []
        self.storage_devices: list[Storage] = []
    
    def install_cpu(self, cores: int, clock_speed_ghz: float) -> None:
        """Install a CPU.
        
        Args:
            cores: Number of cores.
            clock_speed_ghz: Clock speed in GHz.
        """
        self.cpu = CPU(cores, clock_speed_ghz)
    
    def add_ram(self, capacity_gb: int, speed_mhz: int) -> None:
        """Add a RAM module.
        
        Args:
            capacity_gb: Capacity in GB.
            speed_mhz: Speed in MHz.
        """
        self.ram_modules.append(RAM(capacity_gb, speed_mhz))
    
    def add_storage(self, capacity_gb: int, storage_type: str) -> None:
        """Add a storage device.
        
        Args:
            capacity_gb: Capacity in GB.
            storage_type: Type of storage ('SSD' or 'HDD').
        """
        self.storage_devices.append(Storage(capacity_gb, storage_type))
    
    def get_total_ram(self) -> int:
        """Get total RAM capacity.
        
        Returns:
            Sum of all RAM module capacities in GB.
        """
        return sum(ram.capacity_gb for ram in self.ram_modules)
    
    def get_total_storage(self) -> int:
        """Get total storage capacity.
        
        Returns:
            Sum of all storage device capacities in GB.
        """
        return sum(storage.capacity_gb for storage in self.storage_devices)
    
    def boot(self) -> str:
        """Boot the computer.
        
        Returns:
            Boot status message.
        """
        if self.cpu is None:
            return "Boot failed: No CPU installed"
        if len(self.ram_modules) == 0:
            return "Boot failed: No RAM installed"
        if len(self.storage_devices) == 0:
            return "Boot failed: No storage installed"
        
        return (
            f"{self.name} booted successfully with "
            f"{self.cpu.cores}-core CPU, "
            f"{self.get_total_ram()}GB RAM, "
            f"{self.get_total_storage()}GB storage"
        )
    
    def process_task(self, task: str) -> str:
        """Process a task on the CPU.
        
        Args:
            task: Task description.
            
        Returns:
            Processing result or error message.
        """
        if self.cpu is None:
            return "Cannot process: No CPU installed"
        return self.cpu.process(task)
