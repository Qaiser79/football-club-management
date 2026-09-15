from fastapi import HTTPException, APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.team import Team
from app.models.coach import Coach
from app.schemas.coach_schema import (
    CoachCreate,
    CoachResponse,
    CoachListResponse,
)

router = APIRouter(
    prefix="/coach",
    tags=["Coach"]
)

@router.post("/", response_model=CoachResponse, status_code=201)
def create_coach(
    coach: CoachCreate,
    db: Session=Depends(get_db)
):
    team = (
        db.query(Team)
        .filter(Team.id == coach.team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    new_coach = Coach (
        team_id=coach.team_id,
        name=coach.name,
        role=coach.role,
        date_of_birth=coach.date_of_birth,
        nationality=coach.nationality,
        phone=coach.phone,
        email=coach.email,
        bio=coach.bio,
        joined_date=coach.joined_date,
        status=coach.status,
        profile_image=coach.profile_image
    )

    db.add(new_coach)
    db.commit()
    db.refresh(new_coach)

    return new_coach

@router.get("/", response_model=CoachListResponse)
def get_coaches(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = None,
    role: str | None = None,
    sort: str | None = None,
    team_id: int | None = None,
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit

    query = db.query(Coach)

    if role:
        query = query.filter(
            func.lower(Coach.role) == role.lower()
        )

    if team_id:
        team = (
            db.query(Team)
            .filter(Team.id == team_id)
            .first()
        )

        if not team:
            raise HTTPException(
                status_code=404,
                detail="Team not found"
            )

    if team_id is not None:
        query = query.filter(
            Coach.team_id == team_id
        )

    if name:
        query = query.filter(
            Coach.name.ilike(f"%{name}%")
        )

    descending = False

    if sort and sort.lstrip("-") not in ["name", "created_at"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    if sort and sort.startswith("-"):
        descending = True
        sort = sort[1:]

    if sort == "name":
        query = query.order_by(
            Coach.name.desc() if descending else Coach.name
        )

    elif sort == "created_at":
        query = query.order_by(
            Coach.created_at.desc()
            if descending
            else Coach.created_at
        )

    total = query.count()
    pages = (total + limit - 1) // limit

    coaches = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": coaches,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages
    }

