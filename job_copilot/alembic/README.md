# Alembic scaffold

This folder is a minimal scaffold for Alembic migrations. To enable full migrations:

1. Install Alembic: `pip install alembic`
2. Generate `alembic.ini` (or copy a template) and set `sqlalchemy.url` to your `DATABASE_URL` from `.env`.
3. Run `alembic revision --autogenerate -m "initial"` and then `alembic upgrade head`.

Files included:
- `env.py`: minimal environment file that you can adapt to import `app.models.Base`.
- `versions/`: place generated migration scripts here.
