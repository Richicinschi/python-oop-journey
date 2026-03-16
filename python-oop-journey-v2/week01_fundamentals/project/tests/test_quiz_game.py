"""
Unit tests for the CLI Quiz Game.

These tests verify the functionality of all quiz game functions.
Tests use mocking to simulate user input and capture output.

Run with: pytest week01_fundamentals/project/tests/test_quiz_game.py -v
"""

import sys
import io
from typing import Any
from unittest.mock import patch, MagicMock

# Import from reference_solution for testing
# When testing your solution, change this import
sys.path.insert(0, "week01_fundamentals/project/reference_solution")
from quiz_game import (
    load_questions,
    display_question,
    get_user_answer,
    check_answer,
    calculate_score,
    display_results,
    play_again,
    get_performance_message,
    QUESTIONS,
    OPTION_LETTERS,
)


class TestLoadQuestions:
    """Tests for the load_questions function."""
    
    def test_load_questions_returns_tuple(self) -> None:
        """Test that load_questions returns a tuple."""
        questions = load_questions()
        assert isinstance(questions, tuple)
    
    def test_load_questions_not_empty(self) -> None:
        """Test that loaded questions is not empty."""
        questions = load_questions()
        assert len(questions) > 0
    
    def test_load_questions_has_required_keys(self) -> None:
        """Test that each question has the required keys."""
        questions = load_questions()
        required_keys = {"question", "options", "answer"}
        
        for q in questions:
            assert isinstance(q, dict)
            assert required_keys.issubset(set(q.keys()))
    
    def test_load_questions_has_valid_answer(self) -> None:
        """Test that each question has a valid answer letter."""
        questions = load_questions()
        valid_answers = set(OPTION_LETTERS)
        
        for q in questions:
            assert q["answer"] in valid_answers
    
    def test_load_questions_has_four_options(self) -> None:
        """Test that each question has exactly 4 options."""
        questions = load_questions()
        
        for q in questions:
            assert len(q["options"]) == 4


class TestDisplayQuestion:
    """Tests for the display_question function."""
    
    def test_display_question_outputs_question(self, capsys: Any) -> None:
        """Test that display_question outputs the question text."""
        question = {
            "question": "What is the test question?",
            "options": ("A", "B", "C", "D"),
            "answer": "A"
        }
        display_question(question, 1, 5)
        
        captured = capsys.readouterr()
        assert "What is the test question?" in captured.out
    
    def test_display_question_shows_question_number(self, capsys: Any) -> None:
        """Test that display_question shows the question number."""
        question = {
            "question": "Test?",
            "options": ("A", "B", "C", "D"),
            "answer": "A"
        }
        display_question(question, 3, 10)
        
        captured = capsys.readouterr()
        assert "Question 3 of 10" in captured.out
    
    def test_display_question_shows_all_options(self, capsys: Any) -> None:
        """Test that display_question shows all four options."""
        question = {
            "question": "Test?",
            "options": ("Option A", "Option B", "Option C", "Option D"),
            "answer": "A"
        }
        display_question(question, 1, 1)
        
        captured = capsys.readouterr()
        assert "A) Option A" in captured.out
        assert "B) Option B" in captured.out
        assert "C) Option C" in captured.out
        assert "D) Option D" in captured.out


class TestGetUserAnswer:
    """Tests for the get_user_answer function."""
    
    def test_get_user_answer_accepts_uppercase(self) -> None:
        """Test that uppercase input is accepted."""
        with patch("builtins.input", return_value="A"):
            result = get_user_answer()
            assert result == "A"
    
    def test_get_user_answer_accepts_lowercase(self) -> None:
        """Test that lowercase input is converted to uppercase."""
        with patch("builtins.input", return_value="b"):
            result = get_user_answer()
            assert result == "B"
    
    def test_get_user_answer_handles_whitespace(self) -> None:
        """Test that whitespace is stripped from input."""
        with patch("builtins.input", return_value="  c  "):
            result = get_user_answer()
            assert result == "C"
    
    def test_get_user_answer_rejects_invalid_then_accepts_valid(self) -> None:
        """Test that invalid input is rejected and valid is accepted."""
        with patch("builtins.input", side_effect=["X", "Z", "A"]):
            result = get_user_answer()
            assert result == "A"
    
    def test_get_user_answer_rejects_empty_string(self) -> None:
        """Test that empty input is rejected."""
        with patch("builtins.input", side_effect=["", "B"]):
            result = get_user_answer()
            assert result == "B"


class TestCheckAnswer:
    """Tests for the check_answer function."""
    
    def test_check_answer_correct(self, capsys: Any) -> None:
        """Test that correct answer returns True."""
        result = check_answer("A", "A")
        assert result is True
        
        captured = capsys.readouterr()
        assert "Correct" in captured.out
    
    def test_check_answer_incorrect(self, capsys: Any) -> None:
        """Test that incorrect answer returns False."""
        result = check_answer("A", "B")
        assert result is False
        
        captured = capsys.readouterr()
        assert "Wrong" in captured.out or "correct answer was" in captured.out.lower()
    
    def test_check_answer_case_insensitive_correct(self) -> None:
        """Test that answer checking is case-insensitive."""
        result = check_answer("a", "A")
        assert result is True
        
        result = check_answer("B", "b")
        assert result is True
    
    def test_check_answer_shows_correct_answer_when_wrong(self, capsys: Any) -> None:
        """Test that wrong answer shows what the correct answer was."""
        check_answer("A", "C")
        
        captured = capsys.readouterr()
        assert "C" in captured.out


