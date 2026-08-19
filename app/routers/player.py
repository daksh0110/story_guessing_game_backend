from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerResponse
from app.db import get_db
router = APIRouter(
    prefix="/players",
    tags=["Players"],
)


@router.post("/", response_model=PlayerResponse)
def create_player(player: PlayerCreate,    db: Session = Depends(get_db),):
    new_player = Player(
        name=player.name,
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player