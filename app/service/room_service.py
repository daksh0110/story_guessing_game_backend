import secrets
import string
from sqlalchemy.orm import Session

from app.model.room import Room
from app.model.player import Player
import app.schema.room as room_schema
import app.service.player_service as player_service


def generate_room_code(length: int = 4) -> str:
    """Generate a code players can use to join a room."""
    characters = string.ascii_uppercase + string.digits
    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


def create_room(
    db: Session,
    room_data: room_schema.CreateRoomRequest,
) -> tuple[Room, Player, list[Player]]:
    """Create a room and its host player, associating socket ID if provided."""
    room = Room(
        code=generate_room_code(),
        configuration=room_data.configuration.model_dump(mode="json"),
    )

    try:
        db.add(room)
        db.flush()

        host = Player(
            name=room_data.player_name,
            room_id=room.id,
            is_host=True,
            sid=room_data.socket_id,
            connected=True,
        )

        db.add(host)
        db.commit()
        db.refresh(room)
        db.refresh(host)

        return room, host, [host]

    except Exception:
        db.rollback()
        raise


def join_room(
    db: Session,
    data: room_schema.JoinRoomRequest,
) -> tuple[Room, Player, list[Player]]:
    """Join an existing room and create the player, associating socket ID if provided."""
    try:
        room = (
            db.query(Room)
            .filter(Room.code == data.code.strip().upper())
            .first()
        )

        if room is None:
            raise ValueError("Room not found")

        player_count = (
            db.query(Player)
            .filter(Player.room_id == room.id)
            .count()
        )

        max_players = room.configuration.get("max_players", 20)
        if player_count >= max_players:
            raise ValueError("Room is full")

        player = Player(
            name=data.player_name,
            room_id=room.id,
            is_host=False,
            sid=data.socket_id,
            connected=True,
        )
        db.add(player)
        db.commit()
        db.refresh(player)

        all_players = (
            db.query(Player)
            .filter(Player.room_id == room.id)
            .all()
        )

        return room, player, all_players

    except Exception:
        db.rollback()
        raise


def get_room_by_code(db: Session, code: str) -> Room | None:
    """Find a room by code."""
    return db.query(Room).filter(Room.code == code.strip().upper()).first()


def get_room_with_players(
    db: Session, code: str
) -> tuple[Room, list[Player]] | None:
    """Find a room and all its players."""
    room = get_room_by_code(db, code)
    if not room:
        return None
    players = (
        db.query(Player)
        .filter(Player.room_id == room.id)
        .all()
    )
    return room, players