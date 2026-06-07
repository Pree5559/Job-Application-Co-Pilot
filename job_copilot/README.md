# Job Application Co-Pilot

This repository contains the backend and frontend for the Job Application Co-Pilot capstone project.

Backend: FastAPI app serving API endpoints and static frontend.

Quick start (local):

1. Create a Python virtual environment and activate it.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment variables and adjust as needed:

```bash
cp .env.example .env
# Edit .env to set any real API keys or a different DATABASE_URL
```

4. Run the app:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. Open the API docs at: http://localhost:8000/docs

What to include for submission:
- Backend code: this repo contains the FastAPI backend in the `app/` folder.
- `requirements.txt`: root of repository.
- `.env.example`: root of repository (example environment variables).
- Alembic migrations: a minimal `alembic/` scaffold is included. If you use Alembic commands, run `alembic upgrade head` after configuring `alembic.ini` and `.env`.
- Database schema: SQLAlchemy models are in [app/models.py](app/models.py#L1-L200).

Notes:
- The application creates tables automatically via SQLAlchemy `models.Base.metadata.create_all(bind=engine)` on startup.
- If you prefer using Alembic for migrations, initialize Alembic and point `alembic.ini` to `settings.DATABASE_URL`.

Frontend:
- Static files are served from `app/static/`. Open `http://localhost:8000/` to load the UI.

If you'd like, I can also create an initial Alembic migration file that reflects the current models and commit it.
