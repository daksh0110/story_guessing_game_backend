from datetime import datetime

from sqlalchemy import DateTime, String, func,Boolean,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    connected: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
    disconnected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    sid:Mapped[str]=mapped_column(String(100),nullable=True)
    is_host: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )