from fastapi import FastAPI

app = FastAPI(title="Story Guessing Game Backend")


@app.get("/")
def read_root():
    return {"message": "Story Guessing Game API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
