from fastapi import (
    HTTPException,
    APIRouter,
    Depends,
    Query,
    UploadFile,
    File,
)
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.team import Team
from app.models.manager import Manager
from app.schemas.manager_schema import (
    ManagerCreate,
    ManagerResponse,
    ManagerListResponse,
    ManagerUpdate,
)

import os
import shutil
from uuid import uuid4


router = APIRouter(prefix="/manager", tags=["Manager"])


@router.post("/", response_model=ManagerResponse, status_code=201)
def create_manager(
    manager: ManagerCreate,
    db: Session = Depends(get_db),
):
    team = (
        db.query(Team)
        .filter(Team.id == manager.team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found",
        )

    new_manager = Manager(
        team_id=manager.team_id,
        name=manager.name,
        date_of_birth=manager.date_of_birth,
        nationality=manager.nationality,
        phone=manager.phone,
        email=manager.email,
        bio=manager.bio,
        joined_date=manager.joined_date,
        status=manager.status,
        profile_image=manager.profile_image,
    )

    db.add(new_manager)
    db.commit()
    db.refresh(new_manager)

    return new_manager


@router.post("/{manager_id}/image")
def upload_manager_image(
    manager_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    manager = (
        db.query(Manager)
        .filter(Manager.id == manager_id)
        .first()
    )

    if not manager:
        raise HTTPException(
            status_code=404,
            detail="Manager not found",
        )

    allowed_types = (
        "image/jpeg",
        "image/png",
        "image/webp",
    )

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG, PNG, and WebP images are allowed",
        )

    extension = os.path.splitext(
        file.filename or ""
    )[1].lower()

    if not extension:
        extension = ".jpg"

    filename = f"{uuid4()}{extension}"

    upload_dir = "uploads/managers"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(
        upload_dir,
        filename,
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    manager.profile_image = (
        f"/uploads/managers/{filename}"
    )

    db.commit()
    db.refresh(manager)

    return {
        "message": "Manager image uploaded successfully",
        "profile_image": manager.profile_image,
    }


@router.get(
    "/",
    response_model=ManagerListResponse,
)
def get_managers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = None,
    status: str | None = None,
    sort: str | None = None,
    team_id: int | None = None,
    db: Session = Depends(get_db),
):
    offset = (page - 1) * limit

    query = db.query(Manager)

    if status:
        query = query.filter(
            func.lower(Manager.status) == status.lower()
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
                detail="Team not found",
            )

    if team_id is not None:
        query = query.filter(
            Manager.team_id == team_id
        )

    if name:
        query = query.filter(
            Manager.name.ilike(f"%{name}%")
        )

    descending = False

    if sort and sort.lstrip("-") not in [
        "name",
        "created_at",
    ]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field",
        )

    if sort and sort.startswith("-"):
        descending = True
        sort = sort[1:]

    if sort == "name":
        query = query.order_by(
            Manager.name.desc()
            if descending
            else Manager.name
        )

    elif sort == "created_at":
        query = query.order_by(
            Manager.created_at.desc()
            if descending
            else Manager.created_at
        )

    total = query.count()
    pages = (total + limit - 1) // limit

    managers = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": managers,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages,
    }


@router.get(
    "/{manager_id}",
    response_model=ManagerResponse,
)
def get_manager(
    manager_id: int,
    db: Session = Depends(get_db),
):
    manager = (
        db.query(Manager)
        .filter(Manager.id == manager_id)
        .first()
    )

    if not manager:
        raise HTTPException(
            status_code=404,
            detail="Manager not found",
        )

    return manager


@router.put(
    "/{manager_id}",
    response_model=ManagerResponse,
)
def update_manager(
    manager_id: int,
    manager_data: ManagerUpdate,
    db: Session = Depends(get_db),
):
    manager = (
        db.query(Manager)
        .filter(Manager.id == manager_id)
        .first()
    )

    if not manager:
        raise HTTPException(
            status_code=404,
            detail="Manager not found",
        )

    team = (
        db.query(Team)
        .filter(Team.id == manager_data.team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found",
        )

    manager.team_id = manager_data.team_id
    manager.name = manager_data.name
    manager.date_of_birth = manager_data.date_of_birth
    manager.nationality = manager_data.nationality
    manager.phone = manager_data.phone
    manager.email = manager_data.email
    manager.bio = manager_data.bio
    manager.joined_date = manager_data.joined_date
    manager.status = manager_data.status
    manager.profile_image = manager_data.profile_image

    db.commit()
    db.refresh(manager)

    return manager


@router.delete("/{manager_id}")
def delete_manager(
    manager_id: int,
    db: Session = Depends(get_db),
):
    manager = (
        db.query(Manager)
        .filter(Manager.id == manager_id)
        .first()
    )

    if not manager:
        raise HTTPException(
            status_code=404,
            detail="Manager not found",
        )

    db.delete(manager)
    db.commit()

    return {
        "message": "Manager deleted successfully"
    }