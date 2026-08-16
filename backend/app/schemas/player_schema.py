from datetime import datetime
from pydantic import BaseModel, Field

class PlayerCreate(BaseModel):
    team_id: int
    name: str=Field(
        default=None,
        min_length=2,
        max_length=100
    )
    position: str=Field(
        default=None,
        min_length=2,
        max_length=100
    )

class TeamInfo(BaseModel):
    id: int
    name: str
    team_type: str

class PlayerResponse(BaseModel):
    id: int
    team_id: int
    name: str
    position: str
    created_at: datetime
    team: TeamInfo
    model_config={
        "from_attributes": True
    }

class PlayerListResponse(BaseModel):
    items: list[PlayerResponse]
    page: int
    limit: int
    total: int
    pages: int

class PlayerUpdate(BaseModel):
    team_id: int
    name: str=Field(
        default=None,
        min_length=2,
        max_length=100
    )
    position: str=Field(
        default=None,
        min_length=2,
        max_length=100
    )