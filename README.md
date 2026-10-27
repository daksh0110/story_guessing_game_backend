# ⚙️ Story Guessing Game - Backend

Backend service powered by **FastAPI**, **python-socketio**, **SQLAlchemy**, and **PostgreSQL**.

---

## 🚀 Running with Docker (Recommended)

1. Copy environment template:
   ```bash
   cp .env.example .env
   ```
2. Start the database and backend:
   ```bash
   docker compose up -d
   ```
3. Check container status:
   ```bash
   docker compose ps
   ```
4. Access endpoints:
   - **API Root**: `http://localhost:8000/`
   - **Health Check**: `http://localhost:8000/health`
   - **Swagger Docs**: `http://localhost:8000/docs`
   - **Adminer DB UI**: `http://localhost:8080/`

---

## 🐍 Running Locally (Without Docker)

### Prerequisites
- Python 3.10+
- PostgreSQL server running on `localhost:5432`

### Setup
```bash
# 1. Virtual Environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 2. Dependencies
pip install -r requirements.txt

# 3. Environment configuration
# Ensure DATABASE_URL in .env points to your local database:
# DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/story_guessing_game

# 4. Migrations
alembic upgrade head

# 5. Start Server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
