from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from typing import Any
from sqlalchemy.dialects.postgresql import JSONB
class Room(Base):
    __tablename__="rooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    code:Mapped[str] = mapped_column(String(30), nullable=False,unique=True,)
    configuration: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

