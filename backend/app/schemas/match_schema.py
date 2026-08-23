from datetime import datetime

from pydantic import BaseModel, Field


class TeamInfo(BaseModel):
    id: int
    name: str
    team_type: str


class MatchCreate(BaseModel):
    team_id: int
    opponent_name: str = Field(
        min_length=2,
        max_length=100
    )
    match_date: datetime
    competition: str = Field(
        min_length=2,
        max_length=100
    )
    venue: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    is_home: bool
    our_score: int = Field(
        default=0,
        ge=0
    )
    opponent_score: int = Field(
        default=0,
        ge=0
    )
    status: str = Field(
        default="scheduled",
        min_length=2,
        max_length=20
    )


class MatchUpdate(BaseModel):
    team_id: int
    opponent_name: str = Field(
        min_length=2,
        max_length=100
    )
    match_date: datetime
    competition: str = Field(
        min_length=2,
        max_length=100
    )
    venue: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    is_home: bool
    our_score: int = Field(
        default=0,
        ge=0
    )
    opponent_score: int = Field(
        default=0,
        ge=0
    )
    status: str = Field(
        default="scheduled",
        min_length=2,
        max_length=20
    )


class MatchResponse(BaseModel):
    id: int
    team_id: int
    opponent_name: str
    match_date: datetime
    competition: str
    venue: str | None
    is_home: bool
    our_score: int
    opponent_score: int
    status: str
    created_at: datetime
    team: TeamInfo

    model_config = {
        "from_attributes": True
    }


class MatchListResponse(BaseModel):
    items: list[MatchResponse]
    page: int
    limit: int
    total: int
    pages: int