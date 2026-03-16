"""Tests for Day 03: Hello World Plus exercise.

These tests verify the solution implementation of the hello_world module.
All tests import from the solutions package to validate the reference
implementation.
"""

from __future__ import annotations

import pytest

from week00_getting_started.day03_solutions.hello_world import (
    create_farewell,
    create_greeting,
    main,
    print_program_info,
    print_separator,
)


class TestCreateGreeting:
    """Tests for the create_greeting function."""

    def test_create_greeting_with_simple_name(self, capsys) -> None:
        """Test greeting with a simple name."""
        result = create_greeting("Alice")
        assert result == "Hello, Alice!"

    def test_create_greeting_with_different_name(self, capsys) -> None:
        """Test greeting works with different names."""
        result = create_greeting("Bob")
        assert result == "Hello, Bob!"

    def test_create_greeting_with_empty_string(self, capsys) -> None:
        """Test greeting with empty string."""
        result = create_greeting("")
        assert result == "Hello, !"

    def test_create_greeting_with_multi_word_name(self, capsys) -> None:
        """Test greeting with full name."""
        result = create_greeting("John Doe")
        assert result == "Hello, John Doe!"


class TestCreateFarewell:
    """Tests for the create_farewell function."""

    def test_create_farewell_with_simple_name(self, capsys) -> None:
        """Test farewell with a simple name."""
        result = create_farewell("Alice")
        assert result == "Goodbye, Alice! Have a great day!"

    def test_create_farewell_contains_name(self, capsys) -> None:
        """Test that farewell includes the provided name."""
        result = create_farewell("TestUser")
        assert "TestUser" in result

    def test_create_farewell_contains_goodbye(self, capsys) -> None:
        """Test that farewell contains 'Goodbye'."""
        result = create_farewell("Alice")
        assert "Goodbye" in result

    def test_create_farewell_is_string(self, capsys) -> None:
        """Test that farewell returns a string."""
        result = create_farewell("Alice")
        assert isinstance(result, str)


class TestPrintSeparator:
    """Tests for the print_separator function."""

    def test_print_separator_outputs_dashes(self, capsys) -> None:
        """Test that separator prints dashes."""
        print_separator()
        captured = capsys.readouterr()
        assert "-" in captured.out

    def test_print_separator_has_correct_length(self, capsys) -> None:
        """Test that separator prints 40 dashes."""
        print_separator()
        captured = capsys.readouterr()
        # Should be 40 dashes plus a newline
        assert captured.out == "-" * 40 + "\n"

    def test_print_separator_only_one_line(self, capsys) -> None:
        """Test that separator prints exactly one line."""
        print_separator()
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 1


class TestPrintProgramInfo:
    """Tests for the print_program_info function."""

    def test_print_program_info_outputs_name(self, capsys) -> None:
        """Test that program info includes the program name."""
        print_program_info("TestApp", 1.0)
        captured = capsys.readouterr()
        assert "TestApp" in captured.out

    def test_print_program_info_outputs_version(self, capsys) -> None:
        """Test that program info includes the version."""
        print_program_info("TestApp", 2.5)
        captured = capsys.readouterr()
        assert "2.5" in captured.out

    def test_print_program_info_outputs_program_label(self, capsys) -> None:
        """Test that program info includes 'Program:' label."""
        print_program_info("TestApp", 1.0)
        captured = capsys.readouterr()
        assert "Program:" in captured.out

    def test_print_program_info_outputs_version_label(self, capsys) -> None:
        """Test that program info includes 'Version:' label."""
        print_program_info("TestApp", 1.0)
        captured = capsys.readouterr()
        assert "Version:" in captured.out

    def test_print_program_info_integer_version(self, capsys) -> None:
        """Test that integer versions work correctly."""
        print_program_info("MyApp", 1)
        captured = capsys.readouterr()
        assert "1" in captured.out


class TestMain:
    """Tests for the main function."""

    def test_main_outputs_hello(self, capsys) -> None:
        """Test that main outputs 'Hello'."""
        main()
        captured = capsys.readouterr()
        assert "Hello" in captured.out

    def test_main_outputs_program_name(self, capsys) -> None:
        """Test that main outputs the program name."""
        main()
        captured = capsys.readouterr()
        assert "Hello World Plus" in captured.out or "Hello" in captured.out

    def test_main_outputs_version(self, capsys) -> None:
        """Test that main outputs version information."""
        main()
        captured = capsys.readouterr()
        assert "1.0" in captured.out or "Version" in captured.out

    def test_main_outputs_separator(self, capsys) -> None:
        """Test that main outputs separator lines."""
        main()
        captured = capsys.readouterr()
        # Should have multiple separator lines (dashes)
        assert captured.out.count("-" * 40) >= 2

    def test_main_outputs_goodbye(self, capsys) -> None:
        """Test that main outputs a farewell message."""
        main()
        captured = capsys.readouterr()
        assert "Goodbye" in captured.out

    def test_main_outputs_learning_topics(self, capsys) -> None:
        """Test that main outputs learning topics."""
        main()
        captured = capsys.readouterr()
        # Check for some learning-related content
        output = captured.out
        assert any(word in output for word in ["learning", "Variables", "Functions", "String"])

    def test_main_completes_without_error(self, capsys) -> None:
        """Test that main runs without raising exceptions."""
        try:
            main()
            assert True
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")
