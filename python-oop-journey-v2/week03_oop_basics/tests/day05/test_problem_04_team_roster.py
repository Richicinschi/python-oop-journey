"""Tests for Problem 04: Team Roster."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day05.problem_04_team_roster import (
    Player,
    Coach,
    Team,
)


class TestPlayer:
    """Tests for Player class."""
    
    def test_player_init(self) -> None:
        """Test player initialization."""
        player = Player("John Smith", "Forward", 10)
        assert player.name == "John Smith"
        assert player.position == "Forward"
        assert player.jersey_number == 10
        assert player.team is None
    
    def test_player_join_team(self) -> None:
        """Test joining a team."""
        player = Player("John Smith", "Forward", 10)
        result = player.join_team("Lions")
        assert "joined" in result.lower()
        assert player.team == "Lions"
    
    def test_player_leave_team(self) -> None:
        """Test leaving a team."""
        player = Player("John Smith", "Forward", 10)
        player.join_team("Lions")
        result = player.leave_team()
        assert "left" in result.lower()
        assert player.team is None
    
    def test_player_leave_no_team(self) -> None:
        """Test leaving when not on a team."""
        player = Player("John Smith", "Forward", 10)
        result = player.leave_team()
        assert "not on a team" in result.lower()


class TestCoach:
    """Tests for Coach class."""
    
    def test_coach_init(self) -> None:
        """Test coach initialization."""
        coach = Coach("Mike Brown", "Defense")
        assert coach.name == "Mike Brown"
        assert coach.specialty == "Defense"
    
    def test_coach_train_team(self) -> None:
        """Test training the team."""
        coach = Coach("Mike Brown", "Defense")
        result = coach.train_team()
        assert "training" in result.lower()
        assert "defense" in result.lower()


class TestTeam:
    """Tests for Team class."""
    
    def test_team_init(self) -> None:
        """Test team initialization."""
        team = Team("Lions", "New York")
        assert team.name == "Lions"
        assert team.city == "New York"
        assert team.coach is None
        assert team.players == {}
    
    def test_set_coach(self) -> None:
        """Test setting a coach."""
        team = Team("Lions", "New York")
        coach = Coach("Mike Brown", "Defense")
        result = team.set_coach(coach)
        assert team.coach is coach
        assert "coaching" in result.lower()
    
    def test_add_player(self) -> None:
        """Test adding a player."""
        team = Team("Lions", "New York")
        player = Player("John Smith", "Forward", 10)
        result = team.add_player(player)
        assert "added" in result.lower()
        assert 10 in team.players
        assert player.team == "Lions"
    
    def test_add_player_duplicate_jersey(self) -> None:
        """Test adding player with duplicate jersey."""
        team = Team("Lions", "New York")
        player1 = Player("John Smith", "Forward", 10)
        player2 = Player("Jane Doe", "Guard", 10)
        team.add_player(player1)
        result = team.add_player(player2)
        assert "already taken" in result.lower()
    
    def test_remove_player(self) -> None:
        """Test removing a player."""
        team = Team("Lions", "New York")
        player = Player("John Smith", "Forward", 10)
        team.add_player(player)
        result = team.remove_player(10)
        assert result is True
        assert 10 not in team.players
        assert player.team is None
    
    def test_remove_player_not_found(self) -> None:
        """Test removing non-existent player."""
        team = Team("Lions", "New York")
        result = team.remove_player(99)
        assert result is False
    
    def test_find_player(self) -> None:
        """Test finding a player."""
        team = Team("Lions", "New York")
        player = Player("John Smith", "Forward", 10)
        team.add_player(player)
        found = team.find_player(10)
        assert found is player
    
    def test_find_player_not_found(self) -> None:
        """Test finding non-existent player."""
        team = Team("Lions", "New York")
        found = team.find_player(99)
        assert found is None
    
    def test_get_roster(self) -> None:
        """Test getting roster."""
        team = Team("Lions", "New York")
        player1 = Player("John Smith", "Forward", 10)
        player2 = Player("Jane Doe", "Guard", 5)
        team.add_player(player1)
        team.add_player(player2)
        roster = team.get_roster()
        assert len(roster) == 2
        assert "#5" in roster[0]  # Sorted by jersey
        assert "#10" in roster[1]
    
    def test_get_roster_empty(self) -> None:
        """Test getting empty roster."""
        team = Team("Lions", "New York")
        roster = team.get_roster()
        assert roster == ["No players on the team"]
    
    def test_train_with_coach(self) -> None:
        """Test training with a coach."""
        team = Team("Lions", "New York")
        coach = Coach("Mike Brown", "Defense")
        team.set_coach(coach)
        result = team.train()
        assert "training" in result.lower()
    
    def test_train_without_coach(self) -> None:
        """Test training without a coach."""
        team = Team("Lions", "New York")
        result = team.train()
        assert "no coach" in result.lower()
    
    def test_get_player_count(self) -> None:
        """Test getting player count."""
        team = Team("Lions", "New York")
        assert team.get_player_count() == 0
        team.add_player(Player("John", "Forward", 10))
        assert team.get_player_count() == 1
