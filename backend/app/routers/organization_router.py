from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Organization
from app.schemas.organization_schema import (OrganizationCreate, OrganizationResponse,OrganizationUpdate, OrganizationListResponse)


router = APIRouter(
    prefix="/organization",
    tags=["Organization"]
)

@router.post("/",response_model=OrganizationResponse,status_code=201)
def create_organization(
    organization: OrganizationCreate,
    db: Session= Depends(get_db)
):
    new_organization= Organization(
        name=organization.name
    )

    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)

    return new_organization

@router.get("/", response_model=OrganizationListResponse)
def get_organizations(
    page: int=Query(1, ge=1),
    limit: int=Query(10, ge=1, le=100),
    name: str | None=None,
    sort: str | None=None,
    db: Session = Depends(get_db)
):
    query = db.query(Organization)
    descending = False



    if name:
        query=query.filter(
            Organization.name.ilike(f"%{name}%")
        )

    if sort and sort.lstrip("-") not in ["name", "created_at"]:
        raise HTTPException(
            status_code=400,
            detail = "Invalid sort field"
        )

    if sort and sort.startswith("-"):
        descending=True
        sort=sort[1:]

    if sort=="name":
        query=query.order_by(
            Organization.name.desc() if descending else Organization.name
        )
    
    elif sort=="created_at":
        query=query.order_by(
            Organization.created_at.desc() if descending else Organization.created_at
        )

    offset= (page-1)*limit
    total=query.count()
    pages=(total+limit-1)//limit
    organizations= (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {
        "items": organizations,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages
    }

@router.get("/{organization_id}",response_model=OrganizationResponse)
def get_organization(
    organization_id: int,
    db: Session = Depends(get_db)
):
    organization = (
        db.query(Organization)
        .filter(Organization.id==organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )
    return organization

@router.delete("/{organization_id}")
def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db)
):
    organization = (
        db.query(Organization)
        .filter(Organization.id==organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )
    db.delete(organization)
    db.commit()

    return {
        "message": "Organization deleted successfully"
    }

@router.put("/{organization_id}", response_model=OrganizationResponse)
def update_organization(
    organization_id: int,
    organization_data: OrganizationUpdate,
    db: Session = Depends(get_db)
):
    organization=(
        db.query(Organization)
        .filter(Organization.id==organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )
    organization.name=organization_data.name

    db.commit()
    db.refresh(organization)

    return organization

@router.get("/{organization_id}/clubs")
def get_clubs(
    organization_id: int,
    db: Session = Depends(get_db)
):
    organization=(
        db.query(Organization)
        .filter(Organization.id==organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )
    clubs= organization.clubs

    return clubs