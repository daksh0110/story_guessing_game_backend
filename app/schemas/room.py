
from pydantic import BaseModel

class RoomCreate(BaseModel):
    player_id:str

class RooomCreateResponse(BaseModel):
    room_id:str
    room_code:str
    host_player_id:int