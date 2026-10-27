from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.model.player import Player
from app.model.room import Room
from app.schema.player import (
    AssociateSocketRequest,
    CreatePlayerRequest,
    PlayerData,
)
from app.schema.response import ApiResponse
import app.service.player_service as player_service
from app.util.socketio import emit_to_room, enter_room_safe

router = APIRouter(
    prefix="/players",
    tags=["players"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/create",
    response_model=ApiResponse[PlayerData],
    status_code=201,
)
async def create_player_endpoint(
    data: CreatePlayerRequest,
    db: Session = Depends(get_db),
):
    target_room = None
    if data.room_code:
        target_room = (
            db.query(Room)
            .filter(Room.code == data.room_code.strip().upper())
            .first()
        )
        if not target_room:
            raise HTTPException(status_code=404, detail="Room not found for provided code")
    elif data.room_id:
        target_room = db.query(Room).filter(Room.id == data.room_id).first()
        if not target_room:
            raise HTTPException(status_code=404, detail="Room not found for provided ID")

    if not target_room:
        raise HTTPException(
            status_code=400,
            detail="A valid room_code or room_id is required to create a player",
        )

    player = Player(
        name=data.name,
        room_id=target_room.id,
        is_host=data.is_host,
        sid=data.socket_id,
        connected=True,
    )
    saved_player = player_service.create_player(db, player)
    player_data = PlayerData.model_validate(saved_player)

    if data.socket_id:
        await enter_room_safe(data.socket_id, target_room.code)
        await emit_to_room(
            target_room.code,
            "room.player_joined",
            {
                "player": player_data.model_dump(mode="json"),
                "room_code": target_room.code,
            },
        )

    return ApiResponse[PlayerData](
        success=True,
        message="Player created successfully",
        data=player_data,
    )


@router.post(
    "/associate-socket",
    response_model=ApiResponse[PlayerData],
)
async def associate_socket_endpoint(
    data: AssociateSocketRequest,
    db: Session = Depends(get_db),
):
    updated = player_service.update_player_socket(
        db, data.player_id, data.socket_id
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Player not found")

    room = db.query(Room).filter(Room.id == updated.room_id).first()
    room_code = data.room_code or (room.code if room else None)

    if room_code:
        await enter_room_safe(data.socket_id, room_code)
        await emit_to_room(
            room_code,
            "room.player_joined",
            {
                "player": PlayerData.model_validate(updated).model_dump(mode="json"),
                "room_code": room_code,
            },
        )

    return ApiResponse[PlayerData](
        success=True,
        message="Socket associated successfully",
        data=PlayerData.model_validate(updated),
    )


@router.get(
    "/{player_id}",
    response_model=ApiResponse[PlayerData],
)
def get_player_endpoint(
    player_id: int,
    db: Session = Depends(get_db),
):
    player = player_service.get_player_by_id(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    return ApiResponse[PlayerData](
        success=True,
        message="Player retrieved successfully",
        data=PlayerData.model_validate(player),
    )