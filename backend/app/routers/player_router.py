from fastapi import HTTPException, APIRouter, Depends, Query,UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import func

from app.models.team import Team
from app.models.player import Player
from app.schemas.player_schema import PlayerCreate, PlayerResponse, PlayerUpdate,PlayerListResponse

import os
import shutil
from uuid import uuid4

router=APIRouter(
    prefix="/player",
    tags=["Player"]
)

@router.post("/", response_model=PlayerResponse,status_code=201)
def create_player(
    player: PlayerCreate,
    db: Session=Depends(get_db)
):
    team=(
        db.query(Team)
        .filter(Team.id==player.team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    new_player=Player(
        team_id=player.team_id,
        name=player.name,
        position=player.position,
        preferred_foot=player.preferred_foot,
        shirt_number=player.shirt_number,
        date_of_birth=player.date_of_birth,
        nationality=player.nationality,
        phone=player.phone,
        email=player.email,
        bio=player.bio,
        height=player.height,
        weight=player.weight,
        joined_date=player.joined_date,
        profile_image=player.profile_image,
        status=player.status
    )
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player

@router.post("/{player_id}/image")
def upload_player_image(
    player_id: int,
    file: UploadFile = File(...),
    db: Session= Depends(get_db)
):
    player = (
        db.query(Player)
        .filter(Player.id==player_id)
        .first()
    )

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
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

    filename= f"{uuid4()}{extension}"

    upload_dir = "uploads/players"
    os.makedirs(upload_dir,exist_ok=True)

    file_path = os.path.join(upload_dir,filename)

    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    player.profile_image = f"/uploads/players/{filename}"
    db.commit()
    db.refresh(player)

    return {
        "message": "Player image uploaded successfully",
        "profile_image": player.profile_image
    }

@router.get("/", response_model=PlayerListResponse)
def get_players(
    page: int=Query(1, ge=1),
    limit: int=Query(10, ge=1, le=100),
    position: str | None=None,
    name: str | None = None,
    sort: str | None = None,
    team_id: int | None = None,
    db: Session=Depends(get_db)
):
    offset = (page - 1) * limit

    query=db.query(Player)
    if position:
        query = query.filter(
            func.lower(Player.position)==position.lower()
        )

    if team_id:
        team = (
            db.query(Team)
            .filter(Team.id==team_id)
            .first()
        )

        if not team:
            raise HTTPException(
                status_code=404,
                detail="Team not found"
        )

    if team_id is not None:
        query= query.filter(
            Player.team_id==team_id
        )
    
    if name:
        query= query.filter(
            Player.name.ilike(f"%{name}%")
        )

    descending=False

    if sort and sort.lstrip("-") not in ["name", "created_at"]:
        raise HTTPException(
            status_code=400,
            detail = "Invalid sort field"
        )

    if sort and sort.startswith("-"):
        descending = True
        sort = sort[1:]


    if sort=="name":
        query=query.order_by(
            Player.name.desc() if descending else Player.name
            )
    elif sort=="created_at":
        query=query.order_by(
            Player.created_at.desc() if descending else Player.created_at
            )
    total=query.count()
    pages= (total + limit-1)//limit
    
    players= (
        query
        .offset(offset)
        .limit(limit)
        .all()
        )
    return {
        "items": players,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages
    }

@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(
    player_id: int,
    db: Session= Depends(get_db)
):
    
    

    player=(
        db.query(Player)
        .filter(Player.id==player_id)
        .first()
    )
    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not Found"
        )
    return player

@router.delete("/{player_id}")
def delete_player(
    player_id: int,
    db: Session=Depends(get_db)
):
    player=(
        db.query(Player)
        .filter(Player.id==player_id)
        .first()
    )
    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player Not Found"
        )
    db.delete(player)
    db.commit()

    return {
        "message": "Player deleted successfully"
    }

@router.put("/{player_id}", response_model= PlayerResponse)
def update_player(
    player_id: int,
    player_data: PlayerUpdate,
    db: Session= Depends(get_db)
):
    player=(
        db.query(Player)
        .filter(Player.id==player_id)
        .first()
    )
    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not Found"
        )
    team=(
        db.query(Team)
        .filter(Team.id==player_data.team_id)
        .first()
    )
    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not Found"
        )
    player.team_id=player_data.team_id
    player.name=player_data.name
    player.position=player_data.position
    player.preferred_foot = player_data.preferred_foot
    player.shirt_number = player_data.shirt_number
    player.date_of_birth = player_data.date_of_birth
    player.nationality = player_data.nationality
    player.phone = player_data.phone
    player.email = player_data.email
    player.bio = player_data.bio
    player.height = player_data.height
    player.weight = player_data.weight
    player.joined_date = player_data.joined_date
    player.profile_image = player_data.profile_image
    player.status=player_data.status
    db.commit()
    db.refresh(player)

    return player

@router.get("/{player_id}/team")
def get_player_team(
    player_id: int,
    db: Session = Depends(get_db)
):
    player=(
        db.query(Player)
        .filter(Player.id==player_id)
        .first()
    )
    if not player:
        raise HTTPException(
            status_code=404,
            detail = "Player not Found"
        )
    team = player.team

    return team