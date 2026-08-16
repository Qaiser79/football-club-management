from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.club import Club
from app.models.organization import Organization
from app.schemas.club_schema import ClubCreate, ClubResponse,ClubUpdate, ClubListResponse

router = APIRouter(
    prefix="/club",
    tags=["Club"]
)

@router.post("/", response_model=ClubResponse,status_code=201)
def create_club(
    club: ClubCreate,
    db: Session=Depends(get_db)
):
    organization=(
        db.query(Organization)
        .filter(Organization.id==club.organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(
            status_code=404,
            detail= "Organization not found"
        )
    new_club=Club(
        organization_id=club.organization_id,
        name=club.name,
        short_name=club.short_name,
        country=club.country,
    )

    db.add(new_club)
    db.commit()
    db.refresh(new_club)

    return new_club

@router.get("/", response_model=ClubListResponse)
def get_clubs(
    page: int=Query(1, ge=1),
    limit: int=Query(10, ge=1, le=100),
    name: str | None=None,
    sort: str | None=None,
    organization_id: int | None = None,
    db: Session=Depends(get_db)
):
    query= db.query(Club)
    descending=False

    

    if name:
        query=query.filter(
            Club.name.ilike(f"%{name}%")
        )
    
    if organization_id is not None:
        organization = (
            db.query(Organization)
            .filter(Organization.id == organization_id)
            .first()
        )

        if not organization:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

    if organization_id is not None:
        query = query.filter(
            Club.organization_id == organization_id
        )

    if sort and sort.lstrip("-") not in [
            "name",
            "short_name",
            "created_at"
        ]:
            raise HTTPException(
                status_code=400,
                detail="Invalid sort field"
            )

    if sort and sort.startswith("-"):
        descending=True
        sort=sort[1:]

    if sort=="name":
        query=query.order_by(
            Club.name.desc() if descending else Club.name
        )

    elif sort=="short_name":
        query=query.order_by(
            Club.short_name.desc() if descending else Club.short_name
        )
    elif sort=="created_at":
        query=query.order_by(
            Club.created_at.desc() if descending else Club.created_at
        )

    total=query.count()
    pages=(total+limit-1)//limit
    offset= (page-1)*limit
    clubs=(
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": clubs,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages
    }

@router.get("/{club_id}", response_model=ClubResponse)
def get_club(
    club_id: int,
    db: Session=Depends(get_db)
):
    club=(
        db.query(Club)
        .filter(Club.id==club_id)
        .first()
    )

    if not club:
        raise HTTPException(
            status_code=404,
            detail="Club not found")
    return club
    

@router.delete("/{club_id}")
def delete_club(
    club_id: int,
    db: Session=Depends(get_db)
):
    club=(
        db.query(Club)
        .filter(Club.id==club_id)
        .first()
    )
    if not club:
        raise HTTPException(
            status_code=404,
            detail="Club not found")
    db.delete(club)
    db.commit()

    return {
        "message": "Club deleted Successfully"
    }

@router.put("/{club_id}", response_model=ClubResponse)
def update_club(
    club_id: int,
    club_data: ClubUpdate,
    db: Session=Depends(get_db)
):
    club=(
        db.query(Club)
        .filter(Club.id==club_id)
        .first()
    )
    if not club:
        raise HTTPException(
            status_code=404,
            detail="Club not Found")
    
    organization=(
        db.query(Organization)
        .filter(Organization.id==club_data.organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not Found"
        )

    club.organization_id=club_data.organization_id
    club.name=club_data.name
    club.short_name=club_data.short_name
    club.country=club_data.country

    db.commit()
    db.refresh(club)

    return club

@router.get("/{club_id}/teams")
def get_teams(
    club_id: int,
    db: Session = Depends(get_db)
):
    club=(
        db.query(Club)
        .filter(Club.id==club_id)
        .first()
    )
    if not club:
        raise HTTPException(
            status_code=404,
            detail="Club not found"
        )
    teams = club.teams
    return teams