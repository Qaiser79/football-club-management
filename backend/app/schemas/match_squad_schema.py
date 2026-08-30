from pydantic import BaseModel

class MatchSquadPlayer(BaseModel):
    player_id: int
    is_starter: bool

class MatchSquadResponse(BaseModel):
    players: list[MatchSquadPlayer]

class MatchSquadUpdate(BaseModel):
    players: list[MatchSquadPlayer]