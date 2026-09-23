from datetime import datetime

from pydantic import BaseModel, Field


class Player(BaseModel):
    user_id: str
    display_name: str
    team_id: str


class Team(BaseModel):
    team_id: str
    name: str
    players: list[Player] = Field(default_factory=list)


class PlayusGame(BaseModel):
    game_id: str
    group_game_id: str
    game_day: int | None = None
    timestamp: datetime | None = None


class PlayerScore(BaseModel):
    score_id: str
    user_id: str
    group_id: str
    group_game_id: str
    game_id: str | None = None
    score: int
    scored_at: datetime | None = None
    score_source: str | None = None


class TeamBonus(BaseModel):
    team_id: str
    bonus_type: str
    points: int
    reason: str
    game_day: int | None = None
    related_user_id: str | None = None


class LeaderboardEntry(BaseModel):
    rank: int
    identifier: str
    score: int
