from pathlib import Path

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    database_url: str
    socketio_cors_origins: str = (
        "http://localhost:3000,http://localhost:5173"
    )

    model_config = SettingsConfigDict(
        env_file=BACKEND_ROOT / ".env",
        env_file_encoding="utf-8",
         extra="ignore",
    )


try:
    settings = Settings()
except ValidationError as exc:
    raise RuntimeError(
        "DATABASE_URL is missing. Set database_url in "
        f"{BACKEND_ROOT / '.env'} or provide DATABASE_URL "
        "through the environment."
    ) from exc


engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()