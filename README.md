# Story Guessing Game Backend

A FastAPI backend for a story guessing game, built with Python and managed via `uv`.

## Project structure

```text
story_guessing_game_backend/
├── .env
├── .python-version
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   └── routers/
│       └── __init__.py
├── pyproject.toml
├── README.md
├── uv.lock
└── .venv/
```

## Prerequisites

- Python 3.14+
- `uv` installed
- PostgreSQL running locally

## Setup

1. Clone the project.
2. Create or update your `.env` file:

```env
DATABASE_URL=postgresql+psycopg://postgres:1234@localhost:5432/story-game
```

3. Install dependencies:

```bash
uv sync
```

## Create database tables

Run this once after setting up PostgreSQL and your `DATABASE_URL`:

```bash
uv run python create_tables.py
```

This script creates the database tables from the SQLAlchemy models.

## Run the app

```bash
uv run uvicorn app.main:app --reload
```

Then open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## Default endpoints

- `GET /` - health check / welcome route
- `GET /health` - status endpoint
- `GET /docs` - Swagger UI documentation

## Notes

- The app package is the main backend entry point.
- The database connection is configured through the `DATABASE_URL` environment variable.
- You can add routers, services, and schemas under the `app/` package as the project grows.
