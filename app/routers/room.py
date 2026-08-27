from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.models.player import Player
from app.schemas.room import RooomCreateResponse,RoomCreate
from app.db import get_db
from app.auth import get_current_player
from app.models.room import Room
from app.services.room_service import generate_room_code
router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)


@router.post("/", response_model=RooomCreateResponse)
def create_room(
    current_player: Player = Depends(get_current_player),
    db: Session = Depends(get_db),
):
    room_code = generate_room_code(db)

    new_room = Room(
        room_code=room_code,
        host_player_id=current_player.id,
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return new_room