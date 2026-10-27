from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class RoundPlayer(Base):
    __tablename__ = "round_players"

    __table_args__ = (
        UniqueConstraint(
            "round_id",
            "player_id",
            name="uq_round_player",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    round_id: Mapped[int] = mapped_column(
        ForeignKey("game_rounds.id", ondelete="CASCADE"),
        nullable=False,
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )