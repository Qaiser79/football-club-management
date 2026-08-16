from pydantic import BaseModel, Field
from datetime import datetime

class OrganizationCreate(BaseModel):
    name: str=Field(min_length=2, max_length=100)

class OrganizationResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

class OrganizationListResponse(BaseModel):
    items: list[OrganizationResponse]
    page: int
    limit: int
    total: int
    pages: int

class OrganizationUpdate(BaseModel):
    name: str=Field(min_length=2, max_length=100)