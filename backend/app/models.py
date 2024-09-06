from datetime import date, time
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Season(SQLModel, table=True):
    """
    Represents an entire season
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, description="Season years")

    matches: List["Match"] = Relationship(back_populates="season")


class Team(SQLModel, table=True):
    """
    Represents a football team.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, description="Name of the football team")
    
    # Relationships
    home_matches: List["Match"] = Relationship(
        back_populates="home_team",
        sa_relationship_kwargs={"foreign_keys": "Match.home_team_name"}
    )
    away_matches: List["Match"] = Relationship(
        back_populates="away_team",
        sa_relationship_kwargs={"foreign_keys": "Match.away_team_name"}
    )


class Referee(SQLModel, table=True):
    """
    Represents a match referee.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, description="Name of the referee")

    # Relationships
    matches: List["Match"] = Relationship(back_populates="referee")


class Match(SQLModel, table=True):
    """
    Represents a football match with detailed statistics and betting odds.
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    # Basic Match Information
    season_name: str = Field(foreign_key="season.name", description="The season year")
    season: "Season" = Relationship(back_populates="matches")
    division: str = Field(description="League Division")
    match_date: date = Field(description="Match Date (YYYY-MM-DD)")
    match_time: time = Field(description="Match Kick-off Time (HH:MM)")
    
    # Team Relationships
    home_team_name: str = Field(foreign_key="team.name", description="Name of the Home Team")
    away_team_name: str = Field(foreign_key="team.name", description="Name of the Away Team")
    home_team: "Team" = Relationship(back_populates="home_matches", sa_relationship_kwargs={"foreign_keys": "Match.home_team_name"})
    away_team: "Team" = Relationship(back_populates="away_matches", sa_relationship_kwargs={"foreign_keys": "Match.away_team_name"})
    
    # Referee Relationship
    referee_name: Optional[str] = Field(
        default=None, foreign_key="referee.name", description="ID of the Referee"
    )
    referee: Optional["Referee"] = Relationship(back_populates="matches")

    # Full Time Results
    full_time_home_goals: int = Field(description="Full Time Home Team Goals")
    full_time_away_goals: int = Field(description="Full Time Away Team Goals")
    full_time_result: str = Field(
        description="Full Time Result (H=Home Win, D=Draw, A=Away Win)"
    )

    # Half Time Results
    half_time_home_goals: int = Field(description="Half Time Home Team Goals")
    half_time_away_goals: int = Field(description="Half Time Away Team Goals")
    half_time_result: str = Field(
        description="Half Time Result (H=Home Win, D=Draw, A=Away Win)"
    )

    # Match Statistics
    home_shots: Optional[int] = Field(default=None, description="Home Team Shots")
    away_shots: Optional[int] = Field(default=None, description="Away Team Shots")
    home_shots_on_target: Optional[int] = Field(
        default=None, description="Home Team Shots on Target"
    )
    away_shots_on_target: Optional[int] = Field(
        default=None, description="Away Team Shots on Target"
    )
    home_fouls: Optional[int] = Field(
        default=None, description="Home Team Fouls Committed"
    )
    away_fouls: Optional[int] = Field(
        default=None, description="Away Team Fouls Committed"
    )
    home_corners: Optional[int] = Field(default=None, description="Home Team Corners")
    away_corners: Optional[int] = Field(default=None, description="Away Team Corners")
    home_yellow_cards: Optional[int] = Field(
        default=None, description="Home Team Yellow Cards"
    )
    away_yellow_cards: Optional[int] = Field(
        default=None, description="Away Team Yellow Cards"
    )
    home_red_cards: Optional[int] = Field(
        default=None, description="Home Team Red Cards"
    )
    away_red_cards: Optional[int] = Field(
        default=None, description="Away Team Red Cards"
    )

    # Betting Odds - 1X2 (Match Result)
    bet365_home_win_odds: Optional[float] = Field(
        default=None, description="Bet365 Home Win Odds"
    )
    bet365_draw_odds: Optional[float] = Field(
        default=None, description="Bet365 Draw Odds"
    )
    bet365_away_win_odds: Optional[float] = Field(
        default=None, description="Bet365 Away Win Odds"
    )
    bet_and_win_home_win_odds: Optional[float] = Field(
        default=None, description="Bet&Win Home Win Odds"
    )
    bet_and_win_draw_odds: Optional[float] = Field(
        default=None, description="Bet&Win Draw Odds"
    )
    bet_and_win_away_win_odds: Optional[float] = Field(
        default=None, description="Bet&Win Away Win Odds"
    )
    interwetten_home_win_odds: Optional[float] = Field(
        default=None, description="Interwetten Home Win Odds"
    )
    interwetten_draw_odds: Optional[float] = Field(
        default=None, description="Interwetten Draw Odds"
    )
    interwetten_away_win_odds: Optional[float] = Field(
        default=None, description="Interwetten Away Win Odds"
    )
    pinnacle_home_win_odds: Optional[float] = Field(
        default=None, description="Pinnacle Home Win Odds"
    )
    pinnacle_draw_odds: Optional[float] = Field(
        default=None, description="Pinnacle Draw Odds"
    )
    pinnacle_away_win_odds: Optional[float] = Field(
        default=None, description="Pinnacle Away Win Odds"
    )
    william_hill_home_win_odds: Optional[float] = Field(
        default=None, description="William Hill Home Win Odds"
    )
    william_hill_draw_odds: Optional[float] = Field(
        default=None, description="William Hill Draw Odds"
    )
    william_hill_away_win_odds: Optional[float] = Field(
        default=None, description="William Hill Away Win Odds"
    )
    vc_bet_home_win_odds: Optional[float] = Field(
        default=None, description="VC Bet Home Win Odds"
    )
    vc_bet_draw_odds: Optional[float] = Field(
        default=None, description="VC Bet Draw Odds"
    )
    vc_bet_away_win_odds: Optional[float] = Field(
        default=None, description="VC Bet Away Win Odds"
    )
    max_home_win_odds: Optional[float] = Field(
        default=None, description="Market Maximum Home Win Odds"
    )
    max_draw_odds: Optional[float] = Field(
        default=None, description="Market Maximum Draw Odds"
    )
    max_away_win_odds: Optional[float] = Field(
        default=None, description="Market Maximum Away Win Odds"
    )
    avg_home_win_odds: Optional[float] = Field(
        default=None, description="Market Average Home Win Odds"
    )
    avg_draw_odds: Optional[float] = Field(
        default=None, description="Market Average Draw Odds"
    )
    avg_away_win_odds: Optional[float] = Field(
        default=None, description="Market Average Away Win Odds"
    )

    # Betting Odds - Total Goals Over/Under 2.5
    bet365_over_2_5_odds: Optional[float] = Field(
        default=None, description="Bet365 Over 2.5 Goals Odds"
    )
    bet365_under_2_5_odds: Optional[float] = Field(
        default=None, description="Bet365 Under 2.5 Goals Odds"
    )
    pinnacle_over_2_5_odds: Optional[float] = Field(
        default=None, description="Pinnacle Over 2.5 Goals Odds"
    )
    pinnacle_under_2_5_odds: Optional[float] = Field(
        default=None, description="Pinnacle Under 2.5 Goals Odds"
    )
    max_over_2_5_odds: Optional[float] = Field(
        default=None, description="Market Maximum Over 2.5 Goals Odds"
    )
    max_under_2_5_odds: Optional[float] = Field(
        default=None, description="Market Maximum Under 2.5 Goals Odds"
    )
    avg_over_2_5_odds: Optional[float] = Field(
        default=None, description="Market Average Over 2.5 Goals Odds"
    )
    avg_under_2_5_odds: Optional[float] = Field(
        default=None, description="Market Average Under 2.5 Goals Odds"
    )

    # Betting Odds - Asian Handicap
    asian_handicap_line: Optional[float] = Field(
        default=None, description="Asian Handicap Line (Home Team)"
    )
    bet365_asian_handicap_home_odds: Optional[float] = Field(
        default=None, description="Bet365 Asian Handicap Home Team Odds"
    )
    bet365_asian_handicap_away_odds: Optional[float] = Field(
        default=None, description="Bet365 Asian Handicap Away Team Odds"
    )
    pinnacle_asian_handicap_home_odds: Optional[float] = Field(
        default=None, description="Pinnacle Asian Handicap Home Team Odds"
    )
    pinnacle_asian_handicap_away_odds: Optional[float] = Field(
        default=None, description="Pinnacle Asian Handicap Away Team Odds"
    )
    max_asian_handicap_home_odds: Optional[float] = Field(
        default=None, description="Market Maximum Asian Handicap Home Team Odds"
    )
    max_asian_handicap_away_odds: Optional[float] = Field(
        default=None, description="Market Maximum Asian Handicap Away Team Odds"
    )
    avg_asian_handicap_home_odds: Optional[float] = Field(
        default=None, description="Market Average Asian Handicap Home Team Odds"
    )
    avg_asian_handicap_away_odds: Optional[float] = Field(
        default=None, description="Market Average Asian Handicap Away Team Odds"
    )
