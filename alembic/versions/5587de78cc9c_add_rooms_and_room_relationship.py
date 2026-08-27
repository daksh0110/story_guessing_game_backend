"""add rooms and room relationship

Revision ID: 5587de78cc9c
Revises: 
Create Date: 2026-08-23 00:25:21.952215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5587de78cc9c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create the rooms table first.
    # We do NOT create the host_player_id foreign key yet.
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_code", sa.String(length=100), nullable=False),
        sa.Column("room_id", sa.String(length=36), nullable=False),
        sa.Column("host_player_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "WAITING",
                "PLAYING",
                "FINISHED",
                name="roomstatus",
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # 2. Create indexes for rooms.
    op.create_index(
        "ix_rooms_id",
        "rooms",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_rooms_room_id",
        "rooms",
        ["room_id"],
        unique=True,
    )

    # 3. Add room_id to the existing players table.
    op.add_column(
        "players",
        sa.Column(
            "room_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # 4. NOW both tables exist.
    # Add the Room -> Player relationship.
    op.create_foreign_key(
        "fk_rooms_host_player",
        "rooms",
        "players",
        ["host_player_id"],
        ["id"],
    )

    # 5. Add the Player -> Room relationship.
    op.create_foreign_key(
        "fk_players_room",
        "players",
        "rooms",
        ["room_id"],
        ["id"],
    )


def downgrade() -> None:
    # Remove foreign keys first.
    op.drop_constraint(
        "fk_players_room",
        "players",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_rooms_host_player",
        "rooms",
        type_="foreignkey",
    )

    # Remove players.room_id.
    op.drop_column(
        "players",
        "room_id",
    )

    # Remove room indexes.
    op.drop_index(
        "ix_rooms_room_id",
        table_name="rooms",
    )

    op.drop_index(
        "ix_rooms_id",
        table_name="rooms",
    )

    # Finally remove rooms.
    op.drop_table("rooms")