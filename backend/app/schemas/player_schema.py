from datetime import datetime, date
from pydantic import BaseModel, Field

class PlayerCreate(BaseModel):
    team_id: int
    name: str=Field(
        min_length=2,
        max_length=100
    )
    position: str=Field(
        min_length=2,
        max_length=100
    )
    preferred_foot: str | None = None

    shirt_number: int | None = Field(
        default = None,
        ge=1,
        le=99
    )

    date_of_birth: date | None = None

    nationality: str | None = Field(
        default=None,
        max_length=100
    )

    phone: str | None= Field(
        default=None,
        max_length=30
    )

    email: str | None= Field(
            default=None,
            max_length=150
        )

    bio: str | None = None

    height: int | None = Field(
        default=None,
        ge=1
    )

    weight: int | None = Field(
        default=None,
        ge=1
    )

    joined_date: date | None = None

    profile_image: str | None = Field(
        default=None,
        max_length=500
    )

    status: str = "Active"

class TeamInfo(BaseModel):
    id: int
    name: str
    team_type: str

class PlayerResponse(BaseModel):
    id: int
    team_id: int
    name: str
    position: str
    preferred_foot: str | None
    shirt_number: int | None
    date_of_birth: date | None
    nationality: str | None
    phone: str | None
    email: str | None
    bio: str | None
    height: int | None
    weight: int | None
    joined_date: date | None
    profile_image: str | None
    status: str
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
    preferred_foot: str | None = None

    shirt_number: int | None = Field(
        default=None,
        ge=1,
        le=99
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

    height: int | None = Field(
        default=None,
        ge=1
    )

    weight: int | None = Field(
        default=None,
        ge=1
    )

    joined_date: date | None = None

    profile_image: str | None = Field(
        default=None,
        max_length=500
    )

    status: str = "Active"