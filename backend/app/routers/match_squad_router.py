from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Match, MatchSquad, Player
from app.schemas.match_squad_schema import MatchSquadResponse,MatchSquadUpdate

router = APIRouter(
    prefix="/match",
    tags=["Match Squad"]
    )


@router.get("/{match_id}/squad", response_model=MatchSquadResponse)
def get_match_squad(
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

    squad = (
        db.query(MatchSquad)
        .filter(MatchSquad.match_id==match_id)
        .all()
    )

    return {
        "player_ids": [
            item.player_id
            for item in squad
        ]
    }

@router.put("/{match_id}/squad", response_model=MatchSquadResponse)
def update_match_squad(
    match_id: int,
    squad_data: MatchSquadUpdate,
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

    player_ids = squad_data.player_ids

    if len(player_ids) > 15:
        raise HTTPException(
            status_code=400,
            detail="A match squad cannot contain more than 15 players"
        )

    if len(player_ids) != len(set(player_ids)):
        raise HTTPException(
            status_code=400,
            detail="Duplicate players are not allowed"
        )

    players = (
        db.query(Player)
        .filter(Player.id.in_(player_ids))
        .all()
    )

    if len(players) != len(player_ids):
        raise HTTPException(
            status_code=400,
            detail="One or more players were not found"
        )

    invalid_players = [
        player.id
        for player in players
        if player.team_id != match.team_id
    ]

    if invalid_players:
        raise HTTPException(
            status_code=400,
            detail="All squad players must belong to the match team"
        )

    db.query(MatchSquad).filter(
        MatchSquad.match_id == match_id
    ).delete()

    for player_id in player_ids:
        db.add(
            MatchSquad(
                match_id=match_id,
                player_id=player_id,
            )
        )

    db.commit()

    return {
        "player_ids": player_ids
    }