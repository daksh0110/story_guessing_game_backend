# app/services/room_service.py

import random
import string

from sqlalchemy.orm import Session

from app.models.room import Room


def generate_room_code(db: Session, length: int = 6) -> str:
    characters = string.ascii_uppercase + string.digits

    while True:
        room_code = "".join(
            random.choices(characters, k=length)
        )

        existing_room = (
            db.query(Room)
            .filter(Room.room_code == room_code)
            .first()
        )

        if not existing_room:
            return room_code