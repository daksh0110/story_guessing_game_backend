import logging
from datetime import datetime, timezone
import socketio
from app.db.database import SessionLocal, settings
from app.model.player import Player
from app.model.room import Room

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=[
        origin.strip()
        for origin in settings.socketio_cors_origins.split(",")
        if origin.strip()
    ],
)


async def enter_room_safe(sid: str, room_code: str):
    """Safely add a socket connection to a room channel."""
    if not sid or not room_code:
        return
    try:
        await sio.enter_room(sid, room_code.upper())
        logger.info("Socket %s entered room %s", sid, room_code)
    except Exception as exc:
        logger.warning("Could not add socket %s to room %s: %s", sid, room_code, exc)


async def emit_to_room(room_code: str, event: str, data: dict):
    """Emit an event to all clients in a room."""
    try:
        await sio.emit(event, data, room=room_code.upper())
        logger.info("Emitted %s to room %s", event, room_code)
    except Exception as exc:
        logger.warning("Failed emitting %s to room %s: %s", event, room_code, exc)


@sio.event
async def connect(sid, environ, auth):
    auth_keys = list(auth.keys()) if isinstance(auth, dict) else []
    logger.info("Client connected: sid=%s, auth_keys=%s", sid, auth_keys)


@sio.event
async def disconnect(sid, reason):
    logger.info("Client disconnected: sid=%s, reason=%s", sid, reason)
    try:
        with SessionLocal() as db:
            player = db.query(Player).filter(Player.sid == sid).first()
            if player:
                player.connected = False
                player.disconnected_at = datetime.now(timezone.utc)
                room = db.query(Room).filter(Room.id == player.room_id).first()
                db.commit()
                if room:
                    await emit_to_room(
                        room.code,
                        "room.player_left",
                        {
                            "player_id": player.id,
                            "name": player.name,
                            "room_code": room.code,
                        },
                    )
    except Exception as exc:
        logger.error("Error during disconnect cleanup: %s", exc, exc_info=True)


@sio.on("client.ping")
async def handle_ping(sid, data):
    logger.info("Ping received: sid=%s, data=%s", sid, data)
    return {
        "event": "server.pong",
        "server_time": datetime.now(timezone.utc).isoformat(),
    }


@sio.on("room.join")
async def handle_room_join(sid, data):
    """Socket event for joining a room channel and linking session socket ID."""
    logger.info("room.join received from sid=%s with data=%s", sid, data)
    if not isinstance(data, dict):
        return {"success": False, "message": "Invalid payload"}

    room_code = data.get("code") or data.get("room_code")
    player_id = data.get("player_id")

    if not room_code:
        return {"success": False, "message": "Room code is required"}

    room_code = str(room_code).strip().upper()
    await enter_room_safe(sid, room_code)

    updated_player = None
    if player_id:
        try:
            with SessionLocal() as db:
                player = db.query(Player).filter(Player.id == player_id).first()
                if player:
                    player.sid = sid
                    player.connected = True
                    player.disconnected_at = None
                    db.commit()
                    db.refresh(player)
                    updated_player = {
                        "id": player.id,
                        "name": player.name,
                        "room_id": player.room_id,
                        "is_host": player.is_host,
                        "connected": player.connected,
                        "sid": player.sid,
                    }
        except Exception as exc:
            logger.error("Failed to associate player_id %s with sid %s: %s", player_id, sid, exc)

    if updated_player:
        await emit_to_room(
            room_code,
            "room.player_joined",
            {
                "player": updated_player,
                "room_code": room_code,
            },
        )

    return {
        "success": True,
        "sid": sid,
        "room_code": room_code,
        "player": updated_player,
    }


@sio.on("player.associate")
async def handle_player_associate(sid, data):
    """Associate a player record with this socket ID."""
    if not isinstance(data, dict) or not data.get("player_id"):
        return {"success": False, "message": "player_id is required"}

    player_id = data["player_id"]
    try:
        with SessionLocal() as db:
            player = db.query(Player).filter(Player.id == player_id).first()
            if not player:
                return {"success": False, "message": "Player not found"}

            player.sid = sid
            player.connected = True
            player.disconnected_at = None
            db.commit()

            room = db.query(Room).filter(Room.id == player.room_id).first()
            if room:
                await enter_room_safe(sid, room.code)

            return {
                "success": True,
                "player_id": player.id,
                "sid": sid,
                "room_code": room.code if room else None,
            }
    except Exception as exc:
        logger.error("Failed to associate socket in player.associate: %s", exc)
        return {"success": False, "message": str(exc)}