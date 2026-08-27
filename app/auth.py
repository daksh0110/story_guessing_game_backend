# app/auth.py

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.player import Player

security = HTTPBearer()


def get_current_player(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    session_token = credentials.credentials

    player = (
        db.query(Player)
        .filter(Player.session_token == session_token)
        .first()
    )

    if not player:
        raise HTTPException(
            status_code=401,
            detail="Invalid session token",
        )

    return player