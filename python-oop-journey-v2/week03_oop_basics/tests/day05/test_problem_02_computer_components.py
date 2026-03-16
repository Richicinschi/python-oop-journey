"""Tests for Problem 02: Computer Components."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day05.problem_02_computer_components import (
    Computer,
    CPU,
    RAM,
    Storage,
)


class TestCPU:
    """Tests for CPU class."""
    
    def test_cpu_init(self) -> None:
        """Test CPU initialization."""
        cpu = CPU(8, 3.5)
        assert cpu.cores == 8
        assert cpu.clock_speed_ghz == 3.5
    
    def test_cpu_process(self) -> None:
        """Test CPU processing."""
        cpu = CPU(8, 3.5)
        result = cpu.process("compile code")
        assert "compile code" in result
        assert "8-core" in result
        assert "3.5 GHz" in result


class TestRAM:
    """Tests for RAM class."""
    
    def test_ram_init(self) -> None:
        """Test RAM initialization."""
        ram = RAM(16, 3200)
        assert ram.capacity_gb == 16
        assert ram.speed_mhz == 3200
    
    def test_ram_load_fits(self) -> None:
        """Test loading data that fits."""
        ram = RAM(16, 3200)
        assert ram.load(8) is True
        assert ram.load(16) is True
    
    def test_ram_load_too_large(self) -> None:
        """Test loading data that doesn't fit."""
        ram = RAM(16, 3200)
        assert ram.load(32) is False


class TestStorage:
    """Tests for Storage class."""
    
    def test_storage_init(self) -> None:
        """Test storage initialization."""
        storage = Storage(512, "SSD")
        assert storage.capacity_gb == 512
        assert storage.storage_type == "SSD"
    
    def test_storage_write(self) -> None:
        """Test writing to storage."""
        storage = Storage(512, "SSD")
        result = storage.write("data.txt")
        assert "Wrote" in result
        assert "SSD" in result


class TestComputer:
    """Tests for Computer class."""
    
    def test_computer_init(self) -> None:
        """Test computer initialization."""
        computer = Computer("Workstation")
        assert computer.name == "Workstation"
        assert computer.cpu is None
        assert computer.ram_modules == []
        assert computer.storage_devices == []
    
    def test_install_cpu(self) -> None:
        """Test installing CPU."""
        computer = Computer("Workstation")
        computer.install_cpu(8, 3.5)
        assert isinstance(computer.cpu, CPU)
        assert computer.cpu.cores == 8
    
    def test_add_ram(self) -> None:
        """Test adding RAM modules."""
        computer = Computer("Workstation")
        computer.add_ram(16, 3200)
        computer.add_ram(16, 3200)
        assert len(computer.ram_modules) == 2
        assert computer.ram_modules[0].capacity_gb == 16
    
    def test_add_storage(self) -> None:
        """Test adding storage devices."""
        computer = Computer("Workstation")
        computer.add_storage(512, "SSD")
        computer.add_storage(2000, "HDD")
        assert len(computer.storage_devices) == 2
        assert computer.storage_devices[0].storage_type == "SSD"
    
    def test_get_total_ram(self) -> None:
        """Test calculating total RAM."""
        computer = Computer("Workstation")
        computer.add_ram(16, 3200)
        computer.add_ram(8, 2400)
        assert computer.get_total_ram() == 24
    
    def test_get_total_storage(self) -> None:
        """Test calculating total storage."""
        computer = Computer("Workstation")
        computer.add_storage(512, "SSD")
        computer.add_storage(2000, "HDD")
        assert computer.get_total_storage() == 2512
    
    def test_boot_no_cpu(self) -> None:
        """Test booting without CPU."""
        computer = Computer("Workstation")
        result = computer.boot()
        assert "failed" in result.lower()
        assert "cpu" in result.lower()
    
    def test_boot_no_ram(self) -> None:
        """Test booting without RAM."""
        computer = Computer("Workstation")
        computer.install_cpu(8, 3.5)
        result = computer.boot()
        assert "failed" in result.lower()
        assert "ram" in result.lower()
    
    def test_boot_no_storage(self) -> None:
        """Test booting without storage."""
        computer = Computer("Workstation")
        computer.install_cpu(8, 3.5)
        computer.add_ram(16, 3200)
        result = computer.boot()
        assert "failed" in result.lower()
        assert "storage" in result.lower()
    
    def test_boot_success(self) -> None:
        """Test successful boot."""
        computer = Computer("Workstation")
        computer.install_cpu(8, 3.5)
        computer.add_ram(16, 3200)
        computer.add_storage(512, "SSD")
        result = computer.boot()
        assert "booted successfully" in result.lower()
        assert "8-core" in result
        assert "16GB" in result
        assert "512GB" in result
    
    def test_process_task_no_cpu(self) -> None:
        """Test processing without CPU."""
        computer = Computer("Workstation")
        result = computer.process_task("task")
        assert "cannot process" in result.lower()
    
    def test_process_task_with_cpu(self) -> None:
        """Test processing with CPU."""
        computer = Computer("Workstation")
        computer.install_cpu(8, 3.5)
        result = computer.process_task("compile")
        assert "compile" in result
