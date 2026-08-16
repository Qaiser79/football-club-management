from pydantic import BaseModel, Field
from datetime import datetime


class TeamCreate(BaseModel):
    
    club_id: int
    name: str=Field(
        default=None,
        min_length=2,
        max_length=100
    )
    team_type: str=Field(
        default=None,
        min_length=2,
        max_length=100
    )

class ClubInfo(BaseModel):
    id: int
    name:str
    short_name:str | None
    country: str | None

class TeamResponse(BaseModel):
    id: int
    club_id: int
    name: str
    team_type: str
    created_at: datetime
    club: ClubInfo
    model_config={
        "from_attributes":True
    }

class TeamListResponse(BaseModel):
    items: list[TeamResponse]
    page: int
    limit: int
    total: int
    pages: int

class TeamUpdate(BaseModel):
    club_id: int
    name: str=Field(
        default=None,
        min_length=2,
        max_length=100
    )
    team_type: str=Field(
        default=None,
        min_length=2,
        max_length=100
    )