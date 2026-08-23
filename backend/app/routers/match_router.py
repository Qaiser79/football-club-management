from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Match, Team
from app.schemas.match_schema import (
    MatchCreate,
    MatchResponse,
    MatchUpdate,
    MatchListResponse,
)

router = APIRouter(
    prefix="/match",
    tags=["Match"]
)

@router.post("/", response_model=MatchResponse, status_code=201)
def create_match(
    match: MatchCreate,
    db: Session=Depends(get_db)
):
    team=(
        db.query(Team)
        .filter(Team.id==match.team_id)
        .first()
    )
    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not Found"
        )
    new_match = Match(
        team_id=match.team_id,
        opponent_name=match.opponent_name,
        match_date=match.match_date,
        competition=match.competition,
        venue=match.venue,
        is_home=match.is_home,
        our_score=match.our_score,
        opponent_score=match.opponent_score,
        status=match.status,
    )

    db.add(new_match)
    db.commit()
    db.refresh(new_match)

    return new_match

@router.get("/", response_model=MatchListResponse)
def get_matches(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None= None,
    sort: str | None = None,
    db: Session=Depends(get_db)
):
    query= db.query(Match)
    descending= False

    if search:
        search_pattern = f"%{search}%"

        query = query.filter(
            Match.opponent_name.ilike(search_pattern)
            | Match.competition.ilike(search_pattern)
            | Match.venue.ilike(search_pattern)
            | Match.status.ilike(search_pattern)
        )
    
    if sort and sort.lstrip("-") not in [
        "match_date",
        "opponent_name",
        "competition",
    ]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )
    if sort and sort.startswith("-"):
        descending=True
        sort= sort[1:]

    if sort == "match_date":
        query = query.order_by(
            Match.match_date.desc()
            if descending
            else Match.match_date
        )

    elif sort =="opponent_name":
        query=query.order_by(
            Match.opponent_name.desc()
            if descending
            else Match.opponent_name
        )
    elif sort == "competition":
        query = query.order_by(
            Match.competition.desc()
            if descending
            else Match.competition
        )

    offset = (page -1) * limit

    total = query.count()
    pages= (total+limit-1)//limit

    matches=(
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": matches,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages,
    }

@router.get("/{match_id}", response_model=MatchResponse)
def get_match(
    match_id: int,
    db: Session = Depends(get_db)
):
    match = (
        db.query(Match)
        .filter(Match.id == match_id)
        .first()
    )

    if not match:
        raise HTTPException(
            status_code=404,
            detail="Match not found"
        )
    
    return match

@router.put("/{match_id}", response_model=MatchResponse)
def update_match(
    match_id: int,
    match_data: MatchUpdate,
    db: Session = Depends(get_db)
):
    match = (
        db.query(Match)
        .filter(Match.id==match_id)
        .first()
    )

    if not match:
        raise HTTPException(
            status_code=404,
            detail="Match not found"
        )
    
    team=(
        db.query(Team)
        .filter(Team.id==match_data.team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    
    match.team_id = match_data.team_id
    match.opponent_name = match_data.opponent_name
    match.match_date = match_data.match_date
    match.competition = match_data.competition
    match.venue = match_data.venue
    match.is_home = match_data.is_home
    match.our_score = match_data.our_score
    match.opponent_score = match_data.opponent_score
    match.status = match_data.status

    db.commit()
    db.refresh(match)

    return match

@router.delete("/{match_id}")
def delete_match(
    match_id: int,
    db: Session = Depends(get_db)
):
    match = (
        db.query(Match)
        .filter(Match.id==match_id)
        .first()
    )

    if not match:
        raise HTTPException(
            status_code= 404,
            detail="Match not found"
        )
    
    db.delete(match)
    db.commit()

    return {
        "message": "Match deleted successfully"
    }