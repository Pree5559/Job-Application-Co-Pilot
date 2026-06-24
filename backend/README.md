# Backend - Job Application Co-Pilot

## Overview

FastAPI-based backend that provides REST API endpoints for job application management and AI-powered content generation.

## Structure

```
backend/
├── app/
│   ├── agents/           # AI coordination and prompts
│   │   ├── coordinator.py
│   │   └── prompts.py
│   ├── static/           # Frontend files served by FastAPI
│   ├── auth.py          # JWT authentication
│   ├── config.py        # Configuration management
│   ├── database.py      # Database connection
│   ├── main.py          # FastAPI application & routes
│   ├── models.py        # SQLAlchemy models
│   └── schemas.py       # Pydantic schemas
├── alembic/             # Database migrations
├── requirements.txt     # Python dependencies
├── alembic.ini         # Alembic configuration
└── .env.example        # Environment variables template
```

## Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv

# Activate
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and set:
# - GROQ_API_KEY
# - SECRET_KEY
# - DATABASE_URL (optional)
```

### 4. Run Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication
- `POST /signup` - Register new user
- `POST /token` - Login (returns JWT token)

### Applications
- `POST /applications` - Create application with resume & JD
- `GET /applications` - List user's applications
- `GET /applications/{id}` - Get application details
- `GET /applications/{id}/drafts` - Get generated drafts
- `PUT /applications/{id}/status` - Update application status
- `PUT /applications/{id}/regenerate` - Regenerate section
- `POST /applications/{id}/ats-score` - Calculate ATS score

### Downloads
- `GET /applications/{id}/download/resume` - Download resume PDF
- `GET /applications/{id}/download/cover-letter` - Download cover letter DOCX

## Database

Default: SQLite (`job_copilot.db`)
Production: PostgreSQL recommended

### Migrations (Alembic)

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Dependencies

Key packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `pyjwt` - JWT tokens
- `groq` - Groq LLM integration
- `pypdf` - PDF parsing
- `python-docx` - DOCX generation
- `fpdf2` - PDF generation
- `beautifulsoup4` - Web scraping

See `requirements.txt` for full list.

## Testing

```bash
# Start server
uvicorn app.main:app --reload

# Visit API docs
http://localhost:8000/docs
```

## Environment Variables

```env
DATABASE_URL=sqlite:///./job_copilot.db
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.1-8b-instant
GROQ_MAX_TOKENS=800
GROQ_MAX_RETRIES=2
```

## Deployment

See root [DEPLOYMENT.md](../DEPLOYMENT.md) for deployment instructions.
