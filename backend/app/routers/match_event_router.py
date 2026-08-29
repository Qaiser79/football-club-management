from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Match, Player, MatchEvent, MatchSquad
from app.schemas.match_event_schema import (
    MatchEventCreate,
    MatchEventResponse
)

router = APIRouter(
    prefix="/match",
    tags=["Match Events"]
)

@router.post(
    "/{match_id}/events",
    response_model=MatchEventResponse,
    status_code=201
)
def create_match_event(
    match_id: int,
    event_data: MatchEventCreate,
    db: Session=Depends(get_db)
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

    if match.status.lower() !=  "live":
        raise HTTPException(
            status_code=400,
            detail="Events can only be added to scheduled matches"
        )

    player = (
        db.query(Player)
        .filter(Player.id == event_data.player_id)
        .first()
    )

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    squad_player = (
        db.query(MatchSquad)
        .filter(
            MatchSquad.match_id == match_id,
            MatchSquad.player_id == event_data.player_id
        )
        .first()
    )

    if not squad_player:
        raise HTTPException(
            status_code=400,
            detail="Player must be part of the match squad"
        )

    allowed_event_types = {
        "goal",
        "assist",
        "yellow_card",
        "red_card",
        "foul",
        "substitution",
    }

    event_type = event_data.event_type.lower()

    if event_type not in allowed_event_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid event type"
        )

    if event_data.minute is not None and event_data.minute < 1:
        raise HTTPException(
            status_code=400,
            detail="Event minute must be greater than 0"
        )

    new_event = MatchEvent(
        match_id=match_id,
        player_id=event_data.player_id,
        event_type=event_type,
        minute=event_data.minute,
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

@router.get("/{match_id/events}", response_model=list[MatchEventResponse])
def get_match_events(
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
    events = (
        db.query(MatchEvent)
        .filter(MatchEvent.match_id == match_id)
        .order_by(
            MatchEvent.minute.asc(),
            MatchEvent.id.asc()
        )
        .all()
    )

    return events