import uuid

from sqlalchemy import Column, Integer, String,ForeignKey

from app.db import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    session_token = Column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )
    room_id = Column(
        Integer,
        ForeignKey("rooms.id"),
        nullable=True,
    )