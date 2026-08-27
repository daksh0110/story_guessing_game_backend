from fastapi import FastAPI
from app.routers.player import router as player_router
from app.routers.room import router as room_router
app = FastAPI(title="Story Guessing Game Backend")

app.include_router(player_router)
app.include_router(room_router)
@app.get("/")
def read_root():
    return {"message": "Story Guessing Game API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
