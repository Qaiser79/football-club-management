from fastapi import HTTPException, APIRouter, Depends, Query, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func
import os
import shutil
from uuid import uuid4 

from app.database import get_db
from app.models.team import Team
from app.models.coach import Coach
from app.schemas.coach_schema import (
    CoachCreate,
    CoachResponse,
    CoachListResponse,
    CoachUpdate
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

@router.post("/{coach_id}/image")
def upload_coach_image(
    coach_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    coach = (
        db.query(Coach)
        .filter(Coach.id == coach_id)
        .first()
    )

    if not coach:
        raise HTTPException(
            status_code=404,
            detail="Coach not found"
        )

    allowed_types = (
        "image/jpeg",
        "image/png",
        "image/webp",
    )

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG, PNG, and WebP images are allowed"
        )

    extension = os.path.splitext(file.filename or "")[1].lower()

    if not extension:
        extension = ".jpg"

    filename = f"{uuid4()}{extension}"

    upload_dir = "uploads/coaches"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    coach.profile_image = f"/uploads/coaches/{filename}"
    db.commit()
    db.refresh(coach)

    return {
        "message": "Coach image uploaded successfully",
        "profile_image": coach.profile_image
    }

@router.get("/", response_model=CoachListResponse)
def get_coaches(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = None,
    role: str | None = None,
    sort: str | None = None,
    team_id: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit

    query = db.query(Coach)

    if role:
        query = query.filter(
            func.lower(Coach.role) == role.lower()
        )
    if status:
        query = query.filter(func.lower(Coach.status) == status.lower())

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

@router.get("/{coach_id}", response_model=CoachResponse)
def get_coach(
    coach_id: int,
    db: Session = Depends(get_db)
):
    coach = (
        db.query(Coach)
        .filter(Coach.id == coach_id)
        .first()
    )

    if not coach:
        raise HTTPException(
            status_code=404,
            detail="Coach not found"
        )

    return coach

@router.put("/{coach_id}", response_model=CoachResponse)
def update_coach(
    coach_id: int,
    coach_data: CoachUpdate,
    db: Session = Depends(get_db)
):
    coach = (
        db.query(Coach)
        .filter(Coach.id == coach_id)
        .first()
    )

    if not coach:
        raise HTTPException(
            status_code=404,
            detail="Coach not found"
        )

    team = (
        db.query(Team)
        .filter(Team.id == coach_data.team_id)
        .first()
    )

    if not team:
        raise HTTPException (
            status_code=404,
            details="Team not found"
        )

    coach.team_id = coach_data.team_id
    coach.name = coach_data.name
    coach.role = coach_data.role
    coach.date_of_birth = coach_data.date_of_birth
    coach.nationality = coach_data.nationality
    coach.phone = coach_data.phone
    coach.email = coach_data.email
    coach.bio = coach_data.bio
    coach.joined_date = coach_data.joined_date
    coach.status = coach_data.status
    coach.profile_image = coach_data.profile_image

    db.commit()
    db.refresh(coach)

    return coach

@router.delete("/{coach_id}")
def delete_coach(
    coach_id: int,
    db: Session=Depends(get_db)
):
    coach = (
        db.query(Coach)
        .filter(Coach.id == coach_id)
        .first()
    )

    if not coach:
        raise HTTPException(
            status_code=404,
            detail="Coach not found"
        )

    db.delete(coach)
    db.commit()

    return {
        "message": "Coach deleted successfully"
    }