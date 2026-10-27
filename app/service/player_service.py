from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.model.player import Player


def create_player(db: Session, player: Player) -> Player:
    """Create and return a player."""
    try:
        db.add(player)
        db.commit()
        db.refresh(player)
        return player
    except Exception:
        db.rollback()
        raise


def get_player_by_id(db: Session, player_id: int) -> Player | None:
    """Find a player by their ID."""
    return db.query(Player).filter(Player.id == player_id).first()


def get_players_by_room(db: Session, room_id: int) -> list[Player]:
    """Retrieve all players in a room."""
    return db.query(Player).filter(Player.room_id == room_id).all()


def update_player_socket(
    db: Session,
    player_id: int,
    socket_id: str,
) -> Player | None:
    """Associate a session socket ID with an existing player and mark connected."""
    player = get_player_by_id(db, player_id)
    if not player:
        return None

    try:
        player.sid = socket_id
        player.connected = True
        player.disconnected_at = None
        db.commit()
        db.refresh(player)
        return player
    except Exception:
        db.rollback()
        raise


def disconnect_player_by_sid(
    db: Session,
    socket_id: str,
) -> Player | None:
    """Mark a player disconnected by socket ID."""
    player = db.query(Player).filter(Player.sid == socket_id).first()
    if not player:
        return None

    try:
        player.connected = False
        player.disconnected_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(player)
        return player
    except Exception:
        db.rollback()
        raise