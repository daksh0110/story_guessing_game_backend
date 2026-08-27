import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum

from app.db import Base
from enum import Enum

class RoomStatus(str, Enum):
    WAITING = "waiting"
    PLAYING = "playing"
    FINISHED = "finished"

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)

    room_code = Column(String(100), nullable=False)

    room_id = Column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )

    host_player_id = Column(
        Integer,
        ForeignKey("players.id"),
        nullable=False,
    )

    status = Column(
        SQLEnum(RoomStatus),
        nullable=False,
        default=RoomStatus.WAITING,
    )