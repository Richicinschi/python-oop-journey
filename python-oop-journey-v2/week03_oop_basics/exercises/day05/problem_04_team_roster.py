"""Problem 04: Team Roster.

Implement a Team class that aggregates Players and has a Coach.
This demonstrates both aggregation (players) and composition (coach).

Classes to implement:
- Player: with attributes name, position, jersey_number, team (optional)
- Coach: with attributes name, specialty
- Team: aggregates Players, composed of Coach

Methods required:
- Player.join_team(team_name: str) / Player.leave_team()
- Coach.train_team() -> str
- Team.add_player(player: Player) - aggregation
- Team.remove_player(jersey_number: int) -> bool
- Team.set_coach(coach: Coach) - composition
- Team.get_roster() -> list[str]
"""

from __future__ import annotations
from typing import Optional


class Player:
    """A player who can be on a team."""
    
    def __init__(self, name: str, position: str, jersey_number: int) -> None:
        # TODO: Initialize name, position, jersey_number, team (None)
        pass
    
    def join_team(self, team_name: str) -> str:
        # TODO: Set team and return join message
        pass
    
    def leave_team(self) -> str:
        # TODO: Clear team and return leave message
        pass


class Coach:
    """A coach for a team (composition)."""
    
    def __init__(self, name: str, specialty: str) -> None:
        # TODO: Initialize name and specialty
        pass
    
    def train_team(self) -> str:
        # TODO: Return training message with specialty
        pass


class Team:
    """A team composed of a coach, aggregating players."""
    
    def __init__(self, name: str, city: str) -> None:
        # TODO: Initialize name, city, coach (None), players dict (jersey -> Player)
        pass
    
    def set_coach(self, coach: Coach) -> str:
        # TODO: Set coach and return confirmation
        pass
    
    def add_player(self, player: Player) -> str:
        # TODO: Add player to roster if jersey not taken, update player's team
        pass
    
    def remove_player(self, jersey_number: int) -> bool:
        # TODO: Remove player by jersey number, return True if removed
        pass
    
    def find_player(self, jersey_number: int) -> Optional[Player]:
        # TODO: Return player by jersey number or None
        pass
    
    def get_roster(self) -> list[str]:
        # TODO: Return list of player descriptions
        pass
    
    def train(self) -> str:
        # TODO: Delegate to coach if exists, else error message
        pass
