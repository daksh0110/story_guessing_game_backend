from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from fastapi.exceptions import RequestValidationError
import socketio

from app.db.database import settings
from app.util.socketio import sio
from app.router.health import router as health_router
from app.router.room import router as room_router
from app.router.players import router as players_router
from app.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    unexpected_exception_handler,
)

fastapi_app = FastAPI(title="Story Guessing Game API")

cors_origins = [
    origin.strip()
    for origin in settings.socketio_cors_origins.split(",")
    if origin.strip()
]
if not cors_origins:
    cors_origins = ["*"]

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = socketio.ASGIApp(sio, fastapi_app)

fastapi_app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)
fastapi_app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)
fastapi_app.add_exception_handler(
    SQLAlchemyError,
    database_exception_handler,
)
fastapi_app.add_exception_handler(
    Exception,
    unexpected_exception_handler,
)

fastapi_app.include_router(health_router)
fastapi_app.include_router(room_router)
fastapi_app.include_router(players_router)


@fastapi_app.get("/")
def root():
    return {"message": "Hello World"}


@fastapi_app.get("/health")
def health():
    return {"status": "ok"}