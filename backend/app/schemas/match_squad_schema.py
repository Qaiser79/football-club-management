from pydantic import BaseModel

class MatchSquadPlayer(BaseModel):
    player_id: int

class MatchSquadResponse(BaseModel):
    player_ids: list[int]

class MatchSquadUpdate(BaseModel):
    player_ids: list[int]