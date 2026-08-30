from pydantic import BaseModel

class MatchEventCreate(BaseModel):
    player_id: int
    event_type: str
    minute: int | None = None


class MatchEventUpdate(BaseModel):
    player_id: int
    event_type: str
    minute: int | None = None

class MatcheventPlayer(BaseModel):
    id: int
    name: str
    class config:
        from_attributes = True

class MatchEventResponse(BaseModel):
    id: int
    match_id: int
    player_id: int
    event_type: str
    minute: int | None = None
    player: MatcheventPlayer
    class Config:
        from_attributes = True