class TestCalculateScore:
    """Tests for the calculate_score function."""
    
    def test_calculate_score_perfect(self) -> None:
        """Test score calculation for perfect score."""
        result = calculate_score(10, 10)
        assert result == 100.0
    
    def test_calculate_score_zero(self) -> None:
        """Test score calculation for zero correct."""
        result = calculate_score(0, 10)
        assert result == 0.0
    
    def test_calculate_score_half(self) -> None:
        """Test score calculation for half correct."""
        result = calculate_score(5, 10)
        assert result == 50.0
    
    def test_calculate_score_handles_zero_total(self) -> None:
        """Test that zero total returns 0.0 (no division by zero)."""
        result = calculate_score(0, 0)
        assert result == 0.0
    
    def test_calculate_score_decimal(self) -> None:
        """Test score calculation with non-integer result."""
        result = calculate_score(1, 3)
        assert abs(result - 33.333) < 0.01  # Allow for floating point


class TestGetPerformanceMessage:
    """Tests for the get_performance_message function."""
    
    def test_performance_message_excellent(self) -> None:
        """Test message for excellent score (90-100)."""
        msg = get_performance_message(95)
        assert "excellent" in msg.lower() or "master" in msg.lower()
    
    def test_performance_message_good(self) -> None:
        """Test message for good score (70-89)."""
        msg = get_performance_message(75)
        assert "good" in msg.lower() or "job" in msg.lower()
    
    def test_performance_message_not_bad(self) -> None:
        """Test message for average score (50-69)."""
        msg = get_performance_message(60)
        assert "not bad" in msg.lower() or "room" in msg.lower()
    
    def test_performance_message_keep_practicing(self) -> None:
        """Test message for low score (0-49)."""
        msg = get_performance_message(30)
        assert "practicing" in msg.lower() or "better" in msg.lower()


class TestDisplayResults:
    """Tests for the display_results function."""
    
    def test_display_results_shows_score(self, capsys: Any) -> None:
        """Test that display_results shows the score."""
        display_results(7, 10, 70.0)
        
        captured = capsys.readouterr()
        assert "7/10" in captured.out or "7 / 10" in captured.out
    
    def test_display_results_shows_percentage(self, capsys: Any) -> None:
        """Test that display_results shows the percentage."""
        display_results(5, 10, 50.0)
        
        captured = capsys.readouterr()
        assert "50.0%" in captured.out or "50%" in captured.out
    
    def test_display_results_shows_message(self, capsys: Any) -> None:
        """Test that display_results shows a performance message."""
        display_results(9, 10, 90.0)
        
        captured = capsys.readouterr()
        # Should have some text beyond just numbers
        assert len(captured.out) > 20


class TestPlayAgain:
    """Tests for the play_again function."""
    
    def test_play_again_yes_lowercase(self) -> None:
        """Test that 'y' returns True."""
        with patch("builtins.input", return_value="y"):
            result = play_again()
            assert result is True
    
    def test_play_again_yes_uppercase(self) -> None:
        """Test that 'Y' returns True."""
        with patch("builtins.input", return_value="Y"):
            result = play_again()
            assert result is True
    
    def test_play_again_yes_full_word(self) -> None:
        """Test that 'yes' returns True."""
        with patch("builtins.input", return_value="yes"):
            result = play_again()
            assert result is True
    
    def test_play_again_no(self) -> None:
        """Test that 'n' returns False."""
        with patch("builtins.input", return_value="n"):
            result = play_again()
            assert result is False
    
    def test_play_again_any_other_input(self) -> None:
        """Test that any non-y input returns False."""
        with patch("builtins.input", return_value="maybe"):
            result = play_again()
            assert result is False
    
    def test_play_again_handles_whitespace(self) -> None:
        """Test that whitespace is handled properly."""
        with patch("builtins.input", return_value="  y  "):
            result = play_again()
            assert result is True


class TestIntegration:
    """Integration tests for the quiz game."""
    
    def test_full_game_flow(self, capsys: Any) -> None:
        """Test a complete game flow with all correct answers."""
        # Mock inputs: A, B, C, D, C, C, n (answers + play again no)
        answers = [q["answer"] for q in QUESTIONS]
        inputs = answers + ["n"]
        
        with patch("builtins.input", side_effect=inputs):
            from quiz_game import main
            main()
        
        captured = capsys.readouterr()
        # Should show final results
        assert "RESULTS" in captured.out or "Score" in captured.out
    
    def test_game_flow_with_incorrect_answers(self, capsys: Any) -> None:
        """Test game flow with some wrong answers."""
        # All wrong answers, then don't play again
        wrong_answers = ["X" if q["answer"] != "X" else "Y" for q in QUESTIONS]
        # Convert to valid inputs but wrong answers
        wrong_but_valid = []
        for q in QUESTIONS:
            for letter in OPTION_LETTERS:
                if letter != q["answer"]:
                    wrong_but_valid.append(letter)
                    break
        
        inputs = wrong_but_valid + ["n"]
        
        with patch("builtins.input", side_effect=inputs):
            from quiz_game import run_quiz
            run_quiz()
        
        captured = capsys.readouterr()
        assert "Wrong" in captured.out or "0" in captured.out


# Allow running tests directly
if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
