from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import func

from app.models.club import Club
from app.models.team import Team
from app.models.player import Player
from app.schemas.team_schema import TeamCreate, TeamResponse,TeamUpdate,TeamListResponse

router= APIRouter(
    prefix="/team",
    tags=["Team"]
)

@router.post("/", response_model=TeamResponse,status_code=201)
def create_team(
    team: TeamCreate,
    db: Session=Depends(get_db)
):
    club=(
        db.query(Club)
        .filter(Club.id==team.club_id)
        .first()
    )

    if not club:
        raise HTTPException(
            status_code=404,
            detail="Club not Found"
        )
    new_team=Team(
        club_id=team.club_id,
        name=team.name,
        team_type=team.team_type

    )

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team

@router.get("/", response_model= TeamListResponse)
def get_teams(
    page: int= Query(1, ge=1),
    limit: int=Query(10, ge=1, le=100),
    team_type: str | None = None,
    sort: str | None = None,
    club_id: int | None = None,
    db: Session=Depends(get_db)
):
    query=db.query(Team)
    offset= (page-1)*limit
    descending=False
    
    if club_id is not None:
        club = (
            db.query(Club)
            .filter(Club.id == club_id)
            .first()
        )

        if not club:
            raise HTTPException(
                status_code=404,
                detail="Club not found"
            )

    if club_id is not None:
        query = query.filter(
            Team.club_id == club_id
        )

    if team_type:
        query=query.filter(
            func.lower(Team.team_type)==team_type.lower()
        )

    if sort and sort.lstrip("-") not in ["name", "created_at"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )
    
    if sort and sort.startswith("-"):
        descending=True
        sort = sort[1:]

    if sort == "name":
        query = query.order_by(
            Team.name.desc() if descending else Team.name
        )

    elif sort == "created_at":
        query = query.order_by(
            Team.created_at.desc() if descending else Team.created_at
        )
    total= query.count()
    pages= (total+limit-1)//limit
    teams=(
        query
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {
        "items": teams,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages
    }

@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    db: Session=Depends(get_db)
):
    team=(
        db.query(Team)
        .filter(Team.id==team_id)
        .first()

    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team Not Found"
        )

    return team

@router.delete("/{team_id}")
def delete_team(
    team_id:int, 
    db: Session=Depends(get_db)
):
    team=(
        db.query(Team)
        .filter(Team.id==team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team Not found"
        )
    db.delete(team)
    db.commit()

    return {
        "message": "Team deleted successfully"
    }



@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    team_data: TeamUpdate,
    db: Session=Depends(get_db)
):
    team=(
        db.query(Team)
        .filter(Team.id==team_id)
        .first()
    )
    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not Found"
        )
    club=(
        db.query(Club)
        .filter(Club.id==team_data.club_id)
        .first()
    )

    if not club:
        raise HTTPException(
            status_code=404,
            detail="Club not found"
        )
    
    team.club_id=team_data.club_id
    team.name=team_data.name
    team.team_type=team_data.team_type

    db.commit()
    db.refresh(team)

    return team

@router.get("/{team_id}/players")
def get_team_players(
    team_id: int,
    db: Session=Depends(get_db)
):
    team=(
        db.query(Team)
        .filter(Team.id==team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    players=(
        db.query(Player)
        .filter(Player.team_id==team_id)
        .all()
    )

    return players