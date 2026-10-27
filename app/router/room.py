from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
import app.schema.room as RoomSchema
from app.schema.player import PlayerData
from app.schema.response import ApiResponse
import app.service.room_service as room_service
from app.util.socketio import emit_to_room, enter_room_safe

router = APIRouter(
    prefix="/rooms",
    tags=["room"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/create",
    response_model=ApiResponse[RoomSchema.RoomData],
    status_code=201,
)
async def create_room_endpoint(
    data: RoomSchema.CreateRoomRequest,
    db: Session = Depends(get_db),
):
    try:
        room, host, players = room_service.create_room(db, data)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if data.socket_id:
        await enter_room_safe(data.socket_id, room.code)

    player_schemas = [PlayerData.model_validate(p) for p in players]
    host_schema = PlayerData.model_validate(host)

    return ApiResponse[RoomSchema.RoomData](
        success=True,
        message="Room created successfully",
        data=RoomSchema.RoomData(
            id=room.id,
            code=room.code,
            configuration=RoomSchema.RoomConfiguration.model_validate(
                room.configuration
            ),
            players=player_schemas,
            current_player=host_schema,
        ),
    )


@router.post(
    "/join",
    response_model=ApiResponse[RoomSchema.RoomData],
    status_code=200,
)
async def join_room_endpoint(
    data: RoomSchema.JoinRoomRequest,
    db: Session = Depends(get_db),
):
    try:
        room, player, players = room_service.join_room(db, data)
    except ValueError as exc:
        status_code = 404 if "not found" in str(exc).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    player_schema = PlayerData.model_validate(player)
    player_schemas = [PlayerData.model_validate(p) for p in players]

    if data.socket_id:
        await enter_room_safe(data.socket_id, room.code)

    await emit_to_room(
        room.code,
        "room.player_joined",
        {
            "player": player_schema.model_dump(mode="json"),
            "players": [p.model_dump(mode="json") for p in player_schemas],
            "room_code": room.code,
        },
    )

    return ApiResponse[RoomSchema.RoomData](
        success=True,
        message="Joined room successfully",
        data=RoomSchema.RoomData(
            id=room.id,
            code=room.code,
            configuration=RoomSchema.RoomConfiguration.model_validate(
                room.configuration
            ),
            players=player_schemas,
            current_player=player_schema,
        ),
    )


@router.get(
    "/{code}",
    response_model=ApiResponse[RoomSchema.RoomData],
)
def get_room_endpoint(
    code: str,
    db: Session = Depends(get_db),
):
    result = room_service.get_room_with_players(db, code)
    if not result:
        raise HTTPException(status_code=404, detail="Room not found")

    room, players = result
    player_schemas = [PlayerData.model_validate(p) for p in players]

    return ApiResponse[RoomSchema.RoomData](
        success=True,
        message="Room retrieved successfully",
        data=RoomSchema.RoomData(
            id=room.id,
            code=room.code,
            configuration=RoomSchema.RoomConfiguration.model_validate(
                room.configuration
            ),
            players=player_schemas,
        ),
    )