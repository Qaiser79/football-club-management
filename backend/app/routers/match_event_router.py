from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Match, Player, MatchEvent, MatchSquad
from app.schemas.match_event_schema import (
    MatchEventCreate,
    MatchEventUpdate,
    MatchEventResponse
)

router = APIRouter(
    prefix="/match",
    tags=["Match Events"]
)


def get_current_on_field_players(
    match_id: int,
    db: Session
):
    squad = (
        db.query(MatchSquad)
        .filter(MatchSquad.match_id == match_id)
        .all()
    )

    # Start with the original starting XI
    on_field = {
        player.player_id
        for player in squad
        if player.is_starter
    }

    # Replay substitutions to determine the current players on the field
    events = (
        db.query(MatchEvent)
        .filter(
            MatchEvent.match_id == match_id,
            MatchEvent.event_type == "substitution"
        )
        .order_by(
            MatchEvent.minute.asc(),
            MatchEvent.id.asc()
        )
        .all()
    )

    for event in events:
        if event.player_id in on_field:
            on_field.remove(event.player_id)

        if event.related_player_id is not None:
            on_field.add(event.related_player_id)

    return on_field

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
            detail="Events can only be added to live matches"
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


    if event_type == "substitution":

        if event_data.related_player_id is None:
            raise HTTPException(
                status_code=400,
                detail="Substitution requires a player coming in"
            )

        if event_data.player_id == event_data.related_player_id:
            raise HTTPException(
                status_code=400,
                detail="Player coming in cannot be the same as player going out"
            )

        related_player = (
            db.query(Player)
            .filter(Player.id == event_data.related_player_id)
            .first()
        )

        if not related_player:
            raise HTTPException(
                status_code=404,
                detail="Player coming in not found"
            )

        related_squad_player = (
            db.query(MatchSquad)
            .filter(
                MatchSquad.match_id == match_id,
                MatchSquad.player_id == event_data.related_player_id
            )
            .first()
        )

        if not related_squad_player:
            raise HTTPException(
                status_code=400,
                detail="Player coming in must be part of the match squad"
            )

        current_on_field = get_current_on_field_players(
            match_id,
            db
        )

        if event_data.player_id not in current_on_field:
            raise HTTPException(
                status_code=400,
                detail="Player going out is not currently on the field"
            )

        if event_data.related_player_id in current_on_field:
            raise HTTPException(
                status_code=400,
                detail="Player coming in is already on the field"
            )

    if event_data.minute is not None and event_data.minute < 1:
        raise HTTPException(
            status_code=400,
            detail="Event minute must be greater than 0"
        )

    new_event = MatchEvent(
        match_id=match_id,
        player_id=event_data.player_id,
        related_player_id=event_data.related_player_id,
        event_type=event_type,
        minute=event_data.minute,
    )

    db.add(new_event)

    if event_type=="goal":
        match.our_score +=1

    db.commit()
    db.refresh(new_event)

    return new_event

@router.get("/{match_id}/events", response_model=list[MatchEventResponse])
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

@router.delete(
    "/{match_id}/events/{event_id}",
    response_model=MatchEventResponse
)
def delete_match_event(
    match_id: int,
    event_id: int,
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

    if match.status.lower() != "live":
        raise HTTPException(
            status_code=400,
            detail="Events can only be deleted from live matches"
        )

    event = (
        db.query(MatchEvent)
        .filter(
            MatchEvent.id == event_id,
            MatchEvent.match_id == match_id
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Match event not found"
        )

    player = (
        db.query(Player)
        .filter(Player.id == event.player_id)
        .first()
    )

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    response = {
        "id": event.id,
        "match_id": event.match_id,
        "player_id": event.player_id,
        "related_player_id": event.related_player_id,
        "event_type": event.event_type,
        "minute": event.minute,
        "player": {
            "id": player.id,
            "name": player.name,
        },
        "related_player": (
        {
            "id": event.related_player.id,
            "name": event.related_player.name,
        }
        if event.related_player
        else None
        ),
        
    }

    if event.event_type == "goal":
        if match.our_score > 0:
            match.our_score -= 1

    db.delete(event)
    db.commit()

    return response


@router.put(
    "/{match_id}/events/{event_id}",
    response_model=MatchEventResponse
)
def update_match_event(
    match_id: int,
    event_id: int,
    event_data: MatchEventUpdate,
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

    if match.status.lower() != "live":
        raise HTTPException(
            status_code=400,
            detail="Events can only be updated for live matches"
        )

    event = (
        db.query(MatchEvent)
        .filter(
            MatchEvent.id == event_id,
            MatchEvent.match_id == match_id
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Match event not found"
        )

    if match.status.lower() != "live":
        raise HTTPException(
            status_code=400,
            detail="Events can only be edited for live matches"
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

    old_event_type = event.event_type

    if old_event_type != "goal" and event_type == "goal":
        match.our_score += 1

    elif old_event_type == "goal" and event_type != "goal":
        if match.our_score > 0:
            match.our_score -= 1

    event.player_id = event_data.player_id
    event.related_player_id = event_data.related_player_id
    event.event_type = event_type
    event.minute = event_data.minute

    db.commit()

    db.refresh(event)

    player = (
        db.query(Player)
        .filter(Player.id == event.player_id)
        .first()
    )

    return {
        "id": event.id,
        "match_id": event.match_id,
        "player_id": event.player_id,
        "related_player_id": event.related_player_id,
        "event_type": event.event_type,
        "minute": event.minute,
        "player": {
            "id": player.id,
            "name": player.name,
        },
        "related_player": (
        {
            "id": event.related_player.id,
            "name": event.related_player.name,
        }
        if event.related_player
        else None
        ),
    }