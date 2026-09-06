from sqlalchemy.orm import Session

from app.models import MatchEvent, MatchSquad

def get_current_on_field_players(
    match_id: int,
    db: Session,
    minute: int | None = None,
    exclude_event_id: int | None = None
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
    events_query = (
        db.query(MatchEvent)
        .filter(
            MatchEvent.match_id == match_id,
            MatchEvent.event_type == "substitution"
        )
    )

    if exclude_event_id is not None:
        events_query = events_query.filter(
            MatchEvent.id != exclude_event_id
        )

    if minute is not None:
        events_query = events_query.filter(
            MatchEvent.minute <= minute
        )

    events = (
        events_query
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

def has_player_received_red_card(
        match_id: int,
        player_id: int,
        minute: int | None,
        db: Session,
        exclude_event_id: int | None=None
):
    if minute is None:
        return False

    query = (
        db.query(MatchEvent)
        .filter(
            MatchEvent.match_id == match_id,
            MatchEvent.player_id == player_id,
            MatchEvent.event_type == "red_card",
            MatchEvent.minute.isnot(None),
            MatchEvent.minute <= minute
        )
    )

    if exclude_event_id is not None:
        query = query.filter(
            MatchEvent.id != exclude_event_id
        )
    return query.first() is not None
    

def validate_event_timeline(
    match_id: int,
    db: Session,
    override_event_id: int | None = None,
    exclude_event_id: int | None = None,
    override_player_id: int | None = None,
    override_related_player_id: int | None = None,
    override_event_type: str | None = None,
    override_minute: int | None = None,
):
    squad = (
        db.query(MatchSquad)
        .filter(MatchSquad.match_id == match_id)
        .all()
    )

    on_field = {
        player.player_id
        for player in squad
        if player.is_starter
    }

    red_carded = set()

    events = (
        db.query(MatchEvent)
        .filter(MatchEvent.match_id == match_id)
        .all()
    )

    timeline = []

    for event in events:
        if event.id == exclude_event_id:
            continue
        if event.id == override_event_id:
            timeline.append({
                "id": event.id,
                "player_id": override_player_id,
                "related_player_id": override_related_player_id,
                "event_type": override_event_type,
                "minute": override_minute,
            })
        else:
            timeline.append({
                "id": event.id,
                "player_id": event.player_id,
                "related_player_id": event.related_player_id,
                "event_type": event.event_type,
                "minute": event.minute,
            })

    if override_event_id is None and override_event_type is not None:
        timeline.append({
            "id": None,
            "player_id": override_player_id,
            "related_player_id": override_related_player_id,
            "event_type": override_event_type,
            "minute": override_minute,
        })

    timeline.sort(
        key=lambda event: (
            event["minute"] if event["minute"] is not None else 0,
            event["id"] if event["id"] is not None else float("inf")
        )
    )
    print("DEBUG TIMELINE:", timeline)

    for event in timeline:
        player_id = event["player_id"]
        related_player_id = event["related_player_id"]
        event_type = event["event_type"]

        if event_type == "substitution":
            if related_player_id is None:
                return False, "Substitution requires a player coming in"

            if player_id not in on_field:
                return False, "Player going out is not currently on the field"

            if player_id in red_carded:
                return False, "Player going out has already received a red card"

            if related_player_id in on_field:
                return False, "Player coming in is already on the field"

            if related_player_id in red_carded:
                return False, "Player coming in has already received a red card"

            on_field.remove(player_id)
            on_field.add(related_player_id)

        elif event_type == "red_card":
            if player_id not in on_field:
                return False, "Player must currently be on the field"

            if player_id in red_carded:
                return False, "Player has already received a red card"

            red_carded.add(player_id)
            on_field.remove(player_id)

        else:
            if player_id in red_carded:
                return False, "Player has already received a red card"

            if player_id not in on_field:
                return False, "Player must currently be on the field"

    return True, None