"""Solution for Problem 04: Team Roster.

Team with Players and Coach - demonstrates both aggregation (players)
and composition (coach) in the same class.
"""

from __future__ import annotations
from typing import Optional


class Player:
    """A player who can be on a team.
    
    Players exist independently and can move between teams.
    """
    
    def __init__(self, name: str, position: str, jersey_number: int) -> None:
        """Initialize the player.
        
        Args:
            name: Player name.
            position: Playing position.
            jersey_number: Jersey number.
        """
        self.name = name
        self.position = position
        self.jersey_number = jersey_number
        self.team: str | None = None
    
    def join_team(self, team_name: str) -> str:
        """Join a team.
        
        Args:
            team_name: Name of the team to join.
            
        Returns:
            Join confirmation message.
        """
        self.team = team_name
        return f"{self.name} joined {team_name}"
    
    def leave_team(self) -> str:
        """Leave current team.
        
        Returns:
            Leave confirmation message.
        """
        if self.team is None:
            return f"{self.name} is not on a team"
        old_team = self.team
        self.team = None
        return f"{self.name} left {old_team}"


class Coach:
    """A coach for a team (composition).
    
    The coach is composed by the team - they exist only while
    coaching that specific team.
    """
    
    def __init__(self, name: str, specialty: str) -> None:
        """Initialize the coach.
        
        Args:
            name: Coach name.
            specialty: Coaching specialty.
        """
        self.name = name
        self.specialty = specialty
    
    def train_team(self) -> str:
        """Train the team.
        
        Returns:
            Training message.
        """
        return f"Coach {self.name} is training the team in {self.specialty}"


class Team:
    """A team composed of a coach, aggregating players.
    
    The coach is composed (created/managed by the team) while
    players are aggregated (exist independently).
    """
    
    def __init__(self, name: str, city: str) -> None:
        """Initialize the team.
        
        Args:
            name: Team name.
            city: Team city.
        """
        self.name = name
        self.city = city
        self.coach: Coach | None = None
        self.players: dict[int, Player] = {}  # jersey_number -> Player
    
    def set_coach(self, coach: Coach) -> str:
        """Set the team's coach.
        
        Args:
            coach: Coach to set (composition - coach is passed in but managed here).
            
        Returns:
            Confirmation message.
        """
        self.coach = coach
        return f"{coach.name} is now coaching {self.name}"
    
    def add_player(self, player: Player) -> str:
        """Add a player to the team.
        
        Args:
            player: Player to add (aggregation).
            
        Returns:
            Status message.
        """
        if player.jersey_number in self.players:
            return f"Jersey number {player.jersey_number} is already taken"
        
        self.players[player.jersey_number] = player
        player.join_team(self.name)
        return f"{player.name} added to {self.name} with jersey #{player.jersey_number}"
    
    def remove_player(self, jersey_number: int) -> bool:
        """Remove a player from the team.
        
        Args:
            jersey_number: Jersey number of player to remove.
            
        Returns:
            True if player was removed, False if not found.
        """
        player = self.players.get(jersey_number)
        if player is None:
            return False
        
        player.leave_team()
        del self.players[jersey_number]
        return True
    
    def find_player(self, jersey_number: int) -> Optional[Player]:
        """Find a player by jersey number.
        
        Args:
            jersey_number: Jersey number to search for.
            
        Returns:
            Player if found, None otherwise.
        """
        return self.players.get(jersey_number)
    
    def get_roster(self) -> list[str]:
        """Get the team roster.
        
        Returns:
            List of player description strings.
        """
        if not self.players:
            return ["No players on the team"]
        
        roster = []
        for number in sorted(self.players.keys()):
            player = self.players[number]
            roster.append(f"#{number}: {player.name} ({player.position})")
        return roster
    
    def train(self) -> str:
        """Train the team.
        
        Returns:
            Training message or error if no coach.
        """
        if self.coach is None:
            return f"{self.name} has no coach to lead training"
        return self.coach.train_team()
    
    def get_player_count(self) -> int:
        """Get number of players on the team.
        
        Returns:
            Player count.
        """
        return len(self.players)
