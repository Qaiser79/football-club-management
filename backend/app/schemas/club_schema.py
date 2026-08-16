from datetime import datetime
from pydantic import BaseModel, Field

class ClubCreate(BaseModel):
    organization_id: int
    name: str=Field(min_length=2, max_length=100)
    short_name: str | None=Field(
        default=None,
        min_length=2,
        max_length=20
    )
    country: str | None=Field(
        default=None,
        min_length=2,
        max_length=100
    )

class OrganizationInfo(BaseModel):
    id: int
    name: str

class ClubResponse(BaseModel):
    id: int
    organization_id: int
    name: str=Field(min_length=2, max_length=100)
    short_name: str | None
    country: str | None
    created_at: datetime
    organization: OrganizationInfo
    model_config={
        "from_attributes": True
    }

class ClubListResponse(BaseModel):
    items: list[ClubResponse]
    page: int
    limit: int
    total: int
    pages: int

class ClubUpdate(BaseModel):
    organization_id: int
    name: str=Field(min_length=2, max_length=100)
    short_name: str | None=Field(
        default=None,
        min_length=2,
        max_length=20
    )
    country: str | None=Field(
        default= None,
        min_length=2,
        max_length=100
    )
