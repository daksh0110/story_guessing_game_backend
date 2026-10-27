from enum import Enum
from pydantic import BaseModel, Field
from app.schema.player import PlayerData


class RoomCategory(str, Enum):
    COMEDY = "Comedy"
    FANTASY = "Fantasy"
    FAMILY_FRIENDLY = "Family Friendly"
    ADVENTURE = "Adventure"
    SCI_FI = "Sci-Fi"
    MYSTERY = "Mystery"
    ANIMALS = "Animals"
    SCHOOL = "School"
    OFFICE = "Office"
    RANDOM_CHAOS = "Random Chaos"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class RoomConfiguration(BaseModel):
    category: RoomCategory
    max_players: int = Field(ge=2, le=20)
    difficulty: Difficulty


class CreateRoomRequest(BaseModel):
    player_name: str = Field(min_length=2, max_length=30)
    configuration: RoomConfiguration
    socket_id: str | None = None


class JoinRoomRequest(BaseModel):
    player_name: str = Field(min_length=2, max_length=30)
    code: str
    socket_id: str | None = None


class RoomData(BaseModel):
    id: int
    code: str
    configuration: RoomConfiguration
    players: list[PlayerData] = []
    current_player: PlayerData | None = None