from main import app

__all__ = ["app"]


def main() -> None:
    import uvicorn

    uvicorn.run("story_guessing_game_backend.main:app", host="0.0.0.0", port=8000, reload=True)
