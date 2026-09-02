from pydantic import BaseModel

class MatchEventCreate(BaseModel):
    player_id: int
    related_player_id: int | None = None
    event_type: str
    minute: int | None = None


class MatchEventUpdate(BaseModel):
    player_id: int
    related_player_id: int | None = None
    event_type: str
    minute: int | None = None

class MatcheventPlayer(BaseModel):
    id: int
    name: str
    model_config ={
        "from_attributes": True
    }

class MatchEventResponse(BaseModel):
    id: int
    match_id: int
    player_id: int
    related_player_id: int | None = None
    event_type: str
    minute: int | None = None
    player: MatcheventPlayer
    related_player: MatcheventPlayer | None = None
    class Config:
        from_attributes = True