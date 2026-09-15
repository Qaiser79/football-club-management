from datetime import datetime, date
from pydantic import BaseModel, Field
from app.schemas.player_schema import TeamInfo

class CoachCreate(BaseModel):
    team_id: int

    name: str = Field(
        min_length=2,
        max_length=100
    )

    role: str = Field(
        min_length=2,
        max_length=100
    )

    date_of_birth: date | None = None

    nationality: str | None = Field(
        default=None,
        max_length=100
    )

    phone: str | None = Field(
        default=None,
        max_length=30
    )

    email: str | None = Field(
        default=None,
        max_length=150
    )

    bio: str | None = None

    joined_date: date | None = None

    status: str = "Active"

    profile_image: str | None = Field(
        default=None,
        max_length=500
    )


class CoachResponse(BaseModel):
    id: int
    team_id: int
    name: str
    role: str
    date_of_birth: date | None
    nationality: str | None
    phone: str | None
    email: str | None
    bio: str | None
    joined_date: date | None
    status: str
    profile_image: str | None
    created_at: datetime
    team: TeamInfo

    model_config = {
        "from_attributes": True
    }


class CoachListResponse(BaseModel):
    items: list[CoachResponse]
    page: int
    limit: int
    total: int
    pages: int


class CoachUpdate(BaseModel):
    team_id: int

    name: str = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    role: str = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    date_of_birth: date | None = None

    nationality: str | None = Field(
        default=None,
        max_length=100
    )

    phone: str | None = Field(
        default=None,
        max_length=30
    )

    email: str | None = Field(
        default=None,
        max_length=150
    )

    bio: str | None = None

    joined_date: date | None = None

    status: str = "Active"

    profile_image: str | None = Field(
        default=None,
        max_length=500
    )