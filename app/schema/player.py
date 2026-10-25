from datetime import datetime
from pydantic import BaseModel, Field


class PlayerData(BaseModel):
    id: int
    name: str
    room_id: int
    is_host: bool = False
    connected: bool = True
    sid: str | None = None
    created_at: datetime | None = None
    disconnected_at: datetime | None = None

    class Config:
        from_attributes = True


class CreatePlayerRequest(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    room_id: int | None = None
    room_code: str | None = None
    socket_id: str | None = None
    is_host: bool = False


class AssociateSocketRequest(BaseModel):
    player_id: int
    socket_id: str
    room_code: str | None = None
